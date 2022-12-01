from pyspark.sql.types import StructType,BinaryType, StructField, IntegerType, StringType, TimestampType, DateType, BooleanType,DecimalType ,FloatType, DoubleType, ByteType

schemadimdate = StructType(
    [
        StructField('DateKey',IntegerType(),True),
        StructField('FullDateAlternateKey',DateType(),True),
        StructField('DayNumberOfWeek',IntegerType(),True),
        StructField('EnglishDayNameOfWeek',StringType(),True),
        StructField('SpanishDayNameOfWeek',StringType(),True),
        StructField('FrenchDayNameOfWeek',StringType(),True),
        StructField('DayNumberOfMonth',IntegerType(),True),
        StructField('DayNumberOfYear',IntegerType(),True),
        StructField('WeekNumberOfYear',IntegerType(),True),
        StructField('EnglishMonthName',StringType(),True),
        StructField('SpanishMonthName',StringType(),True),
        StructField('FrenchMonthName',StringType(),True),
        StructField('MonthNumberOfYear',IntegerType(),True),
        StructField('CalendarQuarter',IntegerType(),True),
        StructField('CalendarYear',IntegerType(),True),
        StructField('CalendarSemester',IntegerType(),True),
        StructField('FiscalQuarter',IntegerType(),True),
        StructField('FiscalYear',IntegerType(),True),
        StructField('FiscalSemester',IntegerType(),True),
    ]
)

schemadimcurrency = StructType(
    [
        StructField('CurrencyKey',IntegerType(),True),
        StructField('CurrencyAlternateKey',StringType(),True),
        StructField('CurrencyName',StringType(),True),
    ]
)

schemadimcustomer = StructType(
    [
        StructField('CustomerKey',IntegerType(),True),
        StructField('GeographyKey',IntegerType(),True),
        StructField('CustomerAlternateKey',StringType(),True),
        StructField('Title',StringType(),True),
        StructField('FirstName',StringType(),True),
        StructField('MiddleName',StringType(),True),
        StructField('LastName',StringType(),True),
        StructField('NameStyle',BooleanType(),True),
        StructField('BirthDate',DateType(),True),
        StructField('MaritalStatus',StringType(),True),
        StructField('Suffix',StringType(),True),
        StructField('Gender',StringType(),True),
        StructField('EmailAddress',StringType(),True),
        StructField('YearlyIncome',FloatType(),True),
        StructField('TotalChildren',IntegerType(),True),
        StructField('NumberChildrenAtHome',IntegerType(),True),
        StructField('EnglishEducation',StringType(),True),
        StructField('SpanishEducation',StringType(),True),
        StructField('FrenchEducation',StringType(),True),
        StructField('EnglishOccupation',StringType(),True),
        StructField('SpanishOccupation',StringType(),True),
        StructField('FrenchOccupation',StringType(),True),
        StructField('HouseOwnerFlag',StringType(),True),
        StructField('NumberCarsOwned',IntegerType(),True),
        StructField('AddressLine1',StringType(),True),
        StructField('AddressLine2',StringType(),True),
        StructField('Phone',StringType(),True),
        StructField('DateFirstPurchase',DateType(),True),
        StructField('CommuteDistance',StringType(),True),
    ]
)

schemadimgeography = StructType(
    [
        StructField('GeographyKey',IntegerType(),True),
        StructField('City',StringType(),True),
        StructField('StateProvinceCode',StringType(),True),
        StructField('StateProvinceName',StringType(),True),
        StructField('CountryRegionCode',StringType(),True),
        StructField('EnglishCountryRegionName',StringType(),True),
        StructField('SpanishCountryRegionName',StringType(),True),
        StructField('FrenchCountryRegionName',StringType(),True),
        StructField('PostalCode',StringType(),True),
        StructField('SalesTerritoryKey',IntegerType(),True),
        StructField('IpAddressLocator',StringType(),True),
    ]
)

schemadimproduct = StructType(
    [
        StructField('ProductKey',IntegerType(),True),
        StructField('ProductAlternateKey',StringType(),True),
        StructField('ProductSubcategoryKey',IntegerType(),True),
        StructField('WeightUnitMeasureCode',StringType(),True),
        StructField('SizeUnitMeasureCode',StringType(),True),
        StructField('EnglishProductName',StringType(),True),
        StructField('SpanishProductName',StringType(),True),
        StructField('FrenchProductName',StringType(),True),
        StructField('StandardCost',DecimalType(),True),
        StructField('FinishedGoodsFlag',BooleanType(),True),
        StructField('Color',StringType(),True),
        StructField('SafetyStockLevel',IntegerType(),True),
        StructField('ReorderPoint',IntegerType(),True),
        StructField('ListPrice',DecimalType(),True),
        StructField('Size',StringType(),True),
        StructField('SizeRange',StringType(),True),
        StructField('Weight',DecimalType(),True),
        StructField('DaysToManufacture',IntegerType(),True),
        StructField('ProductLine',StringType(),True),
        StructField('DealerPrice',DecimalType(),True),
        StructField('Class',StringType(),True),
        StructField('Style',StringType(),True),
        StructField('ModelName',StringType(),True),
        StructField('LargePhoto',StringType(),True),
        StructField('EnglishDescription',StringType(),True),
        StructField('FrenchDescription',StringType(),True),
        StructField('ChineseDescription',StringType(),True),
        StructField('ArabicDescription',StringType(),True),
        StructField('HebrewDescription',StringType(),True),
        StructField('ThaiDescription',StringType(),True),
        StructField('GermanDescription',StringType(),True),
        StructField('JapaneseDescription',StringType(),True),
        StructField('TurkishDescription',StringType(),True),
        StructField('StartDate',TimestampType(),True),
        StructField('EndDate',TimestampType(),True),
        StructField('Status',StringType(),True),
    ]
)

