package kds.poc.com.inswave.cvt.dao;

import java.util.ArrayList;
import java.util.Map;

import org.springframework.stereotype.Repository;

import com.inswave.elfw.exception.ElException;

import kds.poc.base.cmmn.dao.BaseDefaultAbstractDAO;
import java.util.List;
import kds.poc.com.inswave.cvt.vo.EmpVo;


/**  
 * @ClassSubJect DAO convert 
 * @Class Name : CvtDAO
 * @ConvertTime : 2021-09-23 13:05:54 
 * @Description : 
 * 
 *  Copyright Inswave (C) by Sampler All right reserved.
 */
@Repository("cvtDAO")
public class CvtDAO extends BaseDefaultAbstractDAO {

	public int InsertEmp(EmpVo empVo) throws ElException {
		return (int) insert("com.inswave.cvt.InsertEmp", empVo);
	}

	/**
	 * 사원정보를 갱신한다.
	 * @param empVo 사원정보 EmpVo
	 * @return 갱신된 행 수
	 * @throws ElException
	 */
	public int UpdateEmp(EmpVo empVo) throws ElException {
		return (int) update("com.inswave.cvt.UpdateEmp", empVo);
	}

	public int DeleteEmp(EmpVo empVo) throws ElException {
		return (int) delete("com.inswave.cvt.DeleteEmp", empVo);
	}


	public List<EmpVo> SelectEmp(EmpVo empVo) throws ElException {
		return (List<EmpVo>) list("com.inswave.cvt.SelectEmp", empVo);
	}
}
