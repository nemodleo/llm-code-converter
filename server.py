from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import time
import json

app = FastAPI(title="LLM Code Converter API")

class CodeConversionRequest(BaseModel):
    source_code: str  # 전체 파일 내용
    target_language: str
    source_language: Optional[str] = None
    file_path: Optional[str] = None
    start_line: Optional[int] = None  # 드래그된 시작 라인
    end_line: Optional[int] = None    # 드래그된 끝 라인
    additional_instructions: Optional[str] = None

class FolderConversionRequest(BaseModel):
    folder_path: str
    target_language: str
    source_language: Optional[str] = None
    file_extensions: Optional[List[str]] = None
    additional_instructions: Optional[str] = None

class CodeConversionResponse(BaseModel):
    converted_code: str
    source_language: str
    target_language: str
    file_path: Optional[str] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    processing_time: float
    success: bool
    message: str

class MakeVORequest(BaseModel):
    project_path: str
    additional_instructions: Optional[str] = None

class MakeVOResponse(BaseModel):
    vo_code: str
    file_count: int
    processing_time: float
    success: bool
    message: str

class FolderConversionResponse(BaseModel):
    converted_files: List[dict]
    total_files: int
    successful_conversions: int
    failed_conversions: int
    processing_time: float
    success: bool
    message: str

def generate_dummy_vo_code(project_path: str, file_count: int) -> str:
    """더미 VO 코드 생성"""
    
    project_name = os.path.basename(project_path).replace('-', '_').replace(' ', '_')
    
    dummy_vo_code = f"""// Generated VO (Value Object) for project: {project_name}
// Total files analyzed: {file_count}
// Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}

public class {project_name.capitalize()}VO {{
    
    // Project Information
    private String projectPath;
    private int totalFiles;
    private String generatedAt;
    
    // Dummy Data Fields
    private String id;
    private String name;
    private String description;
    private String status;
    private java.util.Date createdDate;
    private java.util.Date updatedDate;
    
    // Constructor
    public {project_name.capitalize()}VO() {{
        this.projectPath = "{project_path}";
        this.totalFiles = {file_count};
        this.generatedAt = "{time.strftime('%Y-%m-%d %H:%M:%S')}";
        this.status = "ACTIVE";
    }}
    
    // Getters and Setters
    public String getProjectPath() {{
        return projectPath;
    }}
    
    public void setProjectPath(String projectPath) {{
        this.projectPath = projectPath;
    }}
    
    public int getTotalFiles() {{
        return totalFiles;
    }}
    
    public void setTotalFiles(int totalFiles) {{
        this.totalFiles = totalFiles;
    }}
    
    public String getGeneratedAt() {{
        return generatedAt;
    }}
    
    public void setGeneratedAt(String generatedAt) {{
        this.generatedAt = generatedAt;
    }}
    
    public String getId() {{
        return id;
    }}
    
    public void setId(String id) {{
        this.id = id;
    }}
    
    public String getName() {{
        return name;
    }}
    
    public void setName(String name) {{
        this.name = name;
    }}
    
    public String getDescription() {{
        return description;
    }}
    
    public void setDescription(String description) {{
        this.description = description;
    }}
    
    public String getStatus() {{
        return status;
    }}
    
    public void setStatus(String status) {{
        this.status = status;
    }}
    
    public java.util.Date getCreatedDate() {{
        return createdDate;
    }}
    
    public void setCreatedDate(java.util.Date createdDate) {{
        this.createdDate = createdDate;
    }}
    
    public java.util.Date getUpdatedDate() {{
        return updatedDate;
    }}
    
    public void setUpdatedDate(java.util.Date updatedDate) {{
        this.updatedDate = updatedDate;
    }}
    
    // toString method
    @Override
    public String toString() {{
        return "{project_name.capitalize()}VO{{" +
                "projectPath='" + projectPath + '\\'' +
                ", totalFiles=" + totalFiles +
                ", generatedAt='" + generatedAt + '\\'' +
                ", id='" + id + '\\'' +
                ", name='" + name + '\\'' +
                ", description='" + description + '\\'' +
                ", status='" + status + '\\'' +
                ", createdDate=" + createdDate +
                ", updatedDate=" + updatedDate +
                '}}';
    }}
    
    // equals and hashCode methods
    @Override
    public boolean equals(Object o) {{
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        {project_name.capitalize()}VO that = ({project_name.capitalize()}VO) o;
        return java.util.Objects.equals(id, that.id);
    }}
    
    @Override
    public int hashCode() {{
        return java.util.Objects.hash(id);
    }}
}}"""
    
    return dummy_vo_code
    """간단한 언어 감지 (더미 구현)"""
    if file_extension:
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php'
        }
        return ext_map.get(file_extension.lower(), 'unknown')
    
    # 코드 내용 기반 간단 감지
    if 'def ' in code or 'import ' in code:
        return 'python'
    elif 'function ' in code or 'const ' in code or 'let ' in code:
        return 'javascript'
    elif 'public class ' in code or 'System.out.println' in code:
        return 'java'
    else:
        return 'unknown'

def detect_language(code: str, file_extension: str = None) -> str:
    """간단한 언어 감지 (더미 구현)"""
    if file_extension:
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php'
        }
        return ext_map.get(file_extension.lower(), 'unknown')
    
    # 코드 내용 기반 간단 감지
    if 'def ' in code or 'import ' in code:
        return 'python'
    elif 'function ' in code or 'const ' in code or 'let ' in code:
        return 'javascript'
    elif 'public class ' in code or 'System.out.println' in code:
        return 'java'
    else:
        return 'unknown'

