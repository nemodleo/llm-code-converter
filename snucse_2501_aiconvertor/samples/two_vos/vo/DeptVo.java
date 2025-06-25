package kds.poc.com.inswave.cvt.vo;

import com.inswave.elfw.annotation.ElDto;
import com.inswave.elfw.annotation.ElDtoField;
import com.fasterxml.jackson.annotation.JsonFilter;

@JsonFilter("elExcludeFilter")
@ElDto(FldYn = "", logicalName = "부서정보")
public class DeptVo extends com.inswave.eladmin.cmmn.DemoCommVO {
    private static final long serialVersionUID = 1L;

    @ElDtoField(logicalName = "부서번호", physicalName = "deptno", type = "Integer", typeKind = "", fldYn = "", length = 2, dotLen = 0, baseValue = "", desc = "Department number")
    private Integer deptno;

    @ElDtoField(logicalName = "부서명", physicalName = "dname", type = "String", typeKind = "", fldYn = "", length = 50, dotLen = 0, baseValue = "", desc = "Department name")
    private String dname;

    @ElDtoField(logicalName = "지역", physicalName = "loc", type = "String", typeKind = "", fldYn = "", length = 50, dotLen = 0, baseValue = "", desc = "Location")
    private String loc;

    @ElDtoField(logicalName = "예산", physicalName = "budget", type = "Double", typeKind = "", fldYn = "", length = 0, dotLen = 2, baseValue = "", desc = "Department budget")
    private Double budget;

    public Integer getDeptno() {
        return deptno;
    }

    public void setDeptno(Integer deptno) {
        this.deptno = deptno;
    }

    public String getDname() {
        return dname;
    }

    public void setDname(String dname) {
        this.dname = dname;
    }

    public String getLoc() {
        return loc;
    }

    public void setLoc(String loc) {
        this.loc = loc;
    }

    public Double getBudget() {
        return budget;
    }

    public void setBudget(Double budget) {
        this.budget = budget;
    }

    @Override
    public String toString() {
        return "DeptVo [deptno=" + deptno + ", dname=" + dname + ", loc=" + loc + ", budget=" + budget + "]";
    }
} 