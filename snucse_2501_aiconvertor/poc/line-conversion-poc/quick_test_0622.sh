python convert_map_to_vo_v5.py --input samples_eval/SecuritiesInqrPritMgmtBCServiceImpl.java --vo samples_eval/SecuritiesInqrPritMgmtVo.java \
--output samples_eval/refactored.java --model devstral:24b \
--examples samples_eval/in-context-examples.txt

python convert_map_to_vo_v5.py --input samples_eval/SecuritiesInqrPritMgmtBCServiceImpl.java --vo samples_eval/SecuritiesInqrPritMgmtVo.java \
--output samples_eval/refactored.java --model devstral:24b \
--examples samples_eval/new-in-context-examples.txt --examples_out samples_eval/final-in-context-examples.txt --answer samples_eval/gt.java