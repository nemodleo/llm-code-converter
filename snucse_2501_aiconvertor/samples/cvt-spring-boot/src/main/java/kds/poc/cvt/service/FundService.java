package kds.poc.cvt.service;

import java.util.List;
import kds.poc.cvt.model.FundVo;
import kds.poc.cvt.model.FundPerformanceVo;
import kds.poc.cvt.model.FundAnalysisResultVo;

public interface FundService {
    
    // Fund 기본 CRUD
    List<FundVo> list(FundVo filter);
    FundVo save(FundVo vo);
    void update(FundVo vo);
    void delete(FundVo vo);
    FundVo getByCode(String fundCode);
    
    // Fund Performance 관련
    List<FundPerformanceVo> getPerformance(String fundCode);
    List<FundPerformanceVo> getPerformanceByDateRange(String fundCode, String startDate, String endDate);
    void savePerformance(FundPerformanceVo performanceVo);
    
    // Business Logic
    List<FundVo> getTopPerformingFunds(int limit);
    List<FundVo> getFundsByType(String fundType);
    List<FundVo> getFundsByRiskLevel(String riskLevel);
    
    // 종합 분석
    FundAnalysisResultVo performComprehensiveFundAnalysis(String fundCode, String analysisPeriod);
} 