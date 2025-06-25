package kds.poc.cvt.service.impl;

import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;

import kds.poc.cvt.dao.CvtDAO;
import kds.poc.cvt.service.EmpService;

@Service
@RequiredArgsConstructor
@Transactional
public class EmpServiceImpl implements EmpService {

    private final CvtDAO cvtDAO;

    @Override
    public List<Map<String, Object>> list(Map<String, Object> filter) {
        return cvtDAO.selectEmp(filter);
    }

    @Override
    public Map<String, Object> save(Map<String, Object> vo) {
        cvtDAO.insertEmp(vo);
        return vo;
    }

    @Override
    public void update(Map<String, Object> vo) {
        cvtDAO.updateEmp(vo);
    }

    @Override
    public void delete(Map<String, Object> vo) {
        cvtDAO.deleteEmp(vo);
    }
}