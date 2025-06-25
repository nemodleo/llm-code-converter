package kds.poc.com.inswave.cvt.dao;

import java.util.ArrayList;
import java.util.Map;

import org.springframework.stereotype.Repository;

import com.inswave.elfw.exception.ElException;

import kds.poc.base.cmmn.dao.BaseDefaultAbstractDAO;

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

	public int InsertEmp(Map mp) throws ElException {
		return (int) insert("com.inswave.cvt.InsertEmp", mp);
	}

	public int UpdateEmp(Map mp) throws ElException {
		return (int) update("com.inswave.cvt.UpdateEmp", mp);
	}

	public int DeleteEmp(Map mp) throws ElException {
		return (int) delete("com.inswave.cvt.DeleteEmp", mp);
	}


	public ArrayList<Map> SelectEmp(Map mp) throws ElException {
		return (ArrayList<Map>) list("com.inswave.cvt.SelectEmp", mp);
	}
}
