# Business Logic Rules & Definitions

## 1. Test Workspace Definition
A workspace is considered a "Test Workspace" if:
- `is_test_workspace` is `true` or `null`.
- The user's email domain is in the blacklist (e.g., `glcptest.com`, `hpe.com`, `gmail.com`, etc.).

**SQL Logic:**
```sql
CASE
    WHEN is_test_workspace = true THEN 'Test Workspace'
    WHEN is_test_workspace = false THEN 'non Test Workspace'
    WHEN is_test_workspace is null THEN 'Test Workspace'
END
```

## 2. Workspace Auth Version
Determines if a workspace is v1 or v2 based on `organization_id`.

**SQL Logic:**
```sql
CASE
    WHEN organization_id IS NULL THEN 'v1'
    ELSE 'v2'
END
```

## 3. BU Device Type Mapping
Maps `device_type` to Business Unit (BU) categories.

**SQL Logic:**
```sql
CASE
    WHEN device_type IN ('STORAGE', 'DHCI_STORAGE') THEN 'Storage'
    WHEN device_type IN ('COMPUTE') THEN 'Compute'
    WHEN device_type IN ('ALS', 'AP', 'CONTROLLER', 'GATEWAY', 'IAP', 'SWITCH', 'SD_WAN_GW', 'BRIDGE') THEN 'Aruba'
    WHEN device_type IN ('SENSOR') THEN 'UXI'
    ELSE 'Others'
END
```

## 4. Application Name Mapping
Maps `app_id` (Application ID) to Application Name.

**SQL Logic:**
```sql
CASE
    WHEN app_id='683da368-66cb-4ee7-90a9-ec1964768092' THEN 'Aruba'
    WHEN app_id='b394fa01-8858-4d73-8818-eadaf12eaf37' THEN 'Compute'
    WHEN app_id='980eea3c-b063-451e-8a45-ebcaa54fd561' THEN 'Storage'
    WHEN app_id='f4cc7322-f1c0-4546-a06c-74e0c3894769' THEN 'Opsramp'
    WHEN app_id='7cc837db-2045-4d58-a16f-b167bb9fd0d2' THEN 'UXI'
    ELSE 'Others'
END
```

## 5. Storage Type Classification
Classifies storage devices based on `device_model`.

**SQL Logic:**
```sql
CASE 
    WHEN UPPER(device_model) LIKE 'HPE NS DHCI%ALLETRA 5% CTO ARRAY' THEN 'PCBE A5K'
    WHEN UPPER(device_model) LIKE 'HPE NS DHCI%ALLETRA 6%' THEN 'PCBE A6K'
    WHEN UPPER(device_model) LIKE '%DHCI%BASE ARRAY' THEN 'PCBE Nimble'
    WHEN UPPER(device_model) = 'HPE GL PRV CLD W/AL STG MP BASE CONFIG' THEN 'PCBE MP'
    WHEN UPPER(device_model) LIKE 'HPE PRIMERA%CONTROLLER%' OR UPPER(device_model) LIKE 'HPE 3PAR 600%S NODE' THEN 'Block Primera'
    WHEN UPPER(device_model) LIKE '%ALLETRA 5%' THEN 'Block A5K'
    WHEN UPPER(device_model) LIKE 'HPE ALLETRA 6%' OR UPPER(device_model) LIKE 'HPE NS 6% CTO BASE ARRAY' THEN 'Block A6K'
    WHEN UPPER(device_model) LIKE 'HPE NS%DC CTO BASE ARRAY' THEN 'Block Nimble'
    WHEN UPPER(device_model) LIKE '%ALLETRA 9%' THEN 'Block A9K'
    WHEN UPPER(device_model) IN ('HPE GL BLOCK STG MP BASE CLSTR CONFIG', 'HPE GREENLAKE FOR BLOCK STORAGE MP BASE CONFIG') THEN 'Block AMP'
    WHEN UPPER(device_model) IN ('HPE GREENLAKE FILE STG MP BASE CONFIG', 'HPE GREENLAKE FILE STG MP HD BASE CONFIG') THEN 'File AMP'
    WHEN UPPER(device_model) = 'HPE GREENLAKE BLOCK STORAGE FOR AWS VIRTUAL CONFIG' THEN 'Block AWS'
    ELSE 'others'
END
```

## 6. Subscription BU Subtype
Maps `subscription_type` to BU Subtype.

**SQL Logic:**
```sql
CASE
    WHEN subscription_type = 'CENTRAL_STORAGE' THEN 'Storage'
    WHEN subscription_type = 'CENTRAL_COMPUTE' THEN 'Compute'
    WHEN subscription_type LIKE 'UXI%' THEN 'UXI'
    WHEN subscription_type='OPSRAMP' THEN 'Opsramp'
    ELSE 'Aruba'
END
```
