package com.example.vo;

import java.util.*;
import java.sql.Timestamp;

/**
 * 통합 데이터 전달 객체
 * 자동 생성일: 2025-06-20 11:46:04
 * 필드 수: 40개
 */
public class UnifiedDataVO {

    /** 원본 키: 'FUND_CODE' */
    private String fundCode;

    /** 원본 키: 'FUND_TYPE' */
    private String fundType;

    /** 원본 키: 'TOTAL_RETURN' */
    private String totalReturn;

    /** 원본 키: 'RISK_LEVEL' */
    private String riskLevel;

    /** 원본 키: 'SHARPE_RATIO' */
    private String sharpeRatio;

    /** 원본 키: 'MAX_DRAWDOWN' */
    private String maxDrawdown;

    /** 원본 키: 'VOLATILITY' */
    private String VOLATILITY;

    /** 원본 키: 'PERFORMANCE_GRADE' */
    private String performanceGrade;

    /** 원본 키: 'EXCESS_RETURN' */
    private String excessReturn;

    /** 원본 키: 'DAILY_RETURN' */
    private String dailyReturn;

    /** 원본 키: 'RECOMMENDATION' */
    private String RECOMMENDATION;

    /** 원본 키: 'CONFIDENCE_SCORE' */
    private String confidenceScore;

    /** 원본 키: 'OVERALL_GRADE' */
    private String overallGrade;

    /** 원본 키: 'BENCHMARK_RETURN' */
    private String benchmarkReturn;

    /** 원본 키: 'RISK_GRADE' */
    private String riskGrade;

    /** 원본 키: 'EMPNO' */
    private String EMPNO;

    /** 원본 키: 'FUND_NAME' */
    private String fundName;

    /** 원본 키: 'ANNUALIZED_RETURN' */
    private String annualizedReturn;

    /** 원본 키: 'SORTINO_RATIO' */
    private String sortinoRatio;

    /** 원본 키: 'VAR_95' */
    private String var95;

    /** 원본 키: 'CVAR_95' */
    private String cvar95;

    /** 원본 키: 'MARKET_OUTLOOK' */
    private String marketOutlook;

    /** 원본 키: 'OPTIMAL_ALLOCATION' */
    private String optimalAllocation;

    /** 원본 키: 'REBALANCING_THRESHOLD' */
    private String rebalancingThreshold;

    /** 원본 키: 'STRENGTHS' */
    private String STRENGTHS;

    /** 원본 키: 'WEAKNESSES' */
    private String WEAKNESSES;

    /** 원본 키: 'RISKS' */
    private String RISKS;

    /** 원본 키: 'EXPENSE_RATIO' */
    private String expenseRatio;

    /** 원본 키: 'ANALYSIS_DATE' */
    private Date analysisDate;

    /** 원본 키: 'KOSPI' */
    private String KOSPI;

    /** 원본 키: 'KOSDAQ' */
    private String KOSDAQ;

    /** 원본 키: 'MSCI World' */
    private String msciWorld;

    /** 원본 키: 'CORRELATION_WITH_BENCHMARKS' */
    private String correlationWithBenchmarks;

    /** 원본 키: 'INCEPTION_DATE' */
    private Date inceptionDate;

    /** 원본 키: 'MARKET_CORRELATION' */
    private String marketCorrelation;

    /** 원본 키: 'SECTOR_EXPOSURE' */
    private String sectorExposure;

    /** 원본 키: 'TOTAL_ASSETS' */
    private String totalAssets;

    /** 원본 키: 'MONTHLY_RETURN' */
    private String monthlyReturn;

    /** 원본 키: 'YEARLY_RETURN' */
    private String yearlyReturn;

    /** 원본 키: 'COMPLEMENTARY_FUNDS' */
    private String complementaryFunds;

    public UnifiedDataVO() {}

    public UnifiedDataVO(Map<String, Object> map) {
        fromMap(map);
    }

    public String getFundCode() {
        return fundCode;
    }

    public void setFundCode(String fundCode) {
        this.fundCode = fundCode;
    }

    public String getFundType() {
        return fundType;
    }

    public void setFundType(String fundType) {
        this.fundType = fundType;
    }

    public String getTotalReturn() {
        return totalReturn;
    }

