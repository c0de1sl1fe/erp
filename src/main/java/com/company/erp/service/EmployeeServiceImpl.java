package com.company.erp.service;

import com.company.erp.entity.Employee;
import io.jmix.core.DataManager;
import org.springframework.stereotype.Service;

@Service
public class EmployeeServiceImpl implements EmployeeService {
    private final DataManager dataManager;

    public EmployeeServiceImpl(DataManager dataManager) {
        this.dataManager = dataManager;
    }

    @Override
    public Employee getEmployeeByUserUsername(String username) {
        return dataManager.load(Employee.class)
                .query("select e from Employee e where e.user.username = :username")
                .parameter("username", username)
                .optional().orElse(null);
    }
}