import numpy as np
from typing import Any
from pathlib import Path
from .reference_store import ReferenceExample
from .embedder import CodeEmbedder
from .embedder import get_embedding_model


class CaseRetriever:
    """RAG 기반 레퍼런스 예제 검색기"""
    
    def __init__(self, 
                 embedder: CodeEmbedder = None,
                 embedding_data: dict[str, Any] = None,
                 data_dir: str = "data"):
        
        self.data_dir = Path(data_dir)
        self.embedder = embedder
        self.embedding_data = embedding_data
        
        if self.embedder is None:
            self.embedder = CodeEmbedder(model_name=get_embedding_model())
    
    def load_embedding_data(self, filename: str = "map_to_vo_embeddings"):
        """임베딩 데이터 로드"""
        self.embedding_data = self.embedder.load_embeddings(filename)
        print(f"✅ Loaded {len(self.embedding_data['references'])} reference embeddings")
    
    def retrieve_similar_examples(self, 
                                query_line: str,
                                context_before: list[str] = None,
                                context_after: list[str] = None,
                                top_k: int = 5,
                                min_similarity: float = 0.1) -> list[tuple[ReferenceExample, float]]:
        """
        유사한 예제 검색
        
        Args:
            query_line: 변환할 쿼리 라인
            context_before: 이전 컨텍스트 라인들
            context_after: 이후 컨텍스트 라인들  
            top_k: 반환할 예제 수
            min_similarity: 최소 유사도 임계값
            
        Returns:
            (ReferenceExample, similarity_score) 튜플 리스트
        """
        
        if self.embedding_data is None:
            raise ValueError("Embedding data not loaded. Call load_embedding_data() first.")
        
        # 쿼리 임베딩 생성
        use_context = self.embedding_data.get('use_context', True)
        query_embedding = self.embedder.embed_query(
            query_line, 
            context_before, 
            context_after, 
            use_context=use_context
        )
        
        # 유사도 계산
        reference_embeddings = self.embedding_data['embeddings']
        similarities = self.embedder.compute_similarity(query_embedding, reference_embeddings)
        
        # 상위 k개 선택
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            similarity = similarities[idx]
            if similarity >= min_similarity:
                reference = self.embedding_data['references'][idx]
                results.append((reference, float(similarity)))
        
        return results
    
    def retrieve_with_filters(self,
                            query_line: str,
                            context_before: list[str] = None,
                            context_after: list[str] = None,
                            task_type: str = None,
                            top_k: int = 5,
                            min_similarity: float = 0.1) -> list[tuple[ReferenceExample, float]]:
        """
        필터링과 함께 유사한 예제 검색
        
        Args:
            task_type: 특정 태스크 타입으로 필터링
        """
        
        # 기본 검색 수행
        all_results = self.retrieve_similar_examples(
            query_line, context_before, context_after, 
            top_k=top_k*2,  # 필터링을 위해 더 많이 가져옴
            min_similarity=min_similarity
        )
        
        # 태스크 타입 필터링
        if task_type:
            filtered_results = [
                (ref, sim) for ref, sim in all_results 
                if ref.task_type == task_type
            ]
        else:
            filtered_results = all_results
        
        # 상위 k개만 반환
        return filtered_results[:top_k]
    
    def explain_retrieval(self, 
                         query_line: str,
                         retrieved_examples: list[tuple[ReferenceExample, float]],
                         show_details: bool = True) -> str:
        """검색 결과 설명"""
        
        explanation = f"🔍 Query: '{query_line.strip()}'\n"
        explanation += f"📊 Retrieved {len(retrieved_examples)} similar examples:\n\n"
        
        for i, (ref, similarity) in enumerate(retrieved_examples, 1):
            explanation += f"[{i}] Similarity: {similarity:.3f}\n"
            explanation += f"    Input:  '{ref.input_line.strip()}'\n"
            explanation += f"    Output: '{ref.output_line.strip()}'\n"
            
            if show_details and ref.context_before:
                explanation += f"    Context: {' | '.join(ref.context_before[-1:])}\n"
            
            explanation += "\n"
        
        return explanation
    
    def get_statistics(self) -> dict[str, Any]:
        """검색기 통계 정보"""
        if self.embedding_data is None:
            return {"error": "No embedding data loaded"}
        
        references = self.embedding_data['references']
        
        stats = {
            "total_references": len(references),
            "model_name": self.embedding_data.get('model_name', 'unknown'),
            "use_context": self.embedding_data.get('use_context', False),
            "task_types": {}
        }
        
        # 태스크 타입별 통계
        for ref in references:
            task_type = ref.task_type
            if task_type not in stats["task_types"]:
                stats["task_types"][task_type] = 0
            stats["task_types"][task_type] += 1
        
        return stats
    
    def get_prompt(self, query_line: str) -> str | None:
        """쿼리 라인에 대한 프롬프트 생성"""
        return self.explain_retrieval(query_line, self.retrieve_similar_examples(query_line, top_k=3))


# 편의 함수들
def create_retriever_from_files(input_file: str, output_file: str, 
                               embedding_filename: str = "map_to_vo_embeddings") -> CaseRetriever:
    """파일로부터 검색기 생성"""
    from .reference_store import ReferenceStore
    from .embedder import get_recommended_model_for_java
    
    # 1. 레퍼런스 생성
    store = ReferenceStore()
    references = store.create_references_from_files(input_file, output_file)
    store.save_references(references, "temp_references")
    
    # 2. 임베딩 생성
    embedder = CodeEmbedder(model_name=get_recommended_model_for_java())
    embedding_data = embedder.embed_reference_examples(references, use_context=True)
    embedder.save_embeddings(embedding_data, embedding_filename)
    
    # 3. 검색기 생성
    retriever = CaseRetriever(embedder=embedder, embedding_data=embedding_data)
    
    return retriever


def quick_search(query_line: str, 
                context_before: list[str] = None,
                top_k: int = 3) -> list[tuple[ReferenceExample, float]]:
    """빠른 검색 (기본 임베딩 사용)"""
    retriever = CaseRetriever()
    
    try:
        retriever.load_embedding_data()
        return retriever.retrieve_similar_examples(
            query_line, context_before, top_k=top_k
        )
    except Exception as e:
        print(f"❌ Quick search failed: {e}")
        return []


if __name__ == "__main__":
    # 테스트 코드
    retriever = CaseRetriever()
    
    try:
        retriever.load_embedding_data()
        stats = retriever.get_statistics()
        print("📊 Retriever Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # 테스트 쿼리
        # test_query = "public class TestService {"
        # test_query = "public Arraylist<Map> selectHAHAHAExecution(Map doc)  throws ElException {"
        test_query = "public void deleteEmpXDA(Map doc) throws Exception {"
        results = retriever.retrieve_similar_examples(test_query, top_k=3)
        
        if results:
            print("\n" + retriever.explain_retrieval(test_query, results))
        else:
            print("❌ No similar examples found")
            
    except FileNotFoundError:
        print("❌ No embedding data found. Please run embedder.py first to create embeddings.")