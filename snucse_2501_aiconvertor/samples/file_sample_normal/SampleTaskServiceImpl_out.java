package kds.poc.com.inswave.cvt.service.impl;

import java.util.List;
import javax.annotation.Resource;
import org.springframework.stereotype.Service;

import kds.poc.com.inswave.cvt.service.SampleTaskService;
import kds.poc.com.inswave.cvt.vo.EmpVo;
import kds.poc.com.inswave.cvt.dao.CvtDAO;

/**
 * Service implementation for employee management operations.
 */
@Service("sampleTaskServiceImpl")
public class SampleTaskServiceImpl implements SampleTaskService {

    @Resource(name = "cvtDAO")
    private CvtDAO cvtDAO;

    /**
     * Select employee information
     */
    public List<EmpVo> selectEmpXDA(EmpVo empVo) throws Exception {
        return cvtDAO.selectEmp(empVo);
    }

    /**
     * Insert employee information
     */
    public Object insertEmpXDA(EmpVo empVo) throws Exception {
        return cvtDAO.insertEmp(empVo);
    }

    /**
     * Update employee information
     */
    public void updateEmpXDA(EmpVo empVo) throws Exception {
        cvtDAO.updateEmp(empVo);
    }

    /**
     * Delete employee information
     */
    public void deleteEmpXDA(EmpVo empVo) throws Exception {
        cvtDAO.deleteEmp(empVo);
    }
} 