package com.company.erp.view.dashboard;


import com.company.erp.entity.Project;
import com.company.erp.entity.Task;
import com.company.erp.entity.TaskBlock;
import com.company.erp.service.HtmlService;
import com.company.erp.view.main.MainView;
import com.vaadin.flow.component.Html;
import com.vaadin.flow.router.Route;
import io.jmix.core.Messages;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.Target;
import io.jmix.flowui.view.ViewComponent;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.LocalDate;
import java.util.Collection;
import java.util.List;

@Route(value = "dashboard-view", layout = MainView.class)
@ViewController(id = "DashboardView")
@ViewDescriptor(path = "dashboard-view.xml")
public class DashboardView extends StandardView {
    @ViewComponent
    private CollectionLoader<TaskBlock> blocksDl;
    @ViewComponent
    private CollectionLoader<Project> projectsDl;
    @ViewComponent
    private CollectionLoader<Task> tasksDl;
    @ViewComponent
    private CollectionContainer<Task> tasksDc;
    @ViewComponent
    private DataGrid<Task> taskDataGrid;
    @Autowired
    private HtmlService ganttHtmlService;
    @ViewComponent
    private Html ganttHtml;
    @ViewComponent
    private Html statsHtml;

    @Autowired
    private Messages messages;


    @Subscribe
    public void onInit(final InitEvent event) {
        ganttHtml.setHtmlContent(messages.getMessage("emptyGantt"));
        statsHtml.setHtmlContent(messages.getMessage("emptyStats"));
    }



    @Subscribe(id = "projectsDc", target = Target.DATA_CONTAINER)
    public void onProjectsDcItemChange(final InstanceContainer.ItemChangeEvent<Project> event) {
        Project item = event.getItem();
        if (item != null) {
            setGanttHtml(item);
            setStatsHtml(item);
        } else {
            ganttHtml.setHtmlContent(messages.getMessage("emptyGantt"));
            statsHtml.setHtmlContent(messages.getMessage("emptyStats"));
        }
        tasksDl.setParameter("project", item);
        blocksDl.setParameter("task", null);
        tasksDl.load();
        blocksDl.load();
    }

    private void setGanttHtml(Project item) {
        String html = ganttHtmlService.generateGanttHtml(item);
        if (html.isBlank()) {
            html = messages.getMessage("errorGantt");
            html = html.replace("${projectName}", item.getName()).replace("${time}", LocalDate.now().toString());
        }
        ganttHtml.setHtmlContent(html);
    }

    private void setStatsHtml(Project item) {
        String html = ganttHtmlService.generateStatsHtml(item);
        if (html.isBlank()) {
            html = messages.getMessage("errorStats");
            html = html.replace("${projectName}", item.getName()).replace("${time}", LocalDate.now().toString());
        }
        statsHtml.setHtmlContent(html);
    }

    @Subscribe(id = "tasksDc", target = Target.DATA_CONTAINER)
    public void onTasksDcItemChange(final InstanceContainer.ItemChangeEvent<Task> event) {
        blocksDl.setParameter("task", event.getItem());
        blocksDl.load();
    }

    @Subscribe(id = "tasksDc", target = Target.DATA_CONTAINER)
    public void onTasksDcCollectionChange(final CollectionContainer.CollectionChangeEvent<Task> event) {
        List<Task> items = tasksDc.getItems();
        if (!items.isEmpty()) {
            taskDataGrid.select(items.getFirst());
        }
    }
}