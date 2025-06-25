package kds.poc.cvt.mapper;

import java.util.List;
import java.util.Map;
import org.apache.ibatis.annotations.Mapper;

@Mapper   // MyBatis will auto-implement this using the XML
public interface EmpMapper {
    int insertEmp(Map<String, Object> vo);
    int updateEmp(Map<String, Object> vo);
    int deleteEmp(Map<String, Object> vo);
    List<Map<String, Object>> selectEmp(Map<String, Object> vo);
}