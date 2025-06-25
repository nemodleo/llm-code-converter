import pickle
from typing import Any
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from .reference_store import ReferenceExample


class CodeEmbedder:
    """코드 임베딩 생성 클래스"""
    
    def __init__(self, 
                 model_name: str = "microsoft/codebert-base", 
                 data_dir: str = "data"):
        """
        코드 임베딩 모델 초기화
        
        Args:
            model_name: 임베딩 모델명 (코드에 특화된 모델)
                      - microsoft/codebert-base: 코드 이해에 특화
                      - microsoft/graphcodebert-base: 코드 구조 이해
                      - sentence-transformers/all-MiniLM-L6-v2: 범용 (빠름)
        """
        self.model_name = model_name
        self.data_dir = Path(data_dir)
        self.db_dir = self.data_dir / "db"
        self.db_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🔄 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        
        print(f"✅ Embedding model loaded: {self.model_name}")
    
    def preprocess_code_line(self, line: str, context_before: list[str] = None, 
                           context_after: list[str] = None) -> str:
        """코드 라인 전처리"""
        # 앞뒤 공백 제거
        line = line.strip()
        
        # 컨텍스트가 있으면 함께 포함 (선택적)
        if context_before or context_after:
            context_text = ""
            if context_before:
                context_text += " ".join([l.strip() for l in context_before[-2:]])  # 최근 2줄만
            context_text += f" {line} "
            if context_after:
                context_text += " ".join([l.strip() for l in context_after[:2]])   # 다음 2줄만
            return context_text.strip()
        
        return line
    
    def embed_reference_examples(self, references: list[ReferenceExample], 
                               use_context: bool = True) -> dict[str, Any]:
        """레퍼런스 예제들의 임베딩 생성"""
        
        print(f"🔄 Creating embeddings for {len(references)} reference examples")
        
        # 입력 라인들 전처리
        input_texts = []
        for ref in references:
            if use_context:
                text = self.preprocess_code_line(
                    ref.input_line, 
                    ref.context_before, 
                    ref.context_after
                )
            else:
                text = self.preprocess_code_line(ref.input_line)
            input_texts.append(text)
        
        # 임베딩 생성
        embeddings = self.model.encode(input_texts, show_progress_bar=True)
        
        # 결과 구조화
        embedding_data = {
            'embeddings': embeddings,
            'references': references,
            'model_name': self.model_name,
            'use_context': use_context,
            'input_texts': input_texts  # 디버깅용
        }
        
        return embedding_data
    
    def embed_query(self, query_line: str, context_before: list[str] = None, 
                   context_after: list[str] = None, use_context: bool = True) -> np.ndarray:
        """쿼리 라인의 임베딩 생성"""
        
        if use_context:
            text = self.preprocess_code_line(query_line, context_before, context_after)
        else:
            text = self.preprocess_code_line(query_line)
        
        embedding = self.model.encode([text])
        return embedding[0]
    
    def save_embeddings(self, embedding_data: dict[str, Any], filename: str):
        """임베딩 데이터 저장"""
        filepath = self.db_dir / f"{filename}.pkl"
        
        with open(filepath, 'wb') as f:
            pickle.dump(embedding_data, f)
        
        print(f"✅ Embeddings saved to {filepath}")
        return filepath
    
    def load_embeddings(self, filename: str) -> dict[str, Any]:
        """임베딩 데이터 로드"""
        filepath = self.db_dir / f"{filename}.pkl"
        
        if not filepath.exists():
            raise FileNotFoundError(f"Embeddings file not found: {filepath}")
        
        with open(filepath, 'rb') as f:
            embedding_data = pickle.load(f)
        
        print(f"✅ Embeddings loaded from {filepath}")
        return embedding_data
    
    def compute_similarity(self, query_embedding: np.ndarray, 
                          reference_embeddings: np.ndarray) -> np.ndarray:
        """코사인 유사도 계산"""
        from sklearn.metrics.pairwise import cosine_similarity
        
        query_embedding = query_embedding.reshape(1, -1)
        similarities = cosine_similarity(query_embedding, reference_embeddings)[0]
        return similarities


def get_embedding_model(code: int = 0):
    """Java 코드에 적합한 임베딩 모델 반환"""
    models = [
        "microsoft/codebert-base",           # 코드 전용, 정확도 높음
        "microsoft/graphcodebert-base",      # 코드 구조 이해, 더 정확
        "sentence-transformers/all-MiniLM-L6-v2",  # 범용, 빠름
        "BAAI/bge-small-en-v1.5"            # 최신 임베딩 모델, 성능 좋음
    ]

    return models[code]


if __name__ == "__main__":
    # 테스트 코드
    from .reference_store import ReferenceStore
    
    # 레퍼런스 로드
    store = ReferenceStore()
    try:
        references = store.load_references("map_to_vo_samples")
    except FileNotFoundError:
        print("Creating sample references first...")
        references = store.create_sample_references()
    
    if references:
        # 임베딩 생성
        recommended_model = get_embedding_model()
        embedder = CodeEmbedder(model_name=recommended_model)
        
        embedding_data = embedder.embed_reference_examples(references, use_context=False)
        embedder.save_embeddings(embedding_data, "map_to_vo_embeddings")
        
        print(f"✅ Created embeddings for {len(references)} examples")
    else:
        print("❌ No references found")