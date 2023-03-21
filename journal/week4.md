# Week 4 — Postgres and RDS

## Provision an RDS instance 
*This might take about 10-15 minutes, so i'd like to start it up first*

- I ran this command in the terminal 

```
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username crudderroot \
  --master-user-password generalt666. \
  --allocated-storage 20 \
  --availability-zone us-east-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
```
- I got a json output which was a sign that it has probably started working. 



- I went to my aws management console and searched RDS to see if the instance is in creation mode.  



- I went to my docker-compose file to make sure the database commands are still there.  
*I commented out my dynamoDB lin because i don't presently need it*  

- I composed up and started my containers.  

- While my containers where being created i went to check if my RDS was available.  



- I stopped the instance because i don't need it right now and i want to prevent spend.   
*you can only temporarily stop for 7days so i'll be sure to not forget about the instance and come back to it when i need it*  


- Checked if my pg container is running now.  


- I made sure i can connect to my pg instance so i used psql. i copied the code below to my terminal.  
```
psql -Upostgres --host localhost
```



*It prompted me for a password and the password is "password".*   

- I ran some PSQL command to test it out. Below is a list of SQL commands and what they do.  

```
\x on -- expanded display when looking at data
\q -- Quit PSQL
\l -- List all databases
\c database_name -- Connect to a specific database
\dt -- List all tables in the current database
\d table_name -- Describe a specific table
\du -- List all users and their roles
\dn -- List all schemas in the current database
CREATE DATABASE database_name; -- Create a new database
DROP DATABASE database_name; -- Delete a database
CREATE TABLE table_name (column1 datatype1, column2 datatype2, ...); -- Create a new table
DROP TABLE table_name; -- Delete a table
SELECT column1, column2, ... FROM table_name WHERE condition; -- Select data from a table
INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...); -- Insert data into a table
UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition; -- Update data in a table
DELETE FROM table_name WHERE condition; -- Delete data from a table
```  

- I ran the `\l` command to show a list of the current databases.   


> _Note_ When setting up your database from the CLI next time, don't forget to specify your character encoding. I didn't set this now because i'm just testing it out, but if it causes problems later on, i'll do that.  Also set timezone.    

### Create a database 
```
CREATE database cruddur;
``` 
- I created a database named **"Crudder"** and ran the command for listing databases, to confirm its creation.  


### Import Script 
- I created a new SQL file called **schema.sql** and i placed it in **backend-flask/db**.   



#### Add UUID extension 
```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```
I added this command to my **"schema.sql"** file.  

- I ran \q to quit postgres from the terminal. I made sure i was in my backend directory and i ran this code  
```
psql cruddur < db/schema.sql -h localhost -U postgres
```

#### Setting a connection URL string
```
psql postgresql://postgres:password@localhost:5432/cruddur
```
- I ran the command above in my terminal and it opened up my **cruddur** database. Now i'm going to exit the postgres terminal and set it as an environment variable.   

```
export CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"
```
- I typed psql CONNECTION_URL and i was connected to the crudder database.  

- I set it to persist in gitpod environment, so i don't have to set it again.  
```
gp env CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"
``` 

#### Setting a production URL string 
```
PROD_CONNECTION_URL="postgresql://crudderroot:generalt666.@cruddur-db-instance.cjpatr1usl1t.us-east-1.rds.amazonaws.com:5432/cruddur"
``` 
- I ran this command in my terminal. The endpoint detail is gotting from the RDS **connectivity and security** section.  

