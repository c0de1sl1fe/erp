package com.company.erp.view.taskblock;

import com.company.erp.entity.TaskBlock;
import com.company.erp.view.main.MainView;
import com.vaadin.flow.router.Route;
import io.jmix.flowui.view.DialogMode;
import io.jmix.flowui.view.LookupComponent;
import io.jmix.flowui.view.StandardListView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;


@Route(value = "task-blocks", layout = MainView.class)
@ViewController(id = "TaskBlock.list")
@ViewDescriptor(path = "task-block-list-view.xml")
@LookupComponent("taskBlocksDataGrid")
@DialogMode(width = "64em")
public class TaskBlockListView extends StandardListView<TaskBlock> {
}