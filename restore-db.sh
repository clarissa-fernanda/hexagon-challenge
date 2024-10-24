#!/bin/bash

# Download the .bak file (replace URL with the actual location of your file)
wget -O /var/opt/mssql/AdventureWorks2019.bak https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorks2019.bak

# Wait for SQL Server to start
sleep 30s

# Connect to SQL Server and restore the AdventureWorks2019 database
/opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P "YourStrong!Passw0rd" -C -Q "RESTORE DATABASE AdventureWorks2019 FROM DISK = '/var/opt/mssql/AdventureWorks2019.bak' WITH MOVE 'AdventureWorks2019' TO '/var/opt/mssql/data/AdventureWorks2019.mdf', MOVE 'AdventureWorks2019_log' TO '/var/opt/mssql/data/AdventureWorks2019.ldf'"