schemadimproductcategory = StructType(
    [
        StructField('ProductCategoryKey',IntegerType(),True),
        StructField('ProductCategoryAlternateKey',IntegerType(),True),
        StructField('EnglishProductCategoryName',StringType(),True),
        StructField('SpanishProductCategoryName',StringType(),True),
        StructField('FrenchProductCategoryName',StringType(),True),
    ]
)

schemadimproductsubcategory = StructType(
    [
        StructField('ProductSubcategoryKey',IntegerType(),True),
        StructField('ProductSubcategoryAlternateKey',IntegerType(),True),
        StructField('EnglishProductSubcategoryName',StringType(),True),
        StructField('SpanishProductSubcategoryName',StringType(),True),
        StructField('FrenchProductSubcategoryName',StringType(),True),
        StructField('ProductCategoryKey',IntegerType(),True),
    ]
)

schemadimpromotion = StructType(
    [
        StructField('PromotionKey',IntegerType(),True),
        StructField('PromotionAlternateKey',IntegerType(),True),
        StructField('EnglishPromotionName',StringType(),True),
        StructField('SpanishPromotionName',StringType(),True),
        StructField('FrenchPromotionName',StringType(),True),
        StructField('DiscountPct',DoubleType(),True),
        StructField('EnglishPromotionType',StringType(),True),
        StructField('SpanishPromotionType',StringType(),True),
        StructField('FrenchPromotionType',StringType(),True),
        StructField('EnglishPromotionCategory',StringType(),True),
        StructField('SpanishPromotionCategory',StringType(),True),
        StructField('FrenchPromotionCategory',StringType(),True),
        StructField('StartDate',TimestampType(),True),
        StructField('EndDate',TimestampType(),True),
        StructField('MinQty',IntegerType(),True),
        StructField('MaxQty',IntegerType(),True),
    ]
)

schemadimsalesterritory = StructType(
    [
        StructField('SalesTerritoryKey',IntegerType(),True),
        StructField('SalesTerritoryAlternateKey',IntegerType(),True),
        StructField('SalesTerritoryRegion',StringType(),True),
        StructField('SalesTerritoryCountry',StringType(),True),
        StructField('SalesTerritoryGroup',StringType(),True),
        StructField('SalesTerritoryImage',BinaryType(),True),
    ]
)


schemafactinternetsales = StructType(
    [
        StructField('ProductKey',IntegerType(),True),
        StructField('OrderDateKey',IntegerType(),True),
        StructField('DueDateKey',IntegerType(),True),
        StructField('ShipDateKey',IntegerType(),True),
        StructField('CustomerKey',IntegerType(),True),
        StructField('PromotionKey',IntegerType(),True),
        StructField('CurrencyKey',IntegerType(),True),
        StructField('SalesTerritoryKey',IntegerType(),True),
        StructField('SalesOrderNumber',StringType(),True),
        StructField('SalesOrderLineNumber',IntegerType(),True),
        StructField('RevisionNumber',IntegerType(),True),
        StructField('OrderQuantity',IntegerType(),True),
        StructField('UnitPrice',FloatType(),True),
        StructField('ExtendedAmount',FloatType(),True),
        StructField('UnitPriceDiscountPct',DoubleType(),True),
        StructField('DiscountAmount',DoubleType(),True),
        StructField('ProductStandardCost',FloatType(),True),
        StructField('TotalProductCost',FloatType(),True),
        StructField('SalesAmount',FloatType(),True),
        StructField('Freight',FloatType(),True),
        StructField('CarrierTrackingNumber',StringType(),True),
        StructField('CustomerPONumber',StringType(),True),
        StructField('OrderDate',TimestampType(),True),
        StructField('DueDate',TimestampType(),True),
        StructField('ShipDate',TimestampType(),True),
    ]
)

schemafactinternetsalesreason = StructType(
    [
        StructField('SalesOrderNumber',StringType(),True),
        StructField('SalesOrderLineNumber',IntegerType(),True),
        StructField('SalesReasonKey',IntegerType(),True),
    ]
)

schemaaddress = StructType(
    [
        StructField('AddressID',IntegerType(),True),
        StructField('AddressLine1',StringType(),True),
        StructField('AddressLine2',StringType(),True),
        StructField('City',StringType(),True),
        StructField('StateProvince',StringType(),True),
        StructField('CountryRegion',StringType(),True),
        StructField('PostalCode',StringType(),True),
        StructField('rowguid',StringType(),True),
        StructField('ModifiedDate',DateType(),True),
    ]
)

