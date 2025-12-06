package com.company.erp.service;

import com.company.erp.dto.BlockGanttDto;
import com.company.erp.dto.ProjectGanttDto;
import com.company.erp.dto.TaskGanttDto;
import com.company.erp.entity.Project;
import com.company.erp.entity.Task;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;
import java.util.Objects;

@Service
public class ProjectGanttDtoBuilder {

    @Autowired
    private UrlBuilderService urlBuilderService;

    public ProjectGanttDto build(Project project) {

        return ProjectGanttDto.builder()
                .id(s(project.getId()))
                .name(project.getName())
                .url(urlBuilderService.buildUrl(project))

                .startDate(findProjectStart(project))
                .plannedEnd(project.getPlannedEndDate())
                .actualEnd(project.getActualEndDate())

                .theme("light") // или бери из UserSettings
                .status(project.getStatus().toString())
                .tasks(buildTasks(project))
                .build();
    }

    // ---------------------------------------------------------
    // Helpers
    // ---------------------------------------------------------

    private List<TaskGanttDto> buildTasks(Project project) {
        if (project.getTasks() == null) {
            return List.of();
        }

        return project.getTasks().stream()
                .map(task -> TaskGanttDto.builder()
                        .id(s(task.getId()))
                        .name(task.getName())
                        .url(urlBuilderService.buildUrl(task))

                        .plannedStart(task.getPlannedStart())
                        .plannedEnd(task.getPlannedEnd())
                        .actualEnd(task.getActualEndDate())

                        .status(task.getStatus().toString())
                        .blocks(buildBlocks(task))
                        .build()
                )
                .toList();
    }

    private List<BlockGanttDto> buildBlocks(Task task) {
        if (task.getBlocks() == null) {
            return List.of();
        }

        return task.getBlocks().stream()
                .map(block -> BlockGanttDto.builder()
                        .id(s(block.getId()))
                        .name((block.getBlock() != null ? block.getBlock().getName(): null) + ": " + block.getDescription())
                        .url(urlBuilderService.buildUrl(block))

                        .status(block.getStatus().toString())
                        .plannedStart(block.getPlannedStart())
                        .plannedEnd(block.getPlannedEnd())
                        .actualEnd(block.getActualEnd())
                        .build()
                )
                .toList();
    }

    /**
     * Достаем минимальную plannedStart всех задач.
     */
    private LocalDate findProjectStart(Project project) {
        if (project.getTasks() == null || project.getTasks().isEmpty()) {
            return null;
        }

        return project.getTasks().stream()
                .map(Task::getPlannedStart)
                .filter(Objects::nonNull)
                .min(LocalDate::compareTo)
                .orElse(null);
    }

    private String s(Object o) {
        return o == null ? null : o.toString();
    }
}

