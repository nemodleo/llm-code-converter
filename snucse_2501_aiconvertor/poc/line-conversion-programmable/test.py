#!/usr/bin/env python3
"""
converter_and_score.py
~~~~~~~~~~~~~~~~~~~~~~
• convert_line()  – rewrites one legacy Java line to VO style
• score_examples() – quick unit test on 30 examples (100 % pass)

Run:  python converter_and_score.py
"""

import re
from typing import Dict, List

import pathlib
from utils import load_file

# ────────────────────────── 1.  CONVERTER ────────────────────────────
_GET_RE = re.compile(r'MapDataUtil\.getString\(\s*pDoc\s*,\s*"([^"]+)"\s*\)')
_SET_RE = re.compile(r'MapDataUtil\.setString\(\s*pDoc\s*,\s*"([^"]+)"\s*,\s*([^)]*?)\s*\)')

# (A)  return-type == Map
_SIG_RET_MAP = re.compile(
    r'^(\s*(?:public|protected|private)\s+(?:static\s+)?)(?:Map)'
    r'(\s+\w+\s*\()\s*Map\s+(\w+)(\s*\).*)'
)

# (B)  return-type == ArrayList<Map>
_SIG_RET_LIST = re.compile(
    r'^(\s*(?:public|protected|private)\s+(?:static\s+)?)(?:ArrayList\s*<\s*Map\s*>)'
    r'(\s+\w+\s*\()\s*Map\s+(\w+)(\s*\).*)'
)

# (C)  variable declaration  Map foo =
_VAR_DECL = re.compile(r'^(\s*)Map(\s+\w+\s*=)')

# (D)  new HashMap(…)  →  new VO( )
_HASHMAP_NEW = re.compile(r'new\s+HashMap\s*(?:<[^>]*>)?\s*\(\s*\)')

# generic type anywhere else
_LIST_RE = re.compile(r'ArrayList\s*<\s*Map\s*>', re.IGNORECASE)

def _pascal(tok: str) -> str:
    return ''.join(p.capitalize() for p in tok.lower().split('_'))

def convert_line(line: str, vo_type: str = "SecuritiesInqrPritMgmtVo") -> str:
    # 1) getters
    line = _GET_RE.sub(lambda m: f"pDoc.get{_pascal(m.group(1))}()", line)

    # 2) setters
    line = _SET_RE.sub(lambda m: f"pDoc.set{_pascal(m.group(1))}({m.group(2).strip()})", line)

    # 3) method signatures
    m = _SIG_RET_MAP.match(line)
    if m:
        line = f"{m.group(1)}{vo_type}{m.group(2)}{vo_type} {m.group(3)}{m.group(4)}"
    else:
        m = _SIG_RET_LIST.match(line)
        if m:
            line = f"{m.group(1)}ArrayList<{vo_type}>{m.group(2)}{vo_type} {m.group(3)}{m.group(4)}"

    # 4) variable declarations
    line = _VAR_DECL.sub(lambda m: f"{m.group(1)}{vo_type}{m.group(2)}", line)

    # 5) new HashMap() → new VO()
    line = _HASHMAP_NEW.sub(f"new {vo_type}()", line)

    # 6) any remaining ArrayList<Map>
    line = _LIST_RE.sub(f"ArrayList<{vo_type}>", line)
    return line
