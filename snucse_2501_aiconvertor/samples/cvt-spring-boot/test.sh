mvn clean spring-boot:run

#!/usr/bin/env bash
# Simple API smoke-test for the Employee REST endpoints
# Usage: ensure the Spring Boot app is running on http://localhost:8080, then:
#    chmod +x api_test.sh && ./api_test.sh

BASE_URL="http://localhost:8080/api/employees"

echo "1) Initial list of employees"
curl -s "$BASE_URL"
echo -e "\n# Expected: one record for empno=7369 from data.sql"

echo -e "\n2) Create employee 5001"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{"empno":"5001","ename":"LEE","job":"ANALYST","sal":"4000","deptno":"30","account":"1"}'
echo -e "\n# Expected: JSON for 5001, hiredate null (returned VO)"

echo -e "\n3) List filtered by empno=5001"
curl -s "$BASE_URL?empno=5001"
echo -e "\n# Expected: one record for empno=5001 with job=ANALYST and a non-null hiredate"

echo -e "\n4) Update employee 5001 to job= SENIOR"
curl -s -X PUT "$BASE_URL/5001" \
  -H "Content-Type: application/json" \
  -d '{"empno":"5001","ename":"LEE","job":"SENIOR","sal":"4500"}'
echo -e "\n# Expected: no output, HTTP 200 OK"

echo -e "\n5) Verify update via filter"
curl -s "$BASE_URL?empno=5001"
echo -e "\n# Expected: one record for empno=5001 with job=SENIOR"

echo -e "\n6) Delete employee 5001"
curl -s -X DELETE "$BASE_URL/5001"
echo -e "\n# Expected: no output, HTTP 200 OK"

echo -e "\n7) Final list of employees"
curl -s "$BASE_URL"
echo -e "\n# Expected: only the original record for empno=7369 remains"
