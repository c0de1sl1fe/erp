package com.company.erp.service;

import com.company.erp.entity.Project;
import com.company.erp.entity.Task;
import com.company.erp.entity.TaskBlock;
import org.springframework.stereotype.Service;

@Service
public class UrlBuilderServiceImpl implements UrlBuilderService {
    public final static String GANTT_SERVICE_URL = "http://127.0.0.1:8081/";
    public final static String GANTT_STRING = "gantt";
    public final static String STATS_STRING = "stats";
    public final static String BASE_URL = "http://localhost:8080/";
    public final static String PROJECT_URL = "projects/";
    public final static String TASK_URL = "tasks/";
    public final static String BLOCK_URL = "task-blocks/";

    @Override
    public String buildUrl(Project entity) {
        return BASE_URL + PROJECT_URL + entity.getId();
    }

    @Override
    public String buildUrl(Task entity) {
        return BASE_URL + TASK_URL + entity.getId();
    }

    @Override
    public String buildUrl(TaskBlock entity) {
        return BASE_URL + BLOCK_URL + entity.getId();
    }

    @Override
    public String getGanttServiceUrl() {
        return GANTT_SERVICE_URL + GANTT_STRING;
    }

    @Override
    public String getStatsServiceUrl() {
        return GANTT_SERVICE_URL + STATS_STRING;
    }
}
