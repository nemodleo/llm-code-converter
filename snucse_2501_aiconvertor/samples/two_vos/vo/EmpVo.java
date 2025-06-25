package kds.poc.com.inswave.cvt.vo;

import java.io.Serializable;

/**
 * Employee Value Object
 */
public class EmpVo implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    private Integer empNo;
    private String empName;
    private String job;
    private Integer deptNo;
    private Double salary;
    private String hireDate;
    
    public EmpVo() {}
    
    public Integer getEmpNo() {
        return empNo;
    }
    
    public void setEmpNo(Integer empNo) {
        this.empNo = empNo;
    }
    
    public String getEmpName() {
        return empName;
    }
    
    public void setEmpName(String empName) {
        this.empName = empName;
    }
    
    public String getJob() {
        return job;
    }
    
    public void setJob(String job) {
        this.job = job;
    }
    
    public Integer getDeptNo() {
        return deptNo;
    }
    
    public void setDeptNo(Integer deptNo) {
        this.deptNo = deptNo;
    }
    
    public Double getSalary() {
        return salary;
    }
    
    public void setSalary(Double salary) {
        this.salary = salary;
    }
    
    public String getHireDate() {
        return hireDate;
    }
    
    public void setHireDate(String hireDate) {
        this.hireDate = hireDate;
    }
} 