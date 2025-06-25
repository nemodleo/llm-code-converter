from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import time
import json
import logging
import tempfile
import platform

import sys
sys.path.append('snucse_2501_aiconvertor')
from aiconvertor.convertor import run_conversion
from aiconvertor.convertor import ConversionConfig
from aiconvertor.dependency.vo_generator import run_vo_generator
from aiconvertor.dependency.map_to_vo_converter import VOGeneratorConfig
sys.path.pop()


# 시스템별 로그 디렉토리 설정
def get_log_directory():
    system = platform.system()
    if system == "Windows":
        # Windows: %TEMP% 디렉토리 사용
        log_dir = os.path.join(tempfile.gettempdir(), "llm_converter")
    elif system == "Darwin":  # macOS
        # macOS: ~/Library/Logs 사용
        log_dir = os.path.expanduser("~/Library/Logs/llm_converter")
    else:  # Linux
        # Linux: /tmp 또는 ~/.local/share/logs 사용
        log_dir = os.path.expanduser("~/.local/share/llm_converter/logs")
        if not os.access(os.path.dirname(log_dir), os.W_OK):
            log_dir = os.path.join(tempfile.gettempdir(), "llm_converter")
    
    # 디렉토리 생성
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

# 로그 파일 경로 설정
LOG_DIR = get_log_directory()
LOG_FILE_PATH = os.path.join(LOG_DIR, "server.log")

# init log file contents
if os.path.exists(LOG_FILE_PATH):
    os.remove(LOG_FILE_PATH)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 로그 파일 경로 출력
print(f"📋 Log file location: {LOG_FILE_PATH}")
logging.info(f"Log file initialized at: {LOG_FILE_PATH}")


app = FastAPI(title="LLM Code Converter API")

class CodeConversionRequest(BaseModel):
    source_code: str  # 전체 파일 내용
    target_language: str
    source_language: Optional[str] = None
    file_path: Optional[str] = None
    start_line: Optional[int] = None  # 드래그된 시작 라인
    end_line: Optional[int] = None    # 드래그된 끝 라인
    vo_path: Optional[str] = None     # VO 출력 경로
    additional_instructions: Optional[str] = None

class FolderConversionRequest(BaseModel):
    folder_path: str
    target_language: str
    source_language: Optional[str] = None
    file_extensions: Optional[List[str]] = None
    additional_instructions: Optional[str] = None

class CodeConversionResponse(BaseModel):
    converted_code: str
    file_path: Optional[str] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    processing_time: float
    success: bool
    message: str

class MakeVORequest(BaseModel):
    project_path: str
    vo_path: Optional[str] = None     # VO 출력 경로
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


def dummy_convert_code(
    full_file_content: str,  # 전체 파일 내용
    file_path: str = None,
    vo_path: str = None,
    start_line: int = None,    # 드래그된 시작 라인
    end_line: int = None       # 드래그된 끝 라인
) -> str:
    """전체 파일에서 드래그된 라인만 #으로 변환"""
    
    logging.info(f"Processing file: {file_path}")
    logging.info(f"Target lines: {start_line}-{end_line}")
    logging.info(f"Full file content length: {len(full_file_content) if full_file_content else 0}")
    
    time.sleep(0.5)  # API 호출 시뮬레이션
    
    if not full_file_content or start_line is None or end_line is None:
        logging.warning("Missing required data - returning original content")
        return full_file_content or ""
    
    # 전체 파일을 라인별로 분할
    lines = full_file_content.split('\n')
    logging.info(f"Total lines in file: {len(lines)}")
    
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
            logging.info(f"Line {line_num + 1}: '{original_line}' -> '{converted_line}'")
    
    # 전체 파일 반환
    result = '\n'.join(lines)
    logging.info("Conversion completed")
    return result

