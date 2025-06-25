mvn spring-boot:run
curl -X POST http://localhost:8080/api/funds -H "Content-Type: application/json" -d '{"fundCode":"F001","fundName":"테스트펀드","fundType":"주식형","manager":"홍길동","nav":1000,"totalAssets":100000000,"expenseRatio":0.012,"inceptionDate":"2023-01-01","riskLevel":"3","status":"ACTIVE","description":"테스트","lastUpdate":"2024-06-20"}'

# 펀드 등록
curl -X POST http://localhost:8080/api/funds \
  -H "Content-Type: application/json" \
  -d '{
    "FUND_CODE": "F100",
    "FUND_NAME": "AI성장펀드",
    "FUND_TYPE": "주식형",
    "MANAGER": "홍길동",
    "NAV": 1000,
    "TOTAL_ASSETS": 100000000,
    "EXPENSE_RATIO": 0.012,
    "INCEPTION_DATE": "2023-01-01",
    "RISK_LEVEL": "3",
    "STATUS": "ACTIVE",
    "DESCRIPTION": "AI 관련 성장주에 투자",
    "LAST_UPDATE": "2024-06-20"
  }'

    # 펀드 성과 등록
  curl -X POST http://localhost:8080/api/funds/F100/performance \
  -H "Content-Type: application/json" \
  -d '{
    "DATE": "2024-06-20",
    "NAV": 1200,
    "DAILY_RETURN": 0.01,
    "WEEKLY_RETURN": 0.03,
    "MONTHLY_RETURN": 0.08,
    "YEARLY_RETURN": 0.15,
    "TOTAL_RETURN": 0.20,
    "BENCHMARK_RETURN": 0.18,
    "SHARPE_RATIO": 1.2,
    "VOLATILITY": 0.18,
    "MAX_DRAWDOWN": -0.09
  }'

  # 펀드 종합 분석
  curl http://localhost:8080/api/funds/F100/analysis?period=1Y


  # VO-based 구현

  curl -X POST http://localhost:8080/api/funds -H "Content-Type: application/json" -d '{"fundCode": "F100", "fundName": "AI성장펀드", "fundType": "주식형", "manager": "홍길동", "nav": 1000, "totalAssets": 100000000, "expenseRatio": 0.012, "inceptionDate": "2023-01-01", "riskLevel": "3", "status": "ACTIVE", "description": "AI 관련 성장주에 투자", "lastUpdate": "2024-06-20"}'

  curl -X POST http://localhost:8080/api/funds/F100/performance -H "Content-Type: application/json" -d '{"date": "2024-06-20", "nav": 1200, "dailyReturn": 0.01, "weeklyReturn": 0.03, "monthlyReturn": 0.08, "yearlyReturn": 0.15, "totalReturn": 0.20, "benchmarkReturn": 0.18, "sharpeRatio": 1.2, "volatility": 0.18, "maxDrawdown": -0.09}'

  curl http://localhost:8080/api/funds/F100/analysis?period=1Y