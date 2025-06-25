package kds.poc.cvt.model;

import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

@Data
public class FundAnalysisResultVo {
    private String fundCode;
    private String fundName;
    private LocalDate analysisDate;
    
    // 기본 성과 지표
    private BigDecimal totalReturn;
    private BigDecimal annualizedReturn;
    private BigDecimal benchmarkReturn;
    private BigDecimal excessReturn;
    
    // 리스크 지표
    private BigDecimal volatility;
    private BigDecimal sharpeRatio;
    private BigDecimal sortinoRatio;
    private BigDecimal maxDrawdown;
    private BigDecimal var95; // Value at Risk (95% 신뢰수준)
    private BigDecimal cvar95; // Conditional Value at Risk
    
    // 상관관계 분석
    private Map<String, BigDecimal> correlationWithBenchmarks;
    private Map<String, BigDecimal> correlationWithOtherFunds;
    
    // 성과 평가
    private String performanceGrade; // A+, A, B+, B, C, D
    private String riskGrade; // 1, 2, 3, 4, 5
    private String overallGrade; // A+, A, B+, B, C, D
    
    // 투자 추천
    private String recommendation; // BUY, HOLD, SELL
    private BigDecimal confidenceScore; // 0.0 ~ 1.0
    private List<String> strengths;
    private List<String> weaknesses;
    private List<String> risks;
    
    // 시장 분석
    private String marketOutlook; // BULLISH, BEARISH, NEUTRAL
    private BigDecimal marketCorrelation;
    private String sectorExposure;
    
    // 포트폴리오 최적화
    private BigDecimal optimalAllocation; // 최적 배분 비율
    private BigDecimal rebalancingThreshold; // 리밸런싱 임계값
    private List<String> complementaryFunds; // 보완 펀드 추천
} 