    public void setTotalReturn(String totalReturn) {
        this.totalReturn = totalReturn;
    }

    public String getRiskLevel() {
        return riskLevel;
    }

    public void setRiskLevel(String riskLevel) {
        this.riskLevel = riskLevel;
    }

    public String getSharpeRatio() {
        return sharpeRatio;
    }

    public void setSharpeRatio(String sharpeRatio) {
        this.sharpeRatio = sharpeRatio;
    }

    public String getMaxDrawdown() {
        return maxDrawdown;
    }

    public void setMaxDrawdown(String maxDrawdown) {
        this.maxDrawdown = maxDrawdown;
    }

    public String getVOLATILITY() {
        return VOLATILITY;
    }

    public void setVOLATILITY(String VOLATILITY) {
        this.VOLATILITY = VOLATILITY;
    }

    public String getPerformanceGrade() {
        return performanceGrade;
    }

    public void setPerformanceGrade(String performanceGrade) {
        this.performanceGrade = performanceGrade;
    }

    public String getExcessReturn() {
        return excessReturn;
    }

    public void setExcessReturn(String excessReturn) {
        this.excessReturn = excessReturn;
    }

    public String getDailyReturn() {
        return dailyReturn;
    }

    public void setDailyReturn(String dailyReturn) {
        this.dailyReturn = dailyReturn;
    }

    public String getRECOMMENDATION() {
        return RECOMMENDATION;
    }

    public void setRECOMMENDATION(String RECOMMENDATION) {
        this.RECOMMENDATION = RECOMMENDATION;
    }

    public String getConfidenceScore() {
        return confidenceScore;
    }

    public void setConfidenceScore(String confidenceScore) {
        this.confidenceScore = confidenceScore;
    }

    public String getOverallGrade() {
        return overallGrade;
    }

    public void setOverallGrade(String overallGrade) {
        this.overallGrade = overallGrade;
    }

    public String getBenchmarkReturn() {
        return benchmarkReturn;
    }

    public void setBenchmarkReturn(String benchmarkReturn) {
        this.benchmarkReturn = benchmarkReturn;
    }

    public String getRiskGrade() {
        return riskGrade;
    }

    public void setRiskGrade(String riskGrade) {
        this.riskGrade = riskGrade;
    }

    public String getEMPNO() {
        return EMPNO;
    }

    public void setEMPNO(String EMPNO) {
        this.EMPNO = EMPNO;
    }

    public String getFundName() {
        return fundName;
    }

    public void setFundName(String fundName) {
        this.fundName = fundName;
    }

    public String getAnnualizedReturn() {
        return annualizedReturn;
    }

    public void setAnnualizedReturn(String annualizedReturn) {
        this.annualizedReturn = annualizedReturn;
    }

    public String getSortinoRatio() {
        return sortinoRatio;
    }

    public void setSortinoRatio(String sortinoRatio) {
        this.sortinoRatio = sortinoRatio;
    }

    public String getVar95() {
        return var95;
    }

    public void setVar95(String var95) {
        this.var95 = var95;
    }

    public String getCvar95() {
        return cvar95;
    }

    public void setCvar95(String cvar95) {
        this.cvar95 = cvar95;
    }

    public String getMarketOutlook() {
        return marketOutlook;
    }

    public void setMarketOutlook(String marketOutlook) {
        this.marketOutlook = marketOutlook;
    }

    public String getOptimalAllocation() {
        return optimalAllocation;
    }

    public void setOptimalAllocation(String optimalAllocation) {
        this.optimalAllocation = optimalAllocation;
    }

    public String getRebalancingThreshold() {
        return rebalancingThreshold;
    }

    public void setRebalancingThreshold(String rebalancingThreshold) {
        this.rebalancingThreshold = rebalancingThreshold;
    }

    public String getSTRENGTHS() {
        return STRENGTHS;
    }

    public void setSTRENGTHS(String STRENGTHS) {
        this.STRENGTHS = STRENGTHS;
    }

    public String getWEAKNESSES() {
        return WEAKNESSES;
    }

    public void setWEAKNESSES(String WEAKNESSES) {
        this.WEAKNESSES = WEAKNESSES;
    }

    public String getRISKS() {
        return RISKS;
    }