# ─────────────────────────── 2.  EXAMPLES ────────────────────────────
EXAMPLES: List[Dict[str, str]] = [
    # --------- method signatures + list variables ----------
    {"input": "public ArrayList<Map> selectInterestRtrvDuda(Map pDoc) throws ElException {",
     "expected": "public ArrayList<SecuritiesInqrPritMgmtVo> selectInterestRtrvDuda(SecuritiesInqrPritMgmtVo pDoc) throws ElException {"},
    {"input": "ArrayList<Map> result = null;",
     "expected": "ArrayList<SecuritiesInqrPritMgmtVo> result = null;"},
    {"input": "public ArrayList<Map> selectDepositsPsst(Map pDoc) throws ElException {",
     "expected": "public ArrayList<SecuritiesInqrPritMgmtVo> selectDepositsPsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {"},
    {"input": "ArrayList<Map> result = null;",
     "expected": "ArrayList<SecuritiesInqrPritMgmtVo> result = null;"},
    {"input": "public ArrayList<Map> selectDepositsBalance(Map pDoc) throws ElException {",
     "expected": "public ArrayList<SecuritiesInqrPritMgmtVo> selectDepositsBalance(SecuritiesInqrPritMgmtVo pDoc) throws ElException {"},
    {"input": "ArrayList<Map> result = null;",
     "expected": "ArrayList<SecuritiesInqrPritMgmtVo> result = null;"},
    {"input": "public ArrayList<Map> selectDepositsWithdrawal(Map pDoc) throws ElException {",
     "expected": "public ArrayList<SecuritiesInqrPritMgmtVo> selectDepositsWithdrawal(SecuritiesInqrPritMgmtVo pDoc) throws ElException {"},
    {"input": "ArrayList<Map> result = null;",
     "expected": "ArrayList<SecuritiesInqrPritMgmtVo> result = null;"},
    {"input": "public ArrayList<Map> selectGnrzReport(Map pDoc) throws ElException {",
     "expected": "public ArrayList<SecuritiesInqrPritMgmtVo> selectGnrzReport(SecuritiesInqrPritMgmtVo pDoc) throws ElException {"},
    {"input": "ArrayList<Map> result = null;",
     "expected": "ArrayList<SecuritiesInqrPritMgmtVo> result = null;"},
    {"input": "public ArrayList<Map> selectCdSalePsst(Map pDoc) throws ElException {",
     "expected": "public ArrayList<SecuritiesInqrPritMgmtVo> selectCdSalePsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {"},
    {"input": "ArrayList<Map> result = null;",
     "expected": "ArrayList<SecuritiesInqrPritMgmtVo> result = null;"},
    {"input": "public ArrayList<Map> selectBondsSalePsst(Map pDoc) throws ElException {",
     "expected": "public ArrayList<SecuritiesInqrPritMgmtVo> selectBondsSalePsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {"},
    {"input": "ArrayList<Map> result = null;",
     "expected": "ArrayList<SecuritiesInqrPritMgmtVo> result = null;"},
    {"input": "public ArrayList<Map> selectOperatingFundsPsst(Map pDoc) throws ElException {",
     "expected": "public ArrayList<SecuritiesInqrPritMgmtVo> selectOperatingFundsPsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {"},
    {"input": "ArrayList<Map> result = null;",
     "expected": "ArrayList<SecuritiesInqrPritMgmtVo> result = null;"},
    {"input": "public ArrayList<Map> selectFundsExecution(Map pDoc) throws ElException {",
     "expected": "public ArrayList<SecuritiesInqrPritMgmtVo> selectFundsExecution(SecuritiesInqrPritMgmtVo pDoc) throws ElException {"},
    {"input": "ArrayList<Map> result = null;",
     "expected": "ArrayList<SecuritiesInqrPritMgmtVo> result = null;"},
    {"input": "public ArrayList<Map> selectExpirationPsst(Map pDoc) throws ElException {",
     "expected": "public ArrayList<SecuritiesInqrPritMgmtVo> selectExpirationPsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {"},
    {"input": "ArrayList<Map> result = null;",
     "expected": "ArrayList<SecuritiesInqrPritMgmtVo> result = null;"},
    {"input": "public ArrayList<Map> selectMmtLedger(Map pDoc) throws ElException {",
     "expected": "public ArrayList<SecuritiesInqrPritMgmtVo> selectMmtLedger(SecuritiesInqrPritMgmtVo pDoc) throws ElException {"},
    {"input": "ArrayList<Map> result = null;",
     "expected": "ArrayList<SecuritiesInqrPritMgmtVo> result = null;"},

    # --------- MapDataUtil get / set ----------
    {"input": 'trnsDateFrom = MapDataUtil.getString(pDoc, "TRNS_DATE_FROM");',
     "expected": 'trnsDateFrom = pDoc.getTrnsDateFrom();'},
    {"input": 'trnsDateTo = MapDataUtil.getString(pDoc, "TRNS_DATE_TO");',
     "expected": 'trnsDateTo = pDoc.getTrnsDateTo();'},
    {"input": 'MapDataUtil.setString(pDoc, "TRNS_DATE_FROM1", trnsDateFrom);',
     "expected": 'pDoc.setTrnsDateFrom1(trnsDateFrom);'},
    {"input": 'MapDataUtil.setString(pDoc, "TRNS_DATE_TO1", trnsDateTo);',
     "expected": 'pDoc.setTrnsDateTo1(trnsDateTo);'},
    {"input": 'MapDataUtil.setString(pDoc, "TRNS_DATE_FROM2", trnsDateFrom);',
     "expected": 'pDoc.setTrnsDateFrom2(trnsDateFrom);'},
    {"input": 'MapDataUtil.setString(pDoc, "TRNS_DATE_TO2", trnsDateTo);',
     "expected": 'pDoc.setTrnsDateTo2(trnsDateTo);'},
    {"input": 'MapDataUtil.setString(pDoc, "ESTB_BANK_TRNS_BRCD1", MapDataUtil.getString(pDoc, "ESTB_BANK_TRNS_BRCD"));',
     "expected": 'pDoc.setEstbBankTrnsBrcd1(pDoc.getEstbBankTrnsBrcd());'},
    {"input": 'MapDataUtil.setString(pDoc, "ESTB_BANK_TRNS_BRCD2", MapDataUtil.getString(pDoc, "ESTB_BANK_TRNS_BRCD"));',
     "expected": 'pDoc.setEstbBankTrnsBrcd2(pDoc.getEstbBankTrnsBrcd());'},
     {"input": "public Map selectSecuritiesStrcPrdtInfo(Map pDoc) throws ElException {",
      "expected": "public SecuritiesInqrPritMgmtVo selectSecuritiesStrcPrdtInfo(SecuritiesInqrPritMgmtVo pDoc) throws ElException {"}
]

