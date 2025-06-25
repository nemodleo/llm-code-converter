package kds.poc.cvt.service;

import java.util.List;
import java.util.Map;
import kds.poc.cvt.model.FundVo;
import kds.poc.cvt.model.FundPerformanceVo;
import kds.poc.cvt.model.FundAnalysisResultVo;

public interface FundService {
    
    // Fund 기본 CRUD
    List<Map<String, Object>> list(Map<String, Object> filter);
    Map<String, Object> save(Map<String, Object> vo);
    void update(Map<String, Object> vo);
    void delete(Map<String, Object> vo);
    Map<String, Object> getByCode(String fundCode);
    
    // Fund Performance 관련
    List<Map<String, Object>> getPerformance(String fundCode);
    List<Map<String, Object>> getPerformanceByDateRange(String fundCode, String startDate, String endDate);
    void savePerformance(Map<String, Object> performanceVo);
    
    // Business Logic
    List<Map<String, Object>> getTopPerformingFunds(int limit);
    List<Map<String, Object>> getFundsByType(String fundType);
    List<Map<String, Object>> getFundsByRiskLevel(String riskLevel);
    
    // 종합 분석
    Map<String, Object> performComprehensiveFundAnalysis(String fundCode, String analysisPeriod);
} 