    public void setRISKS(String RISKS) {
        this.RISKS = RISKS;
    }

    public String getExpenseRatio() {
        return expenseRatio;
    }

    public void setExpenseRatio(String expenseRatio) {
        this.expenseRatio = expenseRatio;
    }

    public Date getAnalysisDate() {
        return analysisDate;
    }

    public void setAnalysisDate(Date analysisDate) {
        this.analysisDate = analysisDate;
    }

    public String getKOSPI() {
        return KOSPI;
    }

    public void setKOSPI(String KOSPI) {
        this.KOSPI = KOSPI;
    }

    public String getKOSDAQ() {
        return KOSDAQ;
    }

    public void setKOSDAQ(String KOSDAQ) {
        this.KOSDAQ = KOSDAQ;
    }

    public String getMsciWorld() {
        return msciWorld;
    }

    public void setMsciWorld(String msciWorld) {
        this.msciWorld = msciWorld;
    }

    public String getCorrelationWithBenchmarks() {
        return correlationWithBenchmarks;
    }

    public void setCorrelationWithBenchmarks(String correlationWithBenchmarks) {
        this.correlationWithBenchmarks = correlationWithBenchmarks;
    }

    public Date getInceptionDate() {
        return inceptionDate;
    }

    public void setInceptionDate(Date inceptionDate) {
        this.inceptionDate = inceptionDate;
    }

    public String getMarketCorrelation() {
        return marketCorrelation;
    }

    public void setMarketCorrelation(String marketCorrelation) {
        this.marketCorrelation = marketCorrelation;
    }

    public String getSectorExposure() {
        return sectorExposure;
    }

    public void setSectorExposure(String sectorExposure) {
        this.sectorExposure = sectorExposure;
    }

    public String getTotalAssets() {
        return totalAssets;
    }

    public void setTotalAssets(String totalAssets) {
        this.totalAssets = totalAssets;
    }

    public String getMonthlyReturn() {
        return monthlyReturn;
    }

    public void setMonthlyReturn(String monthlyReturn) {
        this.monthlyReturn = monthlyReturn;
    }

    public String getYearlyReturn() {
        return yearlyReturn;
    }

    public void setYearlyReturn(String yearlyReturn) {
        this.yearlyReturn = yearlyReturn;
    }

    public String getComplementaryFunds() {
        return complementaryFunds;
    }

    public void setComplementaryFunds(String complementaryFunds) {
        this.complementaryFunds = complementaryFunds;
    }

