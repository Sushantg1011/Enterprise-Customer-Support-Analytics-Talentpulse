USE EnterpriseCustomerSupport;

--Subquery
SELECT 
	TicketID,
	ResolutionHours
FROM dbo.Tickets
WHERE ResolutionHours >
(SELECT AVG(ResolutionHours)
FROM dbo.Tickets);

SELECT
	e.EmployeeID,
	e.EmployeeName,
	AVG(t.ResolutionHours) as EmployeeAvgResolution
FROM dbo.Tickets as t
INNER JOIN Employees as e
	on t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName
	HAVING AVG(t.ResolutionHours) >
	(SELECT AVG(ResolutionHours)
	FROM dbo.Tickets);

SELECT DISTINCT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID
FROM dbo.Tickets as t
INNER JOIN Employees AS e
	ON t.EmployeeID = e.EmployeeID
WHERE e.DepartmentID IN
(SELECT DepartmentID
FROM dbo.Tickets
GROUP BY DepartmentID
HAVING COUNT(*) > 500);

SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	t.ResolutionHours
FROM dbo.Tickets AS t
INNER JOIN Employees AS e
	ON t.EmployeeID = e.EmployeeID
WHERE t.ResolutionHours >
(SELECT AVG(t2.ResolutionHours)
FROM dbo.Tickets as t2
WHERE t2.DepartmentID = e.DepartmentID);

SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID
FROM dbo.Employees AS e
WHERE EXISTS
(
	SELECT 1
	FROM dbo.Tickets as t
	WHERE t.EmployeeID = e.EmployeeID
	AND t.ResolutionHours >
	(
		SELECT
		AVG(t2.ResolutionHours)
		FROM dbo.Tickets as t2
		WHERE t2.DepartmentID = e.DepartmentID
	)
);


SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID
FROM dbo.Employees AS e
WHERE NOT EXISTS
(
	SELECT 1
	FROM dbo.Tickets AS t
	WHERE t.EmployeeID = e.EmployeeID
	AND t.ResolutionHours >
	(
		SELECT
		AVG(t2.ResolutionHours)
		FROM dbo.Tickets as t2
		WHERE t2.DepartmentID = e.DepartmentID
	)
);

SELECT
	EmployeeID,
	EmployeeAvgResolution
FROM
(	SELECT
		EmployeeID,
		AVG(ResolutionHours) AS EmployeeAvgResolution
	FROM dbo.Tickets
	GROUP BY EmployeeID
) AS EmployeeSummary
WHERE EmployeeAvgResolution > 25;


SELECT
	es.EmployeeID,
	e.EmployeeName,
	d.DepartmentName,
	es.EmployeeAvgResolution
FROM
(	SELECT
		EmployeeID,
		AVG(ResolutionHours) AS EmployeeAvgResolution
	FROM dbo.Tickets
	GROUP BY EmployeeID
) AS es
INNER JOIN dbo.Employees as e
	ON es.EmployeeID = e.EmployeeID
INNER JOIN dbo.Departments as d
	ON e.DepartmentID = d.DepartmentID;


SELECT
	es.EmployeeID,
	e.EmployeeName,
	d.DepartmentName,
	es.EmployeeAvgResolution
FROM
(	SELECT
		EmployeeID,
		AVG(ResolutionHours) AS EmployeeAvgResolution
	FROM dbo.Tickets
	GROUP BY EmployeeID
) AS es
INNER JOIN dbo.Employees as e
	ON es.EmployeeID = e.EmployeeID
INNER JOIN dbo.Departments as d
	ON e.DepartmentID = d.DepartmentID
INNER JOIN 	(
	SELECT
		DepartmentID,
		AVG(ResolutionHours) AS DepartmentAvgResolution
	FROM dbo.Tickets
	GROUP BY DepartmentID
	) as ds
	ON ds.DepartmentID = e.DepartmentID;


SELECT
	e.EmployeeID,
	e.EmployeeName,
	d.DepartmentName,
	AVG(t.ResolutionHours) AS EmployeeAvgResolution,
	(SELECT AVG(t2.ResolutionHours)
FROM dbo.Tickets as t2
WHERE t2.DepartmentID = e.DepartmentID) AS DepartmentAvgResolution
FROM dbo.Tickets AS t
INNER JOIN Employees AS e
	ON t.EmployeeID = e.EmployeeID
INNER JOIN Departments as d
	ON t.DepartmentID = d.DepartmentID
GROUP BY e.EmployeeID, e.EmployeeName,e.DepartmentID, d.DepartmentName
HAVING AVG(t.ResolutionHours) >
(SELECT AVG(t2.ResolutionHours)
FROM dbo.Tickets as t2
WHERE t2.DepartmentID = e.DepartmentID);


SELECT
    fk.name AS ForeignKeyName,
    OBJECT_NAME(fk.parent_object_id) AS ReferencingTable,
    COL_NAME(
        fkc.parent_object_id,
        fkc.parent_column_id
    ) AS ReferencingColumn,
    OBJECT_NAME(fk.referenced_object_id) AS ReferencedTable,
    COL_NAME(
        fkc.referenced_object_id,
        fkc.referenced_column_id
    ) AS ReferencedColumn
FROM sys.foreign_keys AS fk
INNER JOIN sys.foreign_key_columns AS fkc
    ON fk.object_id = fkc.constraint_object_id
ORDER BY
    ReferencingTable,
    ForeignKeyName;
