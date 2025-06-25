package kds.poc.cvt.mapper;

import java.util.List;
import java.util.Map;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface FundMapper {
    
    // Fund 기본 CRUD
    int insertFund(Map<String, Object> fundMap);
    int updateFund(Map<String, Object> fundMap);
    int deleteFund(Map<String, Object> fundMap);
    List<Map<String, Object>> selectFund(Map<String, Object> fundMap);
    Map<String, Object> selectFundByCode(String fundCode);
    
    // Fund Performance 관련
    int insertFundPerformance(Map<String, Object> performanceMap);
    List<Map<String, Object>> selectFundPerformance(String fundCode);
    List<Map<String, Object>> selectFundPerformanceByDateRange(@Param("fundCode") String fundCode, 
                                                               @Param("startDate") String startDate, 
                                                               @Param("endDate") String endDate);
} 