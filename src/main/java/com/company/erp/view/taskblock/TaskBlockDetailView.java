package com.company.erp.view.taskblock;

import com.company.erp.entity.TaskBlock;
import com.company.erp.view.main.MainView;
import com.vaadin.flow.router.Route;
import io.jmix.flowui.view.EditedEntityContainer;
import io.jmix.flowui.view.StandardDetailView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@Route(value = "task-blocks/:id", layout = MainView.class)
@ViewController(id = "TaskBlock.detail")
@ViewDescriptor(path = "task-block-detail-view.xml")
@EditedEntityContainer("taskBlockDc")
public class TaskBlockDetailView extends StandardDetailView<TaskBlock> {
}