-- it is help to move to the database
USE EnterpriseCustomerSupport;

-- it is use to check the current database
SELECT DB_NAME() AS CurrentDatabase;

--Departments
CREATE TABLE dbo.Departments
(
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL
);


--Categories
CREATE TABLE dbo.Categories
(
	CategoryID INT PRIMARY KEY,
	CategoryName VARCHAR(100) NOT NULL,
	Complexity VARCHAR(20) NOT NULL,
	DepartmentID INT NOT NULL,	
	CONSTRAINT FK_Categories_Departments
		FOREIGN KEY (DepartmentID)
		REFERENCES dbo.Departments(DepartmentID)
);

--Customers
CREATE TABLE dbo.Customers
(
	CustomerID INT PRIMARY KEY,
	CustomerName VARCHAR(200) NOT NULL,
	Industry VARCHAR(100) NOT NULL,
	Country VARCHAR(100) NOT NULL,
	[Plan] VARCHAR(20) NOT NULL
);

--Employees
CREATE TABLE dbo.Employees
(
	EmployeeID INT PRIMARY KEY,
	EmployeeName VARCHAR(200) NOT NULL,
	DepartmentID INT NOT NULL,
	ExperienceYears INT NOT NULL
);

--Statuses
CREATE TABLE dbo.Statuses
(
	StatusID INT PRIMARY KEY,
	StatusName VARCHAR(50) NOT NULL
);

--Tickets
CREATE TABLE dbo.Tickets
(
    TicketID INT PRIMARY KEY,

	CreatedAt DATETIME2 NOT NULL,
	FirstResponseAt DATETIME2 NOT NULL,
	FirstResponseHours DECIMAL(10,4) NOT NULL,
	FirstResponseSLAMet BIT NOT NULL,

	ResolvedAt DATETIME2 NOT NULL,
    ResolutionHours DECIMAL(10,4) NULL,

    CustomerID INT NOT NULL,
    CategoryID INT NOT NULL,
    DepartmentID INT NOT NULL,
    EmployeeID INT NOT NULL,

    ExperienceLevel VARCHAR(20) NOT NULL,
    Priority VARCHAR(20) NOT NULL,
    SLAHours INT NOT NULL,
    SLAMet BIT NOT NULL,

    Complexity VARCHAR(20) NOT NULL,
    Lifecycle VARCHAR(30) NOT NULL
);

-- to check the table name
SELECT TABLE_NAME, TABLE_SCHEMA
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;

--Verify each table
SELECT COUNT(*) AS TicketCount FROM Tickets;

SELECT COUNT(*) AS CustomerCount FROM Customers;

SELECT COUNT(*) AS EmployeeCount FROM Employees;

SELECT COUNT(*) AS CategoryCount FROM Categories;

SELECT TOP 5 * FROM Tickets;
SELECT TOP 5 * FROM Customers;

