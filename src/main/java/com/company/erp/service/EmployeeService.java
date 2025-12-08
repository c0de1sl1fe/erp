package com.company.erp.service;

import com.company.erp.entity.Employee;

public interface EmployeeService {
    Employee getEmployeeByUserUsername(String username);
}
