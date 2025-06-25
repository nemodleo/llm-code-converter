// Content data for the website
const content = {
    abstract: `
        <p>인스웨이브(Inswave)사의 Java 프레임워크 'Proworks 4'를 'Proworks 5'로 마이그레이션하는 작업은 현재 수작업 의존도가 높아 비효율적이며, 오류 발생 가능성이 크다는 문제를 안고 있습니다. 본 프로젝트는 이러한 문제를 해결하기 위해 <strong>LLM(거대 언어 모델) 기반의 코드 변환 자동화 도구</strong>를 개발하는 것을 목표로 합니다.</p>
        <p>이를 위해 세 가지 핵심 모듈을 설계 및 구현했습니다: (1) <strong>의존성 분석(Dependency Analysis) 모듈</strong>은 정적 분석과 호출 그래프 파싱(Call Graph Parsing)을 통해 Proworks 5에서 요구하는 데이터 클래스(VO)와 스켈레톤 코드를 자동으로 생성합니다. (2) <strong>코드 변환(Code Conversion) 모듈</strong>은 LLM을 활용해 레거시 코드를 변환하며, RAG(검색 증강 생성) 기법으로 Proworks 5 공식 문서를 참조하여 변환 정확도를 극대화합니다. (3) <strong>자가 개선(Self-Refinement) 모듈</strong>은 Reflexion 기법을 기반으로, LLM이 스스로 생성한 코드의 오류를 분석하고 피드백을 통해 점진적으로 완성도를 높입니다.</p>
        <p>실험 결과, 제안된 파이프라인(RAG + Reflexion)은 <strong>최종 변환 정확도 99%</strong>를 달성했으며 , 이는 기존 규칙 기반(Rule-based) 변환기 대비 <strong>약 20%p 높은 성능</strong>입니다. 이를 통해 마이그레이션 리소스를 크게 절감하고 코드 품질을 향상시킬 수 있음을 입증했습니다.</p>
    `,

    introduction: `
        <p>기업용 애플리케이션 개발에 특화된 Java 프레임워크인 Proworks는 안정적인 백엔드 구축을 위한 다양한 기능을 제공합니다. 최신 버전인 Proworks 5는 성능과 유지보수 편의성이 대폭 향상되었으나, 코드 구조의 근본적인 변화로 인해 Proworks 4에서의 마이그레이션에 높은 기술적, 관리적 부담이 발생하고 있습니다.</p>
        
        <h3>1.1 Problem Statement</h3>
        <p>현행 마이그레이션 과정의 주요 문제점(Pain Points)은 다음과 같습니다:</p>
        <ul class="problem-list">
            <li><strong>규칙 기반 변환의 구조적 한계:</strong> 기존 규칙 기반 방식은 정해진 패턴 외에 다양한 코드 스타일이나 예외 상황을 처리하지 못하여 수작업 개입이 불가피합니다.</li>
            <li><strong>문맥 기반 구조 변환의 비효율성:</strong> 여러 Map 객체를 하나의 VO(Value Object)로 통합하는 등, 코드의 의미적 이해가 필요한 고차원적 변환에 대응하기 어렵습니다.</li>
            <li><strong>과도한 수작업 의존성:</strong> 변환 실패 시 자동화된 복구 절차가 없고, 변환 후 검수 과정 또한 많은 리소스를 소모하여 전체 프로젝트의 일정 지연과 품질 저하를 야기합니다.</li>
        </ul>
    `,

    method: `
        <p>본 프로젝트는 단순한 정규표현식 기반의 치환을 넘어, 코드의 구조적·문맥적 의미를 이해하여 고차원적인 변환을 자동화하는 것을 목표로 합니다. 이를 위해 전체 변환 과정을 여러 단계로 나누는 계획 기반 접근 방식(Planning Approach)을 채택했습니다. 먼저 호출 그래프(Callgraph) 분석을 통해 스켈레톤 코드를 생성한 후, LLM이 각 함수의 내부 로직을 채우는 방식으로 진행하여 LLM의 환각(Hallucination) 문제를 줄이고 변환의 안정성을 높였습니다.</p>
    `,

    methodDetails: `
        <h3>2.1 Development Environment & Constraints</h3>
        <p>기업의 보안 정책을 준수하기 위해 외부 클라우드 API 없이 로컬 환경에서 모든 기능이 실행되도록 시스템을 설계했습니다.</p>
        <div class="tech-stack">
            <span class="tech-tag">Python 3.10</span>
            <span class="tech-tag">Java 1.8</span>
            <span class="tech-tag">FastAPI</span>
            <span class="tech-tag">Ollama</span>
            <span class="tech-tag">FAISS (RAG)</span>
            <span class="tech-tag">Tree-sitter</span>
        </div>
        <div class="solution-highlights">
            <ul>
                <li><strong>로컬 환경 구동:</strong> 인터넷 연결이 없는 폐쇄망 환경에서 완전 작동 </li>
                <li><strong>LLM 제약사항:</strong> 별도의 LLM 학습(Fine-tuning) 없이 사용 </li>
                <li><strong>GPU 효율성:</strong> VRAM 40GB 이하의 단일 A100 GPU 환경에서 안정적 실행 </li>
                <li><strong>VS Code 확장 기능:</strong> 개발자 친화적인 UI/UX 제공을 위해 자체 구현 </li>
            </ul>
        </div>
    `,

    implementation: ``,

    results: `
        <p>시스템의 각 모듈별 성능과 전체 파이프라인의 효율성을 검증하기 위해, 실제 사용 사례를 기반으로 구성된 4가지 카테고리의 평가 데이터셋에 대해 정량 평가를 수행했습니다. 평가는 변환된 코드가 단위 테스트를 통과하는지 여부(Unit test correctness)를 기준으로 측정했습니다.</p>
        
        <h3>4.1 VO Generation Performance</h3>
        <p>Proworks 5의 핵심인 VO(Value Object) 클래스 생성 정확도를 평가한 결과, 기존 LLM(GPT-4.1)이 50%의 정확도를 보인 반면, 본 프로젝트의 <strong>의존성 분석 모듈은 100%의 정확도</strong>로 모든 테스트 케이스에서 완벽하게 VO 클래스를 생성했습니다. 이는 LLM의 환각 문제를 원천 차단하고 안정적인 변환의 기반을 마련했음을 의미합니다.</p>

        <h3>4.2 Code Conversion Pipeline Performance</h3>
        <p>코드 변환 파이프라인의 성능을 단계적으로 측정한 결과, RAG와 Reflexion 모듈이 정확도 향상에 결정적인 역할을 하는 것을 확인했습니다. (Base model: devstral:24b) </p>
         <ul class="problem-list">
            <li><strong>Base (LLM only):</strong> 평균 정확도 54%. 특히 API 호출(API Calls) 변환 정확도는 2%에 불과해 외부 지식 없이는 한계가 명확했습니다.</li>
            <li><strong>Base + RAG:</strong> 평균 정확도 91%로 크게 향상. Proworks 5 문서를 참조하면서 API 호출 정확도가 98%까지 상승했으며, 문서 내 예시 코드 덕분에 다른 영역의 성능도 개선되었습니다.</li>
            <li><strong>Base + Reflexion:</strong> 평균 정확도 69%로 향상. 피드백 루프를 통해 잘못된 패턴을 스스로 교정하는 효과가 있었습니다.</li>
            <li><strong>Base + RAG + Reflexion (Final):</strong> <strong>평균 정확도 99%</strong>를 달성하며 대부분의 항목에서 완벽한 변환 성능을 보였습니다. 이는 두 모듈의 시너지가 매우 효과적임을 증명합니다.</li>
        </ul>
    `,

    achievements: `
        <h3>4.3 Comparison with Baselines</h3>
        <p>제안된 최종 파이프라인의 성능을 기존의 규칙 기반(Rule-based) 변환기와 여러 다른 LLM 모델들과 비교했습니다.</p>
        <div class="results-table-container" style="margin-bottom: 2rem;">
            <table class="results-table enhanced">
                <thead>
                    <tr>
                        <th>Model / Method</th>
                        <th>Avg Score</th>
                        <th>API calls</th>
                        <th>VO get/set</th>
                        <th>Type Changes</th>
                        <th>Edge cases</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Inswave-base (Rule-based)</td>
                        <td>0.79</td>
                        <td>0.32</td>
                        <td>0.99</td>
                        <td>0.98</td>
                        <td>0.87</td>
                    </tr>
                    <tr class="table-row-highlight">
                        <td><strong>Ours (devstral:24b + RAG + Reflexion)</strong></td>
                        <td><span class="result-badge success">0.99</span></td>
                        <td><span class="result-badge success">1.00</span></td>
                        <td><span class="result-badge success">1.00</span></td>
                        <td><span class="result-badge success">1.00</span></td>
                        <td><span class="result-badge success">0.98</span></td>
                    </tr>
                </tbody>
            </table>
            <p style="text-align: center; margin-top: 0.5rem; font-size: 0.9em;"><em>규칙 기반 변환기 대비 약 20%p의 성능 향상을 달성했습니다.</em></p>
        </div>

        <h3>4.4 Implementation Issues & Solutions</h3>
        <p>프로젝트 진행 중 발생했던 주요 기술적 문제와 해결 방안은 다음과 같습니다:</p>
        <div class="problem-list">
            <li><strong>LLM 응답 형식 불일치:</strong> LLM의 출력이 일정하지 않아 파싱 오류가 발생하는 문제가 있었습니다. 프롬프트에 ```java 태그를 명시적으로 삽입하여 코드 블록 출력을 유도하는 방식으로 해결했습니다[cite: 381, 383, 384].</li>
            <li><strong>변환 규칙 미준수:</strong> "주석을 삭제하지 말라"는 등의 명시적 규칙을 LLM이 위반하는 경우가 있었습니다. 이는 Self-Refinement 모듈의 피드백 규칙에 해당 항목을 추가하여 반복적으로 교정하도록 개선했습니다.</li>
            <li><strong>RAG 컨텍스트 부적합:</strong> RAG가 검색한 문서 조각(chunk)이 변환에 필요한 핵심 정보를 포함하지 않는 경우가 있었습니다. 문서의 chunk 크기를 의미 단위로 재조정하고 유사도 기반 필터링을 강화하여 해결했습니다.</li>
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