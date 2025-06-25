package kds.poc.cvt.dao;

import java.util.List;

import org.springframework.stereotype.Repository;

import kds.poc.cvt.mapper.EmpMapper;
import kds.poc.cvt.mapper.FundMapper;
import kds.poc.cvt.model.EmpVo;
import kds.poc.cvt.model.FundVo;
import kds.poc.cvt.model.FundPerformanceVo;

@Repository("cvtDAO")
public class CvtDAO {

    private final EmpMapper empMapper;
    private final FundMapper fundMapper;

    public CvtDAO(EmpMapper empMapper, FundMapper fundMapper) {
        this.empMapper = empMapper;
        this.fundMapper = fundMapper;
    }

    public int insertEmp(EmpVo empVo) {
        return empMapper.insertEmp(empVo);
    }

    public int updateEmp(EmpVo empVo) {
        return empMapper.updateEmp(empVo);
    }

    public int deleteEmp(EmpVo empVo) {
        return empMapper.deleteEmp(empVo);
    }

    public List<EmpVo> selectEmp(EmpVo empVo) {
        return empMapper.selectEmp(empVo);
    }

    public int insertFund(FundVo fundVo) {
        return fundMapper.insertFund(fundVo);
    }

    public int updateFund(FundVo fundVo) {
        return fundMapper.updateFund(fundVo);
    }

    public int deleteFund(FundVo fundVo) {
        return fundMapper.deleteFund(fundVo);
    }

    public List<FundVo> selectFund(FundVo fundVo) {
        return fundMapper.selectFund(fundVo);
    }

    public FundVo selectFundByCode(String fundCode) {
        return fundMapper.selectFundByCode(fundCode);
    }

    public int insertFundPerformance(FundPerformanceVo performanceVo) {
        return fundMapper.insertFundPerformance(performanceVo);
    }

    public List<FundPerformanceVo> selectFundPerformance(String fundCode) {
        return fundMapper.selectFundPerformance(fundCode);
    }

    public List<FundPerformanceVo> selectFundPerformanceByDateRange(String fundCode, String startDate, String endDate) {
        return fundMapper.selectFundPerformanceByDateRange(fundCode, startDate, endDate);
    }
}