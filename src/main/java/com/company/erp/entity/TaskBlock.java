package com.company.erp.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.Index;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

import java.time.LocalDate;
import java.util.UUID;

@JmixEntity
@Table(name = "TASK_BLOCK", indexes = {
        @Index(name = "IDX_TASK_BLOCK_TASK", columnList = "TASK_ID"),
        @Index(name = "IDX_TASK_BLOCK_EMPLOYEE", columnList = "EMPLOYEE_ID")
})
@Entity
public class TaskBlock {
    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @JoinColumn(name = "EMPLOYEE_ID")
    @ManyToOne(fetch = FetchType.LAZY)
    private Employee employee;

    @JoinColumn(name = "TASK_ID")
    @ManyToOne(fetch = FetchType.LAZY)
    private Task task;

    @JoinColumn(name = "BLOCK_ID")
    @ManyToOne(fetch = FetchType.LAZY)
    private Block block;

    @InstanceName
    @Column(name = "DESCRIPTION")
    private String description;

    @Column(name = "PLANNED_START")
    private LocalDate plannedStart;

    @Column(name = "PLANNED_END")
    private LocalDate plannedEnd;

    @Column(name = "ACTUAL_END")
    private LocalDate actualEnd;

    @Column(name = "STATUS")
    private String status;

    public Employee getEmployee() {
        return employee;
    }

    public void setEmployee(Employee employee) {
        this.employee = employee;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public BlockStatus getStatus() {
        return status == null ? null : BlockStatus.fromId(status);
    }

    public void setStatus(BlockStatus status) {
        this.status = status == null ? null : status.getId();
    }

    public void setActualEnd(LocalDate actualEnd) {
        this.actualEnd = actualEnd;
    }

    public LocalDate getActualEnd() {
        return actualEnd;
    }

    public void setPlannedEnd(LocalDate plannedEnd) {
        this.plannedEnd = plannedEnd;
    }

    public LocalDate getPlannedEnd() {
        return plannedEnd;
    }

    public LocalDate getPlannedStart() {
        return plannedStart;
    }

    public void setPlannedStart(LocalDate plannedStart) {
        this.plannedStart = plannedStart;
    }

    public void setBlock(Block block) {
        this.block = block;
    }

    public Block getBlock() {
        return block;
    }

    public Task getTask() {
        return task;
    }

    public void setTask(Task task) {
        this.task = task;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

}