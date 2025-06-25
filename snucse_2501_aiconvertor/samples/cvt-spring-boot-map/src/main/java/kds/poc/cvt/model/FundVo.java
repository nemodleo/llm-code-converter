package kds.poc.cvt.model;

import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;

@Data
public class FundVo {
    private String fundCode;        // 펀드 코드
    private String fundName;        // 펀드명
    private String fundType;        // 펀드 유형 (주식형, 채권형, 혼합형, MMF 등)
    private String manager;         // 펀드 매니저
    private BigDecimal nav;         // 기준가격 (Net Asset Value)
    private BigDecimal totalAssets; // 총 자산
    private BigDecimal expenseRatio; // 총보수율
    private LocalDate inceptionDate; // 설정일
    private String riskLevel;       // 위험도 (1~5등급)
    private String status;          // 상태 (운용중, 운용정지, 해지 등)
    private String description;     // 펀드 설명
    private LocalDate lastUpdate;   // 최종 업데이트일
} 