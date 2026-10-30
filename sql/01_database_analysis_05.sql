USE EnterpriseCustomerSupport;

--UNION / UNION ALL
SELECT e.EmployeeID, e.EmployeeName
FROM dbo.Employees as e
INNER JOIN dbo.Tickets as t
	ON e.EmployeeID = t.EmployeeID
WHERE ResolutionHours > 40

UNION ALL

SELECT e.EmployeeID, e.EmployeeName
FROM dbo.Employees as e
INNER JOIN dbo.Tickets as t
	ON e.EmployeeID = t.EmployeeID
WHERE t.Priority = 'Critical';

--INTERSECT / EXCEPT
SELECT
	e.EmployeeID,
	e.EmployeeName
FROM dbo.Tickets as t
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	WHERE t.Priority = 'Critical'
	GROUP BY e.EmployeeID, e.EmployeeName

INTERSECT

SELECT
	e.EmployeeID,
	e.EmployeeName
FROM dbo.Tickets as t
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	WHERE t.ResolutionHours > 40
	GROUP BY e.EmployeeID, e.EmployeeName;

SELECT
	e.EmployeeID,
	e.EmployeeName
FROM dbo.Tickets as t
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	WHERE t.Priority = 'Critical'
	GROUP BY e.EmployeeID, e.EmployeeName

EXCEPT

SELECT
	e.EmployeeID,
	e.EmployeeName
FROM dbo.Tickets as t
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	WHERE t.ResolutionHours > 40
	GROUP BY e.EmployeeID, e.EmployeeName
