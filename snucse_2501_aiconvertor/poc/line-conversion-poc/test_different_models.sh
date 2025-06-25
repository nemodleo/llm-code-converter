
#!/bin/bash

set -e

# MODELS=("llama3.2" "llama3.1:8b" "qwen3:8b")
MODELS=("llama3.1:8b" "qwen3:8b")
SUMMARY_FILE="model_outputs/error_summary.txt"
mkdir -p model_outputs

INPUT_INIT="samples/SecuritiesInqrPritMgmtBCServiceImpl.java"
INPUT_EVAL="samples_eval/SecuritiesInqrPritMgmtBCServiceImpl.java"
VO_INIT="samples/SecuritiesInqrPritMgmtVo.java"
VO_EVAL="samples_eval/SecuritiesInqrPritMgmtVo.java"
GT="samples_eval/gt.java"
EXAMPLES_INIT="samples/in-context-examples.txt"

echo "Model Error Summary" > "$SUMMARY_FILE"
echo "===================" >> "$SUMMARY_FILE"


for MODEL in "${MODELS[@]}"; do
    SAFE_MODEL=${MODEL//[:\/]/_}

    echo "=== Running for model: $MODEL ==="

    # Step 1: Generate initial refactored output
    python convert_map_to_vo_v3.py --input "$INPUT_INIT" --vo "$VO_INIT" \
        --output samples/refactored.java --model "$MODEL" \
        --examples "$EXAMPLES_INIT" > "model_outputs/log1_${SAFE_MODEL}.txt" 2>&1

    # Step 2: Evaluate and save new in-context examples
    OUTPUT=$(python convert_map_to_vo_v3.py --input "$INPUT_INIT" --vo "$VO_INIT" \
        --output samples/refactored.java --model "$MODEL" \
        --examples "$EXAMPLES_INIT" --examples_out samples_eval/new-in-context-examples.txt \
        --answer samples/gt.java >> "model_outputs/log1_${SAFE_MODEL}.txt" 2>&1)
    ERRORS=$(echo "$OUTPUT" | grep -oE '[0-9]+ errors found' | cut -d' ' -f1)
    ERRORS=${ERRORS:-"ERROR"}
    echo "$MODEL: $ERRORS errors" >> "$SUMMARY_FILE"

    # Step 3: Generate output on eval sample with new context
    python convert_map_to_vo_v3.py --input "$INPUT_EVAL" --vo "$VO_EVAL" \
        --output samples_eval/refactored.java --model "$MODEL" \
        --examples samples_eval/new-in-context-examples.txt > "model_outputs/log2_${SAFE_MODEL}.txt" 2>&1

    # Step 4: Compare with answer and save final examples
    OUTPUT=$(python convert_map_to_vo_v3.py --input "$INPUT_EVAL" --vo "$VO_EVAL" \
        --output samples_eval/refactored.java --model "$MODEL" \
        --examples samples_eval/new-in-context-examples.txt \
        --examples_out samples_eval/final-in-context-examples.txt \
        --answer "$GT" 2>&1)

    echo "$OUTPUT" > "model_outputs/log3_${SAFE_MODEL}.txt"

    ERRORS=$(echo "$OUTPUT" | grep -oE '[0-9]+ errors found' | cut -d' ' -f1)
    ERRORS=${ERRORS:-"ERROR"}
    echo "$MODEL: $ERRORS errors" >> "$SUMMARY_FILE"

    # Optional: Zero-shot section
    # python convert_map_to_vo_v3.py --input "$INPUT_EVAL" --vo "$VO_EVAL" \
    #     --output samples_eval/refactored_zeroshot.java --model "$MODEL" \
    #     --examples "$EXAMPLES_INIT" > "model_outputs/log4_${SAFE_MODEL}.txt" 2>&1

    # OUTPUT_ZERO=$(python convert_map_to_vo_v3.py --input "$INPUT_EVAL" --vo "$VO_EVAL" \
    #     --output samples_eval/refactored_zeroshot.java --model "$MODEL" \
    #     --examples "$EXAMPLES_INIT" \
    #     --examples_out samples_eval/final-zeroshot-in-context-examples.txt \
    #     --answer "$GT" 2>&1)

    # echo "$OUTPUT_ZERO" > "model_outputs/log5_${SAFE_MODEL}.txt"

    # ERRORS_ZERO=$(echo "$OUTPUT_ZERO" | grep -oE '[0-9]+ errors found' | cut -d' ' -f1)
    # ERRORS_ZERO=${ERRORS_ZERO:-"ERROR"}
    # echo "$MODEL (zero-shot): $ERRORS_ZERO errors" >> "$SUMMARY_FILE"
done

echo "=== Done. Summary saved to $SUMMARY_FILE ==="