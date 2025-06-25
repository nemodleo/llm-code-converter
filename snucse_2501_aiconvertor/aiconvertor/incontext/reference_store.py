import json
from pathlib import Path


class ReferenceExample:
    """레퍼런스 예제 클래스"""
    
    def __init__(self, 
                 input_line: str, 
                 output_line: str, 
                 task_type: str,
                 context_before: list[str] = None,
                 context_after: list[str] = None):
        self.input_line = input_line
        self.output_line = output_line
        self.task_type = task_type
        self.context_before = context_before if context_before is not None else []
        self.context_after = context_after if context_after is not None else []


class ReferenceStore:
    """레퍼런스 예제 저장소"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.references_dir = self.data_dir / "references"
        self.references_dir.mkdir(parents=True, exist_ok=True)
        
    def create_references_from_files(self, 
                                   input_file: str, 
                                   output_file: str, 
                                   task_type: str = "map_to_vo",
                                   context_window: int = 2):
        """입력/출력 파일로부터 레퍼런스 예제 생성"""
        
        input_path = Path(input_file)
        output_path = Path(output_file)
        
        if not input_path.exists() or not output_path.exists():
            raise FileNotFoundError(f"Input or output file not found: {input_file}, {output_file}")
        
        # 파일 읽기
        with open(input_path, 'r', encoding='utf-8') as f:
            input_lines = [line.rstrip('\n') for line in f.readlines()]
        
        with open(output_path, 'r', encoding='utf-8') as f:
            output_lines = [line.rstrip('\n') for line in f.readlines()]
        
        if len(input_lines) != len(output_lines):
            raise ValueError(f"Input and output files must have same number of lines. "
                           f"Input: {len(input_lines)}, Output: {len(output_lines)}")
        
        # 레퍼런스 예제 생성
        references = []
        for i, (input_line, output_line) in enumerate(zip(input_lines, output_lines)):
            # 빈 라인이나 동일한 라인은 스킵
            if input_line.strip() == output_line.strip() or not input_line.strip():
                continue
                
            # 컨텍스트 추출
            context_before = input_lines[max(0, i-context_window):i]
            context_after = input_lines[i+1:min(len(input_lines), i+context_window+1)]
            
            reference = ReferenceExample(
                input_line=input_line,
                output_line=output_line,
                task_type=task_type,
                context_before=context_before,
                context_after=context_after
            )
            references.append(reference)
        
        return references
    
    def save_references(self, references: list[ReferenceExample], filename: str):
        """레퍼런스 예제를 파일로 저장"""
        filepath = self.references_dir / f"{filename}.json"
        
        # 직렬화 가능한 형태로 변환
        data = []
        for ref in references:
            data.append({
                'input_line': ref.input_line,
                'output_line': ref.output_line,
                'task_type': ref.task_type,
                'context_before': ref.context_before,
                'context_after': ref.context_after
            })
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Saved {len(references)} references to {filepath}")
        return filepath
    
    def load_references(self, filename: str) -> list[ReferenceExample]:
        """파일로부터 레퍼런스 예제 로드"""
        filepath = self.references_dir / f"{filename}.json"
        
        if not filepath.exists():
            raise FileNotFoundError(f"Reference file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        references = []
        for item in data:
            reference = ReferenceExample(
                input_line=item['input_line'],
                output_line=item['output_line'],
                task_type=item['task_type'],
                context_before=item.get('context_before', []),
                context_after=item.get('context_after', [])
            )
            references.append(reference)
        
        return references
    
    def get_all_reference_files(self) -> list[str]:
        """모든 레퍼런스 파일 목록 반환"""
        files = []
        for file in self.references_dir.glob("*.json"):
            files.append(file.stem)
        return files
    
    def create_sample_references(self):
        """샘플 파일로부터 레퍼런스 생성"""
        input_file = "data/line-conversion-poc/samples/SecuritiesInqrPritMgmtBCServiceImpl.java"
        output_file = "data/line-conversion-poc/samples/gt.java"
        
        try:
            references = self.create_references_from_files(
                input_file=input_file,
                output_file=output_file,
                task_type="map_to_vo"
            )
            
            self.save_references(references, "map_to_vo_samples")
            return references
            
        except Exception as e:
            print(f"❌ Error creating sample references: {e}")
            return []


if __name__ == "__main__":
    # 테스트 코드
    store = ReferenceStore()
    references = store.create_sample_references()
    print(f"Created {len(references)} reference examples")