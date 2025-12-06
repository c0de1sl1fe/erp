package com.company.erp.service;

import com.company.erp.entity.Project;
import com.company.erp.entity.Task;
import com.company.erp.entity.TaskBlock;

public interface UrlBuilderService {
    public String buildUrl(Project project);
    public String buildUrl(Task project);
    public String buildUrl(TaskBlock project);

    public String getGanttServiceUrl();
    public String getStatsServiceUrl();
}
