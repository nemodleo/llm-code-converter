package kds.poc.cvt.mapper;

import java.util.List;
import org.apache.ibatis.annotations.Mapper;
import kds.poc.cvt.model.EmpVo;

@Mapper   // MyBatis will auto-implement this using the XML
public interface EmpMapper {
    int insertEmp(EmpVo vo);
    int updateEmp(EmpVo vo);
    int deleteEmp(EmpVo vo);
    List<EmpVo> selectEmp(EmpVo vo);
}