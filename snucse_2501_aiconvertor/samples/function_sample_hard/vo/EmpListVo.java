package kds.poc.com.inswave.cvt.vo;

import com.inswave.elfw.annotation.ElDto;
import com.inswave.elfw.annotation.ElDtoField;
import com.fasterxml.jackson.annotation.JsonFilter;

@JsonFilter("elExcludeFilter")
@ElDto(FldYn = "", logicalName = "사원정보")
public class EmpListVo extends com.inswave.eladmin.cmmn.DemoCommVO {
    private static final long serialVersionUID = 1L;

    @ElDtoField(logicalName = "사원정보List", physicalName = "empVoList", type = "kds.poc.com.inswave.cvt.vo.EmpVo", typeKind = "List", fldYn = "", length = 0, dotLen = 0, baseValue = "", desc = "")
    private java.util.List<EmpVo> empVoList;

    public java.util.List<EmpVo> getEmpVoList() {
        return empVoList;
    }

    public void setEmpVoList(java.util.List<EmpVo> empVoList) {
        this.empVoList = empVoList;
    }

    @Override
    public String toString() {
        return "EmpListVo [empVoList=" + empVoList + "]";
    }

    public boolean isFixedLengthVo() {
        return false;
    }
} 