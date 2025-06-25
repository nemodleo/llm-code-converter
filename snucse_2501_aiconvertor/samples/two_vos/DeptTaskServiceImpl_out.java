package kds.poc.com.inswave.cvt.service.impl;

import java.util.List;
import javax.annotation.Resource;
import org.springframework.stereotype.Service;

import kds.poc.com.inswave.cvt.service.DeptTaskService;
import kds.poc.com.inswave.cvt.vo.DeptVo;
import kds.poc.com.inswave.cvt.vo.EmpVo;
import kds.poc.com.inswave.cvt.dao.DeptDAO;

/**
 * Service implementation for department management operations.
 */
@Service("deptTaskServiceImpl")
public class DeptTaskServiceImpl implements DeptTaskService {

    @Resource(name = "deptDAO")
    private DeptDAO deptDAO;

    /**
     * Select department information
     */
    public List<DeptVo> selectDeptXDA(DeptVo deptVo) throws Exception {
        return deptDAO.selectDept(deptVo);
    }

    /**
     * Insert department information
     */
    public Object insertDeptXDA(DeptVo deptVo) throws Exception {
        return deptDAO.insertDept(deptVo);
    }

    /**
     * Update department information
     */
    public void updateDeptXDA(DeptVo deptVo) throws Exception {
        deptDAO.updateDept(deptVo);
    }

    /**
     * Delete department information
     */
    public void deleteDeptXDA(DeptVo deptVo) throws Exception {
        deptDAO.deleteDept(deptVo);
    }

    /**
     * Select department with its employees
     * @param empVo Employee value object containing search criteria
     * @return List of departments with associated employees
     */
    public List<DeptVo> selectDeptWithEmpsXDA(EmpVo empVo) throws Exception {
        return deptDAO.selectDeptWithEmps(empVo);
    }
} 