schemacustomer = StructType(
    [
        StructField('CustomerID',IntegerType(),True),
        StructField('NameStyle',StringType(),True),
        StructField('Title',StringType(),True),
        StructField('FirstName',StringType(),True),
        StructField('MiddleName',StringType(),True),
        StructField('LastName',StringType(),True),
        StructField('Suffix',StringType(),True),
        StructField('CompanyName',StringType(),True),
        StructField('SalesPerson',StringType(),True),
        StructField('EmailAddress',StringType(),True),
        StructField('Phone',StringType(),True),
        StructField('PasswordHash',StringType(),True),
        StructField('PasswordSalt',StringType(),True),
        StructField('rowguid',StringType(),True),
        StructField('ModifiedDate',DateType(),True),
    ]
)

schemafcustomeraddress = StructType(
    [
        StructField('CustomerID',IntegerType(),True),
        StructField('AddressID',IntegerType(),True),
        StructField('AddressType',StringType(),True),
        StructField('rowguid',StringType(),True),
        StructField('ModifiedDate',DateType(),True),
    ]
)

schemaproduct = StructType(
    [
        StructField('ProductID',IntegerType(),True),
        StructField('Name',StringType(),True),
        StructField('ProductNumber',StringType(),True),
        StructField('Color',StringType(),True),
        StructField('StandardCost',FloatType(),True),
        StructField('ListPrice',FloatType(),True),
        StructField('Size',StringType(),True),
        StructField('Weight',DoubleType(),True),
        StructField('ProductCategoryID',IntegerType(),True),
        StructField('ProductModelID',IntegerType(),True),
        StructField('SellStartDate',DateType(),True),
        StructField('SellEndDate',DateType(),True),
        StructField('DiscontinuedDate',DateType(),True),
        StructField('ThumbNailPhoto',StringType(),True),
        StructField('ThumbnailPhotoFileName',StringType(),True),
        StructField('rowguid',StringType(),True),
        StructField('ModifiedDate',DateType(),True),
    ]
)

schemaproductcategory = StructType(
    [
        StructField('ProductCategoryID',IntegerType(),True),
        StructField('ParentProductCategoryID',IntegerType(),True),
        StructField('Name',StringType(),True),
        StructField('rowguid',StringType(),True),
        StructField('ModifiedDate',DateType(),True),
    ]
)
schemaproductdescription = StructType(
    [
        StructField('ProductDescriptionID',IntegerType(),True),
        StructField('Description',StringType(),True),
        StructField('rowguid',StringType(),True),
        StructField('ModifiedDate',DateType(),True),
    ]
)
schemaproductmodel= StructType(
    [
        StructField('ProductModelID',IntegerType(),True),
        StructField('Name',StringType(),True),
        StructField('CatalogDescription',StringType(),True),
        StructField('rowguid',StringType(),True),
        StructField('ModifiedDate',DateType(),True),
    ]
)
schemaproductmodelproductdescription = StructType(
    [
        StructField('ProductModelID',IntegerType(),True),
        StructField('ProductDescriptionID',IntegerType(),True),
        StructField('Culture',StringType(),True),
        StructField('rowguid',StringType(),True),
        StructField('ModifiedDate',DateType(),True),
    ]
)
schemasalesorderdetail = StructType(
    [
        StructField('SalesOrderID',IntegerType(),True),
        StructField('SalesOrderDetailID',IntegerType(),True),
        StructField('OrderQty',IntegerType(),True),
        StructField('ProductID',IntegerType(),True),
        StructField('UnitPrice',FloatType(),True),
        StructField('UnitPriceDiscount',FloatType(),True),
        StructField('LineTotal',DoubleType(),True),
        StructField('rowguid',StringType(),True),
        StructField('ModifiedDate',DateType(),True),
    ]
)
schemasalesorderheader = StructType(
    [
        StructField('SalesOrderID',IntegerType(),True),
        StructField('RevisionNumber',IntegerType(),True),
        StructField('OrderDate',DateType(),True),
        StructField('DueDate',DateType(),True),
        StructField('ShipDate',DateType(),True),
        StructField('Status',IntegerType(),True),
        StructField('OnlineOrderFlag',StringType(),True),
        StructField('SalesOrderNumber',StringType(),True),
        StructField('PurchaseOrderNumber',StringType(),True),
        StructField('AccountNumber',StringType(),True),
        StructField('CustomerID',IntegerType(),True),
        StructField('ShipToAddressID',IntegerType(),True),
        StructField('BillToAddressID',IntegerType(),True),
        StructField('ShipMethod',StringType(),True),
        StructField('CreditCardApprovalCode',StringType(),True),
        StructField('SubTotal',FloatType(),True),
        StructField('TaxAmt',FloatType(),True),
        StructField('Freight',FloatType(),True),
        StructField('TotalDue',FloatType(),True),
        StructField('Comment',StringType(),True),
        StructField('rowguid',StringType(),True),
        StructField('ModifiedDate',DateType(),True),
    ]
)