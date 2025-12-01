# Standard Business Logic CTEs

You MUST use the following Common Table Expressions (CTEs) to start your query. These CTEs define the core business entities and logic.

```sql
WITH dsdefinedacct as
     (select platform_customer_id,
             account_type,
             case
             	 when is_test_workspace = true then 'Test Workspace'
             	 when is_test_workspace = false then 'non Test Workspace'
               when is_test_workspace is null then 'Test Workspace'
             end as if_test_workspace
      from "ccs-aquila-tahoe-customersdimension" c 
      WHERE partition_date = FORMAT_DATETIME(CURRENT_DATE - INTERVAL '1' DAY, 'yyyy-MM-dd') ),

customers_auth AS
     (SELECT customer_id AS platform_customer_id,
             CASE
                 WHEN organization_id IS NULL THEN 'v1'
                 ELSE 'v2'
             END AS workspace_auth_version
      FROM "ccs-aquila-louise-accountmanagement-customers"
      WHERE platform_customer_id = 'PLATFORM_ACCOUNT' ),
        
active_sub as
     (select subscription_key, platform_customer_id
      from "ccs-aquila-tahoe-subscriptiondimension"
      where partition_date = FORMAT_DATETIME(CURRENT_DATE - INTERVAL '1' DAY, 'yyyy-MM-dd')
      	and state_type = 'started'
        and subscription_type != 'OPSRAMP'
        and quantity < 10000000 ),

device_sub_dim as
	(
		select subscription_key, serial_number, application_id as app_id
	    from "ccs-aquila-tahoe-devicesubscriptiondimension"
	    where partition_date = FORMAT_DATETIME(CURRENT_DATE - INTERVAL '1' DAY, 'yyyy-MM-dd')
	),

 sm_device as
	 (
	 	select serial_number, device_type
	 	from "ccs-aquila-louise-subscriptionmanagement-smdevice"
	 ),

active_dev as
     (select ca.workspace_auth_version,
     	     dda.if_test_workspace,
             dsd.serial_number,
             dda.account_type,
             case
                 when sd.device_type in ('STORAGE',
                                        'DHCI_STORAGE') then 'Storage'
                 when sd.device_type in ('COMPUTE') then 'Compute'
                 when sd.device_type in ('ALS',
                                        'AP',
                                        'CONTROLLER',
                                        'GATEWAY',
                                        'IAP',
                                        'SWITCH',
                                        'SD_WAN_GW',
                                        'BRIDGE') then 'Aruba'
                 when sd.device_type in ('SENSOR') then 'UXI'
                 else 'Others'
             end as BU_device_type,
             dsd.app_id,
             case
                 when dsd.app_id='683da368-66cb-4ee7-90a9-ec1964768092' then 'Aruba'
                 when dsd.app_id='b394fa01-8858-4d73-8818-eadaf12eaf37' then 'Compute'
                 when dsd.app_id='980eea3c-b063-451e-8a45-ebcaa54fd561' then 'Storage'
                 when dsd.app_id='f4cc7322-f1c0-4546-a06c-74e0c3894769' then 'Opsramp'
                 when dsd.app_id='7cc837db-2045-4d58-a16f-b167bb9fd0d2' then 'UXI'
                 when dsd.app_id is null then 'missing'
                 else 'Others'
             end as application_name
      from active_sub as1
      inner join device_sub_dim dsd on dsd.subscription_key=as1.subscription_key
      inner join sm_device sd on sd.serial_number = dsd.serial_number
      left join dsdefinedacct dda on as1.platform_customer_id=dda.platform_customer_id
      left join customers_auth ca on ca.platform_customer_id = dda.platform_customer_id)
```

## Usage Instructions
1.  **ALWAYS** start your query by copying the CTEs above exactly as they are.
2.  Then, write your final `SELECT` statement querying from `active_dev` or other CTEs as needed.
3.  Filter by `if_test_workspace = 'non Test Workspace'` unless requested otherwise.
