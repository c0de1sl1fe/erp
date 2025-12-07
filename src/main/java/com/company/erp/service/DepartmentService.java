package com.company.erp.service;

import com.company.erp.entity.Department;

public interface DepartmentService {
    Department getDepartmentByUserUsername(String username);
}
