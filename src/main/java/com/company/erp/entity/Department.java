package com.company.erp.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.util.UUID;

@JmixEntity
@Table(name = "DEPARTMENT")
@Entity
public class Department {
    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @InstanceName
    @Column(name = "NAME")
    private String name;

    @Column(name = "DESCRIPTION")
    private String description;

    @Column(name = "MAX_LOAD_HOURS")
    private Integer maxLoadHours;

    @Column(name = "CURRENT_LOAD_HOURS")
    private Integer currentLoadHours;

    public Integer getCurrentLoadHours() {
        return currentLoadHours;
    }

    public void setCurrentLoadHours(Integer currentLoadHours) {
        this.currentLoadHours = currentLoadHours;
    }

    public void setMaxLoadHours(Integer maxLoadHours) {
        this.maxLoadHours = maxLoadHours;
    }

    public Integer getMaxLoadHours() {
        return maxLoadHours;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
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