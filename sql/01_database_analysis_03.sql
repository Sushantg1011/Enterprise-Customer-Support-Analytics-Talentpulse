USE EnterpriseCustomerSupport;

--LAG()

WITH EmployeeAnalysis AS
(
SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	d.DepartmentName,
	ROUND(AVG(t.ResolutionHours), 2) AS EmployeeAvgResolution
FROM dbo.Tickets AS t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName, e.DepartmentID, d.DepartmentName
),
LagAnalysis AS
(
SELECT
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
	LAG(EmployeeAvgResolution) OVER(PARTITION BY DepartmentID ORDER BY EmployeeAvgResolution ASC, EmployeeID) 
	AS PreviousEmployeeAvg
FROM EmployeeAnalysis
)
SELECT
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
	PreviousEmployeeAvg,
	ROUND(EmployeeAvgResolution - PreviousEmployeeAvg, 2) AS DifferenceFromPrevious,
	ROUND(100.0 * (EmployeeAvgResolution - PreviousEmployeeAvg) / NULLIF(PreviousEmployeeAvg, 0), 2) 
	AS PercentageDifference
FROM LagAnalysis;

WITH MonthlyTickets AS
(
SELECT
	DATEFROMPARTS(YEAR(CreatedAt), MONTH(CreatedAt),1) AS Months,
	COUNT(*) AS TicketCount,
	LAG(COUNT(*)) OVER(ORDER BY DATEFROMPARTS(YEAR(CreatedAt), MONTH(CreatedAt),1)) 
	AS PreviousMonthTickets
FROM dbo.Tickets
GROUP BY DATEFROMPARTS(YEAR(CreatedAt), MONTH(CreatedAt),1)
)
SELECT
	Months,
	TicketCount,
	PreviousMonthTickets,
	CAST(
	ROUND(
	(TicketCount - PreviousMonthTickets) * 100.0 
	/ NULLIF(PreviousMonthTickets, 0),
	2) AS DECIMAL(10,2)
	) AS MoMChange
FROM MonthlyTickets;

WITH DepartmentMonthlyTickets AS
(
SELECT
	DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1) AS [Month],
	d.DepartmentName,
	COUNT(*) AS TicketCount,
	LAG(COUNT(*)) 
	OVER(PARTITION BY d.DepartmentName ORDER BY DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1)) 
	AS PreviousMonthTicket
FROM dbo.Tickets as t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
	GROUP BY DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1), d.DepartmentName
),
LagPercentage AS
(
SELECT
	[Month],
	DepartmentName,
	TicketCount,
	PreviousMonthTicket,
	CAST(ROUND((TicketCount - PreviousMonthTicket) * 100.0 / NULLIF(PreviousMonthTicket, 0), 2) 
	AS decimal(10,2)) AS MOMChangePercent
FROM DepartmentMonthlyTickets
)
SELECT
	[Month],
	DepartmentName,
	TicketCount,
	PreviousMonthTicket,
	MOMChangePercent
FROM LagPercentage;

WITH EmployeeMonthlyTicket AS
(
SELECT
	DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1) AS [Month],
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	d.DepartmentName,
	COUNT(*) AS TicketCount,
	LAG(COUNT(*)) OVER(PARTITION BY e.EmployeeID ORDER BY DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1)) 
	AS PreviousMonthTickets
FROM dbo.Tickets as t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1), 
	e.EmployeeID, e.EmployeeName,e.DepartmentID, d.DepartmentName
),
PercentageAnalysis AS
(
SELECT
	[Month],
	EmployeeID,
	EmployeeName,
	DepartmentID,
	DepartmentName,
	TicketCount,
	PreviousMonthTickets,
	CAST(ROUND((TicketCount - PreviousMonthTickets) * 100.0 / NULLIF(PreviousMonthTickets, 0), 2) 
	AS decimal(10,2)) AS MOMChangePercent
FROM EmployeeMonthlyTicket
)
SELECT
	[Month],
	EmployeeName,
	DepartmentName,
	TicketCount,
	PreviousMonthTickets,
	MOMChangePercent
FROM PercentageAnalysis;

WITH DepartmentMonthlyTicket AS
(
SELECT
	DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1) AS [Month],
	d.DepartmentName,
	COUNT(*) AS DepartmentTicketCount,
	ROUND(AVG(t.ResolutionHours), 2) AS DepartmentAvgResolution
FROM dbo.Tickets as t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
	GROUP BY DATEFROMPARTS(YEAR(t.CreatedAt), MONTH(t.CreatedAt), 1), d.DepartmentName
),
PreviousDepartmentAnalysis AS
(
SELECT
	[Month],
	DepartmentName,
	DepartmentTicketCount,
	DepartmentAvgResolution,
	LAG(DepartmentTicketCount) OVER(PARTITION BY DepartmentName ORDER BY [Month]) AS PreviousMonthTicket,
	RANK() OVER(
            PARTITION BY [Month]
            ORDER BY DepartmentTicketCount DESC
        ) AS DepartmentRank
FROM DepartmentMonthlyTicket
)
SELECT
	[Month],
	DepartmentName,
	DepartmentTicketCount,
	DepartmentAvgResolution,
	PreviousMonthTicket,
	CAST(ROUND((DepartmentTicketCount - PreviousMonthTicket) * 100.0 / NULLIF(PreviousMonthTicket, 0), 2) 
	AS decimal(10,2)) AS MOMChangePercent,
	DepartmentRank
	FROM PreviousDepartmentAnalysis
	ORDER BY [Month], DepartmentRank;