    // Map에서 VO로 변환
    public void fromMap(Map<String, Object> map) {
        if (map == null) return;
        
        Object fundCodeValue = map.get("FUND_CODE");
        if (fundCodeValue != null) {
            this.fundCode = fundCodeValue.toString();
        }

        Object fundTypeValue = map.get("FUND_TYPE");
        if (fundTypeValue != null) {
            this.fundType = fundTypeValue.toString();
        }

        Object totalReturnValue = map.get("TOTAL_RETURN");
        if (totalReturnValue != null) {
            this.totalReturn = totalReturnValue.toString();
        }

        Object riskLevelValue = map.get("RISK_LEVEL");
        if (riskLevelValue != null) {
            this.riskLevel = riskLevelValue.toString();
        }

        Object sharpeRatioValue = map.get("SHARPE_RATIO");
        if (sharpeRatioValue != null) {
            this.sharpeRatio = sharpeRatioValue.toString();
        }

        Object maxDrawdownValue = map.get("MAX_DRAWDOWN");
        if (maxDrawdownValue != null) {
            this.maxDrawdown = maxDrawdownValue.toString();
        }

        Object VOLATILITYValue = map.get("VOLATILITY");
        if (VOLATILITYValue != null) {
            this.VOLATILITY = VOLATILITYValue.toString();
        }

        Object performanceGradeValue = map.get("PERFORMANCE_GRADE");
        if (performanceGradeValue != null) {
            this.performanceGrade = performanceGradeValue.toString();
        }

        Object excessReturnValue = map.get("EXCESS_RETURN");
        if (excessReturnValue != null) {
            this.excessReturn = excessReturnValue.toString();
        }

        Object dailyReturnValue = map.get("DAILY_RETURN");
        if (dailyReturnValue != null) {
            this.dailyReturn = dailyReturnValue.toString();
        }

        Object RECOMMENDATIONValue = map.get("RECOMMENDATION");
        if (RECOMMENDATIONValue != null) {
            this.RECOMMENDATION = RECOMMENDATIONValue.toString();
        }

        Object confidenceScoreValue = map.get("CONFIDENCE_SCORE");
        if (confidenceScoreValue != null) {
            this.confidenceScore = confidenceScoreValue.toString();
        }

        Object overallGradeValue = map.get("OVERALL_GRADE");
        if (overallGradeValue != null) {
            this.overallGrade = overallGradeValue.toString();
        }

        Object benchmarkReturnValue = map.get("BENCHMARK_RETURN");
        if (benchmarkReturnValue != null) {
            this.benchmarkReturn = benchmarkReturnValue.toString();
        }

        Object riskGradeValue = map.get("RISK_GRADE");
        if (riskGradeValue != null) {
            this.riskGrade = riskGradeValue.toString();
        }

        Object EMPNOValue = map.get("EMPNO");
        if (EMPNOValue != null) {
            this.EMPNO = EMPNOValue.toString();
        }

        Object fundNameValue = map.get("FUND_NAME");
        if (fundNameValue != null) {
            this.fundName = fundNameValue.toString();
        }

        Object annualizedReturnValue = map.get("ANNUALIZED_RETURN");
        if (annualizedReturnValue != null) {
            this.annualizedReturn = annualizedReturnValue.toString();
        }

        Object sortinoRatioValue = map.get("SORTINO_RATIO");
        if (sortinoRatioValue != null) {
            this.sortinoRatio = sortinoRatioValue.toString();
        }

        Object var95Value = map.get("VAR_95");
        if (var95Value != null) {
            this.var95 = var95Value.toString();
        }

        Object cvar95Value = map.get("CVAR_95");
        if (cvar95Value != null) {
            this.cvar95 = cvar95Value.toString();
        }

        Object marketOutlookValue = map.get("MARKET_OUTLOOK");
        if (marketOutlookValue != null) {
            this.marketOutlook = marketOutlookValue.toString();
        }

        Object optimalAllocationValue = map.get("OPTIMAL_ALLOCATION");
        if (optimalAllocationValue != null) {
            this.optimalAllocation = optimalAllocationValue.toString();
        }

        Object rebalancingThresholdValue = map.get("REBALANCING_THRESHOLD");
        if (rebalancingThresholdValue != null) {
            this.rebalancingThreshold = rebalancingThresholdValue.toString();
        }

        Object STRENGTHSValue = map.get("STRENGTHS");
        if (STRENGTHSValue != null) {
            this.STRENGTHS = STRENGTHSValue.toString();
        }

        Object WEAKNESSESValue = map.get("WEAKNESSES");
        if (WEAKNESSESValue != null) {
            this.WEAKNESSES = WEAKNESSESValue.toString();
        }

        Object RISKSValue = map.get("RISKS");
        if (RISKSValue != null) {
            this.RISKS = RISKSValue.toString();
        }

        Object expenseRatioValue = map.get("EXPENSE_RATIO");
        if (expenseRatioValue != null) {
            this.expenseRatio = expenseRatioValue.toString();
        }

        Object analysisDateValue = map.get("ANALYSIS_DATE");
        if (analysisDateValue != null) {
            if (analysisDateValue instanceof Date) {
                this.analysisDate = (Date) analysisDateValue;
            } else if (analysisDateValue instanceof Timestamp) {
                this.analysisDate = new Date(((Timestamp) analysisDateValue).getTime());
            } else if (analysisDateValue instanceof Long) {
                this.analysisDate = new Date((Long) analysisDateValue);
            }
        }

        Object KOSPIValue = map.get("KOSPI");
        if (KOSPIValue != null) {
            this.KOSPI = KOSPIValue.toString();
        }

        Object KOSDAQValue = map.get("KOSDAQ");
        if (KOSDAQValue != null) {
            this.KOSDAQ = KOSDAQValue.toString();
        }

        Object msciWorldValue = map.get("MSCI World");
        if (msciWorldValue != null) {
            this.msciWorld = msciWorldValue.toString();
        }

        Object correlationWithBenchmarksValue = map.get("CORRELATION_WITH_BENCHMARKS");
        if (correlationWithBenchmarksValue != null) {
            this.correlationWithBenchmarks = correlationWithBenchmarksValue.toString();
        }

        Object inceptionDateValue = map.get("INCEPTION_DATE");
        if (inceptionDateValue != null) {
            if (inceptionDateValue instanceof Date) {
                this.inceptionDate = (Date) inceptionDateValue;
            } else if (inceptionDateValue instanceof Timestamp) {
                this.inceptionDate = new Date(((Timestamp) inceptionDateValue).getTime());
            } else if (inceptionDateValue instanceof Long) {
                this.inceptionDate = new Date((Long) inceptionDateValue);
            }
        }

        Object marketCorrelationValue = map.get("MARKET_CORRELATION");
        if (marketCorrelationValue != null) {
            this.marketCorrelation = marketCorrelationValue.toString();
        }

        Object sectorExposureValue = map.get("SECTOR_EXPOSURE");
        if (sectorExposureValue != null) {
            this.sectorExposure = sectorExposureValue.toString();
        }

        Object totalAssetsValue = map.get("TOTAL_ASSETS");
        if (totalAssetsValue != null) {
            this.totalAssets = totalAssetsValue.toString();
        }

        Object monthlyReturnValue = map.get("MONTHLY_RETURN");
        if (monthlyReturnValue != null) {
            this.monthlyReturn = monthlyReturnValue.toString();
        }

        Object yearlyReturnValue = map.get("YEARLY_RETURN");
        if (yearlyReturnValue != null) {
            this.yearlyReturn = yearlyReturnValue.toString();
        }

        Object complementaryFundsValue = map.get("COMPLEMENTARY_FUNDS");
        if (complementaryFundsValue != null) {
            this.complementaryFunds = complementaryFundsValue.toString();
        }

    }

