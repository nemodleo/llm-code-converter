package kds.poc.com.inswave.cvt.dao;

import java.util.ArrayList;
import java.util.Map;
import org.springframework.stereotype.Repository;
import com.inswave.elfw.exception.ElException;
import kds.poc.base.cmmn.dao.BaseDefaultAbstractDAO;

/**  
 * @ClassSubJect DAO convert 
 * @Class Name : DeptDAO
 * @Description : Department Data Access Object
 * 
 * Copyright Inswave (C) by Sampler All right reserved.
 */
@Repository("deptDAO")
public class DeptDAO extends BaseDefaultAbstractDAO {

    public int insertDept(Map mp) throws ElException {
        return (int) insert("com.inswave.cvt.InsertDept", mp);
    }

    public int updateDept(Map mp) throws ElException {
        return (int) update("com.inswave.cvt.UpdateDept", mp);
    }

    public int deleteDept(Map mp) throws ElException {
        return (int) delete("com.inswave.cvt.DeleteDept", mp);
    }

    public ArrayList<Map> selectDept(Map mp) throws ElException {
        return (ArrayList<Map>) list("com.inswave.cvt.SelectDept", mp);
    }

    public ArrayList<Map> selectDeptWithEmps(Map mp) throws ElException {
        return (ArrayList<Map>) list("com.inswave.cvt.SelectDeptWithEmps", mp);
    }
} 