// Content data for the website
const content = {
    abstract: `
        <p>인스웨이브 사의 Java 프레임워크인 Proworks 4에서 Proworks 5로의 마이그레이션 과정은 현재 수작업에 의존하고 있어 작업 효율이 낮고, 코드 오류 발생 가능성이 높다는 문제를 안고 있다. 본 프로젝트는 이러한 문제를 해결하기 위해 <strong>LLM 기반의 코드 변환 자동화 도구</strong>를 개발하는 것을 목표로 한다.</p>
        <p>이를 위해 세 가지 핵심 모듈을 설계하고 구현하였다: (1) <strong>Dependency Analysis 모듈</strong>은 정적 분석 기반의 Call Graph Parsing을 통해 Proworks 5에서 요구하는 데이터 클래스와 스켈레톤 코드를 자동으로 생성한다. (2) <strong>Code Conversion 모듈</strong>은 LLM을 활용하여 레거시 코드를 신규 API에 맞게 자동 변환하며, RAG 기법을 통해 변환 정확도를 향상시킨다. (3) <strong>Self-Refinement 모듈</strong>은 Reflexion 기법을 기반으로 LLM이 자신의 출력을 분석·피드백하여 점진적으로 코드의 완성도를 높인다.</p>
        <p>이러한 세 모듈의 통합을 통해 수작업 대비 <strong>50% 이상의 자동 변환 정확도</strong>를 달성하였으며, 전체적인 마이그레이션 리소스를 크게 절감할 수 있었다.</p>
    `,

    introduction: `
        <p>기업용 애플리케이션 개발에 특화된 인스웨이브 사의 Java 기반 프레임워크인 Proworks는 안정적인 백엔드 구축과 운영을 위해 다양한 기능을 제공하고 있다. 최근 출시된 Proworks 5는 이전 버전인 Proworks 4에 비해 API 확장, 인터페이스 정비, 성능 개선, 유지보수 편의성 등 다방면에서 향상된 기능을 포함하고 있다.</p>
        
        <h3>1.1 Problem Statement</h3>
        <p>현재 Proworks 4에서 5로의 마이그레이션 과정에서 다음과 같은 주요 문제점들이 발견되었다:</p>
        <ul class="problem-list">
            <li><strong>규칙 기반 변환의 한계:</strong> 기존 마이그레이션 작업은 정해진 치환 규칙을 기반으로 이루어지며, 실환경의 다양한 코드 스타일과 예외 상황을 포괄하지 못한다.</li>
            <li><strong>문맥 기반 구조적 변환의 비효율성:</strong> 복수의 MAP 객체를 하나의 VO 객체로 통합하는 등의 고차원적 변환에 기존 시스템은 대응하지 못한다.</li>
            <li><strong>과도한 수작업 의존성:</strong> 변환 실패 시 복구 자동화가 불가능하고, 모든 실패 구간을 개발자가 수작업으로 보완해야 한다.</li>
        </ul>
    `,

    method: `
        <p>본 프로젝트는 LLM의 코드 이해 및 생성 능력을 활용하여 Proworks 버전 간의 문법적·구조적 차이를 자동으로 변환하는 시스템을 제안한다. 단순한 정규표현식 기반의 치환을 넘어서, 다대다 매핑이 포함된 고차원적인 구조 변환을 자동화하는 것을 지향한다.</p>
    `,

    methodDetails: `
        <h3>2.1 Implementation Architecture</h3>
        <p>전체 시스템은 FastAPI 기반의 RESTful 서버로 구성되었으며, LLM 서빙과 클라이언트 요청 간의 통신을 효율적으로 처리하도록 설계되었다. 사용자 인터페이스는 VS Code 확장 기능 형태로 구현되었으며, 기존의 llm-vscode 오픈소스 프로젝트를 참고하여 프로젝트 요구에 맞는 사용자 경험을 설계하였다.</p>
    `,

    implementation: `
        <h3>3.1 Development Environment</h3>
        <p>본 프로젝트는 기업 보안 정책을 고려하여 로컬 환경에서 실행 가능한 구조로 설계되었다.</p>
        <div class="tech-stack">
            <span class="tech-tag">Python</span>
            <span class="tech-tag">FastAPI</span>
            <span class="tech-tag">Ollama</span>
            <span class="tech-tag">FAISS</span>
            <span class="tech-tag">Tree-sitter</span>
        </div>

        <h3>3.2 Key Features</h3>
        <div class="solution-highlights">
            <ul>
                <li><strong>로컬 환경 지원:</strong> 기업 보안 정책에 따른 폐쇄망 환경에서도 완전 작동</li>
                <li><strong>VS Code 확장:</strong> 개발자 친화적인 사용자 인터페이스 제공</li>
                <li><strong>상업적 라이선스:</strong> 모든 구성 요소가 기업용으로 사용 가능</li>
                <li><strong>GPU 효율성:</strong> 40GB VRAM 이하 환경에서 안정적 실행</li>
            </ul>
        </div>

        <h3>3.3 Architecture Components</h3>
        <p>전체 시스템은 FastAPI 기반의 RESTful 서버로 구성되었으며, LLM 서빙과 클라이언트 요청 간의 통신을 효율적으로 처리하도록 설계되었다. 사용자 인터페이스는 VS Code 확장 기능 형태로 구현되었으며, 기존의 llm-vscode 오픈소스 프로젝트를 참고하여 프로젝트 요구에 맞는 사용자 경험을 설계하였다.</p>
    `,

    results: `
        <p>본 시스템의 성능을 평가하기 위해 일반 평가용 코드(약 100줄, 4-5개 파일)와 고급 평가용 코드(약 1000줄)를 사용하여 실험을 수행하였다.</p>
        
        <h3>4.1 Evaluation Methodology</h3>
        <p>평가는 Exact Match Score를 기준으로 하였으며, 변환된 코드가 기존 로직을 정확히 보존하면서 Proworks 5의 패턴을 준수하는지를 확인하였다. 또한 BLEU score와 같은 정량 지표를 활용하여 코드 품질을 객관적으로 측정하였다.</p>

        <h3>4.2 Performance Metrics</h3>
        <p>실험 결과, 목표로 설정한 50% 이상의 자동 변환 정확도를 달성하였으며, 특히 단순한 Map → VO 변환의 경우 80% 이상의 높은 정확도를 보였다. 복잡한 중첩 구조의 경우에도 40-60%의 변환 성공률을 기록하였다.</p>
    `,

    achievements: `
        <h3>4.3 Key Achievements</h3>
        <div class="solution-highlights">
            <ul>
                <li><strong>마이그레이션 시간 및 비용 대폭 절감:</strong> 기존 수작업 대비 70% 이상의 시간 단축</li>
                <li><strong>코드 품질 및 일관성 향상:</strong> 자동화된 변환으로 인한 일관된 코딩 스타일 적용</li>
                <li><strong>개발자 반복 작업 최소화:</strong> 단순 반복 작업에서 해방되어 고부가가치 작업에 집중 가능</li>
                <li><strong>확장성 확보:</strong> 향후 다양한 프레임워크 전환에 적용 가능한 범용적 시스템 구축</li>
                <li><strong>실무 적용 가능성:</strong> 실제 산업 현장에서의 검증을 통한 실용성 입증</li>
            </ul>
        </div>

        <h3>4.4 Implementation Issues & Solutions</h3>
        <div class="problem-list">
            <li><strong>LLM 응답 형식 불일치:</strong> 프롬프트에 명시적 태그 삽입으로 해결</li>
            <li><strong>변환 규칙 미준수:</strong> Self-Refinement 모듈을 통한 반복적 개선으로 보완</li>
            <li><strong>RAG 맥락 부적합:</strong> 문서 chunk 크기 조정 및 유사도 필터링으로 개선</li>
        </div>
    `
};

// Load content when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    for (const key in content) {
        if (Object.hasOwnProperty.call(content, key)) {
            const element = document.getElementById(`${key}-content`);
            if (element) {
                element.innerHTML = content[key];
            }
        }
    }
});