USE EnterpriseCustomerSupport

--CASE WHEN
SELECT
	TicketID,
	ROUND(ResolutionHours,2) AS ResolutionHours,
	CASE WHEN ResolutionHours < 12 THEN 'Fast'
	WHEN ResolutionHours <= 24 THEN 'Normal'
	ELSE 'Slow' END AS ResolutionCategory
FROM dbo.Tickets

SELECT
	CASE WHEN ResolutionHours < 12 THEN 'Fast'
	WHEN ResolutionHours <= 24 THEN 'Normal'
	ELSE 'Slow' END AS ResolutionCategory,
	Count(*) AS TicketCount
FROM dbo.Tickets
GROUP BY 
	CASE 
		WHEN ResolutionHours < 12 THEN 'Fast'
		WHEN ResolutionHours <=24 THEN 'Normal'
	ELSE 'Slow' END
ORDER BY TicketCount DESC;

SELECT
	CASE WHEN ResolutionHours < 12 THEN 'Fast'
	WHEN ResolutionHours <= 24 THEN 'Normal'
	ELSE 'Slow' END AS ResolutionCategory,
	COUNT(*) AS TicketCount,
	SUM(CASE WHEN SLAMet = 1 THEN 1 ELSE 0 END) AS SLAMetCount,
	ROUND(100.0 * SUM(CASE WHEN SLAMet = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS SLAPercentage
FROM dbo.Tickets
GROUP BY
	CASE WHEN ResolutionHours < 12 THEN 'Fast'
	WHEN ResolutionHours <= 24 THEN 'Normal'
	ELSE 'Slow' END
ORDER BY TicketCount DESC;

SELECT
	COUNT(*) as TotalTickets,
	SUM(CASE WHEN TRY_CONVERT(datetime2, CreatedAt) IS NULL THEN 1 ELSE 0 END) AS InvalidCreatedAt,
	SUM(CASE WHEN TRY_CONVERT(datetime2, FirstResponseAt) IS NULL THEN 1 ELSE 0 END) AS InvalidFirstResponseAt,
	SUM(CASE WHEN TRY_CONVERT(datetime2, ResolvedAt) IS NULL THEN 1 ELSE 0 END) AS InvalidResolvedAt
FROM dbo.Tickets;

SELECT
    COUNT(*) AS TotalTickets,
    SUM(CASE WHEN SLAMet = 1 THEN 1 ELSE 0 END) AS SLAMet,
    SUM(CASE WHEN SLAMet = 0 THEN 1 ELSE 0 END) AS SLABreached,
    CAST(
        100.0 * SUM(CASE WHEN SLAMet = 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0)
        AS DECIMAL(5, 2)
    ) AS SLACompliancePct
FROM dbo.Tickets;

--CTE Common Table Expression
WITH TicketAnalysis AS
	(
	SELECT
		TicketID,
		ResolutionHours,
		SLAMet,
		CASE WHEN ResolutionHours < 12 THEN 'Fast'
		WHEN ResolutionHours <= 24 THEN 'Normal'
		ELSE 'Slow' END AS ResolutionCategory
	FROM dbo.Tickets
)
SELECT
	ResolutionCategory,
	COUNT(*) AS TicketCount,
	SUM(CASE WHEN SLAMet = 1 THEN 1 ELSE 0 END) AS SLAMetCount,
	ROUND(100.0 * SUM(CASE WHEN SLAMet = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS SLAPercentage
FROM TicketAnalysis
GROUP BY ResolutionCategory
ORDER BY TicketCount DESC;

WITH DepartmentAnalysis AS
(
	SELECT
		d.DepartmentID,
		d.DepartmentName,
		COUNT(*) AS TicketCount,
		ROUND(AVG(t.ResolutionHours),2) AS AvgResolutionHours,
		ROUND(100.0 * SUM(CASE WHEN t.SLAMet = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS SLAPercentage
	FROM Tickets as t
	INNER JOIN Departments as d
		ON t.DepartmentID = d.DepartmentID
		GROUP BY d.DepartmentID, d.DepartmentName
	)
SELECT 
	DepartmentName,
	TicketCount,
	AvgResolutionHours,
	SLAPercentage,
	RANK() OVER (ORDER BY SLAPercentage DESC) AS SLARank
FROM DepartmentAnalysis;


WITH EmployeeAnalysis AS
(
	SELECT 
		e.EmployeeID,
		e.EmployeeName,
		COUNT(*) AS TicketCount,
		ROUND(AVG(t.ResolutionHours),2) AS EmployeeAvgResolution
	FROM dbo.Tickets AS t
	INNER JOIN dbo.Employees AS e
		ON t.EmployeeID = e.EmployeeID
		GROUP BY e.EmployeeID, e.EmployeeName
),
OverAllAnalysis AS
(
	SELECT
		ROUND(AVG(ResolutionHours),2) AS OverallAvgResolution
	FROM dbo.Tickets
)
SELECT
	e.EmployeeName,
	e.TicketCount,
	e.EmployeeAvgResolution,
	o.OverallAvgResolution,
	ROUND(e.EmployeeAvgResolution - o.OverallAvgResolution,2) AS DifferenceFromOverall
FROM EmployeeAnalysis as e
CROSS JOIN OverAllAnalysis as o;

--Window Functions
SELECT
	TicketID,
	ResolutionHours,
	Avg(ResolutionHours) OVER() AS OverallAvgResolution
FROM dbo.Tickets;

WITH EmployeeAnalysis AS
(
SELECT
	e.EmployeeID,
	e.EmployeeName,
	COUNT(*) AS TicketCount,
	AVG(t.ResolutionHours) AS EmployeeAvgResolution
FROM dbo.Tickets AS t
INNER JOIN dbo.Employees AS e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName
)
SELECT
	EmployeeName,
	TicketCount,
	ROUND(EmployeeAvgResolution,2) AS EmployeeAvgResolution,
	ROUND(AVG(EmployeeAvgResolution) OVER(),2) AS OverallEmployeeResolution
FROM EmployeeAnalysis;

WITH EmployeeAnalysis AS
(
SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	d.DepartmentName,
	AVG(t.ResolutionHours) AS EmployeeAvgResolution
FROM dbo.Tickets AS t
INNER JOIN dbo.Departments AS d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees AS e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName, e.DepartmentID, d.DepartmentName
),
DepartmentAnalysis AS
(
SELECT
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
	ROUND(AVG(EmployeeAvgResolution) OVER(PARTITION BY DepartmentID),2) AS DepartmentAvgResolution
FROM EmployeeAnalysis
)
SELECT
	EmployeeName,
	DepartmentName,
	ROUND(EmployeeAvgResolution,2) AS EmployeeAvgResolution,
	ROUND(DepartmentAvgResolution,2) AS DepartmentAvgResolution,
	ROUND(EmployeeAvgResolution - DepartmentAvgResolution,2) AS DifferenceFromDepartment
FROM DepartmentAnalysis;

--RANK()
WITH EmployeeAnalysis AS
(
SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	d.DepartmentName,
	AVG(t.ResolutionHours) AS EmployeeAvgResolution
FROM dbo.Tickets AS t
INNER JOIN dbo.Departments AS d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees AS e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName, e.DepartmentID, d.DepartmentName
),
DepartmentAnalysis AS
(
SELECT
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
--	ROUND(AVG(EmployeeAvgResolution) OVER(PARTITION BY DepartmentID),2) AS DepartmentAvgResolution
	RANK() OVER(PARTITION BY DepartmentID ORDER BY EmployeeAvgResolution ASC) AS DepartmentRank
FROM EmployeeAnalysis
)
SELECT
	EmployeeName,
	DepartmentName,
	ROUND(EmployeeAvgResolution,2) AS EmployeeAvgResolution,
	--ROUND(DepartmentAvgResolution,2) AS DepartmentAvgResolution,
	--ROUND(EmployeeAvgResolution - DepartmentAvgResolution,2) AS DifferenceFromDepartment
	DepartmentRank
FROM DepartmentAnalysis;

WITH MonthlyDepartmentTickets AS
(
SELECT
	DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1) AS [Month],
	d.DepartmentName,
	COUNT(*) AS TicketCount
FROM dbo.Tickets AS t
INNER JOIN dbo.Departments AS d
	ON t.DepartmentID = d.DepartmentID
	GROUP BY DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1), d.DepartmentName
),
DepartmentTickets AS
(
SELECT
 [Month],
 DepartmentName,
 TicketCount,
 RANK() OVER(PARTITION BY [Month] ORDER BY TicketCount DESC) AS [Rank]
FROM MonthlyDepartmentTickets
)
SELECT
[Month],
DepartmentName,
TicketCount,
[Rank]
FROM DepartmentTickets
WHERE [Rank] = 1;

WITH EmployeeMonthlyTicket AS
(
SELECT
	DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1) AS [Month],
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	d.DepartmentName,
	ROUND(AVG(t.ResolutionHours), 2) AS EmployeeAvgResolution
FROM dbo.Tickets as t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1), 
	e.EmployeeID, e.EmployeeName,e.DepartmentID, d.DepartmentName
),
RankedEmployees AS
(
SELECT
	[Month],
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
	RANK() OVER(PARTITION BY [Month] ORDER BY EmployeeAvgResolution DESC) AS [Rank]
FROM EmployeeMonthlyTicket
)
SELECT
	[Month],
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
	[Rank]
	FROM RankedEmployees
	WHERE [Rank] <= 3
	ORDER BY [Month], [Rank];

WITH EmployeeMonthlyTicket AS
(
SELECT
	DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1) AS [Month],
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	d.DepartmentName,
	ROUND(AVG(t.ResolutionHours), 2) AS EmployeeAvgResolution
FROM dbo.Tickets as t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1), 
	e.EmployeeID, e.EmployeeName,e.DepartmentID, d.DepartmentName
),
RankedEmployees AS
(
SELECT
	[Month],
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
	RANK() OVER(PARTITION BY [Month] ORDER BY EmployeeAvgResolution DESC) AS [Rank],
	ROUND(AVG(EmployeeAvgResolution) OVER(PARTITION BY [Month], DepartmentID),2) AS DepartmentAvgResolution
FROM EmployeeMonthlyTicket
)
SELECT
	[Month],
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
	DepartmentAvgResolution,
	ROUND((EmployeeAvgResolution - DepartmentAvgResolution) * 100.0 / DepartmentAvgResolution, 2) DifferencePercent,
	[Rank]
	FROM RankedEmployees
	ORDER BY [Month], [Rank];

	
