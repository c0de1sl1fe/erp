package com.company.erp.dto;

import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.time.LocalDate;
import java.util.List;

@Data
@Builder
public class ProjectGanttDto {

    private String id;
    private String name;
    private String url;

    private LocalDate startDate;
    private LocalDate plannedEnd;
    private LocalDate actualEnd;
    private String status;

    private String theme; // "light" / "dark"

    private List<TaskGanttDto> tasks;
}

