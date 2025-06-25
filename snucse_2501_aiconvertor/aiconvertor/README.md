 # Line-by-line conversion

### 코드 변환 요구사항
* 주석 또는 기존 코드의 spacing, Map과 관련 없는 기존 코드에 변경이 없어야 할 것 (diff를 최소화하기 위함)
* variable 이름 또한 변경 금지

### 메인 스크립트 파일
* `convert_map_to_vo.py`: in-context-example, answer과 비교, variable normalization, step-by-step eval 및 rule deduction 등의 기능 포함

### 실행 예시
```
# 변환 수행 및 평가 (refactored.java에 저장됨)
python convert_map_to_vo.py --input samples_eval/SecuritiesInqrPritMgmtBCServiceImpl.java --vo samples_eval/SecuritiesInqrPritMgmtVo.java \
--output samples_eval/refactored.java --model devstral:24b \
--examples samples_eval/in-context-examples.txt --examples_out samples_eval/final-in-context-examples.txt --answer samples_eval/gt.java --normalize-vars --peel-nested

# 변환 수행 및 평가 (rule-deduction 포함) (refactored.java에 저장됨)
python convert_map_to_vo.py --input samples_eval/SecuritiesInqrPritMgmtBCServiceImpl.java --vo samples_eval/SecuritiesInqrPritMgmtVo.java \
--output samples_eval/refactored.java --model devstral:24b \
--examples samples_eval/in-context-examples.txt --examples_out samples_eval/final-in-context-examples.txt --answer samples_eval/gt.java --normalize-vars --peel-nested --deduce-rule

# 전체 프로젝트 코드 변환 (src 폴더)
python convert_map_to_vo.py --input /path/to/src --vo samples_eval/SecuritiesInqrPritMgmtVoProject.java \
--output samples_eval/refactored.java --model devstral:24b \
--examples samples_eval/in-context-examples.txt --examples_out samples_eval/final-in-context-examples.txt --normalize-vars --peel-nested
```

### Features
| 옵션 | 설명 |
|------|------|
| `--use-reflextion` | reflextion |
| `--use-prompt-normalization` | 프롬프트 정규화 사용 |
| `--use-vo-generator` | vo 생성 사용 |
| `--use-api-rag` | Proworks5 api RAG 사용 |
| `--use-case-rag` | Case RAG 사용 |
| `--max-line-limit-offset {num_line_limit}` | LLM 생성시, 라인 수 제한을 위한 오프셋 |
| `--skip-non-map` | Map 관련 코드가 없는 경우 변환 건너뛰기 |