--LEAD()
WITH EmployeeAnalysis AS
(
SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	d.DepartmentName,
	ROUND(AVG(t.ResolutionHours), 2) AS EmployeeAvgResolution
FROM dbo.Tickets AS t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName, e.DepartmentID, d.DepartmentName
),
LeadAnalysis AS
(
SELECT
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
	LEAD(EmployeeAvgResolution) OVER(PARTITION BY DepartmentID ORDER BY EmployeeAvgResolution ASC, EmployeeID) 
	AS NextEmployeeAvg
FROM EmployeeAnalysis
)
SELECT
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
	NextEmployeeAvg,
	ROUND(ABS(EmployeeAvgResolution - NextEmployeeAvg), 2) AS DifferenceFromNext,
	ROUND(100.0 * (EmployeeAvgResolution - NextEmployeeAvg) / NULLIF(NextEmployeeAvg, 0), 2) 
	AS PercentageDifference
FROM LeadAnalysis
WHERE NextEmployeeAvg is NOT NULL
ORDER BY DifferenceFromNext DESC;

--NTILE()
WITH EmployeeAnalysis AS
(
SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	d.DepartmentName,
	ROUND(AVG(t.ResolutionHours), 2) AS EmployeeAvgResolution
FROM dbo.Tickets AS t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName, e.DepartmentID, d.DepartmentName
)
SELECT
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
	NTILE(4) OVER(PARTITION BY DepartmentID ORDER BY EmployeeAvgResolution ASC) AS ResolutionQuartile
FROM EmployeeAnalysis
ORDER BY DepartmentName, ResolutionQuartile, EmployeeAvgResolution


--FIRST_VALUE()
WITH EmployeeAnalysis AS
(
SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	d.DepartmentName,
	ROUND(AVG(t.ResolutionHours), 2) AS EmployeeAvgResolution
FROM dbo.Tickets AS t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName, e.DepartmentID, d.DepartmentName
)
SELECT
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
	FIRST_VALUE(EmployeeName) OVER(PARTITION BY DepartmentID ORDER BY EmployeeAvgResolution ASC, EmployeeID) 
	AS FastestEmployee,
	FIRST_VALUE(EmployeeAvgResolution) OVER(PARTITION BY DepartmentID ORDER BY EmployeeAvgResolution ASC, EmployeeID) 
	AS FastestResolution,
	ROUND(EmployeeAvgResolution - 
		FIRST_VALUE(EmployeeAvgResolution) OVER(PARTITION BY DepartmentID ORDER BY EmployeeAvgResolution ASC),
		2) AS DifferenceFromFastest
FROM EmployeeAnalysis
ORDER BY DepartmentName, EmployeeAvgResolution


--LAST_VALUE()
WITH EmployeeAnalysis AS
(
SELECT
	e.EmployeeID,
	e.EmployeeName,
	e.DepartmentID,
	d.DepartmentName,
	ROUND(AVG(t.ResolutionHours), 2) AS EmployeeAvgResolution
FROM dbo.Tickets AS t
INNER JOIN dbo.Departments as d
	ON t.DepartmentID = d.DepartmentID
INNER JOIN dbo.Employees as e
	ON t.EmployeeID = e.EmployeeID
	GROUP BY e.EmployeeID, e.EmployeeName, e.DepartmentID, d.DepartmentName
)
SELECT
	EmployeeName,
	DepartmentName,
	EmployeeAvgResolution,
	LAST_VALUE(EmployeeName) OVER(PARTITION BY DepartmentID ORDER BY EmployeeAvgResolution ASC, EmployeeID
		ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS SlowestEmployee,
	LAST_VALUE(EmployeeAvgResolution) OVER(PARTITION BY DepartmentID ORDER BY EmployeeAvgResolution ASC, EmployeeID
	ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS SlowestResolution,
	ROUND(LAST_VALUE(EmployeeAvgResolution) OVER(PARTITION BY DepartmentID ORDER BY EmployeeAvgResolution ASC, EmployeeID
		ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) - EmployeeAvgResolution,
		2) AS DifferenceFromSlowest
FROM EmployeeAnalysis
ORDER BY DepartmentName, EmployeeAvgResolution

--SUM() OVER()
SELECT
	CAST(CreatedAt AS DATE) AS TicketDate,
	COUNT(*) AS TicketCount,
	SUM(COUNT(*)) OVER(ORDER BY CAST(CreatedAt AS DATE)) AS CumulativeTickets
FROM dbo.Tickets
GROUP BY CAST(CreatedAt AS DATE)
ORDER BY TicketDate;