def dummy_generate_vo(
    project_path: str = None,
    vo_path: str = None        # VO 출력 경로
) -> str:
    """선택된 코드를 Java VO로 변환"""
    
    logging.info(f"Project path: {project_path}")
    logging.info(f"VO output path: {vo_path}")
    time.sleep(0.5)  # API 호출 시뮬레이션

    # 간단한 VO 생성 (더미 구현)
    vo_class_name = "GeneratedVO"
    if project_path:
        base_name = os.path.basename(project_path)
        vo_class_name = f"{base_name.capitalize()}VO"
    
    vo_code = f"""// Generated Dummy VO
// Source directory: {project_path or 'Unknown'}
// Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}
// VO output path: {vo_path or 'Not specified'}

public class {vo_class_name} {{    
    // Generated VO fields
    private String id;
    private String name;
    private String description;
    private java.util.Date createdDate;
    private java.util.Date updatedDate;
    
    // Constructor
    public {vo_class_name}() {{
        this.createdDate = new java.util.Date();
        this.updatedDate = new java.util.Date();
    }}
    
    // Parameterized Constructor
    public {vo_class_name}(String id, String name, String description) {{
        this();
        this.id = id;
        this.name = name;
        this.description = description;
    }}
    
    // Getters and Setters
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
        return "{vo_class_name}{{" +
                "id='" + id + '\\'' +
                ", name='" + name + '\\'' +
                ", description='" + description + '\\'' +
                ", createdDate=" + createdDate +
                ", updatedDate=" + updatedDate +
                '}}';
    }}
    
    // equals and hashCode methods
    @Override
    public boolean equals(Object o) {{
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        {vo_class_name} that = ({vo_class_name}) o;
        return java.util.Objects.equals(id, that.id);
    }}
    
    @Override
    public int hashCode() {{
        return java.util.Objects.hash(id);
    }}
}}"""
    
    logging.info("VO code generation completed")
    return vo_code

def count_code_files(project_path: str) -> int:
    """프로젝트 경로에서 코드 파일 개수 세기"""
    code_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.php']
    file_count = 0
    
    try:
        for root, dirs, files in os.walk(project_path):
            # 제외할 디렉토리들
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '.vscode', '__pycache__', 'out', 'dist']]
            
            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in code_extensions:
                    file_count += 1
                    
        logging.info(f"Found {file_count} code files in {project_path}")
        return file_count
        
    except Exception as e:
        logging.error(f"Error counting files: {e}")
        return 0

def generate_dummy_vo_code(project_path: str, file_count: int) -> str:
    """더미 VO 코드 생성"""
    
    project_name = os.path.basename(project_path).replace('-', '_').replace(' ', '_')
    safe_project_name = ''.join(c for c in project_name if c.isalnum() or c == '_')
    
    if not safe_project_name or safe_project_name[0].isdigit():
        safe_project_name = 'Project' + safe_project_name
    
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    
    dummy_vo_code = f"""// Generated VO (Value Object) for project: {safe_project_name}
// Total files analyzed: {file_count}
// Generated at: {current_time}

public class {safe_project_name.capitalize()}VO {{
    
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
    public {safe_project_name.capitalize()}VO() {{
        this.projectPath = "{project_path}";
        this.totalFiles = {file_count};
        this.generatedAt = "{current_time}";
        this.status = "ACTIVE";
    }}
    
    // Parameterized Constructor
    public {safe_project_name.capitalize()}VO(String id, String name, String description) {{
        this();
        this.id = id;
        this.name = name;
        this.description = description;
        this.createdDate = new java.util.Date();
        this.updatedDate = new java.util.Date();
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
    
    // Business Methods
    public void updateStatus(String newStatus) {{
        this.status = newStatus;
        this.updatedDate = new java.util.Date();
    }}
    
    public boolean isActive() {{
        return "ACTIVE".equals(this.status);
    }}
    
    // toString method
    @Override
    public String toString() {{
        return "{safe_project_name.capitalize()}VO{{" +
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
        {safe_project_name.capitalize()}VO that = ({safe_project_name.capitalize()}VO) o;
        return java.util.Objects.equals(id, that.id);
    }}
    
    @Override
    public int hashCode() {{
        return java.util.Objects.hash(id);
    }}
}}"""
    
    return dummy_vo_code


