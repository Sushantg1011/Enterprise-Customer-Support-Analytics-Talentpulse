-- it is help to move to the database
USE EnterpriseCustomerSupport;

--SELECT (SELECT Columns FROM table;)
SELECT * FROM dbo.Tickets;

SELECT
	TicketID,
	CustomerID,
	EmployeeID,
	[Priority],
	Complexity,
	Lifecycle
FROM dbo.Tickets;

SELECT TOP 10
	TicketID,
	CustomerID,
	EmployeeID,
	[Priority],
	Complexity,
	Lifecycle
FROM dbo.Tickets
ORDER BY TicketID;

--WHERE (Filtering Data)
SELECT
	TicketID,
	[Priority],
	SLAHours,
	SLAMet
FROM dbo.Tickets
WHERE [Priority] = 'Critical';

SELECT
	TicketID,
	[Priority],
	Complexity,
	Lifecycle
FROM dbo.Tickets
WHERE [Priority] = 'High'
AND Complexity = 'Hard';

SELECT
	TicketID,
	[Priority],
	SLAMet
FROM dbo.Tickets
WHERE SLAMet = 0;

SELECT
	TicketID,
	[Priority],
	SLAHours,
	SLAMet
FROM dbo.Tickets
WHERE SLAHours >= 48;

-- ORDER BY (Sort Data)
SELECT TOP 10
	TicketID,
	ResolutionHours,
	[Priority],
	Complexity,
	Lifecycle
FROM dbo.Tickets
ORDER BY ResolutionHours DESC;

SELECT TOP 10
	TicketID,
	ResolutionHours,
	[Priority],
	Complexity,
	Lifecycle
FROM dbo.Tickets
ORDER BY ResolutionHours;

SELECT TOP 10
	TicketID,
	ResolutionHours,
	Priority,
	SLAMet
FROM dbo.Tickets
WHERE Priority = 'Critical'
ORDER BY ResolutionHours DESC

SELECT TOP 10
	TicketID,
	FirstResponseHours,
	Priority,
	SLAMet
FROM dbo.Tickets
ORDER BY FirstResponseHours DESC;

SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME IN (
      'Tickets',
      'Customers',
      'Employees',
      'Departments',
      'Categories',
      'Statuses'
  )
ORDER BY TABLE_NAME, ORDINAL_POSITION;
