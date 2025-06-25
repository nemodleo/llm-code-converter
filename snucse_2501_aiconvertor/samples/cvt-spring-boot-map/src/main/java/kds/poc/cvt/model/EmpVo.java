package kds.poc.cvt.model;

import lombok.Data;

/** Direct 1-to-1 with EMP table columns (camelCase <-> snake_case handled). */
@Data
public class EmpVo {
    private String empno;
    private String ename;
    private String job;
    private String mgr;
    private String hiredate;   // keep String for parity, or change to Instant
    private String sal;
    private String comm;
    private String deptno;
    private String account;
}