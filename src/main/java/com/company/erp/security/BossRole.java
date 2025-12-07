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

@ResourceRole(name = "BossRole", code = BossRole.CODE)
public interface BossRole {
    String CODE = "boss-role";

    @MenuPolicy(menuIds = {"Project.list", "Task_.list", "TaskBlock.list", "DashboardView", "Department.list", "Employee.list", "Attribute.list"})
    @ViewPolicy(viewIds = {"Project.list", "Task_.list", "TaskBlock.list", "DashboardView", "Department.list", "Employee.list", "Project.detail", "Task_.detail", "MainView", "LoginView", "TaskBlock.detail", "User.list", "Block.list", "Attribute.list", "User.detail"})
    void screens();

    @EntityAttributePolicy(entityClass = Block.class, attributes = "*", action = EntityAttributePolicyAction.VIEW)
    @EntityPolicy(entityClass = Block.class, actions = EntityPolicyAction.READ)
    void block();

    @EntityAttributePolicy(entityClass = Attribute.class, attributes = "*", action = EntityAttributePolicyAction.VIEW)
    @EntityPolicy(entityClass = Attribute.class, actions = EntityPolicyAction.READ)
    void attribute();

    @EntityAttributePolicy(entityClass = Department.class, attributes = "*", action = EntityAttributePolicyAction.VIEW)
    @EntityPolicy(entityClass = Department.class, actions = EntityPolicyAction.READ)
    void department();

    @EntityAttributePolicy(entityClass = Employee.class, attributes = "*", action = EntityAttributePolicyAction.VIEW)
    @EntityPolicy(entityClass = Employee.class, actions = EntityPolicyAction.READ)
    void employee();

    @EntityAttributePolicy(entityClass = Project.class, attributes = "*", action = EntityAttributePolicyAction.VIEW)
    @EntityPolicy(entityClass = Project.class, actions = EntityPolicyAction.READ)
    void project();

    @EntityAttributePolicy(entityClass = Task.class, attributes = "*", action = EntityAttributePolicyAction.VIEW)
    @EntityPolicy(entityClass = Task.class, actions = EntityPolicyAction.READ)
    void task();

    @EntityAttributePolicy(entityClass = User.class, attributes = "*", action = EntityAttributePolicyAction.VIEW)
    @EntityPolicy(entityClass = User.class, actions = EntityPolicyAction.READ)
    void user();

    @EntityAttributePolicy(entityClass = TaskBlock.class, attributes = "*", action = EntityAttributePolicyAction.VIEW)
    @EntityPolicy(entityClass = TaskBlock.class, actions = EntityPolicyAction.READ)
    void taskBlock();

    @SpecificPolicy(resources = {"accessTo.Task", "accessTo.TaskBlock"})
    void specific();
}