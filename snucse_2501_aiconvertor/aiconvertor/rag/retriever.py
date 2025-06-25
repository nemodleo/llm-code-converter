from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import statistics


class ApiRetriever:
    """벡터 저장소를 이용한 문서 검색 클래스"""
    
    def __init__(self, vectorstore_path: str, embedding_model_name: str):
        """
        Args:
            vectorstore_path: 벡터스토어 경로
            embedding_model_name: 임베딩 모델 이름
        """
        self.vectorstore_path = vectorstore_path
        self.embedding_model_name = embedding_model_name
        self.embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.vectorstore = None
        self._load_vectorstore()
    
    def _load_vectorstore(self):
        """벡터스토어 로드"""
        self.vectorstore = FAISS.load_local(
            self.vectorstore_path, 
            self.embedding_model, 
            allow_dangerous_deserialization=True
        )
    
    def analyze_chunks(self):
        """청크 분석 정보 출력"""
        if not self.vectorstore:
            raise ValueError("벡터스토어가 로드되지 않았습니다.")
            
        docs = self.vectorstore.docstore._dict.values()
        lengths = [len(doc.page_content) for doc in docs]

        print(f"총 청크 수: {len(lengths)}")
        print(f"최대 길이: {max(lengths)}")
        print(f"최소 길이: {min(lengths)}")
        print(f"평균 길이: {int(statistics.mean(lengths))}")
        print(f"중앙값 길이: {int(statistics.median(lengths))}")
        print("\n📘 청크:")
        for i, doc in enumerate(list(docs)[:]):
            print(f"[{i}] 길이={len(doc.page_content)} --------------------------------------")
            print(doc.page_content[:] + "\n---\n")
    
    def query(
        self,
        query: str, 
        k: int = 3,
        similarity_threshold: float = 0.9,
        verbose: bool = False
    ) -> list[Document]:
        """
        쿼리에 대해 상위 k개의 관련 문서를 반환 (유사도 임계값 이상만 필터링)
        
        Args:
            query: 검색 쿼리
            k: 반환할 문서 수
            similarity_threshold: 유사도 임계값
            verbose: 상세 출력 여부
            
        Returns:
            List[(Document, similarity_score)]: 필터링된 문서와 유사도 리스트
        """
        if not self.vectorstore:
            raise ValueError("벡터스토어가 로드되지 않았습니다.")
            
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        # 거리를 유사도로 변환하고 임계값 이상인 결과만 필터링
        filtered_results = []
        for doc, distance in results:
            # 변환 옵션들:
            # 1) 1/(1+d) - 부드러운 감소
            # 2) exp(-d) - 지수적 감소
            # 3) max(0, 1-d) - 선형 감소
            similarity = 1 - distance / 100
            if similarity >= similarity_threshold:
                filtered_results.append((doc, similarity))

        if verbose:
            print(f"전체 결과 수: {len(results)}, 필터링된 결과 수: {len(filtered_results)}")
            for i, (doc, similarity) in enumerate(filtered_results):
                print(f"[{i}] 유사도: {similarity:.4f}")
                print(f"본문: {doc.page_content}")
                # 벡터 reconstruct
                # FAISS index에 저장된 벡터 id = i 일 수 있음 (주의: 키와 순서 다를 수 있음)
                # id를 찾으려면 `index_to_docstore_id` 활용
                doc_id = list(self.vectorstore.index_to_docstore_id.keys())[i]
                vec = self.vectorstore.index.reconstruct(i)
                print(f"키: {doc_id}")
                print(f"벡터: {vec[:5]}...")  # 일부만 출력
                print("---")
        
        return filtered_results
    
    def get_prompt(self, query: str, k: int = 3, similarity_threshold: float = 0.9) -> str | None:
        """쿼리에 대한 프롬프트 생성"""
        results = self.query(query, k=k, similarity_threshold=similarity_threshold, verbose=False)
        
        if not results:
            return None
        
        prompt_parts = [f"<related_documents>"]
        
        for i, (doc, similarity) in enumerate(results):
            prompt_parts.append(f"[{i}] similarity: {similarity:.4f}")
            prompt_parts.append(f"```java")
            prompt_parts.append(f"{doc.page_content}")
            prompt_parts.append(f"```")
            prompt_parts.append("")  # 빈 줄 추가
        
        prompt_parts.append(f"</related_documents>")
        
        return "\n".join(prompt_parts)


if __name__ == "__main__":
    embedding_model_name = "microsoft/codebert-base" #"BAAI/bge-base-en-v1.5"
    # embedding_model_name = "nlpai-lab/KURE-v1"
    # embedding_model_name = "monologg/kobert"
    vectorstore_path = f"data/db/proworks5_vectorstore_{embedding_model_name.split('/')[-1]}"

    # ApiRetriever 클래스 사용
    retriever = ApiRetriever(vectorstore_path, embedding_model_name)
    # retriever.analyze_chunks()

    # 쿼리 테스트
    query = "public void deleteEmpXDA(Map doc) throws Exception {"
    # results = retriever.query(query, k=5, similarity_threshold=0.71, verbose=True)

    print(retriever.get_prompt(query, k=5, similarity_threshold=0.71))
