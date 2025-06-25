# Line-by-line conversion

### 코드 변환 요구사항
* 주석 또는 기존 코드의 spacing, Map과 관련 없는 기존 코드에 변경이 없어야 할 것 (diff를 최소화하기 위함)
* variable 이름 또한 변경 금지

### 파일
* `main.py`: generated_converter.py 생성 및 타겟 파일 변환

### 실행 예시
```
# `examples를 바탕으로 변환 함수 fitting 및 파일 변환 (`generated_converter.py`를 바탕으로 `samples_eval/SecuritiesInqrPritMgmtBCServiceImpl.java.converted`에 변환됨)
python main.py \
    --examples samples/in-context-examples-many.txt \
    samples_eval/SecuritiesInqrPritMgmtBCServiceImpl.java \
    samples_eval/SecuritiesInqrPritMgmtBCServiceImpl.java \
  -m devstral:24b --fail-sample-size 20 --max-iters 10 \
  --save-convertor generated_converter.py
```