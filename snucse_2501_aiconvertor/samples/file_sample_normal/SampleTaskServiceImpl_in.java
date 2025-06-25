package kds.poc.com.inswave.cvt.service.impl;

import java.util.List;
import java.util.Map;
import javax.annotation.Resource;
import org.springframework.stereotype.Service;

import kds.poc.com.inswave.cvt.service.SampleTaskService;
import kds.poc.com.inswave.cvt.dao.CvtDAO;

@Service("sampleTaskServiceImpl")
public class SampleTaskServiceImpl implements SampleTaskService {

    @Resource(name = "cvtDAO")
    private CvtDAO cvtDAO;

    public List<Map> selectEmpXDA(Map mp) throws Exception {
        return cvtDAO.selectEmp(mp);
    }

    public Object insertEmpXDA(Map mp) throws Exception {
        return cvtDAO.insertEmp(mp);
    }

    public void updateEmpXDA(Map mp) throws Exception {
        cvtDAO.updateEmp(mp);
    }

    public void deleteEmpXDA(Map mp) throws Exception {
        cvtDAO.deleteEmp(mp);
    }
} 