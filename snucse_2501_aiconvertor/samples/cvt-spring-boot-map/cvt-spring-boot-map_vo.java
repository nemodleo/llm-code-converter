package com.example.vo;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

/**
 * DataVO
 * 자동 생성일: 2025-06-20 12:03:22
 * 필드 수: 40개
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class DataVO {

    // 기본 정보
    private String fundCode; // 펀드 코드
    private String fundType; // 펀드 유형
    private String EMPNO; // 직원번호
    private String fundName; // 펀드명

    // 수익률 정보
    private BigDecimal totalReturn; // 총 수익률
    private BigDecimal excessReturn; // 초과 수익률
    private BigDecimal dailyReturn; // 일일 수익률
    private BigDecimal benchmarkReturn; // 벤치마크 수익률
    private BigDecimal annualizedReturn; // 연환산 수익률
    private BigDecimal monthlyReturn; // 월간 수익률
    private BigDecimal yearlyReturn; // 연간 수익률

    // 리스크 지표
    private Integer riskLevel; // 위험도
    private BigDecimal sharpeRatio; // 샤프 비율
    private BigDecimal maxDrawdown; // 최대 낙폭
    private BigDecimal VOLATILITY; // 변동성
    private String riskGrade; // 위험 등급
    private BigDecimal sortinoRatio; // 소르티노 비율
    private BigDecimal var95; // 95% VaR
    private BigDecimal cvar95; // 95% CVaR
    private String RISKS; // 위험요소

    // 평가 정보
    private String performanceGrade; // 성과 등급
    private String RECOMMENDATION; // 추천 의견
    private BigDecimal confidenceScore; // 신뢰도 점수
    private String overallGrade; // 종합 등급

    // 펀드 운용 정보
    private BigDecimal expenseRatio; // 총보수율
    private LocalDate analysisDate; // 분석일
    private LocalDate inceptionDate; // 설정일
    private BigDecimal totalAssets; // 총 자산

    // 시장 관련 정보
    private String marketOutlook; // 시장 전망
    private String KOSPI; // KOSPI 수익률
    private String KOSDAQ; // KOSDAQ 수익률
    private String msciWorld; // 원본 키: MSCI World
    private BigDecimal correlationWithBenchmarks; // 원본 키: CORRELATION_WITH_BENCHMARKS
    private BigDecimal marketCorrelation; // 시장 상관관계
    private String sectorExposure; // 섹터 노출도

    // 투자 전략 정보
    private String optimalAllocation; // 최적 배분
    private String rebalancingThreshold; // 리밸런싱 임계값
    private String complementaryFunds; // 보완 펀드

    // 기타
    private String STRENGTHS; // 강점
    private String WEAKNESSES; // 약점

    /**
     * Map에서 DataVO로 변환하는 생성자
     */
    public DataVO(Map<String, Object> map) {
        fromMap(map);
    }
    
    /**
     * Map에서 값을 읽어와 VO 필드에 설정
     */
    public void fromMap(Map<String, Object> map) {
        if (map == null) return;
        
        this.fundCode = getString(map, "FUND_CODE");
        this.fundType = getString(map, "FUND_TYPE");
        this.totalReturn = getBigDecimal(map, "TOTAL_RETURN");
        this.riskLevel = getInteger(map, "RISK_LEVEL");
        this.sharpeRatio = getBigDecimal(map, "SHARPE_RATIO");
        this.maxDrawdown = getBigDecimal(map, "MAX_DRAWDOWN");
        this.VOLATILITY = getBigDecimal(map, "VOLATILITY");
        this.performanceGrade = getString(map, "PERFORMANCE_GRADE");
        this.excessReturn = getBigDecimal(map, "EXCESS_RETURN");
        this.dailyReturn = getBigDecimal(map, "DAILY_RETURN");
        this.RECOMMENDATION = getString(map, "RECOMMENDATION");
        this.confidenceScore = getBigDecimal(map, "CONFIDENCE_SCORE");
        this.overallGrade = getString(map, "OVERALL_GRADE");
        this.benchmarkReturn = getBigDecimal(map, "BENCHMARK_RETURN");
        this.riskGrade = getString(map, "RISK_GRADE");
        this.EMPNO = getString(map, "EMPNO");
        this.fundName = getString(map, "FUND_NAME");
        this.annualizedReturn = getBigDecimal(map, "ANNUALIZED_RETURN");
        this.sortinoRatio = getBigDecimal(map, "SORTINO_RATIO");
        this.var95 = getBigDecimal(map, "VAR_95");
        this.cvar95 = getBigDecimal(map, "CVAR_95");
        this.marketOutlook = getString(map, "MARKET_OUTLOOK");
        this.optimalAllocation = getString(map, "OPTIMAL_ALLOCATION");
        this.rebalancingThreshold = getString(map, "REBALANCING_THRESHOLD");
        this.STRENGTHS = getString(map, "STRENGTHS");
        this.WEAKNESSES = getString(map, "WEAKNESSES");
        this.RISKS = getString(map, "RISKS");
        this.expenseRatio = getBigDecimal(map, "EXPENSE_RATIO");
        this.analysisDate = getLocalDate(map, "ANALYSIS_DATE");
        this.KOSPI = getString(map, "KOSPI");
        this.KOSDAQ = getString(map, "KOSDAQ");
        this.msciWorld = getString(map, "MSCI World");
        this.correlationWithBenchmarks = getBigDecimal(map, "CORRELATION_WITH_BENCHMARKS");
        this.inceptionDate = getLocalDate(map, "INCEPTION_DATE");
        this.marketCorrelation = getBigDecimal(map, "MARKET_CORRELATION");
        this.sectorExposure = getString(map, "SECTOR_EXPOSURE");
        this.totalAssets = getBigDecimal(map, "TOTAL_ASSETS");
        this.monthlyReturn = getBigDecimal(map, "MONTHLY_RETURN");
        this.yearlyReturn = getBigDecimal(map, "YEARLY_RETURN");
        this.complementaryFunds = getString(map, "COMPLEMENTARY_FUNDS");
    }
    
    /**
     * VO를 Map으로 변환
     */
    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        
        putIfNotNull(map, "FUND_CODE", this.fundCode);
        putIfNotNull(map, "FUND_TYPE", this.fundType);
        putIfNotNull(map, "TOTAL_RETURN", this.totalReturn);
        putIfNotNull(map, "RISK_LEVEL", this.riskLevel);
        putIfNotNull(map, "SHARPE_RATIO", this.sharpeRatio);
        putIfNotNull(map, "MAX_DRAWDOWN", this.maxDrawdown);
        putIfNotNull(map, "VOLATILITY", this.VOLATILITY);
        putIfNotNull(map, "PERFORMANCE_GRADE", this.performanceGrade);
        putIfNotNull(map, "EXCESS_RETURN", this.excessReturn);
        putIfNotNull(map, "DAILY_RETURN", this.dailyReturn);
        putIfNotNull(map, "RECOMMENDATION", this.RECOMMENDATION);
        putIfNotNull(map, "CONFIDENCE_SCORE", this.confidenceScore);
        putIfNotNull(map, "OVERALL_GRADE", this.overallGrade);
        putIfNotNull(map, "BENCHMARK_RETURN", this.benchmarkReturn);
        putIfNotNull(map, "RISK_GRADE", this.riskGrade);
        putIfNotNull(map, "EMPNO", this.EMPNO);
        putIfNotNull(map, "FUND_NAME", this.fundName);
        putIfNotNull(map, "ANNUALIZED_RETURN", this.annualizedReturn);
        putIfNotNull(map, "SORTINO_RATIO", this.sortinoRatio);
        putIfNotNull(map, "VAR_95", this.var95);
        putIfNotNull(map, "CVAR_95", this.cvar95);
        putIfNotNull(map, "MARKET_OUTLOOK", this.marketOutlook);
        putIfNotNull(map, "OPTIMAL_ALLOCATION", this.optimalAllocation);
        putIfNotNull(map, "REBALANCING_THRESHOLD", this.rebalancingThreshold);
        putIfNotNull(map, "STRENGTHS", this.STRENGTHS);
        putIfNotNull(map, "WEAKNESSES", this.WEAKNESSES);
        putIfNotNull(map, "RISKS", this.RISKS);
        putIfNotNull(map, "EXPENSE_RATIO", this.expenseRatio);
        putIfNotNull(map, "ANALYSIS_DATE", this.analysisDate);
        putIfNotNull(map, "KOSPI", this.KOSPI);
        putIfNotNull(map, "KOSDAQ", this.KOSDAQ);
        putIfNotNull(map, "MSCI World", this.msciWorld);
        putIfNotNull(map, "CORRELATION_WITH_BENCHMARKS", this.correlationWithBenchmarks);
        putIfNotNull(map, "INCEPTION_DATE", this.inceptionDate);
        putIfNotNull(map, "MARKET_CORRELATION", this.marketCorrelation);
        putIfNotNull(map, "SECTOR_EXPOSURE", this.sectorExposure);
        putIfNotNull(map, "TOTAL_ASSETS", this.totalAssets);
        putIfNotNull(map, "MONTHLY_RETURN", this.monthlyReturn);
        putIfNotNull(map, "YEARLY_RETURN", this.yearlyReturn);
        putIfNotNull(map, "COMPLEMENTARY_FUNDS", this.complementaryFunds);
        return map;
    }
    
    /**
     * 정적 팩토리 메서드
     */
    public static DataVO fromMap(Map<String, Object> map) {
        return map == null ? null : new DataVO(map);
    }
    
    // ================= 유틸리티 메서드 =================
    
    private String getString(Map<String, Object> map, String key) {
        Object value = map.get(key);
        return value != null ? value.toString() : null;
    }
    
    private Integer getInteger(Map<String, Object> map, String key) {
        Object value = map.get(key);
        if (value == null) return null;
        try {
            if (value instanceof Integer) return (Integer) value;
            return Integer.valueOf(value.toString());
        } catch (NumberFormatException e) {
            return null;
        }
    }
    
    private Long getLong(Map<String, Object> map, String key) {
        Object value = map.get(key);
        if (value == null) return null;
        try {
            if (value instanceof Long) return (Long) value;
            if (value instanceof Integer) return ((Integer) value).longValue();
            return Long.valueOf(value.toString());
        } catch (NumberFormatException e) {
            return null;
        }
    }
    
    private BigDecimal getBigDecimal(Map<String, Object> map, String key) {
        Object value = map.get(key);
        if (value == null) return null;
        try {
            if (value instanceof BigDecimal) return (BigDecimal) value;
            if (value instanceof Number) return BigDecimal.valueOf(((Number) value).doubleValue());
            return new BigDecimal(value.toString());
        } catch (NumberFormatException e) {
            return null;
        }
    }
    
    private Boolean getBoolean(Map<String, Object> map, String key) {
        Object value = map.get(key);
        if (value == null) return null;
        if (value instanceof Boolean) return (Boolean) value;
        return Boolean.valueOf(value.toString());
    }
    
    private LocalDate getLocalDate(Map<String, Object> map, String key) {
        Object value = map.get(key);
        if (value == null) return null;
        try {
            if (value instanceof LocalDate) return (LocalDate) value;
            if (value instanceof java.util.Date) {
                return ((java.util.Date) value).toInstant()
                    .atZone(java.time.ZoneId.systemDefault()).toLocalDate();
            }
            if (value instanceof java.sql.Date) return ((java.sql.Date) value).toLocalDate();
            if (value instanceof java.sql.Timestamp) {
                return ((java.sql.Timestamp) value).toLocalDateTime().toLocalDate();
            }
            return LocalDate.parse(value.toString());
        } catch (Exception e) {
            return null;
        }
    }
    
    private Object getObject(Map<String, Object> map, String key) {
        return map.get(key);
    }
    
    private void putIfNotNull(Map<String, Object> map, String key, Object value) {
        if (value != null) {
            map.put(key, value);
        }
    }
}
