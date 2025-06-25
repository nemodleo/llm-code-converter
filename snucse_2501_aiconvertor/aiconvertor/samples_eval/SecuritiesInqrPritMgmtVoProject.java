package am.im.securitiesinqrpritmgmt.vo;

import com.inswave.elfw.annotation.ElDto;
import com.inswave.elfw.annotation.ElDtoField;
import com.fasterxml.jackson.annotation.JsonFilter;

@JsonFilter("elExcludeFilter")
@ElDto(FldYn = "", logicalName = "증권조회가격관리 파라미터")
public class SecuritiesInqrPritMgmtVo extends com.inswave.eladmin.cmmn.DemoCommVO {
    private static final long serialVersionUID = 1L;

    @ElDtoField(logicalName = "거래일자 From", physicalName = "TRNS_DATE_FROM", type = "String", length = 8)
    private String trnsDateFrom;

    @ElDtoField(logicalName = "거래일자 To", physicalName = "TRNS_DATE_TO", type = "String", length = 8)
    private String trnsDateTo;

    @ElDtoField(logicalName = "거래일자 From1", physicalName = "TRNS_DATE_FROM1", type = "String", length = 8)
    private String trnsDateFrom1;

    @ElDtoField(logicalName = "거래일자 To1", physicalName = "TRNS_DATE_TO1", type = "String", length = 8)
    private String trnsDateTo1;

    @ElDtoField(logicalName = "거래일자 From2", physicalName = "TRNS_DATE_FROM2", type = "String", length = 8)
    private String trnsDateFrom2;

    @ElDtoField(logicalName = "거래일자 To2", physicalName = "TRNS_DATE_TO2", type = "String", length = 8)
    private String trnsDateTo2;

    @ElDtoField(logicalName = "설정은행코드1", physicalName = "ESTB_BANK_TRNS_BRCD1", type = "String", length = 10)
    private String estbBankTrnsBrcd1;

    @ElDtoField(logicalName = "설정은행코드2", physicalName = "ESTB_BANK_TRNS_BRCD2", type = "String", length = 10)
    private String estbBankTrnsBrcd2;

    @ElDtoField(logicalName = "조회기준일", physicalName = "BSDA", type = "String", length = 8)
    private String bsda;

    @ElDtoField(logicalName = "구분", physicalName = "GUBUN", type = "String", length = 1)
    private String gubun;

    @ElDtoField(logicalName = "페이지", physicalName = "page", type = "Integer", length = 0)
    private Integer page;

    @ElDtoField(logicalName = "페이지크기", physicalName = "pageSize", type = "Integer", length = 0)
    private Integer pageSize;

    @ElDtoField(logicalName = "시작행번호", physicalName = "START_RNUM", type = "Integer", length = 0)
    private Integer startRnum;

    @ElDtoField(logicalName = "종료행번호", physicalName = "END_RNUM", type = "Integer", length = 0)
    private Integer endRnum;

    @ElDtoField(logicalName = "총행수", physicalName = "rowCount", type = "Integer", length = 0)
    private Integer rowCount;

    @ElDtoField(logicalName = "결과상태", physicalName = "resultStatus", type = "Integer", length = 0)
    private Integer resultStatus;

    // getters & setters

    public String getTrnsDateFrom() {
        return trnsDateFrom;
    }

    public void setTrnsDateFrom(String trnsDateFrom) {
        this.trnsDateFrom = trnsDateFrom;
    }

    public String getTrnsDateTo() {
        return trnsDateTo;
    }

    public void setTrnsDateTo(String trnsDateTo) {
        this.trnsDateTo = trnsDateTo;
    }

    public String getTrnsDateFrom1() {
        return trnsDateFrom1;
    }

    public void setTrnsDateFrom1(String trnsDateFrom1) {
        this.trnsDateFrom1 = trnsDateFrom1;
    }

    public String getTrnsDateTo1() {
        return trnsDateTo1;
    }

    public void setTrnsDateTo1(String trnsDateTo1) {
        this.trnsDateTo1 = trnsDateTo1;
    }

    public String getTrnsDateFrom2() {
        return trnsDateFrom2;
    }

    public void setTrnsDateFrom2(String trnsDateFrom2) {
        this.trnsDateFrom2 = trnsDateFrom2;
    }

    public String getTrnsDateTo2() {
        return trnsDateTo2;
    }

    public void setTrnsDateTo2(String trnsDateTo2) {
        this.trnsDateTo2 = trnsDateTo2;
    }

    public String getEstbBankTrnsBrcd1() {
        return estbBankTrnsBrcd1;
    }

    public void setEstbBankTrnsBrcd1(String estbBankTrnsBrcd1) {
        this.estbBankTrnsBrcd1 = estbBankTrnsBrcd1;
    }

    public String getEstbBankTrnsBrcd2() {
        return estbBankTrnsBrcd2;
    }

    public void setEstbBankTrnsBrcd2(String estbBankTrnsBrcd2) {
        this.estbBankTrnsBrcd2 = estbBankTrnsBrcd2;
    }

    public String getBsda() {
        return bsda;
    }

    public void setBsda(String bsda) {
        this.bsda = bsda;
    }

    public String getGubun() {
        return gubun;
    }

    public void setGubun(String gubun) {
        this.gubun = gubun;
    }

    public Integer getPage() {
        return page;
    }

    public void setPage(Integer page) {
        this.page = page;
    }

    public Integer getPageSize() {
        return pageSize;
    }

    public void setPageSize(Integer pageSize) {
        this.pageSize = pageSize;
    }

    public Integer getStartRnum() {
        return startRnum;
    }

    public void setStartRnum(Integer startRnum) {
        this.startRnum = startRnum;
    }

    public Integer getEndRnum() {
        return endRnum;
    }

    public void setEndRnum(Integer endRnum) {
        this.endRnum = endRnum;
    }

    public Integer getRowCount() {
        return rowCount;
    }

    public void setRowCount(Integer rowCount) {
        this.rowCount = rowCount;
    }

    public Integer getResultStatus() {
        return resultStatus;
    }

    public void setResultStatus(Integer resultStatus) {
        this.resultStatus = resultStatus;
    }
}