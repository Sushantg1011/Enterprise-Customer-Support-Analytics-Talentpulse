-- it is help to move to the database
USE EnterpriseCustomerSupport;

--INNER Join
SELECT TOP 10
	t.TicketID,
	t.CustomerID,
	c.CustomerName,
	c.[Plan],
	t.Priority,
	t.ResolutionHours
FROM dbo.Tickets as t
INNER JOIN dbo.Customers as c
	ON t.CustomerID = c.CustomerID;

SELECT
	COUNT(*) AS JoinedTicketRows,
	COUNT(DISTINCT t.TicketID) as DistinctTickets
FROM dbo.Tickets as t
INNER JOIN dbo.Customers as c
	ON t.CustomerID = c.CustomerID

SELECT
	c.[Plan],
	COUNT(*) AS TicketCount
FROM dbo.Tickets as t
INNER JOIN dbo.Customers as c
	ON t.CustomerID = c.CustomerID
GROUP BY c.[Plan]
ORDER BY TicketCount DESC;

SELECT
	e.EmployeeID,
	e.EmployeeName,
	COUNT(*) AS TicketCount
FROM dbo.Tickets as t
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName
	ORDER BY TicketCount DESC;


SELECT
	e.EmployeeID,
	e.EmployeeName,
	COUNT(*) AS TicketCount,
	ROUND(AVG(t.ResolutionHours),2) AS AvgResolutionHours
FROM dbo.Tickets as t
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName
	HAVING COUNT(*) > 500 
	AND AVG(t.ResolutionHours) > 20
	ORDER BY TicketCount DESC;

SELECT
	e.EmployeeID,
	e.EmployeeName,
	t.Priority,
	COUNT(*) AS TicketCount,
	ROUND(AVG(t.ResolutionHours),2) AS AvgResolutionHours
FROM dbo.Tickets as t
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	WHERE t.Priority = 'Critical'
	GROUP BY e.EmployeeID, e.EmployeeName, t.Priority
	HAVING COUNT(*) >= 20
	ORDER BY TicketCount DESC;


SELECT
	d.DepartmentID,
	d.DepartmentName,
	COUNT(*) AS TicketCount,
	ROUND(AVG(t.ResolutionHours),2) AS AvgResolutionHours
FROM dbo.Tickets as t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
	GROUP BY d.DepartmentID, d.DepartmentName
	ORDER BY TicketCount DESC;

SELECT
	d.DepartmentID,
	d.DepartmentName,
	COUNT(*) AS TicketCount,
	COUNT(DISTINCT c.CustomerID) AS UniqueCustomers
FROM dbo.Tickets as t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Customers as c
	ON t.CustomerID = c.CustomerID
	GROUP BY d.DepartmentID, d.DepartmentName;


SELECT
	c.[Plan],
	COUNT(*) AS TicketCount,
	COUNT(DISTINCT c.CustomerID) AS UniqueCustomers,
	ROUND(AVG(t.ResolutionHours),2) AS AvgResolutionHours,
	ROUND(100.0 * SUM(CASE WHEN t.SLAMet = 1 THEN 1 ELSE 0 END) / Count(*),2) AS SLAPercentage
FROM dbo.Tickets as t
INNER JOIN dbo.Customers as c
	ON t.CustomerID = c.CustomerID
	GROUP BY c.[Plan];

--SELF JOIN
SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.ManagerID,
	m.EmployeeName as ManagerName
FROM dbo.Employees as e
JOIN dbo.Employees as m
	ON e.ManagerID = m.EmployeeID;


SELECT
    e.EmployeeName,
    m.EmployeeName AS ManagerName
FROM dbo.Employees AS e
JOIN dbo.Employees AS m
    ON m.EmployeeID = e.ManagerID
WHERE e.ManagerID IN
(SELECT
m.EmployeeID
FROM dbo.Employees as e
JOIN dbo.Employees as m
On m.EmployeeID = e.ManagerID
GROUP BY m.EmployeeID
Having Count(*) >= 3);

--Left Join

SELECT
    t.TicketID,
    t.CustomerID
FROM dbo.Tickets AS t
LEFT JOIN dbo.Customers AS c
    ON t.CustomerID = c.CustomerID
WHERE c.CustomerID IS NULL;

SELECT COUNT(*) AS TicketsWithoutCustomer
FROM dbo.Tickets AS t
LEFT JOIN dbo.Customers AS c
    ON t.CustomerID = c.CustomerID
WHERE c.CustomerID IS NULL;
