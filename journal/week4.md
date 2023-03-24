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



- I created my database again. signing in with `psql -Upostgres --host localhost` then i ran `CREATE database cruddur;` and my database was created. 

- I quit and went back to my directory to run `./bin/db-connect` again and i was connected to my database.  



- I tried listing the tables but i realised there was nothing there. The previous setups didn't persist, so i'll have to run the commands again. I ran them and connected to my database again and everything was fine. 




- I ran `SELECT * FROM activities;` to get a view of what's been happening in the database.   




- I'm going to query my database now. 


- I used my postgres explorer to access mty database and see how it looks. I deleted the session when i was done.  



###### db-sessions
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


##### Installing Postgres driver  
- I added `psycopg[binary]` and `psycopg[pool]` to my requirement.txt file. Then i ran `pip install requirements.txt`   
Next i'm going to create a connection pool.  

- I created a new file in my **backend-flask/lib** directory named **"db.py"**  and i copied the command below into the file.  
```
from psycopg_pool import ConnectionPool
import os


connection_url = os.getenv("CONNECTION_URL")
pool = ConnectionPool(connection_url)
```

- I passed my connection pool through my **"docker-compose.yml"** file.  


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

- I composed up and visited my frontend URL, the page was blank so i viewed logs and i saw a bunch of errors there.  

- I checked the backend URL and i also got an error saying **"pool timeout"**. I checked the backend container logs and i saw the same error.  

- I went to my docker-compose file to change my **"CONNECTION_URL"**  and i composed up again. I checked the backend URL and got a syntax error.  




- I fixed the syntax error and got a type error.  




- I added rows and got an error saying json is not defined.   




- I removed the json line and got an error saying results error, so i removed the result line and i got back some error. It isn't properly fed so i'm going to tweak it a bit. I want to return raw json from postgres and then pass it along, *that way i don't have to worry about additional overhead*   






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



- I updated the sql command and added the query_wrap_array.  I saved and refreshed the frontend URL, then i got this error saying "TypeError: expected bytes, NoneType found".  



- I went to check my **"db.py code and i realised i forgot to add the return statement, so i did that, saved and refreshed the frontend URL again."**  

- I got an error saying 
**"psycopg.errors.SyntaxError: syntax error at or near "{"
LINE 3:   {template}
          ^"**  


- I asked chatgpt and i was given instructions to use double braces to escape the braces in the 'COALESCE' function. I tried that and i still had the same error, I added the **"query_wrap_object"** import statement to my **"home_activities.py"** file. I got the same error. 
I changed from single quotes to double quotes in wrapping my sql query. I refreshed the frontend page and it served data. 
But i got an error saying my token was expired.  



- I closed my workspace and restarted it and now authentication has returned.    



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

- I went to my AWS console, went to my RDS and restarted my RDS. I went to my terminal to run `echo PROD_CONNECTION_URL` and it exported my URL. 

- I ran `psql $PROD_CONNECTION_URL` and it was hanging, we have to get the gitpod address and make it available to the security group.  


- I went to add a new rule to my security group. To allow git pod to access my RDS. 




- I ran `curl ifconfig.me` in my terminal. I got the IP address and added it to the source of my inbound rule.     




- I saved the code to get my IP as an environment variable using `export GITPOD_IP=$(curl ifconfig.me)`  


- I ran `psql $PROD_CONNECTION_URL` again and this time i got an error saying my password authentication failed. I did some searching and realised i had a typographical error in my master username. I didn't feel like deleting and recreating a new RDS instance so i went to my terminal and changed the master username to fit the one created.  I ran `psql $PROD_CONNECTION_URL` and it worked.  



- I ran `\l` to see the list of my tables.  




- 


