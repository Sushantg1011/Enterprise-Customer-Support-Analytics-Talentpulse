-- it is help to move to the database
USE EnterpriseCustomerSupport;

-- Aggregate (Count, Avg, Sum, Min, Max) with GROUP BY & ROUND
SELECT
	Priority,
	Count(*) as TicketCount
FROM dbo.Tickets
GROUP BY Priority;

SELECT
	Priority,
	ROUND(AVG(ResolutionHours),2) AS AvgResolutionHours
FROM dbo.Tickets
GROUP BY Priority;

SELECT
	COUNT(*) AS TotalTickets,
	MIN(CreatedAt) AS FirstTicketDate,
	MAX(CreatedAt) AS LastTicketDate
FROM dbo.Tickets;

SELECT
	Priority,
	ROUND(MIN(ResolutionHours),2) AS FastestResolution,
	ROUND(MAX(ResolutionHours),2) AS SlowestResolution
FROM dbo.Tickets
GROUP BY Priority;

SELECT
	Complexity,
	COUNT(*) AS TicketCount
FROM dbo.Tickets
GROUP BY Complexity;

SELECT
	Priority,
	COUNT(*) AS TicketCount,
	ROUND(AVG(ResolutionHours),2) AS AvgResolutionHours,
	ROUND(MIN(ResolutionHours),2) AS FastestResolution,
	ROUND(MAX(ResolutionHours),2) AS SlowestResolution
FROM dbo.Tickets
GROUP BY Priority;



-- HAVING -> filters groups AFTER grouping
SELECT
	Priority,
	Count(*) as TicketCount
FROM dbo.Tickets
GROUP BY Priority
HAVING COUNT(*) > 10000;

SELECT
	Complexity,
	COUNT(*) AS TicketCount
FROM dbo.Tickets
GROUP BY Complexity
HAVING COUNT(*) > 10000;

SELECT
	Priority,
	ROUND(AVG(ResolutionHours),2) AS AvgResolutionHours
FROM dbo.Tickets
GROUP BY Priority
HAVING AVG(ResolutionHours) > 20;

SELECT
	Priority,
	COUNT(*) AS FailedTickets
FROM dbo.Tickets
WHERE SLAMet = 0
GROUP BY Priority
HAVING COUNT(*) > 1000

--Distinct - Keep only unique values
SELECT
	COUNT(*) AS TotalTickets,
	COUNT(DISTINCT CustomerID) AS UniqueCustomers,
	COUNT(DISTINCT EmployeeID) AS UniqueEmployees,
	COUNT(DISTINCT CategoryID) AS UniqueCategories
FROM dbo.Tickets

--SELECT DISTINCT
--	Priority,
--	Complexity
--FROM dbo.Tickets;


SELECT DISTINCT
	[Plan]
FROM dbo.Customers

SELECT
	Priority,
	Complexity,
	COUNT(*) AS TicketCount
FROM dbo.Tickets
GROUP BY 
	Priority,
	Complexity;

SELECT 
	CustomerID,
	COUNT(*) AS TicketCount 
FROM dbo.Tickets
GROUP BY CustomerID

SELECT TOP 10
	CustomerID,
	COUNT(*) as TicketCount
FROM dbo.Tickets
GROUP BY CustomerID
ORDER BY TicketCount DESC;




