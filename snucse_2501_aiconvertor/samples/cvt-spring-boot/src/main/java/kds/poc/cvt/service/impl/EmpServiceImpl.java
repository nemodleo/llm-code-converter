package kds.poc.cvt.service.impl;

import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;

import kds.poc.cvt.dao.CvtDAO;
import kds.poc.cvt.model.EmpVo;
import kds.poc.cvt.service.EmpService;

@Service
@RequiredArgsConstructor
@Transactional
public class EmpServiceImpl implements EmpService {

    private final CvtDAO cvtDAO;

    @Override
    public List<EmpVo> list(EmpVo filter) {
        return cvtDAO.selectEmp(filter);
    }

    @Override
    public EmpVo save(EmpVo vo) {
        cvtDAO.insertEmp(vo);
        return vo;
    }

    @Override
    public void update(EmpVo vo) {
        cvtDAO.updateEmp(vo);
    }

    @Override
    public void delete(EmpVo vo) {
        cvtDAO.deleteEmp(vo);
    }
}