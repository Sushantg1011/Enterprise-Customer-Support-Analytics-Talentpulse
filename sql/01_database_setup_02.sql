-- it is help to move to the database
USE EnterpriseCustomerSupport;

--Check total rows
SELECT COUNT(*) AS Tickets_Count FROM dbo.Tickets
SELECT COUNT(*) AS Import_Count FROM dbo.Tickets_Import;

--Check the imported data
SELECT TOP 5 * FROM dbo.Tickets_Import;
SELECT COUNT(*) AS CustomerCount FROM dbo.Customers
SELECT TOP 10 * FROM dbo.Customers;
SELECT COUNT(*)	AS EmployeeCount from dbo.Employees
SELECT TOP 10 * FROM dbo.Employees
SELECT * FROM dbo.Departments_Import
SELECT * FROM dbo.Departments
SELECT * FROM dbo.Categories
SELECT * FROM dbo.Statuses

--Move the data into different table
INSERT INTO dbo.Departments
	(DepartmentID, DepartmentName)
SELECT
	DepartmentID,
	DepartmentName
FROM dbo.Departments_Import

--Check the date columns
SELECT TOP 10 CreatedAt, FirstResponseAt, ResolvedAt FROM dbo.Tickets_Import;

--CAST() converts one data type into another.
--TRY_CAST() If conversion works → returns the date. If conversion fails → returns NULL
SELECT TOP 10 CreatedAt, TRY_CAST(CreatedAt AS datetime2) AS CreatedAt_Converted
FROM dbo.Tickets_Import;

--Delete Table
DROP TABLE dbo.Tickets;
DROP TABLE dbo.Customers
DROP TABLE dbo.Employees
DROP TABLE dbo.Departments_Import;
DROP TABLE dbo.Categories
DROP TABLE dbo.Statuses

--Rename Table
EXEC sp_rename 'dbo.Tickets_Import', 'Tickets';
EXEC sp_rename 'dbo.Employees_import', 'Employees';


