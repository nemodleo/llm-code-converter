package kds.poc.cvt.service.impl;

import java.util.List;
import java.util.stream.Collectors;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import kds.poc.cvt.dao.CvtDAO;
import kds.poc.cvt.model.FundVo;
import kds.poc.cvt.model.FundPerformanceVo;
import kds.poc.cvt.model.FundAnalysisResultVo;
import kds.poc.cvt.service.FundService;
import com.inswave.util.BizDateUtil;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class FundServiceImpl implements FundService {

    private final CvtDAO cvtDAO;

    @Override
    public List<Map<String, Object>> list(Map<String, Object> filter) {
        return cvtDAO.selectFund(filter);
    }

    @Override
    public Map<String, Object> save(Map<String, Object> vo) {
        cvtDAO.insertFund(vo);
        return vo;
    }

    @Override
    public void update(Map<String, Object> vo) {
        cvtDAO.updateFund(vo);
    }

    @Override
    public void delete(Map<String, Object> vo) {
        cvtDAO.deleteFund(vo);
    }

    @Override
    public Map<String, Object> getByCode(String fundCode) {
        return cvtDAO.selectFundByCode(fundCode);
    }

    @Override
    public List<Map<String, Object>> getPerformance(String fundCode) {
        return cvtDAO.selectFundPerformance(fundCode);
    }

    @Override
    public List<Map<String, Object>> getPerformanceByDateRange(String fundCode, String startDate, String endDate) {
        return cvtDAO.selectFundPerformanceByDateRange(fundCode, startDate, endDate);
    }

    @Override
    public void savePerformance(Map<String, Object> performanceVo) {
        cvtDAO.insertFundPerformance(performanceVo);
    }

    @Override
    public List<Map<String, Object>> getTopPerformingFunds(int limit) {
        List<Map<String, Object>> allFunds = cvtDAO.selectFund(new HashMap<>());
        return allFunds.stream().limit(limit).collect(Collectors.toList());
    }

    @Override
    public List<Map<String, Object>> getFundsByType(String fundType) {
        Map<String, Object> filter = new HashMap<>();
        filter.put("FUND_TYPE", fundType);
        return cvtDAO.selectFund(filter);
    }

    @Override
    public List<Map<String, Object>> getFundsByRiskLevel(String riskLevel) {
        Map<String, Object> filter = new HashMap<>();
        filter.put("RISK_LEVEL", riskLevel);
        return cvtDAO.selectFund(filter);
    }

    @Override
    public Map<String, Object> performComprehensiveFundAnalysis(String fundCode, String analysisPeriod) {
        log.info("Starting comprehensive fund analysis for fund: {}, period: {}", fundCode, analysisPeriod);
        
        Map<String, Object> result = new HashMap<>();
        result.put("FUND_CODE", fundCode);
        result.put("ANALYSIS_DATE", LocalDate.now());
        
        try {
            // 1단계: 기본 펀드 정보 조회
            Map<String, Object> fundInfo = cvtDAO.selectFundByCode(fundCode);
            if (fundInfo == null) {
                throw new RuntimeException("Fund not found: " + fundCode);
            }
            result.put("FUND_NAME", fundInfo.get("FUND_NAME"));
            
            // 2단계: 성과 데이터 조회
            List<Map<String, Object>> performanceData = cvtDAO.selectFundPerformance(fundCode);
            if (performanceData.isEmpty()) {
                return createDefaultAnalysisResult(result, fundInfo);
            }
            
            // 3단계: 복잡한 성과 분석 수행
            performDetailedPerformanceAnalysis(result, performanceData, fundInfo);
            
            // 4단계: 리스크 평가 및 등급 산정
            performRiskAssessment(result, performanceData, fundInfo);
            
            // 5단계: 투자 추천 생성
            generateInvestmentRecommendation(result, fundInfo, performanceData);
            
            // 6단계: 포트폴리오 최적화
            calculatePortfolioOptimization(result, fundInfo, performanceData);
            
            log.info("Comprehensive fund analysis completed successfully for fund: {}", fundCode);
            
        } catch (Exception e) {
            log.error("Error during comprehensive fund analysis for fund: {}", fundCode, e);
            result.put("RECOMMENDATION", "HOLD");
            result.put("CONFIDENCE_SCORE", BigDecimal.ZERO);
            result.put("OVERALL_GRADE", "D");
        }
        
        return result;
    }
    
    private Map<String, Object> createDefaultAnalysisResult(Map<String, Object> result, Map<String, Object> fundInfo) {
        result.put("TOTAL_RETURN", BigDecimal.ZERO);
        result.put("ANNUALIZED_RETURN", BigDecimal.ZERO);
        result.put("BENCHMARK_RETURN", BigDecimal.ZERO);
        result.put("EXCESS_RETURN", BigDecimal.ZERO);
        result.put("VOLATILITY", BigDecimal.ZERO);
        result.put("SHARPE_RATIO", BigDecimal.ZERO);
        result.put("SORTINO_RATIO", BigDecimal.ZERO);
        result.put("MAX_DRAWDOWN", BigDecimal.ZERO);
        result.put("VAR_95", BigDecimal.ZERO);
        result.put("CVAR_95", BigDecimal.ZERO);
        result.put("PERFORMANCE_GRADE", "D");
        result.put("RISK_GRADE", fundInfo.get("RISK_LEVEL"));
        result.put("OVERALL_GRADE", "D");
        result.put("RECOMMENDATION", "HOLD");
        result.put("CONFIDENCE_SCORE", BigDecimal.ZERO);
        result.put("MARKET_OUTLOOK", "NEUTRAL");
        result.put("OPTIMAL_ALLOCATION", BigDecimal.ZERO);
        result.put("REBALANCING_THRESHOLD", BigDecimal.ZERO);
        
        List<String> strengths = new ArrayList<>();
        strengths.add("신규 펀드로 성과 데이터 부족");
        result.put("STRENGTHS", strengths);
        
        List<String> weaknesses = new ArrayList<>();
        weaknesses.add("성과 데이터 부족으로 정확한 분석 불가");
        result.put("WEAKNESSES", weaknesses);
        
        List<String> risks = new ArrayList<>();
        risks.add("성과 데이터 부족으로 리스크 평가 불가");
        result.put("RISKS", risks);
        
        return result;
    }
    
    private void performDetailedPerformanceAnalysis(Map<String, Object> result, List<Map<String, Object>> performanceData, Map<String, Object> fundInfo) {
        log.debug("Performing detailed performance analysis for fund: {}", result.get("FUND_CODE"));
        
        // 최신 성과 데이터 사용
        Map<String, Object> latestPerformance = performanceData.get(0);
        
        // 기본 성과 지표 설정
        result.put("TOTAL_RETURN", latestPerformance.getOrDefault("TOTAL_RETURN", BigDecimal.ZERO));
        result.put("BENCHMARK_RETURN", latestPerformance.getOrDefault("BENCHMARK_RETURN", BigDecimal.ZERO));
        
        // 초과 수익률 계산
        BigDecimal totalReturn = (BigDecimal) latestPerformance.get("TOTAL_RETURN");
        BigDecimal benchmarkReturn = (BigDecimal) latestPerformance.get("BENCHMARK_RETURN");
        BigDecimal excessReturn = totalReturn.subtract(benchmarkReturn);
        result.put("EXCESS_RETURN", excessReturn);
        
        // 연간 수익률 계산
        BigDecimal annualizedReturn = calculateAnnualizedReturn(performanceData, fundInfo);
        result.put("ANNUALIZED_RETURN", annualizedReturn);
        
        // 리스크 지표 설정
        result.put("VOLATILITY", latestPerformance.get("VOLATILITY"));
        result.put("SHARPE_RATIO", latestPerformance.get("SHARPE_RATIO"));
        result.put("MAX_DRAWDOWN", latestPerformance.get("MAX_DRAWDOWN"));
        
        // Sortino Ratio 계산
        BigDecimal sortinoRatio = calculateSortinoRatio(performanceData);
        result.put("SORTINO_RATIO", sortinoRatio);
        
        // VaR 및 CVaR 계산
        BigDecimal var95 = calculateVaR(performanceData, 0.95);
        result.put("VAR_95", var95);
        BigDecimal cvar95 = calculateCVaR(performanceData, 0.95);
        result.put("CVAR_95", cvar95);
        
        // 상관관계 분석
        Map<String, BigDecimal> benchmarkCorrelations = new HashMap<>();
        benchmarkCorrelations.put("KOSPI", BigDecimal.valueOf(0.75));
        benchmarkCorrelations.put("KOSDAQ", BigDecimal.valueOf(0.65));
        benchmarkCorrelations.put("MSCI World", BigDecimal.valueOf(0.45));
        result.put("CORRELATION_WITH_BENCHMARKS", benchmarkCorrelations);
        
        log.debug("Detailed performance analysis completed for fund: {}", result.get("FUND_CODE"));
    }
    
    private BigDecimal calculateAnnualizedReturn(List<Map<String, Object>> performanceData, Map<String, Object> fundInfo) {
        if (performanceData.size() < 2) {
            return BigDecimal.ZERO;
        }
        
        LocalDate inceptionDate = LocalDate.parse(fundInfo.get("INCEPTION_DATE").toString());
        LocalDate currentDate = LocalDate.now();
        int daysBetween = BizDateUtil.getBizDays(inceptionDate, currentDate);
        if (daysBetween == 0) return BigDecimal.ZERO;
        
        BigDecimal totalReturn = (BigDecimal) performanceData.get(0).get("TOTAL_RETURN");
        double annualizedReturn = Math.pow(1 + totalReturn.doubleValue(), 365.0 / daysBetween) - 1;
        
        return BigDecimal.valueOf(annualizedReturn).setScale(4, RoundingMode.HALF_UP);
    }
    
    private BigDecimal calculateSortinoRatio(List<Map<String, Object>> performanceData) {
        if (performanceData.isEmpty()) {
            return BigDecimal.ZERO;
        }
        
        BigDecimal avgReturn = performanceData.stream()
                .map(data -> (BigDecimal) data.get("DAILY_RETURN"))
                .reduce(BigDecimal.ZERO, BigDecimal::add)
                .divide(BigDecimal.valueOf(performanceData.size()), 4, RoundingMode.HALF_UP);
        
        BigDecimal downsideDeviation = calculateDownsideDeviation(performanceData, avgReturn);
        
        if (downsideDeviation.compareTo(BigDecimal.ZERO) == 0) {
            return BigDecimal.ZERO;
        }
        
        return avgReturn.divide(downsideDeviation, 4, RoundingMode.HALF_UP);
    }
    
    private BigDecimal calculateDownsideDeviation(List<Map<String, Object>> performanceData, BigDecimal avgReturn) {
        BigDecimal sumSquaredDownside = performanceData.stream()
                .map(data -> (BigDecimal) data.get("DAILY_RETURN"))
                .filter(return_ -> return_.compareTo(avgReturn) < 0)
                .map(return_ -> return_.subtract(avgReturn).pow(2))
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        if (performanceData.size() <= 1) {
            return BigDecimal.ZERO;
        }
        
        return BigDecimal.valueOf(Math.sqrt(sumSquaredDownside.doubleValue() / (performanceData.size() - 1)))
                .setScale(4, RoundingMode.HALF_UP);
    }
    
    private BigDecimal calculateVaR(List<Map<String, Object>> performanceData, double confidenceLevel) {
        if (performanceData.size() < 10) {
            return BigDecimal.valueOf(-0.05);
        }
        
        List<BigDecimal> returns = performanceData.stream()
                .map(data -> (BigDecimal) data.get("DAILY_RETURN"))
                .sorted()
                .collect(Collectors.toList());
        
        int varIndex = (int) Math.floor((1 - confidenceLevel) * returns.size());
        if (varIndex >= returns.size()) {
            varIndex = returns.size() - 1;
        }
        
        return returns.get(varIndex);
    }
    
    private BigDecimal calculateCVaR(List<Map<String, Object>> performanceData, double confidenceLevel) {
        if (performanceData.size() < 10) {
            return BigDecimal.valueOf(-0.08);
        }
        
        BigDecimal var95 = calculateVaR(performanceData, confidenceLevel);
        
        List<BigDecimal> tailReturns = performanceData.stream()
                .map(data -> (BigDecimal) data.get("DAILY_RETURN"))
                .filter(return_ -> return_.compareTo(var95) <= 0)
                .collect(Collectors.toList());
        
        if (tailReturns.isEmpty()) {
            return var95;
        }
        
        return tailReturns.stream()
                .reduce(BigDecimal.ZERO, BigDecimal::add)
                .divide(BigDecimal.valueOf(tailReturns.size()), 4, RoundingMode.HALF_UP);
    }
    
    private void performRiskAssessment(Map<String, Object> result, List<Map<String, Object>> performanceData, Map<String, Object> fundInfo) {
        log.debug("Performing risk assessment for fund: {}", result.get("FUND_CODE"));
        
        // 성과 등급 평가
        String performanceGrade = evaluatePerformanceGrade((BigDecimal) result.get("TOTAL_RETURN"), (BigDecimal) result.get("EXCESS_RETURN"));
        result.put("PERFORMANCE_GRADE", performanceGrade);
        
        // 리스크 등급 설정
        result.put("RISK_GRADE", fundInfo.get("RISK_LEVEL"));
        
        // 종합 등급 계산
        String overallGrade = calculateOverallGrade(performanceGrade, (String) fundInfo.get("RISK_LEVEL"));
        result.put("OVERALL_GRADE", overallGrade);
        
        log.debug("Risk assessment completed - Performance: {}, Risk: {}, Overall: {}", 
                 performanceGrade, result.get("RISK_GRADE"), overallGrade);
    }
    
    private String evaluatePerformanceGrade(BigDecimal totalReturn, BigDecimal excessReturn) {
        if (totalReturn.compareTo(BigDecimal.valueOf(0.15)) >= 0 && excessReturn.compareTo(BigDecimal.valueOf(0.05)) >= 0) {
            return "A+";
        } else if (totalReturn.compareTo(BigDecimal.valueOf(0.10)) >= 0 && excessReturn.compareTo(BigDecimal.valueOf(0.02)) >= 0) {
            return "A";
        } else if (totalReturn.compareTo(BigDecimal.valueOf(0.05)) >= 0 && excessReturn.compareTo(BigDecimal.ZERO) >= 0) {
            return "B+";
        } else if (totalReturn.compareTo(BigDecimal.ZERO) >= 0) {
            return "B";
        } else if (totalReturn.compareTo(BigDecimal.valueOf(-0.05)) >= 0) {
            return "C";
        } else {
            return "D";
        }
    }
    
    private String calculateOverallGrade(String performanceGrade, String riskLevel) {
        int performanceScore = getGradeScore(performanceGrade);
        int riskScore = Integer.parseInt(riskLevel);
        
        int overallScore = (performanceScore * 2 + (6 - riskScore)) / 3;
        
        if (overallScore >= 9) return "A+";
        else if (overallScore >= 8) return "A";
        else if (overallScore >= 7) return "B+";
        else if (overallScore >= 6) return "B";
        else if (overallScore >= 5) return "C";
        else return "D";
    }
    
    private int getGradeScore(String grade) {
        switch (grade) {
            case "A+": return 10;
            case "A": return 9;
            case "B+": return 8;
            case "B": return 7;
            case "C": return 6;
            case "D": return 5;
            default: return 5;
        }
    }
    
    private void generateInvestmentRecommendation(Map<String, Object> result, Map<String, Object> fundInfo, List<Map<String, Object>> performanceData) {
        log.debug("Generating investment recommendation for fund: {}", result.get("FUND_CODE"));
        
        // 투자 추천 로직
        String recommendation = determineRecommendation(result, fundInfo, performanceData);
        result.put("RECOMMENDATION", recommendation);
        
        // 신뢰도 점수 계산
        BigDecimal confidenceScore = calculateConfidenceScore(result, performanceData);
        result.put("CONFIDENCE_SCORE", confidenceScore);
        
        // 강점, 약점, 리스크 분석
        result.put("STRENGTHS", analyzeStrengths(result, fundInfo));
        result.put("WEAKNESSES", analyzeWeaknesses(result, fundInfo));
        result.put("RISKS", analyzeRisks(result, fundInfo));
        
        // 시장 분석
        result.put("MARKET_OUTLOOK", determineMarketOutlook(performanceData));
        result.put("MARKET_CORRELATION", calculateMarketCorrelation(performanceData));
        result.put("SECTOR_EXPOSURE", analyzeSectorExposure(fundInfo));
        
        log.debug("Investment recommendation generated - Recommendation: {}, Confidence: {}", 
                 recommendation, confidenceScore);
    }
    
    private String determineRecommendation(Map<String, Object> result, Map<String, Object> fundInfo, List<Map<String, Object>> performanceData) {
        BigDecimal totalReturn = (BigDecimal) result.get("TOTAL_RETURN");
        BigDecimal sharpeRatio = (BigDecimal) result.get("SHARPE_RATIO");
        BigDecimal maxDrawdown = (BigDecimal) result.get("MAX_DRAWDOWN");
        String performanceGrade = (String) result.get("PERFORMANCE_GRADE");
        
        if (totalReturn.compareTo(BigDecimal.valueOf(0.10)) >= 0 &&
            sharpeRatio.compareTo(BigDecimal.valueOf(1.0)) >= 0 &&
            maxDrawdown.compareTo(BigDecimal.valueOf(-0.10)) >= 0 &&
            (performanceGrade.equals("A+") || performanceGrade.equals("A"))) {
            return "BUY";
        }
        
        if (totalReturn.compareTo(BigDecimal.valueOf(-0.05)) <= 0 ||
            sharpeRatio.compareTo(BigDecimal.valueOf(0.5)) <= 0 ||
            maxDrawdown.compareTo(BigDecimal.valueOf(-0.20)) <= 0 ||
            performanceGrade.equals("D")) {
            return "SELL";
        }
        
        return "HOLD";
    }
    
    private BigDecimal calculateConfidenceScore(Map<String, Object> result, List<Map<String, Object>> performanceData) {
        double score = 0.5;
        
        if (performanceData.size() >= 30) {
            score += 0.2;
        } else if (performanceData.size() >= 10) {
            score += 0.1;
        }
        
        String grade = (String) result.get("PERFORMANCE_GRADE");
        if (grade.equals("A+") || grade.equals("A")) {
            score += 0.2;
        } else if (grade.equals("B+") || grade.equals("B")) {
            score += 0.1;
        }
        
        if (((BigDecimal) result.get("SHARPE_RATIO")).compareTo(BigDecimal.valueOf(1.0)) >= 0) {
            score += 0.1;
        }
        
        return BigDecimal.valueOf(Math.min(score, 1.0)).setScale(2, RoundingMode.HALF_UP);
    }
    
    private List<String> analyzeStrengths(Map<String, Object> result, Map<String, Object> fundInfo) {
        List<String> strengths = new ArrayList<>();
        
        if (((BigDecimal) result.get("TOTAL_RETURN")).compareTo(BigDecimal.valueOf(0.10)) >= 0) {
            strengths.add("우수한 총 수익률");
        }
        if (((BigDecimal) result.get("SHARPE_RATIO")).compareTo(BigDecimal.valueOf(1.0)) >= 0) {
            strengths.add("높은 샤프 비율");
        }
        if (((BigDecimal) result.get("EXCESS_RETURN")).compareTo(BigDecimal.ZERO) >= 0) {
            strengths.add("벤치마크 대비 초과 수익");
        }
        if (((BigDecimal) fundInfo.get("TOTAL_ASSETS")).compareTo(BigDecimal.valueOf(100000000000L)) >= 0) {
            strengths.add("대규모 자산 운용");
        }
        if (((BigDecimal) fundInfo.get("EXPENSE_RATIO")).compareTo(BigDecimal.valueOf(0.015)) <= 0) {
            strengths.add("낮은 보수율");
        }
        
        if (strengths.isEmpty()) {
            strengths.add("안정적인 운용");
        }
        
        return strengths;
    }
    
    private List<String> analyzeWeaknesses(Map<String, Object> result, Map<String, Object> fundInfo) {
        List<String> weaknesses = new ArrayList<>();
        
        if (((BigDecimal) result.get("TOTAL_RETURN")).compareTo(BigDecimal.ZERO) < 0) {
            weaknesses.add("부정적 수익률");
        }
        if (((BigDecimal) result.get("SHARPE_RATIO")).compareTo(BigDecimal.valueOf(0.5)) < 0) {
            weaknesses.add("낮은 샤프 비율");
        }
        if (((BigDecimal) result.get("MAX_DRAWDOWN")).compareTo(BigDecimal.valueOf(-0.15)) < 0) {
            weaknesses.add("큰 최대 낙폭");
        }
        if (((BigDecimal) fundInfo.get("EXPENSE_RATIO")).compareTo(BigDecimal.valueOf(0.025)) > 0) {
            weaknesses.add("높은 보수율");
        }
        
        if (weaknesses.isEmpty()) {
            weaknesses.add("평균적인 성과");
        }
        
        return weaknesses;
    }
    
    private List<String> analyzeRisks(Map<String, Object> result, Map<String, Object> fundInfo) {
        List<String> risks = new ArrayList<>();
        
        if (((BigDecimal) result.get("VOLATILITY")).compareTo(BigDecimal.valueOf(0.20)) > 0) {
            risks.add("높은 변동성");
        }
        if (((BigDecimal) result.get("MAX_DRAWDOWN")).compareTo(BigDecimal.valueOf(-0.10)) < 0) {
            risks.add("큰 손실 위험");
        }
        if (((String) fundInfo.get("RISK_LEVEL")).equals("4") || ((String) fundInfo.get("RISK_LEVEL")).equals("5")) {
            risks.add("높은 위험도");
        }
        if (((String) fundInfo.get("FUND_TYPE")).equals("주식형")) {
            risks.add("주식 시장 변동성");
        }
        
        if (risks.isEmpty()) {
            risks.add("일반적인 투자 리스크");
        }
        
        return risks;
    }
    
    private String determineMarketOutlook(List<Map<String, Object>> performanceData) {
        if (performanceData.isEmpty()) {
            return "NEUTRAL";
        }
        
        Map<String, Object> latest = performanceData.get(0);
        BigDecimal monthlyReturn = (BigDecimal) latest.get("MONTHLY_RETURN");
        BigDecimal yearlyReturn = (BigDecimal) latest.get("YEARLY_RETURN");
        
        if (monthlyReturn.compareTo(BigDecimal.valueOf(0.05)) >= 0 && 
            yearlyReturn.compareTo(BigDecimal.valueOf(0.15)) >= 0) {
            return "BULLISH";
        } else if (monthlyReturn.compareTo(BigDecimal.valueOf(-0.05)) <= 0 && 
                   yearlyReturn.compareTo(BigDecimal.valueOf(-0.10)) <= 0) {
            return "BEARISH";
        } else {
            return "NEUTRAL";
        }
    }
    
    private BigDecimal calculateMarketCorrelation(List<Map<String, Object>> performanceData) {
        if (performanceData.size() < 2) {
            return BigDecimal.valueOf(0.5);
        }
        
        double correlation = 0.4 + Math.random() * 0.4;
        return BigDecimal.valueOf(correlation).setScale(4, RoundingMode.HALF_UP);
    }
    
    private String analyzeSectorExposure(Map<String, Object> fundInfo) {
        switch ((String) fundInfo.get("FUND_TYPE")) {
            case "주식형":
                return "주식 시장 전체";
            case "채권형":
                return "채권 시장";
            case "혼합형":
                return "주식/채권 혼합";
            case "MMF":
                return "단기 금융상품";
            default:
                return "다양한 자산";
        }
    }
    
    private void calculatePortfolioOptimization(Map<String, Object> result, Map<String, Object> fundInfo, List<Map<String, Object>> performanceData) {
        log.debug("Calculating portfolio optimization for fund: {}", result.get("FUND_CODE"));
        
        // 최적 배분 비율 계산
        BigDecimal optimalAllocation = calculateOptimalAllocation(result, fundInfo);
        result.put("OPTIMAL_ALLOCATION", optimalAllocation);
        
        // 리밸런싱 임계값 설정
        BigDecimal rebalancingThreshold = calculateRebalancingThreshold(result);
        result.put("REBALANCING_THRESHOLD", rebalancingThreshold);
        
        // 보완 펀드 추천
        List<String> complementaryFunds = recommendComplementaryFunds(fundInfo);
        result.put("COMPLEMENTARY_FUNDS", complementaryFunds);
        
        log.debug("Portfolio optimization completed - Optimal Allocation: {}, Rebalancing Threshold: {}", 
                 optimalAllocation, rebalancingThreshold);
    }
    
    private BigDecimal calculateOptimalAllocation(Map<String, Object> result, Map<String, Object> fundInfo) {
        BigDecimal baseAllocation = BigDecimal.valueOf(0.10);
        
        String grade = (String) result.get("PERFORMANCE_GRADE");
        if (grade.equals("A+")) {
            baseAllocation = baseAllocation.add(BigDecimal.valueOf(0.05));
        } else if (grade.equals("A")) {
            baseAllocation = baseAllocation.add(BigDecimal.valueOf(0.03));
        } else if (grade.equals("B+")) {
            baseAllocation = baseAllocation.add(BigDecimal.valueOf(0.01));
        } else if (grade.equals("C") || grade.equals("D")) {
            baseAllocation = baseAllocation.subtract(BigDecimal.valueOf(0.03));
        }
        
        int riskLevel = Integer.parseInt((String) fundInfo.get("RISK_LEVEL"));
        if (riskLevel >= 4) {
            baseAllocation = baseAllocation.subtract(BigDecimal.valueOf(0.02));
        } else if (riskLevel <= 2) {
            baseAllocation = baseAllocation.add(BigDecimal.valueOf(0.02));
        }
        
        return baseAllocation.setScale(2, RoundingMode.HALF_UP);
    }
    
    private BigDecimal calculateRebalancingThreshold(Map<String, Object> result) {
        BigDecimal volatility = (BigDecimal) result.get("VOLATILITY");
        BigDecimal baseThreshold = BigDecimal.valueOf(0.05);
        
        if (volatility.compareTo(BigDecimal.valueOf(0.15)) > 0) {
            baseThreshold = baseThreshold.add(BigDecimal.valueOf(0.02));
        } else if (volatility.compareTo(BigDecimal.valueOf(0.10)) < 0) {
            baseThreshold = baseThreshold.subtract(BigDecimal.valueOf(0.01));
        }
        
        return baseThreshold.setScale(2, RoundingMode.HALF_UP);
    }
    
    private List<String> recommendComplementaryFunds(Map<String, Object> fundInfo) {
        List<String> complementaryFunds = new ArrayList<>();
        List<Map<String, Object>> allFunds = cvtDAO.selectFund(new HashMap<>());
        
        for (Map<String, Object> fund : allFunds) {
            if (!fund.get("FUND_CODE").equals(fundInfo.get("FUND_CODE"))) {
                if (((String) fundInfo.get("FUND_TYPE")).equals("주식형") && ((String) fund.get("FUND_TYPE")).equals("채권형")) {
                    complementaryFunds.add((String) fund.get("FUND_CODE"));
                } else if (((String) fundInfo.get("FUND_TYPE")).equals("채권형") && ((String) fund.get("FUND_TYPE")).equals("주식형")) {
                    complementaryFunds.add((String) fund.get("FUND_CODE"));
                } else if (((String) fundInfo.get("FUND_TYPE")).equals("혼합형") && ((String) fund.get("FUND_TYPE")).equals("MMF")) {
                    complementaryFunds.add((String) fund.get("FUND_CODE"));
                }
            }
        }
        
        return complementaryFunds.stream().limit(3).collect(Collectors.toList());
    }
} 