def aiconvert_code(
    full_file_content: str,  # 전체 파일 내용
    file_path: str = None,
    vo_path: str = None,
    start_line: int = None,    # 드래그된 시작 라인
    end_line: int = None       # 드래그된 끝 라인
) -> str:
    import os
    os.system(f"""
        cd .snucse_2501_aiconvertor
        poetry run python -m aiconvertor.convertor\
            --use-reflextion\
            --java samples/cvt-spring-boot-map/src/main/java/kds/poc/cvt/service/impl/FundServiceImpl.java\
            --gt samples/cvt-spring-boot/src/main/java/kds/poc/cvt/service/impl/FundServiceImpl.java\
            --context samples/cvt-spring-boot/src/main/java/kds/poc/cvt/model/FundVo.java\
            --mode page\
            -i 3 >> {LOG_FILE_PATH}
        cd ..
    """)
    # TODO: get code from start_line to end_line

    config = ConversionConfig(
        use_reflextion=True,
        java=file_path,
        gt=None,
        vo_path=vo_path,
        mode="line",
        iterations=3,
        max_line_limit_offset=1,
        skip_non_map=True,
        use_prefix_output=True,
        model="devstral:24b",
    )
    converted_code = run_conversion(config)

    if converted_code is None:
        return ""
    
    # TODO: recover code from start_line to end_line

    # with open(os.path.expanduser('~/llm.txt'), 'r', encoding='utf-8') as f:
    #     converted_code = f.read()

    return converted_code

def generate_vo(
    project_path: str = None,
    vo_path: str = None        # VO 출력 경로
) -> str:
    """Java VO 변환.
    """
    # vo_path = "/Users/nemo/Documents/창의적통합설계2/snucse_2501_aiconvertor/samples/cvt-spring-boot-map/vo.java"
    print("[*] generate_vo, ", vo_path)

    # TODO: get vo class

    config = VOGeneratorConfig(
        project_path=project_path,
        vo_path=vo_path,
        vo_class_name="DataVO",
    )

    results = run_vo_generator(config)

    if results is None:
        return ""
    
    converted_code = results['vo_code']

    return converted_code


@app.get("/")
async def root():
    logging.info("Root endpoint accessed")
    return {
        "message": "LLM Code Converter API", 
        "status": "running", 
        "timestamp": time.time(),
        "log_file": LOG_FILE_PATH
    }

@app.get("/health")
async def health_check():
    logging.info("Health check endpoint accessed")
    return {
        "status": "healthy", 
        "timestamp": time.time(),
        "log_file": LOG_FILE_PATH
    }

@app.get("/log-info")
async def log_info():
    """로그 파일 정보 반환"""
    try:
        log_exists = os.path.exists(LOG_FILE_PATH)
        log_size = os.path.getsize(LOG_FILE_PATH) if log_exists else 0
        
        return {
            "log_file_path": LOG_FILE_PATH,
            "log_directory": LOG_DIR,
            "log_exists": log_exists,
            "log_size_bytes": log_size,
            "log_size_mb": round(log_size / (1024 * 1024), 2) if log_size > 0 else 0
        }
    except Exception as e:
        logging.error(f"Error getting log info: {e}")
        return {
            "log_file_path": LOG_FILE_PATH,
            "error": str(e)
        }

@app.post("/convert-code", response_model=CodeConversionResponse)
async def convert_code(request: CodeConversionRequest):
    try:
        start_time = time.time()
        
        # 받은 요청 로깅
        logging.info("=" * 50)
        logging.info("CONVERT-CODE REQUEST RECEIVED:")
        logging.info(f"source_code length: {len(request.source_code) if request.source_code else 0}")
        logging.info(f"file_path: {repr(request.file_path)}")
        logging.info(f"start_line: {repr(request.start_line)}")
        logging.info(f"end_line: {repr(request.end_line)}")
        logging.info(f"vo_path: {repr(request.vo_path)}")
        logging.info("=" * 50)
        
        # 변환 수행
        # if request.target_language.lower() == 'java' and 
        print("request.start_line ", request.start_line)
        print("request.end_line", request.end_line)
        # 기존 # 변환
        print("[*] convert_code")
        fn = aiconvert_code  #dummy_convert_code
        converted_code = fn(
            request.source_code,
            request.file_path,
            request.vo_path,
            request.start_line,
            request.end_line
        )
        print(converted_code)
        
        processing_time = time.time() - start_time
        
        response = CodeConversionResponse(
            converted_code=converted_code,
            file_path=request.file_path,
            start_line=request.start_line,
            end_line=request.end_line,
            processing_time=processing_time,
            success=True,
            message=f"Successfully converted from {request.source_language} to {request.target_language}"
        )
        
        logging.info(f"Code conversion completed successfully in {processing_time:.2f}s")
        return response
    
    except Exception as e:
        logging.error(f"ERROR in convert_code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/make-vo", response_model=MakeVOResponse)
