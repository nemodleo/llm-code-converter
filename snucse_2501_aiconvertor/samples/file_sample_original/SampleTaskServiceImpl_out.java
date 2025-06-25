package kds.poc.com.inswave.cvt.service.impl;

import java.util.List;
import javax.annotation.Resource;
import org.springframework.stereotype.Service;

import kds.poc.com.inswave.cvt.service.SampleTaskService;
import kds.poc.com.inswave.cvt.vo.EmpVo;
import kds.poc.com.inswave.cvt.dao.CvtDAO;

@Service("sampleTaskServiceImpl")
public class SampleTaskServiceImpl implements SampleTaskService {


    // (샘플) SELECT EMPNO, ENAME, JOB, MGR, HIREDATE, SAL, COMM, DEPTNO, ACCOUNT FROM EMP
    public List<EmpVo> selectEmpXDA(EmpVo empVo) throws Exception {
        //XDA xda = null;
        try {
            //xda = XDAFactory.getXDA("default", Constants.KEEP_CONNECTION) ---> (해당 라인의 소스는 변환을 지원하지 않습니다.);
            return cvtDAO.selectEmp(empVo);
        } catch (Exception e) {
            throw e;
        }
    }

    // (샘플) INSERT INTO EMP (EMPNO, ENAME, JOB, MGR, HIREDATE, SAL, COMM, DEPTNO, ACCOUNT) VALUES(5000, '김일', '사원', 8000, sysdate, 3000, 0, 10, 0)

    public Object insertEmpXDA(EmpVo empVo) throws Exception {
        Object result = null;
        //XDA xda = null;
        try {
            //xda = XDAFactory.getXDA("default", Constants.KEEP_CONNECTION) ---> (해당 라인의 소스는 변환을 지원하지 않습니다.);            empVo.setEmpno(5000);
            empVo.setEname("김일");
            empVo.setJob("사원");
            empVo.setMgr(8000);
            empVo.setSal(3000);
            empVo.setComm(0);
            empVo.setDeptno(10);
            empVo.setAccount(0);
            result = cvtDAO.insertEmp(empVo);
        } catch (Exception e) {
            throw e;
        }
        return result;
    }

    // (샘플) UPDATE EMP SET JOB='대리', SAL=6000 WHERE EMPNO = 5000 AND ENAME = '김일'
    public void updateEmpXDA(EmpVo empVo) throws Exception {
        Object result = null;
        //XDA xda = null;
        try {
            //xda = XDAFactory.getXDA("default", Constants.KEEP_CONNECTION) ---> (해당 라인의 소스는 변환을 지원하지 않습니다.);
            empVo.setEmpno("5000");
            empVo.setEname("김일");
            result = cvtDAO.updateEmp(empVo);
        } catch (Exception e) {
            throw e;
        }
    }

    // (샘플) DELETE FROM EMP WHERE EMPNO = 5000 AND ENAME = '김일'
    public void deleteEmpXDA(EmpVo empVo) throws Exception {
        Object result = null;
        //XDA xda = null;
        try {
            //xda = XDAFactory.getXDA("default", Constants.KEEP_CONNECTION) ---> (해당 라인의 소스는 변환을 지원하지 않습니다.);
            empVo.setEmpno(5000);
            empVo.setEname("김일");
            result = cvtDAO.deleteEmp(empVo);
        } catch (Exception e) {
            throw e;
        }
    }

    @Resource(name = "cvtDAO")
    private CvtDAO cvtDAO;
}
