package kds.poc.cvt.model;

import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;

@Data
public class FundPerformanceVo {
    private String fundCode;        // 펀드 코드
    private LocalDate date;         // 기준일
    private BigDecimal nav;         // 기준가격
    private BigDecimal dailyReturn; // 일간 수익률
    private BigDecimal weeklyReturn; // 주간 수익률
    private BigDecimal monthlyReturn; // 월간 수익률
    private BigDecimal yearlyReturn; // 연간 수익률
    private BigDecimal totalReturn; // 누적 수익률
    private BigDecimal benchmarkReturn; // 벤치마크 대비 수익률
    private BigDecimal sharpeRatio; // 샤프 비율
    private BigDecimal volatility;  // 변동성
    private BigDecimal maxDrawdown; // 최대 낙폭
} 