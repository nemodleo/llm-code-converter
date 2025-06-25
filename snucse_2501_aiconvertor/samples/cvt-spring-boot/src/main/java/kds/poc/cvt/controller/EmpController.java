package kds.poc.cvt.controller;

import java.util.List;
import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;
import kds.poc.cvt.model.EmpVo;
import kds.poc.cvt.service.EmpService;

@RestController
@RequestMapping("/api/employees")
@RequiredArgsConstructor
public class EmpController {

    private final EmpService svc;

    /** GET /api/employees?deptno=10 */
    @GetMapping public List<EmpVo> list(EmpVo filter) { return svc.list(filter); }

    /** POST /api/employees  (JSON body) */
    @PostMapping public EmpVo create(@RequestBody EmpVo vo) { return svc.save(vo); }

    /** PUT /api/employees/{id} */
    @PutMapping("/{id}") public void update(@PathVariable String id, @RequestBody EmpVo vo) {
        vo.setEmpno(id);  svc.update(vo);
    }

    /** DELETE /api/employees/{id} */
    @DeleteMapping("/{id}") public void delete(@PathVariable String id) {
        EmpVo vo = new EmpVo(); vo.setEmpno(id); svc.delete(vo);
    }
}