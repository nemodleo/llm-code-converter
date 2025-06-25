package kds.poc.com.inswave.cvt.vo;

import com.inswave.elfw.annotation.ElDto;
import com.inswave.elfw.annotation.ElDtoField;
import com.inswave.elfw.annotation.ElVoField;
import com.fasterxml.jackson.annotation.JsonFilter;

@JsonFilter("elExcludeFilter")
@ElDto(FldYn = "", logicalName = "사원정보")
public class EmpVo extends com.inswave.eladmin.cmmn.DemoCommVO {
    private static final long serialVersionUID = 1L;

    @ElDtoField(logicalName = "사번", physicalName = "empno", type = "String", typeKind = "", fldYn = "", length = 0, dotLen = 0, baseValue = "", desc = "")
    private String empno;

    @ElDtoField(logicalName = "성명", physicalName = "ename", type = "String", typeKind = "", fldYn = "", length = 0, dotLen = 0, baseValue = "", desc = "")
    private String ename;

    @ElDtoField(logicalName = "직업", physicalName = "job", type = "String", typeKind = "", fldYn = "", length = 0, dotLen = 0, baseValue = "", desc = "")
    private String job;

    @ElDtoField(logicalName = "직속상관", physicalName = "mgr", type = "String", typeKind = "", fldYn = "", length = 0, dotLen = 0, baseValue = "", desc = "")
    private String mgr;

    @ElDtoField(logicalName = "입사일", physicalName = "hiredate", type = "String", typeKind = "", fldYn = "", length = 0, dotLen = 0, baseValue = "", desc = "")
    private String hiredate;

    @ElDtoField(logicalName = "급여", physicalName = "sal", type = "String", typeKind = "", fldYn = "", length = 0, dotLen = 0, baseValue = "", desc = "")
    private String sal;

    @ElDtoField(logicalName = "상여", physicalName = "comm", type = "String", typeKind = "", fldYn = "", length = 0, dotLen = 0, baseValue = "", desc = "")
    private String comm;

    @ElDtoField(logicalName = "부서번호", physicalName = "deptno", type = "String", typeKind = "", fldYn = "", length = 0, dotLen = 0, baseValue = "", desc = "")
    private String deptno;

    @ElDtoField(logicalName = "계정", physicalName = "account", type = "String", typeKind = "", fldYn = "", length = 0, dotLen = 0, baseValue = "", desc = "")
    private String account;

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
    public String getMgr() {
        return mgr;
    }

    @ElVoField(physicalName = "mgr")
    public void setMgr(String mgr) {
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
    public String getSal() {
        return sal;
    }

    @ElVoField(physicalName = "sal")
    public void setSal(String sal) {
        this.sal = sal;
    }

    @ElVoField(physicalName = "comm")
    public String getComm() {
        return comm;
    }

    @ElVoField(physicalName = "comm")
    public void setComm(String comm) {
        this.comm = comm;
    }

    @ElVoField(physicalName = "deptno")
    public String getDeptno() {
        return deptno;
    }

    @ElVoField(physicalName = "deptno")
    public void setDeptno(String deptno) {
        this.deptno = deptno;
    }

    @ElVoField(physicalName = "account")
    public String getAccount() {
        return account;
    }

    @ElVoField(physicalName = "account")
    public void setAccount(String account) {
        this.account = account;
    }

    @Override
    public String toString() {
        return "EmpVo [empno=" + empno + ", ename=" + ename + ", job=" + job + ", mgr=" + mgr + ", hiredate=" + hiredate + ", sal=" + sal + ", comm=" + comm + ", deptno=" + deptno + ", account=" + account + "]";
    }

    public boolean isFixedLengthVo() {
        return false;
    }
} 