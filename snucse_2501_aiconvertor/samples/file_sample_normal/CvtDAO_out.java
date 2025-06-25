package kds.poc.com.inswave.cvt.dao;

import java.util.List;
import org.springframework.stereotype.Repository;
import com.inswave.elfw.exception.ElException;
import kds.poc.base.cmmn.dao.BaseDefaultAbstractDAO;
import kds.poc.com.inswave.cvt.vo.EmpVo;

/**  
 * @ClassSubJect DAO convert 
 * @Class Name : CvtDAO
 * @Description : Data Access Object for employee operations
 * 
 * Copyright Inswave (C) by Sampler All right reserved.
 */
@Repository("cvtDAO")
public class CvtDAO extends BaseDefaultAbstractDAO {

    /**
     * Insert employee information
     */
    public int insertEmp(EmpVo empVo) throws ElException {
        return (int) insert("com.inswave.cvt.InsertEmp", empVo);
    }

    /**
     * Update employee information
     */
    public int updateEmp(EmpVo empVo) throws ElException {
        return (int) update("com.inswave.cvt.UpdateEmp", empVo);
    }

    /**
     * Delete employee information
     */
    public int deleteEmp(EmpVo empVo) throws ElException {
        return (int) delete("com.inswave.cvt.DeleteEmp", empVo);
    }

    /**
     * Select employee information
     */
    public List<EmpVo> selectEmp(EmpVo empVo) throws ElException {
        return (List<EmpVo>) list("com.inswave.cvt.SelectEmp", empVo);
    }
} 