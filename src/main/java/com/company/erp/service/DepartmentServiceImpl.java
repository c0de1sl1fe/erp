package com.company.erp.service;

import com.company.erp.entity.Department;
import io.jmix.core.DataManager;
import org.springframework.stereotype.Service;

@Service
public class DepartmentServiceImpl implements DepartmentService {
    private final DataManager dataManager;

    public DepartmentServiceImpl(DataManager dataManager) {
        this.dataManager = dataManager;
    }

    @Override
    public Department getDepartmentByUserUsername(String username) {
        return dataManager.load(Department.class).query("select e.department from Employee e " +
                        "where e.user.username = :username")
                .parameter("username", username)
                .optional().orElse(null);
    }
}
