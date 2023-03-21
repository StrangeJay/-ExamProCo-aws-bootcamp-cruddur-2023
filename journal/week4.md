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
  --master-user-password <password> \
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
- I created a database named **"Cruddur"** and ran the command for listing databases, to confirm its creation.  


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
PROD_CONNECTION_URL="postgresql://crudderroot:generalt666.@<RDS endpoint>:5432/cruddur"
``` 
- I ran this command in my terminal. The endpoint detail is gotten from the RDS **connectivity and security** section.  


#### Easing the DB processes, 
- I created a new folder in the backend directory called **"bin"**. *Bin stands for Binary. This is where i'll save all my bash scripts*. Inside the bin directory i'll  create 3 files named **"db-create"**, **"db-drop"**, **"db-schema-load"**.   

- I opened the db-drop file, found out where bash is in my terminal and used it to add my SHEBANG.  

- I want to create a script that would allow me drop the database easily, the created bin files do not have execute permission so i have to give it to them by running "chmod u+x bin/db-create", "chmod u+x bin/db-drop", "chmod u+x bin/db-schema-drop" 



- I coied the line of code below to my **db-drop** file  
```
#! /usr/bin/bash

echo "db-drop"

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "DROP database cruddur;"  
```  

and i ran it on my terminal with `./bin/db-drop` and the database was dropped.  



- I went to the **db-create** file, and copied the code below into it.  
```
#!/usr/bin/bash

echo "db-create" 

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "CREATE database cruddur;"
```

- I executed the script by running `.bin/db-create` in my terminal.   



- I went to my **schema-load** file, and copied the code below into it. 

``` 
#!/usr/bin/bash

echo "db-schema-load"

schema_path="$(realpath .)/db/schema.sql"
echo $schema_path

psql $CONNECTION_URL cruddur < $schema_path
```

- I executed the script by running `./bin/db-schema-load` in my terminal. and it worked.  




- Now, i want to make sure this script can be executed from any directory, so i changed back to my root directory, and ran the script with `./backend-flask/bin/db-schema-load` and i got an error saying "No such file or directory".  



- I'll figure it out later, for now it works in the backend directory so i'll have to stick to that.  


- I want to write an if statement in my **db-schema-load** file, that allows me toggle between local mode and production mode.  I went back to my backend-flask directory, i copied the code below into the **db-schema-load** file.  

```
if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi
```

- I executed it by running `./bin/db-schema-load prod`  



- It's not connecting to production because we're presently not running it, so i got this error message after a period of it hanging.  

> _Note_ Whenever you see something hanging, it's usually because of connection issues.  


##### Colour coding my scripts 
- I added the line of code below to my **schema-load** file. 
```
GREEN='\033[1;32m'
NO_COLOR='\033[0m'
LABEL="db-schema-load"
printf "${GREEN}== ${LABEL}${NO_COLOR}\n"
```
And i got this colour after executing the script. 



- I did a different color for the other 2 files.   



---
## Creating Tables
[Helpful doc for learning how to create tables](https://www.postgresql.org/docs/current/sql-createtable.html)  

- I went to my **schema.sql** file, and i pasted the following code below there.  
```
CREATE TABLE public.users (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text,
  handle text
  cognito_user_id text,
  created_at TIMESTAMP default current_timestamp NOT NULL
);

CREATE TABLE public.activities (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  message text NOT NULL,
  replies_count integer DEFAULT 0,
  reposts_count integer DEFAULT 0,
  likes_count integer DEFAULT 0,
  reply_to_activity_uuid integer,
  expires_at TIMESTAMP,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
``` 



- If i run this code twice, it'll create problems, so i added commands to drop the table if they already exist before creating them again.  
```
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;
```

- I ran them with `./bin/db-schema-load`  



- I kept getting an error saying 
*"psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
        Is the server running locally and accepting connections on that socket?"*  

- I went back to my **db-schema-load** file and realised there was a typo, i fixed that and tried again and it worked this time.  




- I created a new file for connection. "db-connect", and i gave it execute privileges with `chmod u+x .bin/db-connect`  
and i ran it with `./bin/db-connect`  



- I wanted to see my tables so i ran the `\dt` command to confirm the existence of my table.  



- I created a db-seed file.  





- Created another file in the db directory named **seed.sql**  




- It didn't run so i went to my **schema.sql** and added the user uuid, i ran my schema with `./bin/db-schema-load` then i ran the seed again with `./bin/db-seed`and it works now.  



