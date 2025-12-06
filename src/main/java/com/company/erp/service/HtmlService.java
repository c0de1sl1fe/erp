package com.company.erp.service;

import com.company.erp.entity.Project;

/**
 * Service for simple gantt diagram from external service via rest
 *
 */
public interface HtmlService {
    public String generateGanttHtml(Project project);

    public String generateStatsHtml(Project project);
}
