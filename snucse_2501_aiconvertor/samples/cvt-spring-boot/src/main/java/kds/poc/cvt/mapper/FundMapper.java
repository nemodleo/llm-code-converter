package kds.poc.cvt.mapper;

import java.util.List;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import kds.poc.cvt.model.FundVo;
import kds.poc.cvt.model.FundPerformanceVo;

@Mapper
public interface FundMapper {
    
    // Fund 기본 CRUD
    int insertFund(FundVo fundVo);
    int updateFund(FundVo fundVo);
    int deleteFund(FundVo fundVo);
    List<FundVo> selectFund(FundVo fundVo);
    FundVo selectFundByCode(String fundCode);
    
    // Fund Performance 관련
    int insertFundPerformance(FundPerformanceVo performanceVo);
    List<FundPerformanceVo> selectFundPerformance(String fundCode);
    List<FundPerformanceVo> selectFundPerformanceByDateRange(@Param("fundCode") String fundCode, 
                                                             @Param("startDate") String startDate, 
                                                             @Param("endDate") String endDate);
} 