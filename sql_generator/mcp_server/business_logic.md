# Standard Business Logic CTEs

You MUST use the following Common Table Expressions (CTEs) to start your query. These CTEs define the core business entities and logic.

```sql
WITH active_sub as
     (select subscription_key, platform_customer_id
      from columnar."hybrid:pa-load"."ccs-mira-tahoe-subscriptiondimension_latest"
      where state_type = 'started'
        and subscription_type != 'OPSRAMP'
        and quantity < 10000000 ),

active_dev as
     (select case
                 when is_test_workspace = 1 then 'Test Workspace'
                 when is_test_workspace = 0 then 'non Test Workspace'
                 when is_test_workspace is null then 'Test Workspace'
             end as if_test_workspace,
             serial_number,
             device_type as BU_device_type,
             application_id as app_id,
             is_active
      from columnar."hybrid:pa-load"."ccs-mira-tahoe-devicedimension_latest"
      where is_active = true 
        and is_archived = false)
```

## Usage Instructions
1.  **ALWAYS** start your query by copying the CTEs above exactly as they are.
2.  Then, write your final `SELECT` statement querying from `active_dev` or other CTEs as needed.
3.  Filter by `if_test_workspace = 'non Test Workspace'` unless requested otherwise.

## Additional Definitions & Rules
- **Active Workspace**: A workspace is considered active if it has at least one active subscription or at least one active device, and is provisioned on the corresponding application.
- **Active Subscription**: An 'active subscription' is one where the `state_type` in the `subscriptiondimension` table is 'started'.
- **Subscription State**: The state is derived from date columns. If a subscription is not in 'suspended', 'cancelled', 'locked', 'ended', or 'none', it is considered 'started'.
- **Business Unit**: Derived from `subscription_type`. 'CENTRAL_STORAGE' -> Storage, 'CENTRAL_COMPUTE' -> Compute, 'OPSRAMP' -> OpsRamp, 'UXI*' -> UXI, Others -> Aruba.
- **Active Device**: An 'active device' is indicated by the `is_active` flag in the `devicedimension` table being `true` and `is_archived` being `false`.
