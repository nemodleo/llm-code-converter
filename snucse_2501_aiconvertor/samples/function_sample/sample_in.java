    // (샘플) SELECT EMPNO, ENAME, JOB, MGR, HIREDATE, SAL, COMM, DEPTNO, ACCOUNT FROM EMP
    public Object selectEmpXDA(Map doc) throws Exception {
        Object result = null;
        //XDA xda = null;
        try {
            //xda = XDAFactory.getXDA("default", Constants.KEEP_CONNECTION) ---> (해당 라인의 소스는 변환을 지원하지 않습니다.);
            result = cvtDAO.SelectEmp(doc);
        } catch (Exception e) {
            throw e;
        }
        return result;
    }