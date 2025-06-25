package kds.poc.cvt.dao;

import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Repository;

import kds.poc.cvt.mapper.EmpMapper;
import kds.poc.cvt.mapper.FundMapper;

@Repository("cvtDAO")
public class CvtDAO {

    private final EmpMapper empMapper;
    private final FundMapper fundMapper;

    public CvtDAO(EmpMapper empMapper, FundMapper fundMapper) {
        this.empMapper = empMapper;
        this.fundMapper = fundMapper;
    }

    public int insertEmp(Map<String, Object> empMap) {
        return empMapper.insertEmp(empMap);
    }

    public int updateEmp(Map<String, Object> empMap) {
        return empMapper.updateEmp(empMap);
    }

    public int deleteEmp(Map<String, Object> empMap) {
        return empMapper.deleteEmp(empMap);
    }

    public List<Map<String, Object>> selectEmp(Map<String, Object> empMap) {
        return empMapper.selectEmp(empMap);
    }

    public int insertFund(Map<String, Object> fundMap) {
        return fundMapper.insertFund(fundMap);
    }

    public int updateFund(Map<String, Object> fundMap) {
        return fundMapper.updateFund(fundMap);
    }

    public int deleteFund(Map<String, Object> fundMap) {
        return fundMapper.deleteFund(fundMap);
    }

    public List<Map<String, Object>> selectFund(Map<String, Object> fundMap) {
        return fundMapper.selectFund(fundMap);
    }

    public Map<String, Object> selectFundByCode(String fundCode) {
        return fundMapper.selectFundByCode(fundCode);
    }

    public int insertFundPerformance(Map<String, Object> performanceMap) {
        return fundMapper.insertFundPerformance(performanceMap);
    }

    public List<Map<String, Object>> selectFundPerformance(String fundCode) {
        return fundMapper.selectFundPerformance(fundCode);
    }

    public List<Map<String, Object>> selectFundPerformanceByDateRange(String fundCode, String startDate, String endDate) {
        return fundMapper.selectFundPerformanceByDateRange(fundCode, startDate, endDate);
    }
}