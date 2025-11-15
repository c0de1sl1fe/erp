package com.company.erp.entity;

import io.jmix.core.DeletePolicy;
import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.entity.annotation.OnDeleteInverse;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.Index;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@JmixEntity
@Table(name = "TASK_", indexes = {
        @Index(name = "IDX_TASK__PROJECT", columnList = "PROJECT_ID"),
        @Index(name = "IDX_TASK__ROLE_RESPONSIBLE", columnList = "ROLE_RESPONSIBLE_ID")
})
@Entity(name = "Task_")
public class Task {
    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @InstanceName
    @Column(name = "NAME")
    private String name;

    @OnDeleteInverse(DeletePolicy.CASCADE)
    @JoinColumn(name = "PROJECT_ID")
    @ManyToOne(fetch = FetchType.LAZY)
    private Project project;

    @JoinColumn(name = "ROLE_RESPONSIBLE_ID")
    @ManyToOne(fetch = FetchType.LAZY)
    private Department roleResponsible;

    @Column(name = "PLANNED_START")
    private LocalDate plannedStart;

    @Column(name = "PLANNED_END")
    private LocalDate plannedEnd;

    @Column(name = "ACTUAL_END_DATE")
    private LocalDate actualEndDate;

    @Column(name = "PLANNED_BUDGET", precision = 19, scale = 2)
    private BigDecimal plannedBudget;

    @Column(name = "ACTUAL_BUDGET")
    private BigDecimal actualBudget;

    @OneToMany(mappedBy = "task")
    private List<TaskBlock> blocks;

    @JoinTable(name = "TASK_ATTRIBUTE_LINK",
            joinColumns = @JoinColumn(name = "TASK_ID"),
            inverseJoinColumns = @JoinColumn(name = "ATTRIBUTE_ID"))
    @ManyToMany
    private List<Attribute> attribute;

    public void setAttribute(List<Attribute> attribute) {
        this.attribute = attribute;
    }

    public List<Attribute> getAttribute() {
        return attribute;
    }

    public LocalDate getActualEndDate() {
        return actualEndDate;
    }

    public void setActualEndDate(LocalDate actualEndDate) {
        this.actualEndDate = actualEndDate;
    }

    public Department getRoleResponsible() {
        return roleResponsible;
    }

    public void setRoleResponsible(Department roleResponsible) {
        this.roleResponsible = roleResponsible;
    }

    public List<TaskBlock> getBlocks() {
        return blocks;
    }

    public void setBlocks(List<TaskBlock> blocks) {
        this.blocks = blocks;
    }

    public void setPlannedEnd(LocalDate plannedEnd) {
        this.plannedEnd = plannedEnd;
    }

    public LocalDate getPlannedEnd() {
        return plannedEnd;
    }

    public void setPlannedStart(LocalDate plannedStart) {
        this.plannedStart = plannedStart;
    }

    public LocalDate getPlannedStart() {
        return plannedStart;
    }

    public Project getProject() {
        return project;
    }

    public void setProject(Project project) {
        this.project = project;
    }

    public BigDecimal getPlannedBudget() {
        return plannedBudget;
    }

    public void setPlannedBudget(BigDecimal plannedBudget) {
        this.plannedBudget = plannedBudget;
    }


    public void setActualBudget(BigDecimal actualBudget) {
        this.actualBudget = actualBudget;
    }

    public BigDecimal getActualBudget() {
        return actualBudget;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

}