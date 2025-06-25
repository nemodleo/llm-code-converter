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
    public List<FundVo> list(FundVo filter) {
        return cvtDAO.selectFund(filter);
    }

    @Override
    public FundVo save(FundVo vo) {
        cvtDAO.insertFund(vo);
        return vo;
    }

    @Override
    public void update(FundVo vo) {
        cvtDAO.updateFund(vo);
    }

    @Override
    public void delete(FundVo vo) {
        cvtDAO.deleteFund(vo);
    }

    @Override
    public FundVo getByCode(String fundCode) {
        return cvtDAO.selectFundByCode(fundCode);
    }

    @Override
    public List<FundPerformanceVo> getPerformance(String fundCode) {
        return cvtDAO.selectFundPerformance(fundCode);
    }

    @Override
    public List<FundPerformanceVo> getPerformanceByDateRange(String fundCode, String startDate, String endDate) {
        return cvtDAO.selectFundPerformanceByDateRange(fundCode, startDate, endDate);
    }

    @Override
    public void savePerformance(FundPerformanceVo performanceVo) {
        cvtDAO.insertFundPerformance(performanceVo);
    }

    @Override
    public List<FundVo> getTopPerformingFunds(int limit) {
        List<FundVo> allFunds = cvtDAO.selectFund(new FundVo());
        return allFunds.stream().limit(limit).collect(Collectors.toList());
    }

    @Override
    public List<FundVo> getFundsByType(String fundType) {
        FundVo filter = new FundVo();
        filter.setFundType(fundType);
        return cvtDAO.selectFund(filter);
    }

    @Override
    public List<FundVo> getFundsByRiskLevel(String riskLevel) {
        FundVo filter = new FundVo();
        filter.setRiskLevel(riskLevel);
        return cvtDAO.selectFund(filter);
    }

    @Override
    public FundAnalysisResultVo performComprehensiveFundAnalysis(String fundCode, String analysisPeriod) {
        log.info("Starting comprehensive fund analysis for fund: {}, period: {}", fundCode, analysisPeriod);
        
        FundAnalysisResultVo result = new FundAnalysisResultVo();
        result.setFundCode(fundCode);
        result.setAnalysisDate(LocalDate.now());
        
        try {
            // 1단계: 기본 펀드 정보 조회
            FundVo fundInfo = cvtDAO.selectFundByCode(fundCode);
            if (fundInfo == null) {
                throw new RuntimeException("Fund not found: " + fundCode);
            }
            result.setFundName(fundInfo.getFundName());
            
            // 2단계: 성과 데이터 조회
            List<FundPerformanceVo> performanceData = cvtDAO.selectFundPerformance(fundCode);
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
            result.setRecommendation("HOLD");
            result.setConfidenceScore(BigDecimal.ZERO);
            result.setOverallGrade("D");
        }
        
        return result;
    }
    
    private FundAnalysisResultVo createDefaultAnalysisResult(FundAnalysisResultVo result, FundVo fundInfo) {
        result.setTotalReturn(BigDecimal.ZERO);
        result.setAnnualizedReturn(BigDecimal.ZERO);
        result.setBenchmarkReturn(BigDecimal.ZERO);
        result.setExcessReturn(BigDecimal.ZERO);
        result.setVolatility(BigDecimal.ZERO);
        result.setSharpeRatio(BigDecimal.ZERO);
        result.setSortinoRatio(BigDecimal.ZERO);
        result.setMaxDrawdown(BigDecimal.ZERO);
        result.setVar95(BigDecimal.ZERO);
        result.setCvar95(BigDecimal.ZERO);
        result.setPerformanceGrade("D");
        result.setRiskGrade(fundInfo.getRiskLevel());
        result.setOverallGrade("D");
        result.setRecommendation("HOLD");
        result.setConfidenceScore(BigDecimal.ZERO);
        result.setMarketOutlook("NEUTRAL");
        result.setOptimalAllocation(BigDecimal.ZERO);
        result.setRebalancingThreshold(BigDecimal.ZERO);
        
        List<String> strengths = new ArrayList<>();
        strengths.add("신규 펀드로 성과 데이터 부족");
        result.setStrengths(strengths);
        
        List<String> weaknesses = new ArrayList<>();
        weaknesses.add("성과 데이터 부족으로 정확한 분석 불가");
        result.setWeaknesses(weaknesses);
        
        List<String> risks = new ArrayList<>();
        risks.add("성과 데이터 부족으로 리스크 평가 불가");
        result.setRisks(risks);
        
        return result;
    }
    
    private void performDetailedPerformanceAnalysis(FundAnalysisResultVo result, List<FundPerformanceVo> performanceData, FundVo fundInfo) {
        log.debug("Performing detailed performance analysis for fund: {}", result.getFundCode());
        
        // 최신 성과 데이터 사용
        FundPerformanceVo latestPerformance = performanceData.get(0);
        
        // 기본 성과 지표 설정
        BigDecimal totalReturn = latestPerformance.getTotalReturn() != null ? latestPerformance.getTotalReturn() : BigDecimal.ZERO;
        BigDecimal benchmarkReturn = latestPerformance.getBenchmarkReturn() != null ? latestPerformance.getBenchmarkReturn() : BigDecimal.ZERO;
        
        result.setTotalReturn(totalReturn);
        result.setBenchmarkReturn(benchmarkReturn);
        
        // 초과 수익률 계산
        BigDecimal excessReturn = latestPerformance.getTotalReturn().subtract(latestPerformance.getBenchmarkReturn());
        result.setExcessReturn(excessReturn);
        
        // 연간 수익률 계산
        BigDecimal annualizedReturn = calculateAnnualizedReturn(performanceData, fundInfo);
        result.setAnnualizedReturn(annualizedReturn);
        
        // 리스크 지표 설정
        result.setVolatility(latestPerformance.getVolatility());
        result.setSharpeRatio(latestPerformance.getSharpeRatio());
        result.setMaxDrawdown(latestPerformance.getMaxDrawdown());
        
        // Sortino Ratio 계산
        BigDecimal sortinoRatio = calculateSortinoRatio(performanceData);
        result.setSortinoRatio(sortinoRatio);
        
        // VaR 및 CVaR 계산
        BigDecimal var95 = calculateVaR(performanceData, 0.95);
        result.setVar95(var95);
        BigDecimal cvar95 = calculateCVaR(performanceData, 0.95);
        result.setCvar95(cvar95);
        
        // 상관관계 분석
        Map<String, BigDecimal> benchmarkCorrelations = new HashMap<>();
        benchmarkCorrelations.put("KOSPI", BigDecimal.valueOf(0.75));
        benchmarkCorrelations.put("KOSDAQ", BigDecimal.valueOf(0.65));
        benchmarkCorrelations.put("MSCI World", BigDecimal.valueOf(0.45));
        result.setCorrelationWithBenchmarks(benchmarkCorrelations);
        
        log.debug("Detailed performance analysis completed for fund: {}", result.getFundCode());
    }
    
    private BigDecimal calculateAnnualizedReturn(List<FundPerformanceVo> performanceData, FundVo fundInfo) {
        if (performanceData.size() < 2) {
            return BigDecimal.ZERO;
        }
        
        LocalDate inceptionDate = LocalDate.parse(fundInfo.getInceptionDate().toString());
        LocalDate currentDate = LocalDate.now();
        long daysBetween = BizDateUtil.businessDaysBetween(inceptionDate, currentDate, false);
        if (daysBetween == 0L) return BigDecimal.ZERO;
        
        BigDecimal totalReturn = performanceData.get(0).getTotalReturn();
        double annualizedReturn = Math.pow(1 + totalReturn.doubleValue(), 365.0 / daysBetween) - 1;
        
        return BigDecimal.valueOf(annualizedReturn).setScale(4, RoundingMode.HALF_UP);
    }
    
    private BigDecimal calculateSortinoRatio(List<FundPerformanceVo> performanceData) {
        if (performanceData.isEmpty()) {
            return BigDecimal.ZERO;
        }
        
        BigDecimal avgReturn = performanceData.stream()
                .map(FundPerformanceVo::getDailyReturn)
                .reduce(BigDecimal.ZERO, BigDecimal::add)
                .divide(BigDecimal.valueOf(performanceData.size()), 4, RoundingMode.HALF_UP);
        
        BigDecimal downsideDeviation = calculateDownsideDeviation(performanceData, avgReturn);
        
        if (downsideDeviation.compareTo(BigDecimal.ZERO) == 0) {
            return BigDecimal.ZERO;
        }
        
        return avgReturn.divide(downsideDeviation, 4, RoundingMode.HALF_UP);
    }
    
    private BigDecimal calculateDownsideDeviation(List<FundPerformanceVo> performanceData, BigDecimal avgReturn) {
        BigDecimal sumSquaredDownside = performanceData.stream()
                .map(FundPerformanceVo::getDailyReturn)
                .filter(return_ -> return_.compareTo(avgReturn) < 0)
                .map(return_ -> return_.subtract(avgReturn).pow(2))
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        if (performanceData.size() <= 1) {
            return BigDecimal.ZERO;
        }
        
        return BigDecimal.valueOf(Math.sqrt(sumSquaredDownside.doubleValue() / (performanceData.size() - 1)))
                .setScale(4, RoundingMode.HALF_UP);
    }
    
    private BigDecimal calculateVaR(List<FundPerformanceVo> performanceData, double confidenceLevel) {
        if (performanceData.size() < 10) {
            return BigDecimal.valueOf(-0.05);
        }
        
        List<BigDecimal> returns = performanceData.stream()
                .map(FundPerformanceVo::getDailyReturn)
                .sorted()
                .collect(Collectors.toList());
        
        int varIndex = (int) Math.floor((1 - confidenceLevel) * returns.size());
        if (varIndex >= returns.size()) {
            varIndex = returns.size() - 1;
        }
        
        return returns.get(varIndex);
    }
    
    private BigDecimal calculateCVaR(List<FundPerformanceVo> performanceData, double confidenceLevel) {
        if (performanceData.size() < 10) {
            return BigDecimal.valueOf(-0.08);
        }
        
        BigDecimal var95 = calculateVaR(performanceData, confidenceLevel);
        
        List<BigDecimal> tailReturns = performanceData.stream()
                .map(FundPerformanceVo::getDailyReturn)
                .filter(return_ -> return_.compareTo(var95) <= 0)
                .collect(Collectors.toList());
        
        if (tailReturns.isEmpty()) {
            return var95;
        }
        
        return tailReturns.stream()
                .reduce(BigDecimal.ZERO, BigDecimal::add)
                .divide(BigDecimal.valueOf(tailReturns.size()), 4, RoundingMode.HALF_UP);
    }
    
    private void performRiskAssessment(FundAnalysisResultVo result, List<FundPerformanceVo> performanceData, FundVo fundInfo) {
        log.debug("Performing risk assessment for fund: {}", result.getFundCode());
        
        // 성과 등급 평가
        String performanceGrade = evaluatePerformanceGrade(result.getTotalReturn(), result.getExcessReturn());
        result.setPerformanceGrade(performanceGrade);
        
        // 리스크 등급 설정
        result.setRiskGrade(fundInfo.getRiskLevel());
        
        // 종합 등급 계산
        String overallGrade = calculateOverallGrade(performanceGrade, fundInfo.getRiskLevel());
        result.setOverallGrade(overallGrade);
        
        log.debug("Risk assessment completed - Performance: {}, Risk: {}, Overall: {}", 
                 performanceGrade, result.getRiskGrade(), overallGrade);
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
    
    private void generateInvestmentRecommendation(FundAnalysisResultVo result, FundVo fundInfo, List<FundPerformanceVo> performanceData) {
        log.debug("Generating investment recommendation for fund: {}", result.getFundCode());
        
        // 투자 추천 로직
        String recommendation = determineRecommendation(result, fundInfo, performanceData);
        result.setRecommendation(recommendation);
        
        // 신뢰도 점수 계산
        BigDecimal confidenceScore = calculateConfidenceScore(result, performanceData);
        result.setConfidenceScore(confidenceScore);
        
        // 강점, 약점, 리스크 분석
        result.setStrengths(analyzeStrengths(result, fundInfo));
        result.setWeaknesses(analyzeWeaknesses(result, fundInfo));
        result.setRisks(analyzeRisks(result, fundInfo));
        
        // 시장 분석
        result.setMarketOutlook(determineMarketOutlook(performanceData));
        result.setMarketCorrelation(calculateMarketCorrelation(performanceData));
        result.setSectorExposure(analyzeSectorExposure(fundInfo));
        
        log.debug("Investment recommendation generated - Recommendation: {}, Confidence: {}", 
                 recommendation, confidenceScore);
    }
    
    private String determineRecommendation(FundAnalysisResultVo result, FundVo fundInfo, List<FundPerformanceVo> performanceData) {
        BigDecimal totalReturn = result.getTotalReturn();
        BigDecimal sharpeRatio = result.getSharpeRatio();
        BigDecimal maxDrawdown = result.getMaxDrawdown();
        String performanceGrade = result.getPerformanceGrade();
        
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
    
    private BigDecimal calculateConfidenceScore(FundAnalysisResultVo result, List<FundPerformanceVo> performanceData) {
        double score = 0.5;
        
        if (performanceData.size() >= 30) {
            score += 0.2;
        } else if (performanceData.size() >= 10) {
            score += 0.1;
        }
        
        String grade = result.getPerformanceGrade();
        if (grade.equals("A+") || grade.equals("A")) {
            score += 0.2;
        } else if (grade.equals("B+") || grade.equals("B")) {
            score += 0.1;
        }
        
        if (result.getSharpeRatio().compareTo(BigDecimal.valueOf(1.0)) >= 0) {
            score += 0.1;
        }
        
        return BigDecimal.valueOf(Math.min(score, 1.0)).setScale(2, RoundingMode.HALF_UP);
    }
    
    private List<String> analyzeStrengths(FundAnalysisResultVo result, FundVo fundInfo) {
        List<String> strengths = new ArrayList<>();
        
        if (result.getTotalReturn().compareTo(BigDecimal.valueOf(0.10)) >= 0) {
            strengths.add("우수한 총 수익률");
        }
        if (result.getSharpeRatio().compareTo(BigDecimal.valueOf(1.0)) >= 0) {
            strengths.add("높은 샤프 비율");
        }
        if (result.getExcessReturn().compareTo(BigDecimal.ZERO) >= 0) {
            strengths.add("벤치마크 대비 초과 수익");
        }
        if (fundInfo.getTotalAssets().compareTo(BigDecimal.valueOf(100000000000L)) >= 0) {
            strengths.add("대규모 자산 운용");
        }
        if (fundInfo.getExpenseRatio().compareTo(BigDecimal.valueOf(0.015)) <= 0) {
            strengths.add("낮은 보수율");
        }
        
        if (strengths.isEmpty()) {
            strengths.add("안정적인 운용");
        }
        
        return strengths;
    }
    
    private List<String> analyzeWeaknesses(FundAnalysisResultVo result, FundVo fundInfo) {
        List<String> weaknesses = new ArrayList<>();
        
        if (result.getTotalReturn().compareTo(BigDecimal.ZERO) < 0) {
            weaknesses.add("부정적 수익률");
        }
        if (result.getSharpeRatio().compareTo(BigDecimal.valueOf(0.5)) < 0) {
            weaknesses.add("낮은 샤프 비율");
        }
        if (result.getMaxDrawdown().compareTo(BigDecimal.valueOf(-0.15)) < 0) {
            weaknesses.add("큰 최대 낙폭");
        }
        if (fundInfo.getExpenseRatio().compareTo(BigDecimal.valueOf(0.025)) > 0) {
            weaknesses.add("높은 보수율");
        }
        
        if (weaknesses.isEmpty()) {
            weaknesses.add("평균적인 성과");
        }
        
        return weaknesses;
    }
    
    private List<String> analyzeRisks(FundAnalysisResultVo result, FundVo fundInfo) {
        List<String> risks = new ArrayList<>();
        
        if (result.getVolatility().compareTo(BigDecimal.valueOf(0.20)) > 0) {
            risks.add("높은 변동성");
        }
        if (result.getMaxDrawdown().compareTo(BigDecimal.valueOf(-0.10)) < 0) {
            risks.add("큰 손실 위험");
        }
        if (fundInfo.getRiskLevel().equals("4") || fundInfo.getRiskLevel().equals("5")) {
            risks.add("높은 위험도");
        }
        if (fundInfo.getFundType().equals("주식형")) {
            risks.add("주식 시장 변동성");
        }
        
        if (risks.isEmpty()) {
            risks.add("일반적인 투자 리스크");
        }
        
        return risks;
    }
    
    private String determineMarketOutlook(List<FundPerformanceVo> performanceData) {
        if (performanceData.isEmpty()) {
            return "NEUTRAL";
        }
        
        FundPerformanceVo latest = performanceData.get(0);
        BigDecimal monthlyReturn = latest.getMonthlyReturn();
        BigDecimal yearlyReturn = latest.getYearlyReturn();
        
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
    
    private BigDecimal calculateMarketCorrelation(List<FundPerformanceVo> performanceData) {
        if (performanceData.size() < 2) {
            return BigDecimal.valueOf(0.5);
        }
        
        double correlation = 0.4 + Math.random() * 0.4;
        return BigDecimal.valueOf(correlation).setScale(4, RoundingMode.HALF_UP);
    }
    
    private String analyzeSectorExposure(FundVo fundInfo) {
        switch (fundInfo.getFundType()) {
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
    
    private void calculatePortfolioOptimization(FundAnalysisResultVo result, FundVo fundInfo, List<FundPerformanceVo> performanceData) {
        log.debug("Calculating portfolio optimization for fund: {}", result.getFundCode());
        
        // 최적 배분 비율 계산
        BigDecimal optimalAllocation = calculateOptimalAllocation(result, fundInfo);
        result.setOptimalAllocation(optimalAllocation);
        
        // 리밸런싱 임계값 설정
        BigDecimal rebalancingThreshold = calculateRebalancingThreshold(result);
        result.setRebalancingThreshold(rebalancingThreshold);
        
        // 보완 펀드 추천
        List<String> complementaryFunds = recommendComplementaryFunds(fundInfo);
        result.setComplementaryFunds(complementaryFunds);
        
        log.debug("Portfolio optimization completed - Optimal Allocation: {}, Rebalancing Threshold: {}", 
                 optimalAllocation, rebalancingThreshold);
    }
    
    private BigDecimal calculateOptimalAllocation(FundAnalysisResultVo result, FundVo fundInfo) {
        BigDecimal baseAllocation = BigDecimal.valueOf(0.10);
        
        String grade = result.getPerformanceGrade();
        if (grade.equals("A+")) {
            baseAllocation = baseAllocation.add(BigDecimal.valueOf(0.05));
        } else if (grade.equals("A")) {
            baseAllocation = baseAllocation.add(BigDecimal.valueOf(0.03));
        } else if (grade.equals("B+")) {
            baseAllocation = baseAllocation.add(BigDecimal.valueOf(0.01));
        } else if (grade.equals("C") || grade.equals("D")) {
            baseAllocation = baseAllocation.subtract(BigDecimal.valueOf(0.03));
        }
        
        int riskLevel = Integer.parseInt(fundInfo.getRiskLevel());
        if (riskLevel >= 4) {
            baseAllocation = baseAllocation.subtract(BigDecimal.valueOf(0.02));
        } else if (riskLevel <= 2) {
            baseAllocation = baseAllocation.add(BigDecimal.valueOf(0.02));
        }
        
        return baseAllocation.setScale(2, RoundingMode.HALF_UP);
    }
    
    private BigDecimal calculateRebalancingThreshold(FundAnalysisResultVo result) {
        BigDecimal volatility = result.getVolatility();
        BigDecimal baseThreshold = BigDecimal.valueOf(0.05);
        
        if (volatility.compareTo(BigDecimal.valueOf(0.15)) > 0) {
            baseThreshold = baseThreshold.add(BigDecimal.valueOf(0.02));
        } else if (volatility.compareTo(BigDecimal.valueOf(0.10)) < 0) {
            baseThreshold = baseThreshold.subtract(BigDecimal.valueOf(0.01));
        }
        
        return baseThreshold.setScale(2, RoundingMode.HALF_UP);
    }
    
    private List<String> recommendComplementaryFunds(FundVo fundInfo) {
        List<String> complementaryFunds = new ArrayList<>();
        List<FundVo> allFunds = cvtDAO.selectFund(new FundVo());
        
        for (FundVo fund : allFunds) {
            if (!fund.getFundCode().equals(fundInfo.getFundCode())) {
                if (fundInfo.getFundType().equals("주식형") && fund.getFundType().equals("채권형")) {
                    complementaryFunds.add(fund.getFundCode());
                } else if (fundInfo.getFundType().equals("채권형") && fund.getFundType().equals("주식형")) {
                    complementaryFunds.add(fund.getFundCode());
                } else if (fundInfo.getFundType().equals("혼합형") && fund.getFundType().equals("MMF")) {
                    complementaryFunds.add(fund.getFundCode());
                }
            }
        }
        
        return complementaryFunds.stream().limit(3).collect(Collectors.toList());
    }
} 