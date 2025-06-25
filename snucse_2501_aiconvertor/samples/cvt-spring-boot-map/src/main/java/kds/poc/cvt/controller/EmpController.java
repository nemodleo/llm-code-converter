package kds.poc.cvt.controller;

import java.util.List;
import java.util.Map;
import java.util.HashMap;
import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;
import kds.poc.cvt.service.EmpService;

@RestController
@RequestMapping("/api/employees")
@RequiredArgsConstructor
public class EmpController {

    private final EmpService svc;

    /** GET /api/employees?deptno=10 */
    @GetMapping public List<Map<String, Object>> list(Map<String, Object> filter) { return svc.list(filter); }

    /** POST /api/employees  (JSON body) */
    @PostMapping public Map<String, Object> create(@RequestBody Map<String, Object> vo) { return svc.save(vo); }

    /** PUT /api/employees/{id} */
    @PutMapping("/{id}") public void update(@PathVariable String id, @RequestBody Map<String, Object> vo) {
        vo.put("EMPNO", id);  svc.update(vo);
    }

    /** DELETE /api/employees/{id} */
    @DeleteMapping("/{id}") public void delete(@PathVariable String id) {
        Map<String, Object> vo = new HashMap<>(); vo.put("EMPNO", id); svc.delete(vo);
    }
}