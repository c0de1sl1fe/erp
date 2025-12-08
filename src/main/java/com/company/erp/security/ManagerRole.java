package com.company.erp.security;

import com.company.erp.entity.Attribute;
import com.company.erp.entity.Block;
import com.company.erp.entity.Department;
import com.company.erp.entity.Employee;
import com.company.erp.entity.Project;
import com.company.erp.entity.Task;
import com.company.erp.entity.TaskBlock;
import com.company.erp.entity.User;
import io.jmix.security.model.EntityAttributePolicyAction;
import io.jmix.security.model.EntityPolicyAction;
import io.jmix.security.role.annotation.EntityAttributePolicy;
import io.jmix.security.role.annotation.EntityPolicy;
import io.jmix.security.role.annotation.ResourceRole;
import io.jmix.security.role.annotation.SpecificPolicy;
import io.jmix.securityflowui.role.annotation.MenuPolicy;
import io.jmix.securityflowui.role.annotation.ViewPolicy;

@ResourceRole(name = "ManagerRole", code = ManagerRole.CODE)
public interface ManagerRole {
    String CODE = "manager-role";

    @MenuPolicy(menuIds = {"Project.list", "Task_.list", "TaskBlock.list", "DashboardView", "Block.list", "Attribute.list", "Employee.list", "Department.list"})
    @ViewPolicy(viewIds = {"Project.list", "Task_.list", "TaskBlock.list", "DashboardView", "Block.list", "Attribute.list", "Employee.list", "User.list", "MainView", "Task_.detail", "Project.detail", "TaskBlock.detail", "Department.detail", "Department.list", "LoginView"})
    void screens();

    @EntityAttributePolicy(entityClass = Attribute.class, attributes = "*", action = EntityAttributePolicyAction.MODIFY)
    @EntityPolicy(entityClass = Attribute.class, actions = EntityPolicyAction.ALL)
    void attribute();

    @EntityAttributePolicy(entityClass = Block.class, attributes = "*", action = EntityAttributePolicyAction.MODIFY)
    @EntityPolicy(entityClass = Block.class, actions = EntityPolicyAction.ALL)
    void block();

    @EntityAttributePolicy(entityClass = Department.class, attributes = "*", action = EntityAttributePolicyAction.MODIFY)
    @EntityPolicy(entityClass = Department.class, actions = EntityPolicyAction.ALL)
    void department();

    @EntityAttributePolicy(entityClass = Employee.class, attributes = "*", action = EntityAttributePolicyAction.MODIFY)
    @EntityPolicy(entityClass = Employee.class, actions = EntityPolicyAction.ALL)
    void employee();

    @EntityAttributePolicy(entityClass = Project.class, attributes = "*", action = EntityAttributePolicyAction.MODIFY)
    @EntityPolicy(entityClass = Project.class, actions = EntityPolicyAction.ALL)
    void project();

    @EntityAttributePolicy(entityClass = Task.class, attributes = "*", action = EntityAttributePolicyAction.MODIFY)
    @EntityPolicy(entityClass = Task.class, actions = EntityPolicyAction.ALL)
    void task();

    @EntityAttributePolicy(entityClass = TaskBlock.class, attributes = "*", action = EntityAttributePolicyAction.MODIFY)
    @EntityPolicy(entityClass = TaskBlock.class, actions = EntityPolicyAction.ALL)
    void taskBlock();

    @EntityPolicy(entityClass = User.class, actions = EntityPolicyAction.READ)
    void user();

    @SpecificPolicy(resources = {"accessTo.Task", "accessTo.TaskBlock"})
    void specific();
}