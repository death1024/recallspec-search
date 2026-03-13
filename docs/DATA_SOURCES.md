# Data Sources

## CPSC (Consumer Product Safety Commission)

**API:** https://www.saferproducts.gov/RestWebServices/

**Coverage:** Consumer products (toys, appliances, furniture, etc.)

**Endpoints:**
- `/Recall` - Get recalls with date filters
- `/RecallSearch` - Search by keyword

**Key Fields:**
- RecallNumber, ProductName, Manufacturer
- ModelNumber, UPC, Hazard, Remedy
- RecallDate, Distribution

**Sync Strategy:**
- Initial: Last 5 years (1825 days)
- Incremental: Daily checks for new recalls

## NHTSA (National Highway Traffic Safety Administration)

**API:** https://api.nhtsa.gov/

**Coverage:** Vehicles, tires, child seats, equipment

**Endpoints:**
- `/recalls/recallsByVehicle?vin={vin}` - VIN lookup
- `/recalls/recallsByVehicle?make={make}&model={model}&modelYear={year}` - Make/model search

**Key Fields:**
- NHTSACampaignNumber, Make, Model, ModelYear
- Component, Consequence, Remedy
- ReportReceivedDate

**Sync Strategy:**
- Initial: Bulk download (1949-present available)
- Incremental: Daily API checks

**Important:** VIN lookup does not show already-repaired recalls

## FDA (Food & Drug Administration)

**API:** https://api.fda.gov/

**Coverage:** Drugs, medical devices, food

**Endpoints:**
- `/drug/enforcement.json` - Drug recalls
- `/device/enforcement.json` - Device recalls
- `/food/enforcement.json` - Food recalls

**Key Fields:**
- product_description, reason_for_recall
- code_info, distribution_pattern
- recall_initiation_date, status

**Sync Strategy:**
- Initial: Last 2 years
- Incremental: Weekly updates

**Limitations:**
- Data should not be used to independently alert public
- Cannot track full recall lifecycle
- Must display disclaimers per PRD section 11.2
