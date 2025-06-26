// Content data for the website
const content = {
    abstract: `
        <p>인스웨이브(Inswave)사의 Java 프레임워크 'Proworks 4'를 'Proworks 5'로 마이그레이션하는 작업은 수작업 의존도가 높아 비효율적이며, 오류 발생 가능성 또한 큽니다. 본 프로젝트는 이러한 문제를 해결하기 위해 <strong>LLM(거대 언어 모델) 기반의 코드 변환 자동화 도구</strong>를 개발하는 것을 목표로 합니다.</p>
        <p>이를 위해 세 가지 핵심 모듈을 설계 및 구현했습니다. (1) <strong>의존성 분석(Dependency Analysis) 모듈</strong>은 정적 분석과 호출 그래프(Call Graph) 파싱을 통해 Proworks 5에서 요구하는 데이터 클래스(VO)와 스켈레톤 코드를 자동 생성합니다. (2) <strong>코드 변환(Code Conversion) 모듈</strong>은 LLM을 활용해 레거시 코드를 변환하며, RAG(검색 증강 생성) 기법을 통해 Proworks 5 공식 문서를 참조하여 정확도를 높입니다. (3) <strong>자가 개선(Self-Refinement) 모듈</strong>은 Reflexion 기법을 기반으로, LLM이 스스로 생성한 코드의 오류를 분석하고 피드백을 통해 점진적으로 완성도를 향상시킵니다.</p>
        <p>실험 결과, 제안한 파이프라인(RAG + Reflexion)은 <strong>최종 변환 정확도 ~100%</strong>를 달성했으며, 이는 기존 규칙 기반(Rule-based) 변환기 대비 <strong>약 20%p 향상된 성능</strong>입니다. 이를 통해 마이그레이션 리소스를 대폭 절감하고 코드 품질을 개선할 수 있음을 입증했습니다.</p>
    `,

    introduction: `
        <p>Proworks는 기업용 애플리케이션 개발에 특화된 Java 프레임워크로, 안정적인 백엔드 구축을 위한 다양한 기능을 제공합니다. 최신 버전인 Proworks 5는 성능과 유지보수 편의성이 대폭 향상되었지만, 코드 구조의 근본적인 변화로 인해 Proworks 4에서의 마이그레이션은 높은 기술적·관리적 부담을 동반합니다.</p>
        
        <h3>Problem Statement</h3>
        <p>현재 마이그레이션 과정의 주요 문제점(Pain Points)은 다음과 같습니다:</p>
        <ul class="problem-list">
            <li><strong>규칙 기반 변환의 구조적 한계:</strong> 기존 규칙 기반 방식은 정해진 패턴 외의 다양한 코드 스타일이나 예외 상황을 처리하지 못해 수작업 개입이 불가피합니다.</li>
            <li><strong>문맥 기반 구조 변환의 비효율성:</strong> 여러 Map 객체를 하나의 VO(Value Object)로 통합하는 등 코드 의미를 이해해야 하는 고차원적 변환에는 한계가 있습니다.</li>
            <li><strong>과도한 수작업 의존성:</strong> 변환 실패 시 자동 복구가 불가능하고, 검수 또한 많은 리소스를 소모하여 전체 일정 지연과 품질 저하를 야기합니다.</li>
        </ul>
    `,

    method: `
        <p>본 프로젝트는 단순한 정규표현식 치환을 넘어 코드의 구조와 문맥을 이해하여 고차원적인 변환을 자동화하는 것을 목표로 합니다. 이를 위해 전체 변환 과정을 여러 단계로 나눈 계획 기반 접근 방식(Planning Approach)을 채택했습니다. 먼저 호출 그래프(Call Graph)를 분석해 스켈레톤 코드를 생성한 후, LLM이 각 함수의 내부 로직을 채워넣는 방식으로 환각(Hallucination)을 줄이고 변환 안정성을 확보했습니다.</p>
    `,

    methodDetails: `
        <h3>Development Environment & Constraints</h3>
        <p>기업의 보안 정책을 고려해, 외부 클라우드 API 없이 로컬 환경에서 모든 기능이 작동하도록 시스템을 설계했습니다.</p>
        <div class="tech-stack">
            <span class="tech-tag">Python 3.10</span>
            <span class="tech-tag">Java 1.8</span>
            <span class="tech-tag">FastAPI</span>
            <span class="tech-tag">Ollama</span>
            <span class="tech-tag">FAISS (RAG)</span>
            <span class="tech-tag">Tree-sitter</span>
            <span class="tech-tag">LangChain</span>
        </div>
        <div class="solution-highlights">
            <ul>
                <li><strong>로컬 환경 완전 대응:</strong> 인터넷 연결이 없는 폐쇄망에서도 전 기능 작동</li>
                <li><strong>LLM 활용 제약:</strong> 별도 파인튜닝(Fine-tuning) 없이 사전학습 모델만 활용</li>
                <li><strong>GPU 효율성 확보:</strong> A100 GPU (VRAM 40GB 이하) 단일 장비에서 안정적 실행</li>
                <li><strong>VS Code 확장 제공:</strong> 개발자 친화적 UI/UX를 위한 자체 플러그인 구현</li>
            </ul>
        </div>
    `,

    implementation: ``,

    results: `
        <p>시스템의 각 모듈별 성능과 전체 파이프라인의 효율성을 검증하기 위해 실제 사례 기반의 4가지 평가 카테고리에 대해 정량 평가를 수행했습니다. 평가는 변환된 코드가 단위 테스트를 통과하는지(Unit Test Correctness) 여부로 측정했습니다.</p>
        
        <h3>VO Generation Performance</h3>
        <p>Proworks 5의 핵심인 VO 클래스 생성 정확도를 평가한 결과, 기존 LLM(GPT-4.1)은 50% 정확도를 보인 반면, 본 프로젝트의 <strong>의존성 분석 모듈은 100%</strong> 정확도로 모든 테스트 케이스에서 완벽한 VO 생성을 달성했습니다.</p>

        <h3>Code Conversion Pipeline Performance</h3>
        <p>변환 파이프라인의 각 조합별 성능을 단계적으로 측정했습니다. (Base model: devstral:24b)</p>
        <ul class="problem-list">
            <li><strong>Base (LLM only):</strong> 평균 정확도 54%. 특히 API 호출 변환은 2%에 불과해 외부 지식 없이는 한계가 분명했습니다.</li>
            <li><strong>Base + RAG:</strong> 평균 정확도 91%로 급상승. 공식 문서를 참조함으로써 API 호출 정확도가 98%에 도달했습니다.</li>
            <li><strong>Base + Reflexion:</strong> 평균 정확도 69%. 반복 피드백을 통해 오류 패턴을 스스로 교정하는 효과를 확인했습니다.</li>
            <li><strong>Base + RAG + Reflexion (Final):</strong> <strong>평균 정확도 ~100%</strong>. 모든 영역에서 완벽한 수준의 변환 성능을 보이며 두 기법의 시너지를 입증했습니다.</li>
        </ul>
    `,

    achievements: `
        <h3>Comparison with Baselines</h3>
        <p>최종 파이프라인의 성능을 기존 규칙 기반 변환기 및 다양한 LLM 기반 방법들과 비교했습니다.</p>
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

        <h3>Implementation Issues & Solutions</h3>
        <p>프로젝트 진행 중 발생한 주요 기술적 문제와 해결 방안은 다음과 같습니다:</p>
        <div class="problem-list">
            <li><strong>LLM 응답 형식 불일치:</strong> LLM 출력이 일정하지 않아 파싱 오류가 발생. 프롬프트에 <code>\`\`\`java</code> 태그를 명시적으로 삽입하여 해결했습니다.</li>
            <li><strong>변환 규칙 미준수:</strong> "주석 삭제 금지" 등 명시 규칙을 위반하는 사례가 있었고, Self-Refinement 모듈의 피드백 규칙에 추가해 반복 학습으로 교정했습니다.</li>
            <li><strong>RAG 컨텍스트 부적합:</strong> 검색된 문서 조각이 핵심 정보를 포함하지 않는 문제를, 의미 단위 기반의 chunk 재조정과 유사도 필터링 강화를 통해 해결했습니다.</li>
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