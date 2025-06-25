package kds.poc.com.inswave.cvt.service.impl;

import java.util.List;
import java.util.Map;
import javax.annotation.Resource;
import org.springframework.stereotype.Service;

import kds.poc.com.inswave.cvt.service.DeptTaskService;
import kds.poc.com.inswave.cvt.dao.DeptDAO;

@Service("deptTaskServiceImpl")
public class DeptTaskServiceImpl implements DeptTaskService {

    @Resource(name = "deptDAO")
    private DeptDAO deptDAO;

    public List<Map> selectDeptXDA(Map mp) throws Exception {
        return deptDAO.selectDept(mp);
    }

    public Object insertDeptXDA(Map mp) throws Exception {
        return deptDAO.insertDept(mp);
    }

    public void updateDeptXDA(Map mp) throws Exception {
        deptDAO.updateDept(mp);
    }

    public void deleteDeptXDA(Map mp) throws Exception {
        deptDAO.deleteDept(mp);
    }

    public List<Map> selectDeptWithEmpsXDA(Map mp) throws Exception {
        return deptDAO.selectDeptWithEmps(mp);
    }
} 