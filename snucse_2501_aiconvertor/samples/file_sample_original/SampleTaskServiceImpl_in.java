package kds.poc.com.inswave.cvt.service.impl;

import java.util.ArrayList;

import java.util.Map;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import kds.poc.com.inswave.cvt.service.SampleTaskService;

@Service("sampleTaskServiceImpl")
public class SampleTaskServiceImpl implements SampleTaskService {

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

    // (샘플) INSERT INTO EMP (EMPNO, ENAME, JOB, MGR, HIREDATE, SAL, COMM, DEPTNO, ACCOUNT) VALUES(5000, '김일', '사원', 8000, sysdate, 3000, 0, 10, 0)
    public Object insertEmpXDA(Map doc) throws Exception {
        Object result = null;
        //XDA xda = null;
        try {
            //xda = XDAFactory.getXDA("default", Constants.KEEP_CONNECTION) ---> (해당 라인의 소스는 변환을 지원하지 않습니다.);
            doc.put("EMPNO", 5000);
            doc.put("ENAME", "김일");
            doc.put("JOB", "사원");
            doc.put("MGR", 8000);
            doc.put("SAL", 3000);
            doc.put("COMM", 0);
            doc.put("DEPTNO", 10);
            doc.put("ACCOUNT", 0);
            result = cvtDAO.InsertEmp(doc);
        } catch (Exception e) {
            throw e;
        }
        return result;
    }

    // (샘플) UPDATE EMP SET JOB='대리', SAL=6000 WHERE EMPNO = 5000 AND ENAME = '김일'
    public void updateEmpXDA(Map doc) throws Exception {
        Object result = null;
        //XDA xda = null;
        try {
            //xda = XDAFactory.getXDA("default", Constants.KEEP_CONNECTION) ---> (해당 라인의 소스는 변환을 지원하지 않습니다.);
            doc.put("EMPNO", "5000");
            doc.put("ENAME", "김일");
            result = cvtDAO.UpdateEmp(doc);
        } catch (Exception e) {
            throw e;
        }
    }

    // (샘플) DELETE FROM EMP WHERE EMPNO = 5000 AND ENAME = '김일'
    public void deleteEmpXDA(Map doc) throws Exception {
        Object result = null;
        //XDA xda = null;
        try {
            //xda = XDAFactory.getXDA("default", Constants.KEEP_CONNECTION) ---> (해당 라인의 소스는 변환을 지원하지 않습니다.);
            doc.put("EMPNO", 5000);
            doc.put("ENAME", "김일");
            result = cvtDAO.DeleteEmp(doc);
        } catch (Exception e) {
            throw e;
        }
    }

    @Resource(name = "cvtDAO")
    private kds.poc.com.inswave.cvt.dao.CvtDAO cvtDAO;
}
