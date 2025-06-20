# llm-code-converter

## User Manual
프로젝트의 대표 사이트는 다음과 같다..
https://nemodleo.github.io/llm-code-converter

### 개요
LLM 기반 코드 변환 VS Code Extension을 통해 코드 변환 개발자들이 실제 Proworks 4 프로젝트를 Proworks 5로 마이그레이션하는 과정을 자동화하는 데 이용할 수 있다. 해당 익스텐션은 복잡한 Map 기반 로직을 Value Object (VO) 기반의 정적 구조로 변환하고 변환 정확도를 높이는 로직이 다수 포함되어 있다.

### 시스템 요구 사항
운영체제: Windows, macOS, Linux
VS Code: 최신 버전 설치
Python 환경: Python 3.8 이상 (백엔드 서버 구동용)
GPU: 40GB 이하 VRAM을 가진 GPU (LLM 로컬 실행을 위함. Ollama 등 사용 시 권장)
네트워크: 고객사 보안 정책에 따라 폐쇄망 환경에서도 작동 가능 (외부 LLM API 사용 제한)
설치 및 설정
다음을 통해 프로젝트를 다운로드받을 수 있다.
	git clone https://github.com/nemodleo/llm-code-converter.git
현재 이 Extension은 공개 마켓플레이스에 등록되어 있지는 않으므로, .vsix 파일을 통해 수동으로 설치해야 한다.
Extension 설치:
VS Code 왼쪽 사이드바에서 Extensions 뷰 (Ctrl+Shift+X 또는 Cmd+Shift+X)를 연다.
Extensions 뷰 상단의 ... (점 3개) 메뉴를 클릭한 후, Install from VSIX...를 선택한다.
다운로드받은 llm-code-converter-extension.vsix 파일을 선택하고 Install을 클릭한다.
설치가 완료되면 VS Code를 다시 시작하여 Extension을 활성화한다.
extension side panel에 LLM Code Converter가 존재하면 설치가 완료된다.
	Extension 사용시 직전에 FastAPI 서버 구동을 python server.py을 통해 진행할 수 있다.

### Extension 사용 방법

LLM 기반 코드 변환 VS Code Extension은 사이드 패널을 통해 직관적인 코드 변환 기능을 제공한다. VS Code 좌측 사이드바에 추가된 LLM Code Converter 아이콘을 클릭하면, "VO GENERATOR"와 "CODE CONVERTER" 두 가지 세션이 나타난다.
Extension은 두 가지 주요 코드 변환 작업을 지원한다. 첫째, VO 생성 기능은 Proworks 4 프로젝트의 Map 기반 데이터 구조를 Proworks 5의 VO 기반 구조로 자동 변환하기 위한 첫 단계이다. 이 기능을 사용하려면 Extension 사이드 패널에서 "VO GENERATOR" 세션을 선택한 후, 변환 대상 Java 프로젝트의 루트 경로를 Project Path에, 생성된 VO 클래스 파일이 저장될 경로를 Output Path에 입력한다. 경로 입력 후 해당 세션 내의 "Generate VO" 버튼을 클릭하면, 프로젝트 내의 Map 사용 패턴을 분석하여 Proworks 5 형식의 VO 클래스들이 지정된 Output Path에 생성된다.

둘째, Map to VO 코드 변환 기능은 기존 Java 코드 내의 Map 기반 로직을 생성된 VO 클래스를 활용하여 변환한다. 이 기능을 사용하려면 Extension 사이드 패널에서 "CODE CONVERTER" 세션을 선택한 후, 변환하고자 하는 Java 파일에서 코드의 일부 또는 전체를 마우스로 드래그하여 선택한다. 선택된 코드가 없으면 현재 파일 전체가 변환 대상으로 간주될 수 있다. 선택된 코드 위에서 마우스 우클릭한 후, 컨텍스트 메뉴에서 "Convert Selected Code Map to VO"를 선택한다. 변환 실행 시 팝업되는 입력창에 "변수명은 camelCase로"와 같이 추가적인 변환 지시(사용자 프롬프트)를 입력할 수 있다. 이는 LLM이 변환 결과를 사용자의 특정 요구사항에 맞춰 최적화하도록 돕는다. 변환된 결과 코드는 보통 새로운 파일로 생성되거나, 현재 파일의 적절한 위치에 삽입된다.

변환이 완료되면, Extension은 원본 코드와 변환된 코드를 나란히 비교할 수 있는 변환 결과 비교(Before vs After) 기능을 제공하여 변경 사항을 직관적으로 확인하고 검수할 수 있다. 또한, Extension 사이드 패널의 하단이나 VS Code의 출력(Output) 패널을 통해 변환 과정의 로그와 현재 상태를 확인할 수 있다. 만약 코드 변환 중 오류가 발생하면, 해당 출력 패널에 상세한 로그와 함께 예외 메시지가 표시되어 문제 해결에 도움을 준다.