def dummy_convert_code(
    full_file_content: str,  # 전체 파일 내용 (source_code에서 받음)
    target_language: str, 
    source_language: str = None,
    file_path: str = None,
    start_line: int = None,    # 드래그된 시작 라인
    end_line: int = None       # 드래그된 끝 라인
) -> str:
    """전체 파일에서 드래그된 라인만 #으로 변환"""
    
    print(f"Processing file: {file_path}")
    print(f"Target lines: {start_line}-{end_line}")
    print(f"Source language: {source_language}")
    print(f"Target language: {target_language}")
    print(f"Full file content length: {len(full_file_content) if full_file_content else 0}")
    
    time.sleep(0.5)  # API 호출 시뮬레이션
    
    if not full_file_content or start_line is None or end_line is None:
        print("Missing required data - returning original content")
        return full_file_content or ""
    
    # 전체 파일을 라인별로 분할
    lines = full_file_content.split('\n')
    print(f"Total lines in file: {len(lines)}")
    
    # 드래그된 라인들만 #으로 변환
    for line_num in range(start_line - 1, min(end_line, len(lines))):  # 0-based index
        if line_num < len(lines):
            original_line = lines[line_num]
            converted_line = ""
            
            # 해당 라인의 모든 글자를 #으로 변환 (공백과 탭은 유지)
            for char in original_line:
                if char in [' ', '\t']:  
                    converted_line += char  # 공백과 탭은 유지
                else:
                    converted_line += '#'   # 다른 모든 글자는 #으로 변환
            
            lines[line_num] = converted_line
            print(f"Line {line_num + 1}: '{original_line}' -> '{converted_line}'")
    
    # 전체 파일 반환
    result = '\n'.join(lines)
    print("Conversion completed")
    return result

@app.get("/")
async def root():
    return {"message": "LLM Code Converter API", "status": "running"}

@app.post("/convert-code", response_model=CodeConversionResponse)
async def convert_code(request: CodeConversionRequest):
    try:
        start_time = time.time()
        
        # 받은 요청 전체 출력
        print("=" * 50)
        print("RECEIVED REQUEST:")
        print(f"source_code length: {len(request.source_code) if request.source_code else 0}")
        print(f"target_language: {repr(request.target_language)}")
        print(f"source_language: {repr(request.source_language)}")
        print(f"file_path: {repr(request.file_path)}")
        print(f"start_line: {repr(request.start_line)}")
        print(f"end_line: {repr(request.end_line)}")
        print("=" * 50)
        
        # 소스 언어 감지
        if not request.source_language:
            if request.file_path:
                # 파일 확장자로 언어 감지
                file_ext = os.path.splitext(request.file_path)[1]
                source_language = detect_language(request.source_code, file_ext)
            else:
                source_language = detect_language(request.source_code)
        else:
            source_language = request.source_language
        
        # 더미 변환 수행
        converted_code = dummy_convert_code(
            request.source_code,     # 전체 파일 내용
            request.target_language, 
            source_language,
            request.file_path,
            request.start_line,      # 드래그된 시작 라인
            request.end_line         # 드래그된 끝 라인
        )
        
        processing_time = time.time() - start_time
        
        return CodeConversionResponse(
            converted_code=converted_code,
            source_language=source_language,
            target_language=request.target_language,
            file_path=request.file_path,
            start_line=request.start_line,
            end_line=request.end_line,
            processing_time=processing_time,
            success=True,
            message=f"Successfully converted from {source_language} to {request.target_language}"
        )
    
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert-folder", response_model=FolderConversionResponse)
async def convert_folder(request: FolderConversionRequest):
    try:
        start_time = time.time()
        
        if not os.path.exists(request.folder_path):
            raise HTTPException(status_code=404, detail="Folder not found")
        
        # 기본 파일 확장자 설정
        if not request.file_extensions:
            request.file_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c']
        
        converted_files = []
        successful_conversions = 0
        failed_conversions = 0
        
        # 폴더 내 파일들 처리
        for root, dirs, files in os.walk(request.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1]
                
                if file_ext in request.file_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            source_code = f.read()
                        
                        # 소스 언어 감지
                        source_language = detect_language(source_code, file_ext)
                        
                        # 더미 변환 수행
                        converted_code = dummy_convert_code(
                            source_code, 
                            request.target_language, 
                            source_language
                        )
                        
                        converted_files.append({
                            "file_path": file_path,
                            "original_code": source_code,
                            "converted_code": converted_code,
                            "source_language": source_language,
                            "target_language": request.target_language,
                            "success": True,
                            "error": None
                        })
                        successful_conversions += 1
                    
                    except Exception as e:
                        converted_files.append({
                            "file_path": file_path,
                            "original_code": None,
                            "converted_code": None,
                            "source_language": None,
                            "target_language": request.target_language,
                            "success": False,
                            "error": str(e)
                        })
                        failed_conversions += 1
        
        processing_time = time.time() - start_time
        total_files = len(converted_files)
        
        return FolderConversionResponse(
            converted_files=converted_files,
            total_files=total_files,
            successful_conversions=successful_conversions,
            failed_conversions=failed_conversions,
            processing_time=processing_time,
            success=True,
            message=f"Processed {total_files} files: {successful_conversions} successful, {failed_conversions} failed"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)