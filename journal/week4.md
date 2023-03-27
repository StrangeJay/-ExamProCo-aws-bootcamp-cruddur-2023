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
![output for cli db run](https://user-images.githubusercontent.com/105195327/226775503-77ae4e6c-38d6-4e1e-aaba-403c9a8539b1.png)   

- I went to my aws management console and searched RDS to see if the instance is in creation mode.  
![db creation in console](https://user-images.githubusercontent.com/105195327/226775536-cf94ad82-6c95-4069-b8db-b514428e844f.png)  

- I went to my [docker-compose file](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/docker-compose.yml) to make sure the database commands are still there.  
*I commented out my dynamoDB line because i don't presently need it*  
![db in dockercompose](https://user-images.githubusercontent.com/105195327/226775634-5cef7b7f-c708-4826-83ad-4d85a8ee51a2.png)   

- I composed up and started my containers.  

- While my containers where being created i went to check if my RDS was available.  
![RDS running in console](https://user-images.githubusercontent.com/105195327/226775658-f5dc558b-b546-46f1-a388-b86a68a6f41d.png)   

- I stopped the instance because i don't need it right now and i want to prevent spend.   
*you can only temporarily stop for 7days so i'll be sure to not forget about the instance and come back to it when i need it*  
![stop rds instance](https://user-images.githubusercontent.com/105195327/226775729-0a056fbc-2661-4bea-b309-b2b7ea252fca.png)   

- Checked if my pg container is running now.  
![running pg container](https://user-images.githubusercontent.com/105195327/226775781-8d8400b1-44d7-4e65-af2e-1e4042acba6c.png)  

- I made sure i can connect to my pg instance so i used psql. i copied the code below to my terminal.  
```
psql -Upostgres --host localhost
```

![psql login](https://user-images.githubusercontent.com/105195327/226775836-bd7424a1-279a-486d-8775-447d8c2a8f2c.png)  

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
![list of pg databases](https://user-images.githubusercontent.com/105195327/226775867-04c2fd82-113c-4f04-bf6c-99dcf58f3a93.png)   

> **Note** When setting up your database from the CLI next time, don't forget to specify your character encoding. I didn't set this now because i'm just testing it out, but if it causes problems later on, i'll do that.  Also set timezone.    

---
### Create a database 
```
CREATE database cruddur;
``` 
- I created a database named **"Cruddur"** and ran the command for listing databases, to confirm its creation.  
![created db 1st](https://user-images.githubusercontent.com/105195327/226776281-3edc7d9a-2434-4810-b70d-5ec5e7522100.png)  

![created db](https://user-images.githubusercontent.com/105195327/226776057-904f849b-a759-4dc1-a7cf-23599f418db9.png)   


### Import Script 
- I created a new SQL file called [**schema.sql**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/db/schema.sql) and i placed it in [**backend-flask/db**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/tree/main/backend-flask/db).   

#### Add UUID extension 
```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```
I added this command to my [**"schema.sql"**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/db/schema.sql) file.  

- I ran \q to quit postgres from the terminal. I made sure i was in my backend directory and i ran this code  
```
psql cruddur < db/schema.sql -h localhost -U postgres
```

#### Setting a connection URL string
```
psql postgresql://postgres:password@localhost:5432/cruddur
```
![crudder db](https://user-images.githubusercontent.com/105195327/226777603-542fea3f-c762-4dbb-a467-060e00201503.png)

- I ran the command above in my terminal and it opened up my **cruddur** database. Now i'm going to exit the postgres terminal and set it as an environment variable.   

```
export CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"
```
- I typed psql $CONNECTION_URL and i was connected to the cruddur database.  
![psql db connection](https://user-images.githubusercontent.com/105195327/226777886-4e6f0d3e-dbfd-4578-9388-15a9339dfec3.png)   

- I set it to persist in gitpod environment, so i don't have to set it again.  
```
gp env CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"
``` 

---
#### Setting a production URL string 
```
PROD_CONNECTION_URL="postgresql://crudderroot:<password>@<RDS endpoint>:5432/cruddur"
``` 
> **Note** Replace <password> with your RDS password, and <RDS endpoint> with your RDS endpoint.  
  *The endpoint detail is gotten from the RDS **"connectivity and security"** section.*  
  ![RDS endpoint cleaned](https://user-images.githubusercontent.com/105195327/226778632-774328be-e4b6-410e-a8e9-eb01830da68c.png)   

- I ran this command in my terminal. 

---
#### Automating the DB processes, 
- I created a new folder in the backend directory called **"bin"**. *Bin stands for Binary. This is where i'll save all my bash scripts*. Inside the bin directory i'll  create 3 files named **"db-create"**, **"db-drop"**, **"db-schema-load"**.   

- I opened the [db-drop file](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/db-drop), found out where bash is in my terminal and used it to add my SHEBANG.  
  ![whereis bash](https://user-images.githubusercontent.com/105195327/226778748-1b9e7f44-19f2-4c01-b200-f4818bf55a49.png)  

- I want to create a script that would allow me drop the database easily, the created bin files do not have execute permission so i have to give it to them by running "chmod u+x bin/db-create", "chmod u+x bin/db-drop", "chmod u+x bin/db-schema-load" 
![bin files with permission](https://user-images.githubusercontent.com/105195327/226778877-b04dca40-aebf-42ee-89cc-d93d50ab764b.png)  

- I copied the line of code below to my [**db-drop**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/db-drop) file  
```
#! /usr/bin/bash

echo "db-drop"

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "DROP database cruddur;"  
```  

and i ran it on my terminal with `./bin/db-drop` and the database was dropped.  
![drop database confirmed](https://user-images.githubusercontent.com/105195327/226779343-7945dd43-786d-45be-83b8-a7533fe7acc8.png)   

- I went to the [**db-create**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/db-create) file, and copied the code below into it.  
```
#!/usr/bin/bash

echo "db-create" 

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "CREATE database cruddur;"
```

- I executed the script by running `.bin/db-create` in my terminal.   
![create database](https://user-images.githubusercontent.com/105195327/226779420-d1680357-0485-468f-ba03-05beeb190707.png)   

- I went to my [**db- schema-load**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/db-schema-load) file, and copied the code below into it. 

``` 
#!/usr/bin/bash

echo "db-schema-load"

schema_path="$(realpath .)/db/schema.sql"
echo $schema_path

psql $CONNECTION_URL cruddur < $schema_path
```

- I executed the script by running `./bin/db-schema-load` in my terminal. and it worked.  
![schema load script](https://user-images.githubusercontent.com/105195327/226779511-c1fd220c-9902-47b1-9ff5-9c6265c2af3c.png)   

- Now, i want to make sure this script can be executed from any directory, so i changed back to my root directory, and ran the script with `./backend-flask/bin/db-schema-load` and i got an error saying "No such file or directory".  
![db schema error](https://user-images.githubusercontent.com/105195327/226779569-d4a4b648-fea8-4f10-91c0-2da24f1e2d5b.png)  

- I'll figure it out later, for now it works in the backend directory so i'll have to stick to that.  


- I want to write an if statement in my [**db-schema-load**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/db-schema-load) file, that allows me toggle between local mode and production mode.  I went back to my backend-flask directory, i copied the code below into the [**db-schema-load**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/db-schema-load) file.  

```
if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi
``` 
                                           
![schema if statement](https://user-images.githubusercontent.com/105195327/226779873-f576e50f-9331-4491-ad3c-914fbacf3c2a.png)

- I executed it by running `./bin/db-schema-load prod`  
![schema load prod mode](https://user-images.githubusercontent.com/105195327/226779924-729a773b-ba0f-4ae1-9d0b-c9c9665e430a.png)   
*It's not connecting to production because we're presently not running it.*  

> **Note** Whenever you see something hanging, it's usually because of connection issues.  


##### Colour coding my scripts 
[Colour code examples](https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux)
- I added the line of code below to my [**db-schema-load**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/db-schema-load) file. 
```
GREEN='\033[1;32m'
NO_COLOR='\033[0m'
LABEL="db-schema-load"
printf "${GREEN}== ${LABEL}${NO_COLOR}\n"
```
And i got this colour after executing the script. 
![colour code schema](https://user-images.githubusercontent.com/105195327/226780087-25d748a1-b930-46c5-ae99-bbe8c52ae320.png)   

- I did a different color for the other 2 files.   
![Colour code all](https://user-images.githubusercontent.com/105195327/226780131-cb1f3d34-e931-48b9-8ee0-949cc4ff9037.png)  

---
## Creating Tables
[Helpful doc for learning how to create tables](https://www.postgresql.org/docs/current/sql-createtable.html)  

- I went to my [**schema.sql**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/db/schema.sql) file, and i pasted the following code below there.  
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
![create table](https://user-images.githubusercontent.com/105195327/226780193-3bc98b14-f607-497b-87bf-2c680ed73699.png)   

- If i run this code twice, it'll create problems, so i added commands to drop the table if they already exist before creating them again.  
```
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;
```

- I ran them with `./bin/db-schema-load`  
  
- I kept getting an error  
![create table rror](https://user-images.githubusercontent.com/105195327/226780366-01db013e-6b03-4c82-9a12-cf01f9050ee8.png)   

- I went back to my [**db-schema-load**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/db-schema-load) file and realised there was a typo, i fixed that and tried again and it worked this time.  
![create table working](https://user-images.githubusercontent.com/105195327/226780468-9a65e774-b235-45ae-a917-460948d1f119.png)   

- I created a new file for connection. ["db-connect"](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/db-connect), and i gave it execute privileges with `chmod u+x .bin/db-connect`  
and i ran it with `./bin/db-connect`  
![db connect done](https://user-images.githubusercontent.com/105195327/226780544-fdd90a67-84ba-4561-b149-7e6deeff888b.png)   

- I wanted to see my tables so i ran the `\dt` command to confirm the existence of my table.  
![my tables viewed](https://user-images.githubusercontent.com/105195327/226780571-3268ce6c-49d1-429c-9afa-2f83252059ed.png)   

- I created a [db-seed file](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/db-seed) and copied the code below into it.  
```
seed_path="$(realpath .)/db/seed.sql"

echo $seed_path

psql $CONNECTION_URL cruddur < $seed_path
```
- Created another file in the db directory named [**seed.sql**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/db/seed.sql) and copied the code below into it.  
```
INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown' ,'MOCK'),
  ('Andrew Bayko', 'bayko' ,'MOCK'),
  ('Jay Kaneki', 'jay' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
```
                                         
- I ran it with `./bin/db-seed` but it didn't run.  
  ![error running seed](https://user-images.githubusercontent.com/105195327/226781569-0e02fa74-de46-48d0-9cb4-f537de30227a.png)   

- I went to my [**schema.sql**](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/blob/main/backend-flask/db/schema.sql) file and added the user uuid, i ran my schema with `./bin/db-schema-load` then i ran the seed again with `./bin/db-seed`and it works now.  
![user uuid line](https://user-images.githubusercontent.com/105195327/226781610-a2c313f9-0104-40c6-a446-2193c169aace.png)   

![seeded data](https://user-images.githubusercontent.com/105195327/226781659-02e343a3-339a-49b6-8e7e-044c6d0191e9.png)   

I stopped my workspace for a while, to be continued later.  
---
  
- I tried connecting to my database with `./bin/db-connect` but i got an error 
![error trying to log back in](https://user-images.githubusercontent.com/105195327/227788948-97a787ea-2673-459d-b1f4-e253f2e94916.png)   

- I created my database again. signing in with `psql -Upostgres --host localhost` then i ran `CREATE database cruddur;` and my database was created. 

- I quit and went back to my directory to run `./bin/db-connect` again and i was connected to my database.  
![db connecting now](https://user-images.githubusercontent.com/105195327/227789127-9ddde347-dc24-4c6e-bce4-af165ea86de4.png)  

- I tried listing the tables but i realised there was nothing there. The previous setups didn't persist, so i'll have to run the commands again. I ran them and connected to my database again and everything was fine.  
![Ran all scripts again](https://user-images.githubusercontent.com/105195327/227789245-17ca27c2-4bf9-4d74-8753-6c6c9f204d56.png)  

- I ran `SELECT * FROM activities;` to get a view of what's been happening in the database.   
![SELECT ALL FROM](https://user-images.githubusercontent.com/105195327/227789256-72c95283-7173-40b7-92d1-bd4804efcfea.png)  

###### Testing out 
- I used my postgres explorer to access mty database and see how it looks. I deleted the session when i was done.  
![postgres explorer connection](https://user-images.githubusercontent.com/105195327/227789562-3999de29-6881-4f80-9f17-4bad9741ad21.png)   

##### db-sessions
- I created a file in my [bin directory](https://github.com/StrangeJay/aws-bootcamp-cruddur-2023/tree/main/backend-flask/bin), named **db-sessions**                                

- I copied the code below into the file.  
```
#!/usr/bin/bash 

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-sessions"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"


if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi


NO_DB_URL=$(sed 's/\/cruddur//g' <<<"$URL")
psql $NO_DB_URL -c "select pid as process_id, \
       usename as user,  \
       datname as db, \
       client_addr, \
       application_name as app,\
       state \
from pg_stat_activity;"
``` 

*This would check the idle connections left open.*  

- I gave the file execute privileges, and ran `./bin/db-sessions`  
![one active db session](https://user-images.githubusercontent.com/105195327/227789634-9b46d069-d28b-49c7-a368-050f1a4fdc3a.png)  

- I created a file **"db-setup"** to easily setup everything for our database. I copied the code below into the file.  

```
#!/usr/bin/bash 

-e # stop if it fails at any point

BLUE='\033[1;34m'
NO_COLOR='\033[0m'
LABEL="db-setup"
printf "${BLUE}== ${LABEL}${NO_COLOR}\n"

echo "db-setup"

bin_path="$(realpath .)/bin"

source "$bin_path/db-drop"
source "$bin_path/db-create"
source "$bin_path/db-schema-load"
source "$bin_path/db-seed"
```

- I gave it execute privileges and ran `./bin/db-setup` 
*I'm only doing this locally, so i didn't add an if else statement*  
![db setup](https://user-images.githubusercontent.com/105195327/227789678-28085cba-c741-4cff-ba12-0d072bb72a8f.png)
---
  
#### Installing Postgres driver  
- I added `psycopg[binary]` and `psycopg[pool]` to my requirement.txt file. Then i ran `pip install requirements.txt`   
Next i'm going to create a connection pool.  

- I created a new file in my **backend-flask/lib** directory named **"db.py"**  and i copied the command below into the file.  
```
from psycopg_pool import ConnectionPool
import os


connection_url = os.getenv("CONNECTION_URL")
pool = ConnectionPool(connection_url)
```
![Connection pool](https://user-images.githubusercontent.com/105195327/227789716-712ffbf9-292b-485a-bfda-5948bd898020.png)  

- I passed my connection pool through my **"docker-compose.yml"** file.  
![docker compose connection url](https://user-images.githubusercontent.com/105195327/227789726-ae2a389b-4155-4423-ae9e-2e43a7e0d607.png)  

- I imported the connection pool into my **"home_activities.py"** file.  
```
from lib.db import pool 
``` 

```
 sql = """
      SELELECT * FROM activities
      """  
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchall()
      return json[0]
      return results
```
![connection pool home activities](https://user-images.githubusercontent.com/105195327/227789746-37c8e01e-d315-4b88-8d64-1b896b1e1d57.png)  

- I composed up and visited my frontend URL, the page was blank so i viewed logs and i saw a bunch of errors there.  
![errors in frontend logs](https://user-images.githubusercontent.com/105195327/227789798-440d7999-91c9-4ecc-9603-c11c296a00be.png)  

- I checked the backend URL and i also got an error saying **"pool timeout"**. I checked the backend container logs and i saw the same error.  
![backend pool timeout error](https://user-images.githubusercontent.com/105195327/227789904-78599609-06f4-4af3-8113-383fdcba4cff.png)  
  
  ![backend error log pool error](https://user-images.githubusercontent.com/105195327/227789927-41557518-c64f-4006-a212-755df27aa61c.png)  

- I went to my docker-compose file to change my **"CONNECTION_URL"**  and i composed up again. I checked the backend URL and got a syntax error.  

![error logs 1st fix connection url](https://user-images.githubusercontent.com/105195327/227789966-78f78709-da6c-4d14-a5cd-712866d47444.png)  

![backend syntax error](https://user-images.githubusercontent.com/105195327/227789975-623aaa6c-67b8-4467-a703-415887f4c470.png)  
  
  ![syntax error in home activities](https://user-images.githubusercontent.com/105195327/227790300-0986e12f-f6de-4c5b-8414-308fb95e5ce5.png)

- I fixed the syntax error and got a type error.  
![type error backend](https://user-images.githubusercontent.com/105195327/227790317-3e5b79e0-e4a0-4be0-89f9-533f8d2c1764.png)   

- I added rows and got an error saying json is not defined.   
![name error logs backend](https://user-images.githubusercontent.com/105195327/227790338-3265e81b-2261-4a55-9706-48dd296cee71.png)   

- I removed the json line and got an error saying results error, so i removed the result line and i got back some error. It isn't properly fed so i'm going to tweak it a bit. I want to return raw json from postgres and then pass it along, *that way i don't have to worry about additional overhead*   
![data but not perfect yet](https://user-images.githubusercontent.com/105195327/227790407-eb70e564-4271-4019-9410-ab8d085a7df7.png)   

- I went to my db.py file and copied the code below into the file.  
```
def query_wrap_object(template):
  sql = '''
  (SELECT COALESCE(row_to_json(object_row),'{}'::json) FROM (
  {template}
  ) object_row);
  '''

def query_wrap_array(template):
  sql = '''
  (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
  {template}
  ) array_row);
  '''
```

- I went to my **"home_activities.py"** file and updated the import command by adding `query_wrap_array` 
![updated import statement](https://user-images.githubusercontent.com/105195327/227790514-d072e2f2-8beb-4913-adb6-3d88b6e3c16f.png)   

- I updated the sql command and added the query_wrap_array.  I saved and refreshed the frontend URL, then i got this error saying "TypeError: expected bytes, NoneType found".  ![update home activities with querry](https://user-images.githubusercontent.com/105195327/227790534-2af93b28-44f8-4b79-b4ee-04556850037a.png)  

![sql query error](https://user-images.githubusercontent.com/105195327/227790564-026a2084-84ec-48ac-94ca-575c5f6968e3.png)  

- I went to check my **"db.py code and i realised i forgot to add the return statement, so i did that, saved and refreshed the frontend URL again."**  
![return none error fix](https://user-images.githubusercontent.com/105195327/227791022-ad41b4e2-bc8a-436f-a3b6-1571e694e044.png)  

- I got an error saying 
**"psycopg.errors.SyntaxError: syntax error at or near "{"
LINE 3:   {template}
          ^"**  

- I asked chatgpt and i was given instructions to use double braces to escape the braces in the 'COALESCE' function. I tried that and i still had the same error, I added the **"query_wrap_object"** import statement to my **"home_activities.py"** file. I got the same error. 
I changed from single quotes to double quotes in wrapping my sql query. I refreshed the frontend page and it served data. 
But i got an error saying my token was expired.  
![frontend feeding data](https://user-images.githubusercontent.com/105195327/227791054-ef9c6b38-3c32-425c-94ac-5b688c0f8a03.png)  

- I closed my workspace and restarted it and now authentication has returned.    
![authentication now working](https://user-images.githubusercontent.com/105195327/227791090-ab9753bc-c465-4178-8086-956960708536.png)  
---
  
- Now i want to query the database. I copied the code below into my **"home_activities.py"** 
```
SELECT
  activities.uuid,
  users.display_name,
  users.handle,
  activities.message,
  activities.replies_count,
  activities.reposts_count,
  activities.likes_count,
  activities.reply_to_activity_uuid,
  activities.expires_at,
  activities.created_at
FROM public.activities
LEFT JOIN public.users ON users.uuid = activities.user_uuid
ORDER BY activities.created_at DESC
```
![data query in home activities](https://user-images.githubusercontent.com/105195327/227791106-5a82b084-a9ba-46da-8e01-dc2a2ce00965.png)   
  
![my first query](https://user-images.githubusercontent.com/105195327/227791149-b2c8f27d-474f-4bd7-b7c0-6663ba7b380a.png)

- I went to my AWS console, went to my RDS and restarted my RDS. I went to my terminal to run `echo PROD_CONNECTION_URL` and it exported my URL. 
![echo prod connection url](https://user-images.githubusercontent.com/105195327/227791176-55bf4a6a-d699-4a3b-96c1-c08a20f23ecb.png)  

- I ran `psql $PROD_CONNECTION_URL` and it was hanging, we have to get the gitpod address and make it available to the security group.  
![prod connection url hanging](https://user-images.githubusercontent.com/105195327/227791203-054f6a90-a92b-4ab4-a6da-e11ca719ca47.png)  

- I went to add a new rule to my security group. To allow git pod to access my RDS. 
![edit inbound rule](https://user-images.githubusercontent.com/105195327/227791524-5329f026-a4c1-492d-8205-ba37e2f8f2db.png)  

![add security rule](https://user-images.githubusercontent.com/105195327/227791529-0068c474-9d3e-47bc-99af-930c691f5592.png)  

- I ran `curl ifconfig.me` in my terminal. I got the IP address and added it to the source of my inbound rule.     
![GITPOD curl ifconfig](https://user-images.githubusercontent.com/105195327/227791549-e2b2c71c-52f2-470d-93ca-4c9424782132.png)  

![added IP to inbound rule](https://user-images.githubusercontent.com/105195327/227791591-7a44b188-1ba1-4a79-b983-ad5d57bafdd6.png)   

- I saved the code to get my IP as an environment variable using `export GITPOD_IP=$(curl ifconfig.me)`  

- I ran `psql $PROD_CONNECTION_URL` again and this time i got an error saying my password authentication failed. 
  ![prod connection url failed password authentication](https://user-images.githubusercontent.com/105195327/227791610-6abf9897-f551-4b84-baad-cc6bcd4f5e32.png)  
  
- I did some searching and realised i had a typographical error in my master username. I didn't feel like deleting and recreating a new RDS instance so i went to my terminal and changed the master username to fit the one created.  I ran `psql $PROD_CONNECTION_URL` and it worked.  
![working prod connection](https://user-images.githubusercontent.com/105195327/227791628-9d686866-c1fa-46a9-bf1d-a2f2d88d8a2b.png)   

- I ran `\l` to see the list of my tables.  
![database list in prod](https://user-images.githubusercontent.com/105195327/227791657-ebd56de1-d98c-4dd8-bcd7-3ace775f7ee3.png)  

*Everytime the environment is spinned up, i'll have to update the GITPOD ip in my security group, so i'm going to create a script that automatically updates it whenever i spin up a new environment.*
---
  
##### Automating GITPOD_IP RDS SG Update
- I went to my management console to grab the security group ID and the security group rule ID, i inputed them in the commands below and ran it in my terminal.  

```
export DB_SG_ID="<sg-ID>"
gp env DB_SG_ID="<sg-ID>"
export DB_SG_RULE_ID="<sgr-ID>"
gp env DB_SG_RULE_ID="<sgr-ID>" 
```

- Now i'll use this command to automate the process. 
```
aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
    --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={Description=GITPOD,IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
``` 

To test it i'll remove my previous inbound rule, run this command, then go and check if the new one has been set. 
  ![working auto gitpod ip update  RDS console  1st](https://user-images.githubusercontent.com/105195327/227791801-8d0f37cc-06d6-415c-9036-445448a0c0d9.png)  

- I kept getting an error message saying CIDR block /32 is malformed. 

- After much investigation, i realised i didn't save my GITPOD_IP to the environment and i stopped and restarted my workspace prior to this step. So i exported my GITPOD_IP again and saved to env. I tried running the command again and it worked this time. 
![working auto gitpod ip update](https://user-images.githubusercontent.com/105195327/227791859-74d1c3a8-a88e-4089-a755-6604e55373a2.png)  
  
![working auto gitpod ip update  RDS console](https://user-images.githubusercontent.com/105195327/227791864-c2daab27-718f-481d-8f36-69e1f3323e11.png)   

*I want this to be updated everytime i start my workspace, so i'm going to create an additional script to that effect.* 

- I went to my **"bin"** directory and created another script called **"rds-update-sg-rule"** i copied the necessary command into it and gave it execute priviledges.  
  ![rds-upgrade-rule and permission](https://user-images.githubusercontent.com/105195327/227791926-ffeb4c5f-e107-450e-9e83-98463d7ea33c.png)   

###### Set it to autorun during startup 
- I went to my gitpod.yml file and put the command below in it.  
```
command: |
      export GITPOD_IP=$(curl ifconfig.me)
      source  "$THEIA_WORKSPACE_ROOT/backend-flask/bin/rds-update-sg-rule"
``` 
![rds-update rule in gitpodyml](https://user-images.githubusercontent.com/105195327/227791937-0201cd73-a273-43c1-8df3-f5d617cd65cf.png)  

- I wanted to test this so i closed my workspace, removed the inbound rule in my security group and started the workspace again. The sg update rule was working. 
![working gitpod yml file](https://user-images.githubusercontent.com/105195327/227791986-577714a2-9882-41e1-bcb6-5ee8ae06ddd6.png)  

- I checked my security group inbound rule from the console and the new GITPOD_IP has been added.  
![new ip in rds console](https://user-images.githubusercontent.com/105195327/227792012-73963f19-7b91-4db8-9747-3ceb7c33900a.png)   

- I ran my db-setup and db-connect, and everything works fine. Data is being loaded on my frontend. 
![working prod connection 2](https://user-images.githubusercontent.com/105195327/227792046-3d3c4c4a-3f7a-4094-b33c-95a7c408afeb.png)  

![front end showing](https://user-images.githubusercontent.com/105195327/227792054-d81c1142-2c84-497a-86eb-8395013b8a06.png)   


*Stopping my workspace for a while*
---
- I went to my **"dockercompose.yml"** and set my production connection url then i composed up. 

- I ran `./bin/db-schema-load prod` in my backend directory, i went to the frontend URL and no data was being served, this is expected because we haven't loaded a schema. 


- I checked my logs and got an error saying my app is unauthenticated.  
 
 




