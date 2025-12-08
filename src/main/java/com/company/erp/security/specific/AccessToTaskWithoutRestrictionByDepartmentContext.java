package com.company.erp.security.specific;

import io.jmix.core.accesscontext.SpecificOperationAccessContext;

public class AccessToTaskWithoutRestrictionByDepartmentContext extends SpecificOperationAccessContext {

    public static final String NAME = "accessTo.Task";

    public AccessToTaskWithoutRestrictionByDepartmentContext() {
        super(NAME);
    }
}