package kds.poc.com.inswave.cvt.vo;

import com.inswave.elfw.annotation.ElDto;
import com.inswave.elfw.annotation.ElDtoField;
import com.inswave.elfw.annotation.ElVoField;
import com.fasterxml.jackson.annotation.JsonFilter;

@JsonFilter("elExcludeFilter")
@ElDto(FldYn = "", logicalName = "사원정보")
public class EmpVo extends com.inswave.eladmin.cmmn.DemoCommVO {
    private static final long serialVersionUID = 1L;

    @ElDtoField(logicalName = "사번", physicalName = "empno", type = "String", typeKind = "", fldYn = "", length = 4, dotLen = 0, baseValue = "", desc = "Employee number")
    private String empno;

    @ElDtoField(logicalName = "성명", physicalName = "ename", type = "String", typeKind = "", fldYn = "", length = 50, dotLen = 0, baseValue = "", desc = "Employee name")
    private String ename;

    @ElDtoField(logicalName = "직업", physicalName = "job", type = "String", typeKind = "", fldYn = "", length = 50, dotLen = 0, baseValue = "", desc = "Job title")
    private String job;

    @ElDtoField(logicalName = "직속상관", physicalName = "mgr", type = "Integer", typeKind = "", fldYn = "", length = 0, dotLen = 0, baseValue = "", desc = "Manager employee number")
    private Integer mgr;

    @ElDtoField(logicalName = "입사일", physicalName = "hiredate", type = "String", typeKind = "", fldYn = "", length = 10, dotLen = 0, baseValue = "", desc = "Hire date (YYYY-MM-DD)")
    private String hiredate;

    @ElDtoField(logicalName = "급여", physicalName = "sal", type = "Double", typeKind = "", fldYn = "", length = 0, dotLen = 2, baseValue = "", desc = "Salary")
    private Double sal;

    @ElDtoField(logicalName = "상여", physicalName = "comm", type = "Double", typeKind = "", fldYn = "", length = 0, dotLen = 2, baseValue = "", desc = "Commission")
    private Double comm;

    @ElDtoField(logicalName = "부서번호", physicalName = "deptno", type = "Integer", typeKind = "", fldYn = "", length = 0, dotLen = 0, baseValue = "", desc = "Department number")
    private Integer deptno;

    @ElDtoField(logicalName = "계정", physicalName = "account", type = "Double", typeKind = "", fldYn = "", length = 0, dotLen = 2, baseValue = "", desc = "Account balance")
    private Double account;

    @ElVoField(physicalName = "empno")
    public String getEmpno() {
        return empno;
    }

    @ElVoField(physicalName = "empno")
    public void setEmpno(String empno) {
        this.empno = empno;
    }

    @ElVoField(physicalName = "ename")
    public String getEname() {
        return ename;
    }

    @ElVoField(physicalName = "ename")
    public void setEname(String ename) {
        this.ename = ename;
    }

    @ElVoField(physicalName = "job")
    public String getJob() {
        return job;
    }

    @ElVoField(physicalName = "job")
    public void setJob(String job) {
        this.job = job;
    }

    @ElVoField(physicalName = "mgr")
    public Integer getMgr() {
        return mgr;
    }

    @ElVoField(physicalName = "mgr")
    public void setMgr(Integer mgr) {
        this.mgr = mgr;
    }

    @ElVoField(physicalName = "hiredate")
    public String getHiredate() {
        return hiredate;
    }

    @ElVoField(physicalName = "hiredate")
    public void setHiredate(String hiredate) {
        this.hiredate = hiredate;
    }

    @ElVoField(physicalName = "sal")
    public Double getSal() {
        return sal;
    }

    @ElVoField(physicalName = "sal")
    public void setSal(Double sal) {
        this.sal = sal;
    }

    @ElVoField(physicalName = "comm")
    public Double getComm() {
        return comm;
    }

    @ElVoField(physicalName = "comm")
    public void setComm(Double comm) {
        this.comm = comm;
    }

    @ElVoField(physicalName = "deptno")
    public Integer getDeptno() {
        return deptno;
    }

    @ElVoField(physicalName = "deptno")
    public void setDeptno(Integer deptno) {
        this.deptno = deptno;
    }

    @ElVoField(physicalName = "account")
    public Double getAccount() {
        return account;
    }

    @ElVoField(physicalName = "account")
    public void setAccount(Double account) {
        this.account = account;
    }

    @Override
    public String toString() {
        return "EmpVo [empno=" + empno + ", ename=" + ename + ", job=" + job + 
               ", mgr=" + mgr + ", hiredate=" + hiredate + ", sal=" + sal + 
               ", comm=" + comm + ", deptno=" + deptno + ", account=" + account + "]";
    }

    public boolean isFixedLengthVo() {
        return false;
    }
} 