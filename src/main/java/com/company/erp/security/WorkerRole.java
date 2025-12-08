package com.company.erp.security;

import com.company.erp.entity.Block;
import com.company.erp.entity.Department;
import com.company.erp.entity.Employee;
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

@ResourceRole(name = "WorkerRole", code = WorkerRole.CODE)
public interface WorkerRole {
    String CODE = "worker-role";

    @MenuPolicy(menuIds = {"Task_.list", "TaskBlock.list", "Block.list"})
    @ViewPolicy(viewIds = {"Task_.list", "TaskBlock.list", "Task_.detail", "TaskBlock.detail", "Block.list"})
    void screens();

    @EntityAttributePolicy(entityClass = Block.class, attributes = "*", action = EntityAttributePolicyAction.MODIFY)
    @EntityPolicy(entityClass = Block.class, actions = EntityPolicyAction.ALL)
    void block();

    @EntityAttributePolicy(entityClass = Task.class, attributes = {"project", "roleResponsible", "plannedBudget", "attribute"}, action = EntityAttributePolicyAction.VIEW)
    @EntityAttributePolicy(entityClass = Task.class, attributes = {"id", "status", "name", "plannedStart", "plannedEnd", "actualEndDate", "actualBudget", "blocks"}, action = EntityAttributePolicyAction.MODIFY)
    @EntityPolicy(entityClass = Task.class, actions = EntityPolicyAction.ALL)
    void task();

    @EntityAttributePolicy(entityClass = TaskBlock.class, attributes = {"task", "employee"}, action = EntityAttributePolicyAction.VIEW)
    @EntityAttributePolicy(entityClass = TaskBlock.class, attributes = {"id", "block", "description", "plannedStart", "plannedEnd", "actualEnd", "status"}, action = EntityAttributePolicyAction.MODIFY)
    @EntityPolicy(entityClass = TaskBlock.class, actions = EntityPolicyAction.ALL)
    void taskBlock();

    @SpecificPolicy(resources = {"restriction.TaskBlock", "restriction.Task"})
    void specific();

    @EntityAttributePolicy(entityClass = User.class, attributes = "*", action = EntityAttributePolicyAction.VIEW)
    @EntityPolicy(entityClass = User.class, actions = EntityPolicyAction.READ)
    void user();

    @EntityAttributePolicy(entityClass = Employee.class, attributes = "*", action = EntityAttributePolicyAction.VIEW)
    @EntityPolicy(entityClass = Employee.class, actions = EntityPolicyAction.READ)
    void employee();

    @EntityAttributePolicy(entityClass = Department.class, attributes = "*", action = EntityAttributePolicyAction.VIEW)
    @EntityPolicy(entityClass = Department.class, actions = EntityPolicyAction.READ)
    void department();
}