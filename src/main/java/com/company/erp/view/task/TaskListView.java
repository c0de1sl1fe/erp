package com.company.erp.view.task;

import com.company.erp.entity.Department;
import com.company.erp.entity.Task;
import com.company.erp.security.specific.AccessToTaskWithoutRestrictionByDepartmentContext;
import com.company.erp.service.DepartmentService;
import com.company.erp.view.main.MainView;
import com.vaadin.flow.router.Route;
import io.jmix.core.AccessManager;
import io.jmix.core.security.CurrentAuthentication;
import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.view.DialogMode;
import io.jmix.flowui.view.LookupComponent;
import io.jmix.flowui.view.StandardListView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewComponent;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;


@Route(value = "tasks", layout = MainView.class)
@ViewController(id = "Task_.list")
@ViewDescriptor(path = "task-list-view.xml")
@LookupComponent("tasksDataGrid")
@DialogMode(width = "64em")
public class TaskListView extends StandardListView<Task> {
    @ViewComponent
    private CollectionLoader<Task> tasksDl;

    @Autowired
    private CurrentAuthentication currentAuthentication;
    @Autowired
    private DepartmentService departmentService;
    @Autowired
    private AccessManager accessManager;


    @Subscribe
    public void onBeforeShow(final BeforeShowEvent event) {
        AccessToTaskWithoutRestrictionByDepartmentContext context = new AccessToTaskWithoutRestrictionByDepartmentContext();
        accessManager.applyRegisteredConstraints(context);
        if (!context.isPermitted()) {
            UserDetails user = currentAuthentication.getUser();
            Department departmentByUserUsername = departmentService.getDepartmentByUserUsername(user.getUsername());
            tasksDl.setParameter("department", departmentByUserUsername);
            tasksDl.load();

        }
    }

}