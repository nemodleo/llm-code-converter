CREATE TABLE EMP (
  EMPNO    VARCHAR(10)  PRIMARY KEY,
  ENAME    VARCHAR(50),
  JOB      VARCHAR(30),
  MGR      VARCHAR(10),
  HIREDATE TIMESTAMP,
  SAL      VARCHAR(20),
  COMM     VARCHAR(20),
  DEPTNO   VARCHAR(10),
  ACCOUNT  VARCHAR(10)
);

-- 펀드 정보 테이블
CREATE TABLE FUND (
  FUND_CODE       VARCHAR(20)  PRIMARY KEY,
  FUND_NAME       VARCHAR(100) NOT NULL,
  FUND_TYPE       VARCHAR(30)  NOT NULL,  -- 주식형, 채권형, 혼합형, MMF 등
  MANAGER         VARCHAR(50),
  NAV             DECIMAL(10,4),           -- 기준가격
  TOTAL_ASSETS    DECIMAL(15,2),           -- 총 자산
  EXPENSE_RATIO   DECIMAL(5,4),            -- 총보수율
  INCEPTION_DATE  DATE,                    -- 설정일
  RISK_LEVEL      VARCHAR(10),             -- 위험도 (1~5등급)
  STATUS          VARCHAR(20)  DEFAULT '운용중', -- 운용중, 운용정지, 해지 등
  DESCRIPTION     VARCHAR(500),
  LAST_UPDATE     DATE
);

-- 펀드 성과 테이블
CREATE TABLE FUND_PERFORMANCE (
  FUND_CODE        VARCHAR(20),
  DATE             DATE,
  NAV              DECIMAL(10,4),
  DAILY_RETURN     DECIMAL(8,4),           -- 일간 수익률
  WEEKLY_RETURN    DECIMAL(8,4),           -- 주간 수익률
  MONTHLY_RETURN   DECIMAL(8,4),           -- 월간 수익률
  YEARLY_RETURN    DECIMAL(8,4),           -- 연간 수익률
  TOTAL_RETURN     DECIMAL(8,4),           -- 누적 수익률
  BENCHMARK_RETURN DECIMAL(8,4),           -- 벤치마크 대비 수익률
  SHARPE_RATIO     DECIMAL(8,4),           -- 샤프 비율
  VOLATILITY       DECIMAL(8,4),           -- 변동성
  MAX_DRAWDOWN     DECIMAL(8,4),           -- 최대 낙폭
  PRIMARY KEY (FUND_CODE, DATE),
  FOREIGN KEY (FUND_CODE) REFERENCES FUND(FUND_CODE)
);