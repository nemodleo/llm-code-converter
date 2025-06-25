package kds.poc.cvt.controller;

import java.util.List;
import java.util.Map;
import java.util.HashMap;
import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;
import kds.poc.cvt.model.FundVo;
import kds.poc.cvt.model.FundPerformanceVo;
import kds.poc.cvt.model.FundAnalysisResultVo;
import kds.poc.cvt.service.FundService;

@RestController
@RequestMapping("/api/funds")
@RequiredArgsConstructor
public class FundController {

    private final FundService fundService;

    /** GET /api/funds - 펀드 목록 조회 */
    @GetMapping 
    public List<Map<String, Object>> list(Map<String, Object> filter) { 
        return fundService.list(filter); 
    }

    /** GET /api/funds/{fundCode} - 특정 펀드 조회 */
    @GetMapping("/{fundCode}")
    public Map<String, Object> getByCode(@PathVariable String fundCode) {
        return fundService.getByCode(fundCode);
    }

    /** POST /api/funds - 펀드 생성 */
    @PostMapping 
    public Map<String, Object> create(@RequestBody Map<String, Object> vo) { 
        return fundService.save(vo); 
    }

    /** PUT /api/funds/{fundCode} - 펀드 수정 */
    @PutMapping("/{fundCode}") 
    public void update(@PathVariable String fundCode, @RequestBody Map<String, Object> vo) {
        vo.put("FUND_CODE", fundCode);
        fundService.update(vo);
    }

    /** DELETE /api/funds/{fundCode} - 펀드 삭제 */
    @DeleteMapping("/{fundCode}") 
    public void delete(@PathVariable String fundCode) {
        Map<String, Object> vo = new HashMap<>();
        vo.put("FUND_CODE", fundCode);
        fundService.delete(vo);
    }

    /** GET /api/funds/{fundCode}/performance - 펀드 성과 조회 */
    @GetMapping("/{fundCode}/performance")
    public List<Map<String, Object>> getPerformance(@PathVariable String fundCode) {
        return fundService.getPerformance(fundCode);
    }

    /** GET /api/funds/{fundCode}/performance/range - 기간별 펀드 성과 조회 */
    @GetMapping("/{fundCode}/performance/range")
    public List<Map<String, Object>> getPerformanceByDateRange(
            @PathVariable String fundCode,
            @RequestParam String startDate,
            @RequestParam String endDate) {
        return fundService.getPerformanceByDateRange(fundCode, startDate, endDate);
    }

    /** POST /api/funds/{fundCode}/performance - 펀드 성과 데이터 저장 */
    @PostMapping("/{fundCode}/performance")
    public void savePerformance(@PathVariable String fundCode, @RequestBody Map<String, Object> performanceVo) {
        performanceVo.put("FUND_CODE", fundCode);
        fundService.savePerformance(performanceVo);
    }

    /** GET /api/funds/top/{limit} - 상위 성과 펀드 조회 */
    @GetMapping("/top/{limit}")
    public List<Map<String, Object>> getTopPerformingFunds(@PathVariable int limit) {
        return fundService.getTopPerformingFunds(limit);
    }

    /** GET /api/funds/type/{fundType} - 펀드 유형별 조회 */
    @GetMapping("/type/{fundType}")
    public List<Map<String, Object>> getFundsByType(@PathVariable String fundType) {
        return fundService.getFundsByType(fundType);
    }

    /** GET /api/funds/risk/{riskLevel} - 위험도별 펀드 조회 */
    @GetMapping("/risk/{riskLevel}")
    public List<Map<String, Object>> getFundsByRiskLevel(@PathVariable String riskLevel) {
        return fundService.getFundsByRiskLevel(riskLevel);
    }

    /**
     * GET /api/funds/{fundCode}/analysis?period=1Y
     * 펀드 종합 분석 결과 반환
     */
    @GetMapping("/{fundCode}/analysis")
    public Map<String, Object> analyzeFund(@PathVariable String fundCode, @RequestParam(defaultValue = "1Y") String period) {
        return fundService.performComprehensiveFundAnalysis(fundCode, period);
    }
} 