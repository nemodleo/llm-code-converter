# **LLM Code Converter: 사용자 매뉴얼**

**프로젝트 공식 사이트:** [https://nemodleo.github.io/llm-code-converter](https://nemodleo.github.io/llm-code-converter)

---

### **1. 개요 (Overview)**

**LLM Code Converter**는 레거시 Proworks 4 프로젝트를 최신 Proworks 5 프레임워크로 마이그레이션하는 개발자를 위해 설계된 고성능 Visual Studio Code Extension입니다. 본 확장 프로그램은 복잡하고 오류 발생 가능성이 높은 Map 기반의 동적 데이터 구조를 정적 타입의 Value Object(VO) 기반 코드로 자동 변환하는 과정을 지원합니다. 정교한 변환 로직을 내장하여 높은 정확도로 코드 변환을 수행함으로써, 개발 생산성과 코드 품질을 획기적으로 향상시킵니다.

---

### **2. 시스템 요구 사항 (System Requirements)**

최적의 성능과 호환성을 위해 다음 환경을 권장합니다.

* **운영체제:** Windows, macOS, Linux
* **VS Code:** 최신 버전
* **Python 환경:** Python 3.8 이상 (백엔드 서버 구동용)
* **GPU:** 40GB 이하의 VRAM을 갖춘 GPU (로컬 LLM 구동 시 권장, 예: Ollama)
* **네트워크:** 외부 LLM API에 의존하지 않아, 고객사 보안 정책에 따른 폐쇄망 환경에서도 완벽하게 작동하도록 설계되었습니다.

---

### **3. 설치 및 설정 (Installation & Setup)**

#### **Step 1: 프로젝트 다운로드**
터미널 또는 Git 클라이언트를 통해 아래 명령어로 프로젝트 소스 코드를 다운로드합니다.
```bash
git clone [https://github.com/nemodleo/llm-code-converter.git](https://github.com/nemodleo/llm-code-converter.git)
````

#### **Step 2: 백엔드 서버 실행**

코드 변환 로직을 처리하는 FastAPI 백엔드 서버를 실행해야 합니다. 프로젝트의 루트 디렉터리에서 다음 명령어를 입력하십시오.

```bash
python server.py
```

*이 서버는 Extension이 정상적으로 기능하기 위한 필수 구성 요소입니다.*

#### **Step 3: VS Code Extension 설치**

본 Extension은 마켓플레이스에 등록되어 있지 않으므로, `.vsix` 파일을 통해 수동으로 설치해야 합니다.

1.  VS Code 좌측 사이드바에서 **Extensions** 뷰를 엽니다 (`Ctrl+Shift+X` 또는 `Cmd+Shift+X`).
2.  Extensions 뷰 상단의 `...` (더보기) 메뉴를 클릭합니다.
3.  \*\*`Install from VSIX...`\*\*를 선택합니다.
4.  다운로드한 `llm-code-converter-extension.vsix` 파일을 찾아 `Install` 버튼을 클릭합니다.
5.  설치가 완료되면, 변경 사항을 완전히 적용하기 위해 VS Code를 다시 시작합니다.

#### **Step 4: 설치 확인**

VS Code를 재시작한 후, 좌측 사이드바(Activity Bar)에 **LLM Code Converter** 아이콘이 나타나면 설치가 성공적으로 완료된 것입니다.

-----

### **4. Extension 사용 방법 (How to Use)**

LLM Code Converter는 사이드 패널을 통해 직관적인 사용자 인터페이스를 제공합니다. 사이드바의 아이콘을 클릭하면 \*\*`VO GENERATOR`\*\*와 **`CODE CONVERTER`** 두 가지 핵심 기능을 사용할 수 있습니다.

#### **기능 1: VO 생성 (VO GENERATOR)**

이 기능은 Proworks 4의 Map 기반 데이터 구조를 분석하여 Proworks 5와 호환되는 Value Object(VO) 클래스를 자동으로 생성합니다.

1.  Extension 사이드 패널에서 **`VO GENERATOR`** 세션을 확장합니다.
2.  **`Project Path`**: 변환할 Java 프로젝트의 루트 디렉터리 경로를 입력합니다.
3.  **`Output Path`**: 생성된 VO 클래스 파일들을 저장할 경로를 지정합니다.
4.  **`Generate VO`** 버튼을 클릭하여 VO 생성을 시작합니다.

Extension은 프로젝트 전체의 Map 사용 패턴을 정밀하게 분석하여, 지정된 경로에 Proworks 5 형식의 VO 클래스들을 자동으로 생성합니다.

#### **기능 2: 코드 변환 (CODE CONVERTER)**

기존 Java 코드에 포함된 Map 기반 로직을 사전에 생성된 VO를 사용하도록 변환합니다.

1.  변환을 원하는 Java 파일을 엽니다.
2.  파일 내에서 변환할 코드 영역을 마우스로 드래그하여 선택합니다. (※ 별도 선택 영역이 없을 경우, 현재 파일 전체가 변환 대상으로 간주될 수 있습니다.)
3.  선택된 코드 위에서 마우스 오른쪽 버튼을 클릭하여 컨텍스트 메뉴를 엽니다.
4.  메뉴에서 \*\*`Convert Selected Code Map to VO`\*\*를 선택합니다.
5.  실행 시 나타나는 팝업 입력창에 변환에 대한 추가 지시사항(사용자 프롬프트)을 입력할 수 있습니다. 이는 LLM이 사용자의 세부 요구사항에 맞춰 변환 결과를 최적화하도록 돕습니다.
      * *예시: "변수명은 camelCase로 작성해줘"*
6.  변환된 코드는 일반적으로 새 파일로 생성되거나 현재 파일의 적절한 위치에 삽입됩니다.

-----

### **5. 결과 확인 및 디버깅 (Review & Debugging)**

#### **변환 결과 비교 (Before vs. After)**

코드 변환이 완료되면, 원본 코드와 변환된 코드를 나란히 비교할 수 있는 \*\*Diff 뷰(Side-by-Side View)\*\*가 제공됩니다. 이를 통해 변경된 내용을 직관적으로 확인하고 신속하게 검수할 수 있습니다.

#### **로그 및 상태 모니터링 (Logging & Status)**

변환 과정의 모든 로그와 현재 상태는 Extension 사이드 패널 하단 또는 VS Code의 **출력(Output)** 패널에서 실시간으로 확인할 수 있습니다. 만약 변환 중 오류가 발생하면, 상세한 로그와 예외 메시지가 해당 패널에 출력되어 문제 해결을 지원합니다.
