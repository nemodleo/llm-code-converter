#!/usr/bin/env python3
"""
DB 연동용 Map 파라미터 전달 객체 예제 프로젝트 생성기
DAO와 서비스 간의 데이터 전달에 Map을 사용하는 패턴
"""

import os
from pathlib import Path

def create_db_map_project(project_name="db-map-example"):
    """DB 연동용 Map 사용 예제 프로젝트 생성"""
    
    project_root = Path(project_name)
    src_main_java = project_root / "src" / "main" / "java" / "com" / "example"
    
    # 디렉토리 구조 생성
    directories = [
        src_main_java / "service",
        src_main_java / "dao", 
        src_main_java / "controller",
        src_main_java / "model",
        project_root / "src" / "test" / "java" / "com" / "example"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    # 1. 사용자 DAO - DB 연동 계층
    user_dao = """package com.example.dao;

import java.util.*;
import java.sql.*;

public class UserDao {
    
    /**
     * 사용자 목록 조회 - 검색 조건을 Map으로 받음
     */
    public List<Map<String, Object>> selectUserList(Map<String, Object> params) {
        List<Map<String, Object>> userList = new ArrayList<>();
        
        try {
            StringBuilder sql = new StringBuilder();
            sql.append("SELECT user_id, name, email, age, dept_code, status, ");
            sql.append("       created_date, updated_date ");
            sql.append("FROM users WHERE 1=1 ");
            
            // 동적 쿼리 조건
            if (params.get("name") != null) {
                sql.append("AND name LIKE CONCAT('%', ?, '%') ");
            }
            if (params.get("dept_code") != null) {
                sql.append("AND dept_code = ? ");
            }
            if (params.get("status") != null) {
                sql.append("AND status = ? ");
            }
            if (params.get("min_age") != null) {
                sql.append("AND age >= ? ");
            }
            if (params.get("max_age") != null) {
                sql.append("AND age <= ? ");
            }
            
            // 정렬 조건
            String sortBy = (String) params.get("sort_by");
            if (sortBy != null) {
                sql.append("ORDER BY ").append(sortBy);
                String sortOrder = (String) params.get("sort_order");
                if ("DESC".equalsIgnoreCase(sortOrder)) {
                    sql.append(" DESC");
                }
            }
            
            // 페이징
            if (params.get("limit") != null) {
                sql.append(" LIMIT ?");
                if (params.get("offset") != null) {
                    sql.append(" OFFSET ?");
                }
            }
            
            System.out.println("실행 SQL: " + sql.toString());
            System.out.println("파라미터: " + params);
            
            // 실제 DB 연동 시뮬레이션 (샘플 데이터 반환)
            userList = createSampleUserData(params);
            
        } catch (Exception e) {
            System.err.println("사용자 목록 조회 오류: " + e.getMessage());
        }
        
        return userList;
    }
    
    /**
     * 사용자 상세 조회
     */
    public Map<String, Object> selectUserById(Map<String, Object> params) {
        try {
            String sql = "SELECT * FROM users WHERE user_id = ?";
            System.out.println("실행 SQL: " + sql);
            System.out.println("파라미터: " + params);
            
            // 샘플 데이터 반환
            Map<String, Object> user = new HashMap<>();
            user.put("user_id", params.get("user_id"));
            user.put("name", "김철수");
            user.put("email", "kim@company.com");
            user.put("age", 30);
            user.put("dept_code", "DEV001");
            user.put("position", "Senior Developer");
            user.put("salary", 5000000);
            user.put("status", "A");
            user.put("created_date", new Date());
            user.put("updated_date", new Date());
            
            return user;
            
        } catch (Exception e) {
            System.err.println("사용자 조회 오류: " + e.getMessage());
            return null;
        }
    }
    
    /**
     * 사용자 등록
     */
    public int insertUser(Map<String, Object> params) {
        try {
            String sql = "INSERT INTO users (user_id, name, email, age, dept_code, " +
                        "position, salary, status, created_date) " +
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, NOW())";
            
            System.out.println("실행 SQL: " + sql);
            System.out.println("파라미터: " + params);
            
            // 등록 성공 시뮬레이션
            return 1;
            
        } catch (Exception e) {
            System.err.println("사용자 등록 오류: " + e.getMessage());
            return 0;
        }
    }
    
    /**
     * 사용자 정보 수정
     */
    public int updateUser(Map<String, Object> params) {
        try {
            StringBuilder sql = new StringBuilder();
            sql.append("UPDATE users SET updated_date = NOW() ");
            
            if (params.get("name") != null) {
                sql.append(", name = ? ");
            }
            if (params.get("email") != null) {
                sql.append(", email = ? ");
            }
            if (params.get("age") != null) {
                sql.append(", age = ? ");
            }
            if (params.get("dept_code") != null) {
                sql.append(", dept_code = ? ");
            }
            if (params.get("position") != null) {
                sql.append(", position = ? ");
            }
            if (params.get("salary") != null) {
                sql.append(", salary = ? ");
            }
            if (params.get("status") != null) {
                sql.append(", status = ? ");
            }
            
            sql.append("WHERE user_id = ?");
            
            System.out.println("실행 SQL: " + sql.toString());
            System.out.println("파라미터: " + params);
            
            return 1;
            
        } catch (Exception e) {
            System.err.println("사용자 수정 오류: " + e.getMessage());
            return 0;
        }
    }
    
    /**
     * 사용자 삭제 (논리 삭제)
     */
    public int deleteUser(Map<String, Object> params) {
        try {
            String sql = "UPDATE users SET status = 'D', updated_date = NOW() WHERE user_id = ?";
            
            System.out.println("실행 SQL: " + sql);
            System.out.println("파라미터: " + params);
            
            return 1;
            
        } catch (Exception e) {
            System.err.println("사용자 삭제 오류: " + e.getMessage());
            return 0;
        }
    }
    
    /**
     * 부서별 사용자 통계
     */
    public List<Map<String, Object>> selectUserStatsByDept(Map<String, Object> params) {
        try {
            StringBuilder sql = new StringBuilder();
            sql.append("SELECT dept_code, COUNT(*) as user_count, ");
            sql.append("       AVG(age) as avg_age, AVG(salary) as avg_salary ");
            sql.append("FROM users WHERE status = 'A' ");
            
            if (params.get("start_date") != null) {
                sql.append("AND created_date >= ? ");
            }
            if (params.get("end_date") != null) {
                sql.append("AND created_date <= ? ");
            }
            
            sql.append("GROUP BY dept_code ORDER BY user_count DESC");
            
            System.out.println("실행 SQL: " + sql.toString());
            System.out.println("파라미터: " + params);
            
            // 샘플 통계 데이터
            List<Map<String, Object>> stats = new ArrayList<>();
            
            Map<String, Object> devStats = new HashMap<>();
            devStats.put("dept_code", "DEV001");
            devStats.put("user_count", 15);
            devStats.put("avg_age", 32.5);
            devStats.put("avg_salary", 5200000.0);
            stats.add(devStats);
            
            Map<String, Object> salesStats = new HashMap<>();
            salesStats.put("dept_code", "SALES01");
            salesStats.put("user_count", 12);
            salesStats.put("avg_age", 29.8);
            salesStats.put("avg_salary", 4800000.0);
            stats.add(salesStats);
            
            return stats;
            
        } catch (Exception e) {
            System.err.println("부서별 통계 조회 오류: " + e.getMessage());
            return new ArrayList<>();
        }
    }
    
    private List<Map<String, Object>> createSampleUserData(Map<String, Object> params) {
        List<Map<String, Object>> users = new ArrayList<>();
        
        // 샘플 사용자 1
        Map<String, Object> user1 = new HashMap<>();
        user1.put("user_id", "USR001");
        user1.put("name", "김개발");
        user1.put("email", "kim.dev@company.com");
        user1.put("age", 28);
        user1.put("dept_code", "DEV001");
        user1.put("position", "Developer");
        user1.put("salary", 4500000);
        user1.put("status", "A");
        user1.put("created_date", new Date());
        users.add(user1);
        
        // 샘플 사용자 2
        Map<String, Object> user2 = new HashMap<>();
        user2.put("user_id", "USR002");
        user2.put("name", "이기획");
        user2.put("email", "lee.plan@company.com");
        user2.put("age", 35);
        user2.put("dept_code", "PLAN01");
        user2.put("position", "Planner");
        user2.put("salary", 5200000);
        user2.put("status", "A");
        user2.put("created_date", new Date());
        users.add(user2);
        
        return users;
    }
}
"""

    # 2. 부서 DAO
    dept_dao = """package com.example.dao;

import java.util.*;

public class DeptDao {
    
    /**
     * 부서 목록 조회
     */
    public List<Map<String, Object>> selectDeptList(Map<String, Object> params) {
        try {
            StringBuilder sql = new StringBuilder();
            sql.append("SELECT dept_code, dept_name, parent_dept_code, ");
            sql.append("       manager_id, budget, status ");
            sql.append("FROM departments WHERE 1=1 ");
            
            if (params.get("status") != null) {
                sql.append("AND status = ? ");
            }
            if (params.get("parent_dept_code") != null) {
                sql.append("AND parent_dept_code = ? ");
            }
            
            System.out.println("실행 SQL: " + sql.toString());
            System.out.println("파라미터: " + params);
            
            // 샘플 부서 데이터
            List<Map<String, Object>> deptList = new ArrayList<>();
            
            Map<String, Object> dept1 = new HashMap<>();
            dept1.put("dept_code", "DEV001");
            dept1.put("dept_name", "개발팀");
            dept1.put("parent_dept_code", "IT001");
            dept1.put("manager_id", "MGR001");
            dept1.put("budget", 100000000);
            dept1.put("status", "A");
            deptList.add(dept1);
            
            Map<String, Object> dept2 = new HashMap<>();
            dept2.put("dept_code", "SALES01");
            dept2.put("dept_name", "영업팀");
            dept2.put("parent_dept_code", "BIZ001");
            dept2.put("manager_id", "MGR002");
            dept2.put("budget", 80000000);
            dept2.put("status", "A");
            deptList.add(dept2);
            
            return deptList;
            
        } catch (Exception e) {
            System.err.println("부서 목록 조회 오류: " + e.getMessage());
            return new ArrayList<>();
        }
    }
    
    /**
     * 부서별 예산 사용 현황
     */
    public List<Map<String, Object>> selectBudgetUsage(Map<String, Object> params) {
        try {
            String sql = "SELECT d.dept_code, d.dept_name, d.budget, " +
                        "COALESCE(SUM(e.amount), 0) as used_amount, " +
                        "(d.budget - COALESCE(SUM(e.amount), 0)) as remaining_amount " +
                        "FROM departments d " +
                        "LEFT JOIN expenses e ON d.dept_code = e.dept_code " +
                        "WHERE d.status = 'A' " +
                        "AND e.expense_date BETWEEN ? AND ? " +
                        "GROUP BY d.dept_code, d.dept_name, d.budget";
            
            System.out.println("실행 SQL: " + sql);
            System.out.println("파라미터: " + params);
            
            // 샘플 예산 데이터
            List<Map<String, Object>> budgetUsage = new ArrayList<>();
            
            Map<String, Object> usage1 = new HashMap<>();
            usage1.put("dept_code", "DEV001");
            usage1.put("dept_name", "개발팀");
            usage1.put("budget", 100000000);
            usage1.put("used_amount", 75000000);
            usage1.put("remaining_amount", 25000000);
            budgetUsage.add(usage1);
            
            return budgetUsage;
            
        } catch (Exception e) {
            System.err.println("예산 현황 조회 오류: " + e.getMessage());
            return new ArrayList<>();
        }
    }
}
"""

    # 3. 프로젝트 DAO
    project_dao = """package com.example.dao;

import java.util.*;

public class ProjectDao {
    
    /**
     * 프로젝트 목록 조회
     */
    public List<Map<String, Object>> selectProjectList(Map<String, Object> params) {
        try {
            StringBuilder sql = new StringBuilder();
            sql.append("SELECT project_id, project_name, dept_code, ");
            sql.append("       start_date, end_date, budget, status, ");
            sql.append("       progress_rate, manager_id ");
            sql.append("FROM projects WHERE 1=1 ");
            
            if (params.get("dept_code") != null) {
                sql.append("AND dept_code = ? ");
            }
            if (params.get("status") != null) {
                sql.append("AND status = ? ");
            }
            if (params.get("start_date") != null) {
                sql.append("AND start_date >= ? ");
            }
            if (params.get("end_date") != null) {
                sql.append("AND end_date <= ? ");
            }
            
            System.out.println("실행 SQL: " + sql.toString());
            System.out.println("파라미터: " + params);
            
            // 샘플 프로젝트 데이터
            List<Map<String, Object>> projects = new ArrayList<>();
            
            Map<String, Object> project1 = new HashMap<>();
            project1.put("project_id", "PRJ001");
            project1.put("project_name", "신규 쇼핑몰 개발");
            project1.put("dept_code", "DEV001");
            project1.put("start_date", "2024-01-01");
            project1.put("end_date", "2024-06-30");
            project1.put("budget", 50000000);
            project1.put("status", "진행중");
            project1.put("progress_rate", 75);
            project1.put("manager_id", "USR001");
            projects.add(project1);
            
            return projects;
            
        } catch (Exception e) {
            System.err.println("프로젝트 목록 조회 오류: " + e.getMessage());
            return new ArrayList<>();
        }
    }
    
    /**
     * 프로젝트 참여자 조회
     */
    public List<Map<String, Object>> selectProjectMembers(Map<String, Object> params) {
        try {
            String sql = "SELECT pm.project_id, pm.user_id, u.name, u.position, " +
                        "pm.role, pm.join_date, pm.allocation_rate " +
                        "FROM project_members pm " +
                        "JOIN users u ON pm.user_id = u.user_id " +
                        "WHERE pm.project_id = ? " +
                        "ORDER BY pm.join_date";
            
            System.out.println("실행 SQL: " + sql);
            System.out.println("파라미터: " + params);
            
            // 샘플 참여자 데이터
            List<Map<String, Object>> members = new ArrayList<>();
            
            Map<String, Object> member1 = new HashMap<>();
            member1.put("project_id", params.get("project_id"));
            member1.put("user_id", "USR001");
            member1.put("name", "김개발");
            member1.put("position", "Senior Developer");
            member1.put("role", "팀장");
            member1.put("join_date", "2024-01-01");
            member1.put("allocation_rate", 100);
            members.add(member1);
            
            return members;
            
        } catch (Exception e) {
            System.err.println("프로젝트 참여자 조회 오류: " + e.getMessage());
            return new ArrayList<>();
        }
    }
}
"""

    # 4. 사용자 서비스
    user_service = """package com.example.service;

import com.example.dao.UserDao;
import java.util.*;

public class UserService {
    private UserDao userDao;
    
    public UserService() {
        this.userDao = new UserDao();
    }
    
    /**
     * 사용자 목록 조회 (검색 조건 포함)
     */
    public List<Map<String, Object>> getUserList(Map<String, Object> searchParams) {
        System.out.println("[UserService] 사용자 목록 조회 요청");
        System.out.println("검색 조건: " + searchParams);
        
        // 기본값 설정
        Map<String, Object> params = new HashMap<>(searchParams);
        if (params.get("limit") == null) {
            params.put("limit", 20);  // 기본 20개
        }
        if (params.get("offset") == null) {
            params.put("offset", 0);   // 기본 0부터
        }
        if (params.get("sort_by") == null) {
            params.put("sort_by", "created_date");  // 기본 정렬
            params.put("sort_order", "DESC");
        }
        
        return userDao.selectUserList(params);
    }
    
    /**
     * 사용자 상세 정보 조회
     */
    public Map<String, Object> getUserDetail(String userId) {
        System.out.println("[UserService] 사용자 상세 조회: " + userId);
        
        Map<String, Object> params = new HashMap<>();
        params.put("user_id", userId);
        
        return userDao.selectUserById(params);
    }
    
    /**
     * 사용자 등록
     */
    public boolean createUser(Map<String, Object> userInfo) {
        System.out.println("[UserService] 사용자 등록 요청");
        System.out.println("등록 정보: " + userInfo);
        
        // 필수값 검증
        if (userInfo.get("name") == null || userInfo.get("email") == null) {
            throw new IllegalArgumentException("필수 정보가 누락되었습니다.");
        }
        
        // 사용자 ID 생성
        String userId = "USR" + System.currentTimeMillis();
        userInfo.put("user_id", userId);
        
        // 기본값 설정
        if (userInfo.get("status") == null) {
            userInfo.put("status", "A");  // 활성
        }
        
        int result = userDao.insertUser(userInfo);
        return result > 0;
    }
    
    /**
     * 사용자 정보 수정
     */
    public boolean updateUser(String userId, Map<String, Object> updateInfo) {
        System.out.println("[UserService] 사용자 정보 수정: " + userId);
        System.out.println("수정 정보: " + updateInfo);
        
        Map<String, Object> params = new HashMap<>(updateInfo);
        params.put("user_id", userId);
        
        int result = userDao.updateUser(params);
        return result > 0;
    }
    
    /**
     * 부서별 사용자 통계
     */
    public List<Map<String, Object>> getDeptUserStats(Map<String, Object> dateRange) {
        System.out.println("[UserService] 부서별 사용자 통계 조회");
        System.out.println("기간: " + dateRange);
        
        return userDao.selectUserStatsByDept(dateRange);
    }
    
    /**
     * 활성 사용자만 조회
     */
    public List<Map<String, Object>> getActiveUsers() {
        System.out.println("[UserService] 활성 사용자 목록 조회");
        
        Map<String, Object> params = new HashMap<>();
        params.put("status", "A");
        params.put("sort_by", "name");
        params.put("sort_order", "ASC");
        
        return userDao.selectUserList(params);
    }
    
    /**
     * 부서별 사용자 조회
     */
    public List<Map<String, Object>> getUsersByDept(String deptCode) {
        System.out.println("[UserService] 부서별 사용자 조회: " + deptCode);
        
        Map<String, Object> params = new HashMap<>();
        params.put("dept_code", deptCode);
        params.put("status", "A");
        
        return userDao.selectUserList(params);
    }
}
"""

    # 5. 부서 서비스
    dept_service = """package com.example.service;

import com.example.dao.DeptDao;
import com.example.dao.UserDao;
import java.util.*;

public class DeptService {
    private DeptDao deptDao;
    private UserDao userDao;
    
    public DeptService() {
        this.deptDao = new DeptDao();
        this.userDao = new UserDao();
    }
    
    /**
     * 부서 목록 조회
     */
    public List<Map<String, Object>> getDeptList(Map<String, Object> searchParams) {
        System.out.println("[DeptService] 부서 목록 조회");
        System.out.println("검색 조건: " + searchParams);
        
        Map<String, Object> params = new HashMap<>(searchParams);
        if (params.get("status") == null) {
            params.put("status", "A");  // 기본적으로 활성 부서만
        }
        
        return deptDao.selectDeptList(params);
    }
    
    /**
     * 부서별 예산 사용 현황
     */
    public List<Map<String, Object>> getBudgetUsage(String startDate, String endDate) {
        System.out.println("[DeptService] 부서별 예산 사용 현황 조회");
        System.out.println("기간: " + startDate + " ~ " + endDate);
        
        Map<String, Object> params = new HashMap<>();
        params.put("start_date", startDate);
        params.put("end_date", endDate);
        
        return deptDao.selectBudgetUsage(params);
    }
    
    /**
     * 부서별 상세 정보 (부서 정보 + 소속 사용자 + 예산)
     */
    public Map<String, Object> getDeptDetailInfo(String deptCode) {
        System.out.println("[DeptService] 부서 상세 정보 조회: " + deptCode);
        
        Map<String, Object> result = new HashMap<>();
        
        // 부서 기본 정보
        Map<String, Object> deptParams = new HashMap<>();
        deptParams.put("dept_code", deptCode);
        List<Map<String, Object>> deptList = deptDao.selectDeptList(deptParams);
        if (!deptList.isEmpty()) {
            result.put("dept_info", deptList.get(0));
        }
        
        // 소속 사용자 목록
        Map<String, Object> userParams = new HashMap<>();
        userParams.put("dept_code", deptCode);
        userParams.put("status", "A");
        List<Map<String, Object>> userList = userDao.selectUserList(userParams);
        result.put("user_list", userList);
        result.put("user_count", userList.size());
        
        // 부서 통계
        Map<String, Object> statsParams = new HashMap<>();
        List<Map<String, Object>> stats = userDao.selectUserStatsByDept(statsParams);
        for (Map<String, Object> stat : stats) {
            if (deptCode.equals(stat.get("dept_code"))) {
                result.put("dept_stats", stat);
                break;
            }
        }
        
        return result;
    }
}
"""

    # 6. 프로젝트 서비스
    project_service = """package com.example.service;

import com.example.dao.ProjectDao;
import com.example.dao.UserDao;
import java.util.*;

public class ProjectService {
    private ProjectDao projectDao;
    private UserDao userDao;
    
    public ProjectService() {
        this.projectDao = new ProjectDao();
        this.userDao = new UserDao();
    }
    
    /**
     * 프로젝트 목록 조회
     */
    public List<Map<String, Object>> getProjectList(Map<String, Object> searchParams) {
        System.out.println("[ProjectService] 프로젝트 목록 조회");
        System.out.println("검색 조건: " + searchParams);
        
        return projectDao.selectProjectList(searchParams);
    }
    
    /**
     * 부서별 진행 중인 프로젝트 조회
     */
    public List<Map<String, Object>> getActiveProjectsByDept(String deptCode) {
        System.out.println("[ProjectService] 부서별 진행 프로젝트 조회: " + deptCode);
        
        Map<String, Object> params = new HashMap<>();
        params.put("dept_code", deptCode);
        params.put("status", "진행중");
        
        return projectDao.selectProjectList(params);
    }
    
    /**
     * 프로젝트 상세 정보 (프로젝트 정보 + 참여자)
     */
    public Map<String, Object> getProjectDetail(String projectId) {
        System.out.println("[ProjectService] 프로젝트 상세 조회: " + projectId);
        
        Map<String, Object> result = new HashMap<>();
        
        // 프로젝트 기본 정보
        Map<String, Object> projectParams = new HashMap<>();
        projectParams.put("project_id", projectId);
        List<Map<String, Object>> projectList = projectDao.selectProjectList(projectParams);
        if (!projectList.isEmpty()) {
            result.put("project_info", projectList.get(0));
        }
        
        // 프로젝트 참여자 목록
        Map<String, Object> memberParams = new HashMap<>();
        memberParams.put("project_id", projectId);
        List<Map<String, Object>> members = projectDao.selectProjectMembers(memberParams);
        result.put("members", members);
        result.put("member_count", members.size());
        
        // 참여자별 상세 정보 추가
        List<Map<String, Object>> memberDetails = new ArrayList<>();
        for (Map<String, Object> member : members) {
            String userId = (String) member.get("user_id");
            Map<String, Object> userParams = new HashMap<>();
            userParams.put("user_id", userId);
            Map<String, Object> userDetail = userDao.selectUserById(userParams);
            
            Map<String, Object> memberDetail = new HashMap<>();
            memberDetail.put("user_id", member.get("user_id"));
            memberDetail.put("name", member.get("name"));
            memberDetail.put("position", member.get("position"));
            memberDetail.put("role", member.get("role"));
            memberDetail.put("allocation_rate", member.get("allocation_rate"));
            memberDetail.put("email", userDetail != null ? userDetail.get("email") : null);
            memberDetail.put("dept_code", userDetail != null ? userDetail.get("dept_code") : null);
            
            memberDetails.add(memberDetail);
        }
        result.put("member_details", memberDetails);
        
        return result;
    }
    
    /**
     * 기간별 프로젝트 현황
     */
    public Map<String, Object> getProjectStatusByPeriod(String startDate, String endDate) {
        System.out.println("[ProjectService] 기간별 프로젝트 현황 조회");
        System.out.println("기간: " + startDate + " ~ " + endDate);
        
        Map<String, Object> params = new HashMap<>();
        params.put("start_date", startDate);
        params.put("end_date", endDate);
        
        List<Map<String, Object>> projects = projectDao.selectProjectList(params);
        
        // 상태별 통계 계산
        Map<String, Object> result = new HashMap<>();
        Map<String, Integer> statusCount = new HashMap<>();
        int totalBudget = 0;
        double avgProgress = 0.0;
        
        for (Map<String, Object> project : projects) {
            String status = (String) project.get("status");
            statusCount.put(status, statusCount.getOrDefault(status, 0) + 1);
            
            Integer budget = (Integer) project.get("budget");
            if (budget != null) {
                totalBudget += budget;
            }
            
            Integer progress = (Integer) project.get("progress_rate");
            if (progress != null) {
                avgProgress += progress;
            }
        }
        
        if (!projects.isEmpty()) {
            avgProgress = avgProgress / projects.size();
        }
        
        result.put("project_list", projects);
        result.put("total_count", projects.size());
        result.put("status_statistics", statusCount);
        result.put("total_budget", totalBudget);
        result.put("average_progress", avgProgress);
        
        return result;
    }
}
"""

    # 7. 컨트롤러
    controller = """package com.example.controller;

import com.example.service.*;
import java.util.*;

public class MainController {
    private UserService userService;
    private DeptService deptService;
    private ProjectService projectService;
    
    public MainController() {
        this.userService = new UserService();
        this.deptService = new DeptService();
        this.projectService = new ProjectService();
    }
    
    /**
     * 사용자 검색 API
     */
    public Map<String, Object> searchUsers(Map<String, Object> requestParams) {
        System.out.println("[Controller] 사용자 검색 API 호출");
        System.out.println("요청 파라미터: " + requestParams);
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            // 검색 조건 구성
            Map<String, Object> searchParams = new HashMap<>();
            
            if (requestParams.get("name") != null) {
                searchParams.put("name", requestParams.get("name"));
            }
            if (requestParams.get("dept_code") != null) {
                searchParams.put("dept_code", requestParams.get("dept_code"));
            }
            if (requestParams.get("min_age") != null) {
                searchParams.put("min_age", requestParams.get("min_age"));
            }
            if (requestParams.get("max_age") != null) {
                searchParams.put("max_age", requestParams.get("max_age"));
            }
            
            // 페이징 정보
            if (requestParams.get("page") != null) {
                int page = (Integer) requestParams.get("page");
                int size = requestParams.get("size") != null ? (Integer) requestParams.get("size") : 10;
                searchParams.put("limit", size);
                searchParams.put("offset", (page - 1) * size);
            }
            
            List<Map<String, Object>> users = userService.getUserList(searchParams);
            
            response.put("success", true);
            response.put("data", users);
            response.put("count", users.size());
            
        } catch (Exception e) {
            response.put("success", false);
            response.put("error", e.getMessage());
        }
        
        return response;
    }
    
    /**
     * 부서 정보 대시보드 API
     */
    public Map<String, Object> getDeptDashboard(Map<String, Object> requestParams) {
        System.out.println("[Controller] 부서 대시보드 API 호출");
        System.out.println("요청 파라미터: " + requestParams);
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            String deptCode = (String) requestParams.get("dept_code");
            
            // 부서 상세 정보
            Map<String, Object> deptDetail = deptService.getDeptDetailInfo(deptCode);
            
            // 부서의 진행 중인 프로젝트
            List<Map<String, Object>> activeProjects = projectService.getActiveProjectsByDept(deptCode);
            
            // 응답 구성
            response.put("success", true);
            response.put("dept_info", deptDetail.get("dept_info"));
            response.put("user_count", deptDetail.get("user_count"));
            response.put("dept_stats", deptDetail.get("dept_stats"));
            response.put("active_projects", activeProjects);
            response.put("project_count", activeProjects.size());
            
        } catch (Exception e) {
            response.put("success", false);
            response.put("error", e.getMessage());
        }
        
        return response;
    }
    
    /**
     * 프로젝트 현황 보고서 API
     */
    public Map<String, Object> getProjectReport(Map<String, Object> requestParams) {
        System.out.println("[Controller] 프로젝트 현황 보고서 API 호출");
        System.out.println("요청 파라미터: " + requestParams);
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            String startDate = (String) requestParams.get("start_date");
            String endDate = (String) requestParams.get("end_date");
            String deptCode = (String) requestParams.get("dept_code");
            
            Map<String, Object> reportParams = new HashMap<>();
            reportParams.put("start_date", startDate);
            reportParams.put("end_date", endDate);
            if (deptCode != null) {
                reportParams.put("dept_code", deptCode);
            }
            
            // 프로젝트 현황 조회
            Map<String, Object> projectStatus = projectService.getProjectStatusByPeriod(startDate, endDate);
            
            // 부서별 사용자 통계
            Map<String, Object> statsParams = new HashMap<>();
            statsParams.put("start_date", startDate);
            statsParams.put("end_date", endDate);
            List<Map<String, Object>> deptStats = userService.getDeptUserStats(statsParams);
            
            response.put("success", true);
            response.put("period", Map.of("start_date", startDate, "end_date", endDate));
            response.put("project_status", projectStatus);
            response.put("dept_statistics", deptStats);
            response.put("generated_at", new Date());
            
        } catch (Exception e) {
            response.put("success", false);
            response.put("error", e.getMessage());
        }
        
        return response;
    }
    
    /**
     * 사용자 등록 API
     */
    public Map<String, Object> createUser(Map<String, Object> requestParams) {
        System.out.println("[Controller] 사용자 등록 API 호출");
        System.out.println("요청 파라미터: " + requestParams);
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            // 필수 필드 검증
            if (requestParams.get("name") == null || requestParams.get("email") == null) {
                response.put("success", false);
                response.put("error", "필수 필드가 누락되었습니다. (name, email)");
                return response;
            }
            
            // 사용자 정보 구성
            Map<String, Object> userInfo = new HashMap<>();
            userInfo.put("name", requestParams.get("name"));
            userInfo.put("email", requestParams.get("email"));
            userInfo.put("age", requestParams.get("age"));
            userInfo.put("dept_code", requestParams.get("dept_code"));
            userInfo.put("position", requestParams.get("position"));
            userInfo.put("salary", requestParams.get("salary"));
            
            boolean success = userService.createUser(userInfo);
            
            if (success) {
                response.put("success", true);
                response.put("message", "사용자가 성공적으로 등록되었습니다.");
                response.put("user_id", userInfo.get("user_id"));
            } else {
                response.put("success", false);
                response.put("error", "사용자 등록에 실패했습니다.");
            }
            
        } catch (Exception e) {
            response.put("success", false);
            response.put("error", e.getMessage());
        }
        
        return response;
    }
}
"""

    # 8. 메인 애플리케이션
    main_app = """package com.example;

import com.example.controller.MainController;
import com.example.service.*;
import java.util.*;

public class Application {
    public static void main(String[] args) {
        System.out.println("=== DB 연동용 Map 파라미터 예제 시스템 ===");
        
        MainController controller = new MainController();
        
        // 1. 사용자 검색 테스트
        System.out.println("\\n1. 사용자 검색 테스트");
        Map<String, Object> searchParams = new HashMap<>();
        searchParams.put("name", "김");
        searchParams.put("dept_code", "DEV001");
        searchParams.put("page", 1);
        searchParams.put("size", 10);
        
        Map<String, Object> searchResult = controller.searchUsers(searchParams);
        System.out.println("검색 결과: " + searchResult);
        
        // 2. 부서 대시보드 테스트
        System.out.println("\\n2. 부서 대시보드 테스트");
        Map<String, Object> deptParams = new HashMap<>();
        deptParams.put("dept_code", "DEV001");
        
        Map<String, Object> deptDashboard = controller.getDeptDashboard(deptParams);
        System.out.println("부서 대시보드: " + deptDashboard);
        
        // 3. 프로젝트 현황 보고서 테스트
        System.out.println("\\n3. 프로젝트 현황 보고서 테스트");
        Map<String, Object> reportParams = new HashMap<>();
        reportParams.put("start_date", "2024-01-01");
        reportParams.put("end_date", "2024-12-31");
        
        Map<String, Object> projectReport = controller.getProjectReport(reportParams);
        System.out.println("프로젝트 보고서: " + projectReport);
        
        // 4. 사용자 등록 테스트
        System.out.println("\\n4. 사용자 등록 테스트");
        Map<String, Object> newUserParams = new HashMap<>();
        newUserParams.put("name", "신입사원");
        newUserParams.put("email", "newbie@company.com");
        newUserParams.put("age", 25);
        newUserParams.put("dept_code", "DEV001");
        newUserParams.put("position", "Junior Developer");
        newUserParams.put("salary", 3500000);
        
        Map<String, Object> createResult = controller.createUser(newUserParams);
        System.out.println("사용자 등록 결과: " + createResult);
    }
}
"""

    # 파일들 생성
    files_to_create = [
        (src_main_java / "Application.java", main_app),
        (src_main_java / "controller" / "MainController.java", controller),
        (src_main_java / "service" / "UserService.java", user_service),
        (src_main_java / "service" / "DeptService.java", dept_service),
        (src_main_java / "service" / "ProjectService.java", project_service),
        (src_main_java / "dao" / "UserDao.java", user_dao),
        (src_main_java / "dao" / "DeptDao.java", dept_dao),
        (src_main_java / "dao" / "ProjectDao.java", project_dao),
    ]
    
    for file_path, content in files_to_create:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # README.md 생성
    readme_content = f"""# {project_name.upper()}

DB 연동용 Map 파라미터 전달 객체 사용 예제 프로젝트

## 프로젝트 개요

이 프로젝트는 DAO와 서비스 계층 간의 **DB 연동용 파라미터 전달**에 Map을 사용하는 전형적인 패턴을 보여줍니다.

## 프로젝트 구조

```
{project_name}/
├── src/main/java/com/example/
│   ├── Application.java                 # 메인 실행 클래스
│   ├── controller/
│   │   └── MainController.java          # API 컨트롤러
│   ├── service/
│   │   ├── UserService.java             # 사용자 비즈니스 로직
│   │   ├── DeptService.java             # 부서 비즈니스 로직
│   │   └── ProjectService.java          # 프로젝트 비즈니스 로직
│   └── dao/
│       ├── UserDao.java                 # 사용자 데이터 접근 계층
│       ├── DeptDao.java                 # 부서 데이터 접근 계층
│       └── ProjectDao.java              # 프로젝트 데이터 접근 계층
└── README.md
```

## Map 사용 패턴

### 1. **쿼리 파라미터 전달**
```java
// Service → DAO 파라미터 전달
Map<String, Object> params = new HashMap<>();
params.put("name", searchName);
params.put("dept_code", deptCode);
params.put("status", "A");
params.put("limit", 20);
params.put("offset", 0);

List<Map<String, Object>> users = userDao.selectUserList(params);
```

### 2. **DB 결과 반환**
```java
// DAO → Service 결과 반환
Map<String, Object> user = new HashMap<>();
user.put("user_id", "USR001");
user.put("name", "김개발");
user.put("email", "kim@company.com");
user.put("dept_code", "DEV001");
user.put("salary", 5000000);
return user;
```

### 3. **동적 쿼리 조건**
```java
// 조건부 WHERE 절 구성
if (params.get("name") != null) {{
    sql.append("AND name LIKE CONCAT('%', ?, '%') ");
}}
if (params.get("dept_code") != null) {{
    sql.append("AND dept_code = ? ");
}}
```

## 주요 Map 키들

이 프로젝트에서 사용되는 주요 Map 키들:

### 사용자 관련
- `user_id`, `name`, `email`, `age`, `dept_code`
- `position`, `salary`, `status`, `created_date`, `updated_date`
- `login_count`, `last_login`

### 부서 관련  
- `dept_code`, `dept_name`, `parent_dept_code`, `manager_id`
- `budget`, `used_amount`, `remaining_amount`

### 프로젝트 관련
- `project_id`, `project_name`, `start_date`, `end_date`
- `progress_rate`, `allocation_rate`, `role`

### 검색/페이징 관련
- `limit`, `offset`, `sort_by`, `sort_order`
- `page`, `size`, `start_date`, `end_date`

### 응답 관련
- `success`, `error`, `message`, `data`, `count`
- `timestamp`, `generated_at`

## 실행 방법

```bash
# 프로젝트 디렉토리로 이동
cd {project_name}

# 컴파일
javac -cp "src/main/java" -d "build/classes" src/main/java/com/example/*.java src/main/java/com/example/*/*.java

# 실행
java -cp "build/classes" com.example.Application
```

## Map → VO 변환 대상

이 프로젝트의 모든 Map 사용을 하나의 통합 VO 클래스로 변환할 수 있습니다:

### 변환 전 (Map 사용):
```java
Map<String, Object> params = new HashMap<>();
params.put("user_id", userId);
params.put("dept_code", deptCode);
params.put("status", "A");

Map<String, Object> user = userDao.selectUserById(params);
String userName = (String) user.get("name");
Integer userAge = (Integer) user.get("age");
```

### 변환 후 (VO 사용):
```java
UnifiedDataVO params = new UnifiedDataVO();
params.setUserId(userId);
params.setDeptCode(deptCode);
params.setStatus("A");

UnifiedDataVO user = userDao.selectUserById(params);
String userName = user.getName();
Integer userAge = user.getAge();
```

## 변환 도구 사용

```bash
# 분석 실행 (dry-run)
python map_to_vo_converter.py {project_name} --dry-run

# 실제 변환 실행
python map_to_vo_converter.py {project_name} \\
    --vo-package com.example.model \\
    --vo-class DataTransferVO
```

이 예제는 실제 업무에서 자주 사용되는 DB 연동 Map 패턴을 포함하고 있어 Map → VO 변환 도구의 테스트에 적합합니다.
"""

    with open(project_root / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ DB 연동용 Map 예제 프로젝트 생성 완료: {project_root}")
    print(f"📁 디렉토리: {project_root.absolute()}")
    print(f"📄 Java 파일: {len(files_to_create)}개")
    print("\n🔍 주요 Map 사용 패턴:")
    print("- DAO 메서드 파라미터 전달 (검색조건, 페이징, 정렬)")
    print("- DB 쿼리 결과 반환 (사용자, 부서, 프로젝트 정보)")
    print("- API 요청/응답 데이터 구조")
    print("- 통계 및 집계 데이터")
    
    return project_root

if __name__ == "__main__":
    import sys
    project_name = sys.argv[1] if len(sys.argv) > 1 else "db-map-example"
    create_db_map_project(project_name)


# # 1. 예제 프로젝트 생성
# poetry run python db_map_example_project.py sample-project

# # 2. 프로젝트 확인
# cd sample-project
# find . -name "*.java" | head -10

# # 3. Map 분석 및 변환
# poetry run python map_to_vo_converter.py sample-project --dry-run

# # 4. 실제 변환 실행
# poetry run python map_to_vo_converter.py sample-project \
#     --vo-package com.example.model \
#     --vo-class DataTransferVO