WITH EmployeeMonthlyTicket AS
(
SELECT
	DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1) AS [Month],
	e.EmployeeID,
	e.EmployeeName,
	d.DepartmentName,
	COUNT(*) AS EmployeeTicketCounts
FROM dbo.Tickets as t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1), 
	e.EmployeeID, e.EmployeeName, d.DepartmentName
),
RankedEmployees AS
(
SELECT
	[Month],
	EmployeeName,
	DepartmentName,
	EmployeeTicketCounts,
	SUM(EmployeeTicketCounts) OVER(PARTITION BY [Month], DepartmentName) AS DepartmentTicketCounts,
	RANK() OVER(
            PARTITION BY [Month], DepartmentName
            ORDER BY EmployeeTicketCounts DESC
        ) AS EmployeeRank
FROM EmployeeMonthlyTicket
)
SELECT
	[Month],
	EmployeeName,
	DepartmentName,
	EmployeeTicketCounts,
	DepartmentTicketCounts,
	ROUND(EmployeeTicketCounts * 100.0 / NULLIF(DepartmentTicketCounts, 0),2
) AS ContributionPercent,
	EmployeeRank
	FROM RankedEmployees
	WHERE EmployeeRank = 1
	ORDER BY [Month], DepartmentName, EmployeeRank;