    // VO에서 Map으로 변환
    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        if (this.fundCode != null) {
            map.put("FUND_CODE", this.fundCode);
        }
        if (this.fundType != null) {
            map.put("FUND_TYPE", this.fundType);
        }
        if (this.totalReturn != null) {
            map.put("TOTAL_RETURN", this.totalReturn);
        }
        if (this.riskLevel != null) {
            map.put("RISK_LEVEL", this.riskLevel);
        }
        if (this.sharpeRatio != null) {
            map.put("SHARPE_RATIO", this.sharpeRatio);
        }
        if (this.maxDrawdown != null) {
            map.put("MAX_DRAWDOWN", this.maxDrawdown);
        }
        if (this.VOLATILITY != null) {
            map.put("VOLATILITY", this.VOLATILITY);
        }
        if (this.performanceGrade != null) {
            map.put("PERFORMANCE_GRADE", this.performanceGrade);
        }
        if (this.excessReturn != null) {
            map.put("EXCESS_RETURN", this.excessReturn);
        }
        if (this.dailyReturn != null) {
            map.put("DAILY_RETURN", this.dailyReturn);
        }
        if (this.RECOMMENDATION != null) {
            map.put("RECOMMENDATION", this.RECOMMENDATION);
        }
        if (this.confidenceScore != null) {
            map.put("CONFIDENCE_SCORE", this.confidenceScore);
        }
        if (this.overallGrade != null) {
            map.put("OVERALL_GRADE", this.overallGrade);
        }
        if (this.benchmarkReturn != null) {
            map.put("BENCHMARK_RETURN", this.benchmarkReturn);
        }
        if (this.riskGrade != null) {
            map.put("RISK_GRADE", this.riskGrade);
        }
        if (this.EMPNO != null) {
            map.put("EMPNO", this.EMPNO);
        }
        if (this.fundName != null) {
            map.put("FUND_NAME", this.fundName);
        }
        if (this.annualizedReturn != null) {
            map.put("ANNUALIZED_RETURN", this.annualizedReturn);
        }
        if (this.sortinoRatio != null) {
            map.put("SORTINO_RATIO", this.sortinoRatio);
        }
        if (this.var95 != null) {
            map.put("VAR_95", this.var95);
        }
        if (this.cvar95 != null) {
            map.put("CVAR_95", this.cvar95);
        }
        if (this.marketOutlook != null) {
            map.put("MARKET_OUTLOOK", this.marketOutlook);
        }
        if (this.optimalAllocation != null) {
            map.put("OPTIMAL_ALLOCATION", this.optimalAllocation);
        }
        if (this.rebalancingThreshold != null) {
            map.put("REBALANCING_THRESHOLD", this.rebalancingThreshold);
        }
        if (this.STRENGTHS != null) {
            map.put("STRENGTHS", this.STRENGTHS);
        }
        if (this.WEAKNESSES != null) {
            map.put("WEAKNESSES", this.WEAKNESSES);
        }
        if (this.RISKS != null) {
            map.put("RISKS", this.RISKS);
        }
        if (this.expenseRatio != null) {
            map.put("EXPENSE_RATIO", this.expenseRatio);
        }
        if (this.analysisDate != null) {
            map.put("ANALYSIS_DATE", this.analysisDate);
        }
        if (this.KOSPI != null) {
            map.put("KOSPI", this.KOSPI);
        }
        if (this.KOSDAQ != null) {
            map.put("KOSDAQ", this.KOSDAQ);
        }
        if (this.msciWorld != null) {
            map.put("MSCI World", this.msciWorld);
        }
        if (this.correlationWithBenchmarks != null) {
            map.put("CORRELATION_WITH_BENCHMARKS", this.correlationWithBenchmarks);
        }
        if (this.inceptionDate != null) {
            map.put("INCEPTION_DATE", this.inceptionDate);
        }
        if (this.marketCorrelation != null) {
            map.put("MARKET_CORRELATION", this.marketCorrelation);
        }
        if (this.sectorExposure != null) {
            map.put("SECTOR_EXPOSURE", this.sectorExposure);
        }
        if (this.totalAssets != null) {
            map.put("TOTAL_ASSETS", this.totalAssets);
        }
        if (this.monthlyReturn != null) {
            map.put("MONTHLY_RETURN", this.monthlyReturn);
        }
        if (this.yearlyReturn != null) {
            map.put("YEARLY_RETURN", this.yearlyReturn);
        }
        if (this.complementaryFunds != null) {
            map.put("COMPLEMENTARY_FUNDS", this.complementaryFunds);
        }
        return map;
    }

    // 정적 변환 메서드
    public static UnifiedDataVO fromMap(Map<String, Object> map) {
        if (map == null) return null;
        return new UnifiedDataVO(map);
    }

    // 특정 키 값 존재 확인
    public boolean hasValue(String key) {
        switch (key) {
            case "FUND_CODE": return this.fundCode != null;
            case "FUND_TYPE": return this.fundType != null;
            case "TOTAL_RETURN": return this.totalReturn != null;
            case "RISK_LEVEL": return this.riskLevel != null;
            case "SHARPE_RATIO": return this.sharpeRatio != null;
            case "MAX_DRAWDOWN": return this.maxDrawdown != null;
            case "VOLATILITY": return this.VOLATILITY != null;
            case "PERFORMANCE_GRADE": return this.performanceGrade != null;
            case "EXCESS_RETURN": return this.excessReturn != null;
            case "DAILY_RETURN": return this.dailyReturn != null;
            case "RECOMMENDATION": return this.RECOMMENDATION != null;
            case "CONFIDENCE_SCORE": return this.confidenceScore != null;
            case "OVERALL_GRADE": return this.overallGrade != null;
            case "BENCHMARK_RETURN": return this.benchmarkReturn != null;
            case "RISK_GRADE": return this.riskGrade != null;
            case "EMPNO": return this.EMPNO != null;
            case "FUND_NAME": return this.fundName != null;
            case "ANNUALIZED_RETURN": return this.annualizedReturn != null;
            case "SORTINO_RATIO": return this.sortinoRatio != null;
            case "VAR_95": return this.var95 != null;
            case "CVAR_95": return this.cvar95 != null;
            case "MARKET_OUTLOOK": return this.marketOutlook != null;
            case "OPTIMAL_ALLOCATION": return this.optimalAllocation != null;
            case "REBALANCING_THRESHOLD": return this.rebalancingThreshold != null;
            case "STRENGTHS": return this.STRENGTHS != null;
            case "WEAKNESSES": return this.WEAKNESSES != null;
            case "RISKS": return this.RISKS != null;
            case "EXPENSE_RATIO": return this.expenseRatio != null;
            case "ANALYSIS_DATE": return this.analysisDate != null;
            case "KOSPI": return this.KOSPI != null;
            case "KOSDAQ": return this.KOSDAQ != null;
            case "MSCI World": return this.msciWorld != null;
            case "CORRELATION_WITH_BENCHMARKS": return this.correlationWithBenchmarks != null;
            case "INCEPTION_DATE": return this.inceptionDate != null;
            case "MARKET_CORRELATION": return this.marketCorrelation != null;
            case "SECTOR_EXPOSURE": return this.sectorExposure != null;
            case "TOTAL_ASSETS": return this.totalAssets != null;
            case "MONTHLY_RETURN": return this.monthlyReturn != null;
            case "YEARLY_RETURN": return this.yearlyReturn != null;
            case "COMPLEMENTARY_FUNDS": return this.complementaryFunds != null;
            default: return false;
        }
    }

    // 특정 키 값 조회
    public Object getValue(String key) {
        switch (key) {
            case "FUND_CODE": return this.fundCode;
            case "FUND_TYPE": return this.fundType;
            case "TOTAL_RETURN": return this.totalReturn;
            case "RISK_LEVEL": return this.riskLevel;
            case "SHARPE_RATIO": return this.sharpeRatio;
            case "MAX_DRAWDOWN": return this.maxDrawdown;
            case "VOLATILITY": return this.VOLATILITY;
            case "PERFORMANCE_GRADE": return this.performanceGrade;
            case "EXCESS_RETURN": return this.excessReturn;
            case "DAILY_RETURN": return this.dailyReturn;
            case "RECOMMENDATION": return this.RECOMMENDATION;
            case "CONFIDENCE_SCORE": return this.confidenceScore;
            case "OVERALL_GRADE": return this.overallGrade;
            case "BENCHMARK_RETURN": return this.benchmarkReturn;
            case "RISK_GRADE": return this.riskGrade;
            case "EMPNO": return this.EMPNO;
            case "FUND_NAME": return this.fundName;
            case "ANNUALIZED_RETURN": return this.annualizedReturn;
            case "SORTINO_RATIO": return this.sortinoRatio;
            case "VAR_95": return this.var95;
            case "CVAR_95": return this.cvar95;
            case "MARKET_OUTLOOK": return this.marketOutlook;
            case "OPTIMAL_ALLOCATION": return this.optimalAllocation;
            case "REBALANCING_THRESHOLD": return this.rebalancingThreshold;
            case "STRENGTHS": return this.STRENGTHS;
            case "WEAKNESSES": return this.WEAKNESSES;
            case "RISKS": return this.RISKS;
            case "EXPENSE_RATIO": return this.expenseRatio;
            case "ANALYSIS_DATE": return this.analysisDate;
            case "KOSPI": return this.KOSPI;
            case "KOSDAQ": return this.KOSDAQ;
            case "MSCI World": return this.msciWorld;
            case "CORRELATION_WITH_BENCHMARKS": return this.correlationWithBenchmarks;
            case "INCEPTION_DATE": return this.inceptionDate;
            case "MARKET_CORRELATION": return this.marketCorrelation;
            case "SECTOR_EXPOSURE": return this.sectorExposure;
            case "TOTAL_ASSETS": return this.totalAssets;
            case "MONTHLY_RETURN": return this.monthlyReturn;
            case "YEARLY_RETURN": return this.yearlyReturn;
            case "COMPLEMENTARY_FUNDS": return this.complementaryFunds;
            default: return null;
        }
    }

    @Override
    public String toString() {
        return "UnifiedDataVO{" +
                "fundCode=" + fundCode +
                ", fundType=" + fundType +
                ", totalReturn=" + totalReturn +
                ", riskLevel=" + riskLevel +
                ", sharpeRatio=" + sharpeRatio +
                ", ..." +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        UnifiedDataVO that = (UnifiedDataVO) o;
        return Objects.equals(fundCode, that.fundCode);
    }

    @Override
    public int hashCode() {
        return Objects.hash(fundCode);
    }
}
