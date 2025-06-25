package kds.poc.com.inswave.cvt.dao;

import java.util.List;
import org.springframework.stereotype.Repository;
import com.inswave.elfw.exception.ElException;
import kds.poc.base.cmmn.dao.BaseDefaultAbstractDAO;
import kds.poc.com.inswave.cvt.vo.DeptVo;
import kds.poc.com.inswave.cvt.vo.EmpVo;

/**  
 * @ClassSubJect DAO convert 
 * @Class Name : DeptDAO
 * @Description : Department Data Access Object
 * 
 * Copyright Inswave (C) by Sampler All right reserved.
 */
@Repository("deptDAO")
public class DeptDAO extends BaseDefaultAbstractDAO {

    /**
     * Insert department information
     */
    public int insertDept(DeptVo deptVo) throws ElException {
        return (int) insert("com.inswave.cvt.InsertDept", deptVo);
    }

    /**
     * Update department information
     */
    public int updateDept(DeptVo deptVo) throws ElException {
        return (int) update("com.inswave.cvt.UpdateDept", deptVo);
    }

    /**
     * Delete department information
     */
    public int deleteDept(DeptVo deptVo) throws ElException {
        return (int) delete("com.inswave.cvt.DeleteDept", deptVo);
    }

    /**
     * Select department information
     */
    public List<DeptVo> selectDept(DeptVo deptVo) throws ElException {
        return (List<DeptVo>) list("com.inswave.cvt.SelectDept", deptVo);
    }

    /**
     * Select department with its employees
     * @param empVo Employee value object containing search criteria
     * @return List of departments with associated employees
     */
    public List<DeptVo> selectDeptWithEmps(EmpVo empVo) throws ElException {
        return (List<DeptVo>) list("com.inswave.cvt.SelectDeptWithEmps", empVo);
    }
} 