WITH EmployeeMonthlyTicket AS
(
SELECT
	DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1) AS [Month],
	e.EmployeeID,
	e.EmployeeName,
	d.DepartmentName,
	COUNT(*) AS EmployeeTickets
FROM dbo.Tickets as t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1), 
	e.EmployeeID, e.EmployeeName, d.DepartmentName
),
RankedEmployees AS
(
SELECT
	[Month],
	DepartmentName,
	EmployeeName,
	EmployeeTickets,
	SUM(EmployeeTickets) OVER(PARTITION BY [Month], DepartmentName) AS DepartmentTickets,
	RANK() OVER(
            PARTITION BY [Month], DepartmentName
            ORDER BY EmployeeTickets DESC
        ) AS EmployeeRank
FROM EmployeeMonthlyTicket
)
SELECT
	[Month],
	DepartmentName,
	EmployeeName,
	EmployeeTickets,
	DepartmentTickets,
	ROUND(EmployeeTickets * 100.0 / NULLIF(DepartmentTickets, 0),2
) AS ContributionPercent,
	EmployeeRank
	FROM RankedEmployees
	ORDER BY [Month], DepartmentName, EmployeeRank;

--DENSE_RANK()
WITH EmployeeAnalysis AS
(
SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	d.DepartmentName,
	AVG(t.ResolutionHours) AS EmployeeAvgResolution
FROM dbo.Tickets AS t
INNER JOIN dbo.Departments AS d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees AS e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName, e.DepartmentID, d.DepartmentName
),
DepartmentAnalysis AS
(
SELECT
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
--	ROUND(AVG(EmployeeAvgResolution) OVER(PARTITION BY DepartmentID),2) AS DepartmentAvgResolution
	DENSE_RANK() OVER(PARTITION BY DepartmentID ORDER BY EmployeeAvgResolution ASC) AS DepartmentRank
FROM EmployeeAnalysis
)
SELECT
	EmployeeName,
	DepartmentName,
	ROUND(EmployeeAvgResolution,2) AS EmployeeAvgResolution,
	--ROUND(DepartmentAvgResolution,2) AS DepartmentAvgResolution,
	--ROUND(EmployeeAvgResolution - DepartmentAvgResolution,2) AS DifferenceFromDepartment
	DepartmentRank
