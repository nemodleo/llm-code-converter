package kds.poc.cvt.service;

import java.util.List;
import java.util.Map;

public interface EmpService {
    List<Map<String, Object>> list(Map<String, Object> filter);
    Map<String, Object> save(Map<String, Object> vo);
    void update(Map<String, Object> vo);
    void delete(Map<String, Object> vo);
}