package com.company.erp.view.taskblock;

import com.company.erp.entity.Employee;
import com.company.erp.entity.TaskBlock;
import com.company.erp.security.specific.AccessToTaskBlockWithoutRestrictionByEmployeeContext;
import com.company.erp.service.EmployeeService;
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


@Route(value = "task-blocks", layout = MainView.class)
@ViewController(id = "TaskBlock.list")
@ViewDescriptor(path = "task-block-list-view.xml")
@LookupComponent("taskBlocksDataGrid")
@DialogMode(width = "64em")
public class TaskBlockListView extends StandardListView<TaskBlock> {
    @ViewComponent
    private CollectionLoader<TaskBlock> taskBlocksDl;

    @Autowired
    private EmployeeService employeeService;
    @Autowired
    private CurrentAuthentication currentAuthentication;
    @Autowired
    private AccessManager accessManager;

    @Subscribe
    public void onBeforeShow(final BeforeShowEvent event) {
        applyRestrictions();
    }

    private void applyRestrictions() {
        AccessToTaskBlockWithoutRestrictionByEmployeeContext context = new AccessToTaskBlockWithoutRestrictionByEmployeeContext();
        accessManager.applyRegisteredConstraints(context);
        if (!context.isPermitted()) {
            UserDetails user = currentAuthentication.getUser();
            Employee employee = employeeService.getEmployeeByUserUsername(user.getUsername());
            taskBlocksDl.setParameter("employee", employee);
            taskBlocksDl.load();
        }
    }
}