FROM DepartmentAnalysis;

--ROW_NUMBER()
WITH EmployeeAnalysis AS
(
SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	d.DepartmentName,
	AVG(t.ResolutionHours) AS EmployeeAvgResolution
FROM dbo.Tickets AS t
INNER JOIN dbo.Departments AS d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees AS e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName, e.DepartmentID, d.DepartmentName
),
DepartmentAnalysis AS
(
SELECT
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
--	ROUND(AVG(EmployeeAvgResolution) OVER(PARTITION BY DepartmentID),2) AS DepartmentAvgResolution
	ROW_NUMBER() OVER(PARTITION BY DepartmentID ORDER BY EmployeeAvgResolution ASC) AS DepartmentRank
FROM EmployeeAnalysis
)
SELECT
	EmployeeName,
	DepartmentName,
	ROUND(EmployeeAvgResolution,2) AS EmployeeAvgResolution,
	--ROUND(DepartmentAvgResolution,2) AS DepartmentAvgResolution,
	--ROUND(EmployeeAvgResolution - DepartmentAvgResolution,2) AS DifferenceFromDepartment
	DepartmentRank
FROM DepartmentAnalysis;

--TEST Data
WITH TestData AS
(
    SELECT *
    FROM (VALUES
        ('Employee A', 10),
        ('Employee B', 20),
        ('Employee C', 20),
        ('Employee D', 30)
    ) AS x(EmployeeName, Score)
)
SELECT
    EmployeeName,
    Score,
    ROW_NUMBER() OVER(ORDER BY Score) AS RowNumber,
    RANK() OVER(ORDER BY Score) AS RankNumber,
    DENSE_RANK() OVER(ORDER BY Score) AS DenseRank
FROM TestData;