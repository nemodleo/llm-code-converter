# CVT Spring Boot - 펀드 관리 시스템

금융권에서 사용할 수 있는 고급 펀드 관리 시스템입니다.

## 🚀 주요 기능

### 1. 펀드 기본 관리
- 펀드 정보 CRUD (생성, 조회, 수정, 삭제)
- 펀드 유형별 분류 (주식형, 채권형, 혼합형, MMF)
- 위험도별 분류 (1~5등급)
- 펀드 매니저 관리

### 2. 펀드 성과 관리
- 일간/주간/월간/연간 수익률 추적
- 누적 수익률 및 벤치마크 대비 성과
- 샤프 비율, 변동성, 최대 낙폭 등 리스크 지표
- 기간별 성과 분석

### 3. 고급 검색 및 필터링
- 펀드명 검색 (부분 일치)
- 펀드 유형별 필터링
- 위험도별 필터링
- 상위 성과 펀드 조회

## 📊 데이터 모델

### Fund (펀드 정보)
- `fundCode`: 펀드 코드 (PK)
- `fundName`: 펀드명
- `fundType`: 펀드 유형 (주식형, 채권형, 혼합형, MMF)
- `manager`: 펀드 매니저
- `nav`: 기준가격 (Net Asset Value)
- `totalAssets`: 총 자산
- `expenseRatio`: 총보수율
- `inceptionDate`: 설정일
- `riskLevel`: 위험도 (1~5등급)
- `status`: 상태 (운용중, 운용정지, 해지)
- `description`: 펀드 설명
- `lastUpdate`: 최종 업데이트일

### FundPerformance (펀드 성과)
- `fundCode`: 펀드 코드 (FK)
- `date`: 기준일
- `nav`: 기준가격
- `dailyReturn`: 일간 수익률
- `weeklyReturn`: 주간 수익률
- `monthlyReturn`: 월간 수익률
- `yearlyReturn`: 연간 수익률
- `totalReturn`: 누적 수익률
- `benchmarkReturn`: 벤치마크 대비 수익률
- `sharpeRatio`: 샤프 비율
- `volatility`: 변동성
- `maxDrawdown`: 최대 낙폭

## 🔌 API 엔드포인트

### 펀드 기본 관리

#### 펀드 목록 조회
```http
GET /api/funds
GET /api/funds?fundType=주식형&riskLevel=4
```

#### 특정 펀드 조회
```http
GET /api/funds/{fundCode}
```

#### 펀드 생성
```http
POST /api/funds
Content-Type: application/json

{
  "fundCode": "F001",
  "fundName": "KB국민주식혼합증권투자신탁",
  "fundType": "혼합형",
  "manager": "김철수",
  "nav": 12500.50,
  "totalAssets": 150000000000,
  "expenseRatio": 0.0150,
  "inceptionDate": "2020-01-15",
  "riskLevel": "3",
  "status": "운용중",
  "description": "국내 주식과 채권을 혼합 투자하는 펀드",
  "lastUpdate": "2024-01-15"
}
```

#### 펀드 수정
```http
PUT /api/funds/{fundCode}
Content-Type: application/json
```

#### 펀드 삭제
```http
DELETE /api/funds/{fundCode}
```

### 펀드 성과 관리

#### 펀드 성과 조회
```http
GET /api/funds/{fundCode}/performance
```

#### 기간별 성과 조회
```http
GET /api/funds/{fundCode}/performance/range?startDate=2024-01-01&endDate=2024-01-15
```

#### 성과 데이터 저장
```http
POST /api/funds/{fundCode}/performance
Content-Type: application/json

{
  "date": "2024-01-15",
  "nav": 12500.50,
  "dailyReturn": 0.0150,
  "weeklyReturn": 0.0850,
  "monthlyReturn": 0.0250,
  "yearlyReturn": 0.1200,
  "totalReturn": 0.2500,
  "benchmarkReturn": 0.1100,
  "sharpeRatio": 1.25,
  "volatility": 0.1800,
  "maxDrawdown": -0.0800
}
```

### 고급 검색 및 분석

#### 상위 성과 펀드 조회
```http
GET /api/funds/top/{limit}
```

#### 펀드 유형별 조회
```http
GET /api/funds/type/{fundType}
```

#### 위험도별 조회
```http
GET /api/funds/risk/{riskLevel}
```

## 🛠 기술 스택

- **Framework**: Spring Boot 3.x
- **Database**: H2 (In-Memory)
- **ORM**: MyBatis
- **Build Tool**: Maven
- **Language**: Java 8+

## 🚀 실행 방법

1. 프로젝트 클론
```bash
git clone <repository-url>
cd cvt-spring-boot
```

2. 애플리케이션 실행
```bash
mvn spring-boot:run
```

3. API 테스트
```bash
# 펀드 목록 조회
curl -X GET "http://localhost:8080/api/funds"

# 특정 펀드 조회
curl -X GET "http://localhost:8080/api/funds/F001"

# 펀드 성과 조회
curl -X GET "http://localhost:8080/api/funds/F001/performance"
```

## 📈 샘플 데이터

시스템에는 다음과 같은 샘플 데이터가 포함되어 있습니다:

- **5개의 펀드**: 주식형, 채권형, 혼합형, MMF 등 다양한 유형
- **성과 데이터**: 각 펀드별 일간/주간/월간/연간 수익률 및 리스크 지표
- **실제 금융 데이터**: NAV, 총 자산, 보수율 등 실제와 유사한 데이터

## 🔮 향후 확장 계획

1. **포트폴리오 관리**: 고객별 투자 포트폴리오 구성
2. **실시간 시세**: 외부 API 연동을 통한 실시간 NAV 업데이트
3. **알림 시스템**: 수익률 변동 시 알림 기능
4. **보고서 생성**: PDF/Excel 형태의 성과 보고서
5. **사용자 권한 관리**: 역할별 접근 권한 제어

## 📝 라이선스

이 프로젝트는 교육 및 데모 목적으로 제작되었습니다. 