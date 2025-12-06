package com.company.erp.service;

import com.company.erp.dto.ProjectGanttDto;
import com.company.erp.entity.Project;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class HtmlServiceImpl implements HtmlService {

    private final String gantServiceUrl = "";

    private static final Logger log = LoggerFactory.getLogger(HtmlServiceImpl.class);
    private final RestClient restClient;
    private final ProjectGanttDtoBuilder projectGanttDtoBuilder;
    private final UrlBuilderService urlBuilderService;

    public HtmlServiceImpl(RestClient restClient, ProjectGanttDtoBuilder projectGanttDtoBuilder, UrlBuilderService urlBuilderService) {
        this.restClient = restClient;
        this.projectGanttDtoBuilder = projectGanttDtoBuilder;
        this.urlBuilderService = urlBuilderService;
    }

    @Override
    public String generateGanttHtml(Project project) {
        ProjectGanttDto dto = projectGanttDtoBuilder.build(project);
        String defMessage = "";
        try {
            String response = restClient.post()
                    .uri(urlBuilderService.getGanttServiceUrl())
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(dto)
                    .retrieve()
                    .body(String.class);

            if (response == null || response.isBlank()) {
                return defMessage;
            }

            return response;

        } catch (Exception e) {
            // Логируем, но не падаем
            System.err.println("Failed to call Gantt Render Service: " + e.getMessage());
            return defMessage;
        }
    }

    @Override
    public String generateStatsHtml(Project project) {
        ProjectGanttDto dto = projectGanttDtoBuilder.build(project);
        String defMessage = "";
        try {
            String response = restClient.post()
                    .uri(urlBuilderService.getStatsServiceUrl())
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(dto)
                    .retrieve()
                    .body(String.class);

            if (response == null || response.isBlank()) {
                return defMessage;
            }

            return response;

        } catch (Exception e) {
            // Логируем, но не падаем
            System.err.println("Failed to call Gantt Render Service: " + e.getMessage());
            return defMessage;
        }
    }
}