# add the two new ones
EXAMPLES += [
    {"input": "Map result = null;", "expected": "SecuritiesInqrPritMgmtVo result = null;"},
    {"input": "Map bizInput = new HashMap();",
     "expected": "SecuritiesInqrPritMgmtVo bizInput = new SecuritiesInqrPritMgmtVo();"},
]


# ─────────────────────────── 3.  SCORER ───────────────────────────────
def score_examples() -> None:
    passed = 0
    for i, ex in enumerate(EXAMPLES, 1):
        got = convert_line(ex["input"])
        if got.strip() == ex["expected"].strip():
            passed += 1
        else:
            print(f"[FAIL {i}]")
            print("  input    :", ex["input"])
            print("  expected :", ex["expected"])
            print("  got      :", got, end="\n\n")
    total = len(EXAMPLES)
    print(f"→ {passed}/{total} lines passed ({passed/total:.1%})")

from generated_converter import convert_line
if __name__ == "__main__":
    score_examples()

    def convert_file(src: pathlib.Path, conv_func, vo_type: str, suffix: str = ".converted") -> pathlib.Path:
        dst = src.with_suffix(src.suffix + suffix)
        converted = [convert_line(line, vo_type=vo_type) for line in load_file(src).splitlines()]
        dst.write_text("\n".join(converted), encoding="utf-8")
        print(dst)
        return dst

    convert_file(pathlib.Path("samples_eval/SecuritiesInqrPritMgmtBCServiceImpl.java"),
                 convert_line, "SecuritiesInqrPritMgmtVo", ".converted")