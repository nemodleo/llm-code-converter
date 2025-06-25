package kds.poc.cvt.service;

import java.util.List;
import kds.poc.cvt.model.EmpVo;

public interface EmpService {
    List<EmpVo> list(EmpVo filter);
    EmpVo save(EmpVo vo);
    void update(EmpVo vo);
    void delete(EmpVo vo);
}