async def make_vo(request: MakeVORequest):
    try:
        start_time = time.time()
        
        logging.info("=" * 50)
        logging.info("MAKE-VO REQUEST RECEIVED:")
        logging.info(f"project_path: {repr(request.project_path)}")
        logging.info(f"vo_path: {repr(request.vo_path)}")
        logging.info(f"additional_instructions: {repr(request.additional_instructions)}")
        logging.info("=" * 50)
        
        # 프로젝트 경로 존재 확인
        if not os.path.exists(request.project_path):
            raise HTTPException(status_code=404, detail=f"Project path not found: {request.project_path}")
        
        if not os.path.isdir(request.project_path):
            raise HTTPException(status_code=400, detail=f"Path is not a directory: {request.project_path}")

        fn = generate_vo  # dummy_generate_vo
        vo_code = fn(
            request.project_path,
            request.vo_path,
        )
        
        # 파일 개수 세기
        file_count = count_code_files(request.project_path)
        
        # VO 코드 생성
        # vo_code = generate_dummy_vo_code(request.project_path, file_count)
#         vo_code = """
# """
        
        processing_time = time.time() - start_time
        
        response = MakeVOResponse(
            vo_code=vo_code,
            file_count=file_count,
            processing_time=processing_time,
            success=True,
            message=f"Successfully generated VO for {file_count} files"
        )
        
        logging.info(f"VO generation completed successfully: {file_count} files processed in {processing_time:.2f}s")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"ERROR in make_vo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert-folder", response_model=FolderConversionResponse)
async def convert_folder(request: FolderConversionRequest):
    try:
        start_time = time.time()
        
        logging.info("=" * 50)
        logging.info("CONVERT-FOLDER REQUEST RECEIVED:")
        logging.info(f"folder_path: {repr(request.folder_path)}")
        logging.info(f"target_language: {repr(request.target_language)}")
        logging.info(f"file_extensions: {repr(request.file_extensions)}")
        logging.info("=" * 50)
        
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
            # 제외할 디렉토리들
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '.vscode', '__pycache__', 'out', 'dist']]
            
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1]
                
                if file_ext in request.file_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            source_code = f.read()
                        
                        # 더미 변환 수행 (전체 파일 변환)
                        converted_code = dummy_convert_code(
                            source_code,
                            file_path
                        )
                        
                        converted_files.append({
                            "file_path": file_path,
                            "original_code": source_code,
                            "converted_code": converted_code,
                            "success": True,
                            "error": None
                        })
                        successful_conversions += 1
                        logging.info(f"Successfully converted: {file_path}")
                    
                    except Exception as e:
                        converted_files.append({
                            "file_path": file_path,
                            "original_code": None,
                            "converted_code": None,
                            "success": False,
                            "error": str(e)
                        })
                        failed_conversions += 1
                        logging.error(f"Failed to convert {file_path}: {e}")
        
        processing_time = time.time() - start_time
        total_files = len(converted_files)
        
        response = FolderConversionResponse(
            converted_files=converted_files,
            total_files=total_files,
            successful_conversions=successful_conversions,
            failed_conversions=failed_conversions,
            processing_time=processing_time,
            success=True,
            message=f"Processed {total_files} files: {successful_conversions} successful, {failed_conversions} failed"
        )
        
        logging.info(f"Folder conversion completed: {total_files} files processed in {processing_time:.2f}s")
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"ERROR in convert_folder: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    logging.info("=" * 60)
    logging.info("🚀 Starting LLM Code Converter API server...")
    logging.info(f"📋 Log file: {LOG_FILE_PATH}")
    logging.info("🌐 Server will be available at: http://localhost:8000")
    logging.info("📚 API documentation available at: http://localhost:8000/docs")
    logging.info("📊 Log info endpoint: http://localhost:8000/log-info")
    logging.info("=" * 60)

    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        access_log=True
    )
