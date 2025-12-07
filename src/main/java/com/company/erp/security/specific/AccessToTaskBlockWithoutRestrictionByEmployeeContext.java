package com.company.erp.security.specific;

import io.jmix.core.accesscontext.SpecificOperationAccessContext;

public class AccessToTaskBlockWithoutRestrictionByEmployeeContext extends SpecificOperationAccessContext {

    public static final String NAME = "accessTo.TaskBlock";

    public AccessToTaskBlockWithoutRestrictionByEmployeeContext() {
        super(NAME);
    }
}