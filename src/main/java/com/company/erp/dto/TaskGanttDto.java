package com.company.erp.dto;

import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.time.LocalDate;
import java.util.List;

@Data
@Builder
public class TaskGanttDto {

    private String id;
    private String name;
    private String url;

    private LocalDate plannedStart;
    private LocalDate plannedEnd;
    private LocalDate actualEnd;
    private String status;

    private List<BlockGanttDto> blocks;
}

