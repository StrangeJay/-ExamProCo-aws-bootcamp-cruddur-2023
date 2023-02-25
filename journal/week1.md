# Week 1 — App Containerization 

## Containerize Backend  

### Run Flask locally
- I changed directory to the **backend-flask** directory
- I ran `pip3 install -r requirements.txt` to install the necessary requirements
- I ran the code `python3 -m flask run --host=0.0.0.0 --port=4567` 
- I went to the address on `exposed ports` but kept getting 404 error from the server 
- ![exposed ports](https://user-images.githubusercontent.com/105195327/221190009-690bfd01-9f57-44bd-a774-949fcc176f4a.png)  

![not found url](https://user-images.githubusercontent.com/105195327/221189534-19281e49-4311-4695-b0f2-cae97a3ca286.png)  

- I unlocked the 4567 port and made it public, and tried again, i got the same error. 

- I was receiving a 404 error in the terminal
![404 error](https://user-images.githubusercontent.com/105195327/221190502-f32e218b-1490-48ce-abd5-22516ecbf105.png)  
*This means the server is running and it's accepting requests, but nothing is showing up*.   

- I appended the endpoint `/api/activities/home` to the url and this time i got a different error   
![internal server error](https://user-images.githubusercontent.com/105195327/221190136-ee1b6d0a-1981-4d52-bc0e-8a3ee38f5800.png)  

- I configured the frontend and backend environment variable by running the following command 
`export FRONTEND_URL="*"`  
`export BACKEND_URL="*"`  
![Fend Bend Var](https://user-images.githubusercontent.com/105195327/221193448-aa861acb-543a-4484-839c-1c93ab593c14.png)

- I tried the command again, and this time i got data in json format  
![json data](https://user-images.githubusercontent.com/105195327/221193492-e0bee396-3042-4fe4-b950-8d60f48d3ae2.png)

- I got a 200 status response code on my terminal, which indicates the request has succeeded  
![http 200](https://user-images.githubusercontent.com/105195327/221193529-5474a0f8-c781-432c-829d-698c55a8e1de.png)

- I stopped the server with `ctrl + c`  
- I unset the frontend and backend variables by running the commands below 
`unset FRONTEND_URL`
`unset BACKEND_URL`  
- I confirmed that i unset the environment variable by running `env | grep FRONTEND` and `env | grep BACKEND` 

### Add a Dockerfile
- I created a Dockerfile file in the **backend-flask** directory. 
- I inputted the necessary commands needed to run my Dockerfile.  
![Screenshot_20230223_130152](https://user-images.githubusercontent.com/105195327/220917090-cbbccaf3-76b8-49ae-807b-554eda20b384.png)

- I added comments to my Dockerfile to better understand how what is going on, things being copied, and things being installed on the host OS, and things being installed in the container.  

### Build Container 
- I went back to my product directory by running `cd ..` 
- I built my docker container by running the following command 
`docker build -t  backend-flask ./backend-flask`  
![successfully built docker image](https://user-images.githubusercontent.com/105195327/221204548-c60b937c-8ced-4ed0-8e21-bb4431d3fde9.png)

- I ran `docker images` to see my docker images
![docker image](https://user-images.githubusercontent.com/105195327/221204637-e07381cd-4392-46ca-8e23-9cff5c8bd127.png)

#### Setting Environment Variables
- I tried setting it with this command `FRONTEND_URL="*" BACKEND_URL="*" docker run --rm -p 4567:4567 -it backend-flask` and i got **not found** when i went to the address. 
- I checked docker logs by clicking on the Docker icon and right clicking the running container, then i clicked **attach shell**  
- I checked if the environment variable has been set by typing `env`, no frontend or backend environment variable was set.  
- I stopped the running container  
- I set the frontend and backend environment variable by running `set FRONTEND_URL="*"` and `set BACKEND_URL="*"` respectively.  
- i ran the command `docker run --rm -p 4567:4567 -it backend-flask -e FRONTEND_URL -e BACKEND_URL` and i got an error message 
![Daemon error](https://user-images.githubusercontent.com/105195327/221319475-ea838168-e202-4713-94f6-c2d45e9a4a0a.png)  

- I realised the container image name has to be the last point so i flipped the command a bit and ran `docker run --rm -p 4567:4567 -it -e FRONTEND_URL -e BACKEND_URL backend -flask`  
*I could've used the command `docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask` and then i wouldn't have had to set the frontend and backend environment variable first like i did.*  
- It was successful. Or at least i thought it was.   
- I went to my exposed ports to make sure port 4567 is open and public, i visited the web address with the necessary endpoint and i was taken to the error page below.  
![running container](https://user-images.githubusercontent.com/105195327/221319497-9a93f95e-832f-4b04-a408-4417f2a1a7de.png)  
- I saw the following error in my terminal  
![error](https://user-images.githubusercontent.com/105195327/221320653-a6a522b7-aa1f-4ce9-ac0e-d7be19e2e0f9.png)  

- I ran the second command that adds the setting of environment variable `docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask` and this time i got the desired result.  
![Screenshot_20230225_002925](https://user-images.githubusercontent.com/105195327/221320692-d1be8aec-c9ef-44b8-8265-4fca04a84d77.png)  
- I ran `docker ps` to confirm that my container is running. 
![running container2](https://user-images.githubusercontent.com/105195327/221321915-dc80aa3e-a469-467d-83c8-ae3b3e812a7c.png)  

> **Note** The **"--rm"** flag cleans up the image when we stop the container, the **"-e"** flag sets environment variable. 
---
## Containerize Frontend
- I changed directory to my front end directory `frontend-react-js` and ran `npm i`
- I created a Dockerfile in my frontend directory and copied the command below into it.  

> FROM node:16.18

> ENV PORT=3000  

> COPY . /frontend-react-js  
> WORKDIR /frontend-react-js  
> RUN npm install  
> EXPOSE ${PORT}  
> CMD ["npm", "start"]  

- I went back to my product directory with `cd ..`  
- i created a **docker-compose.yml file** and pasted the necessary text into the file.  
- I right-clicked the **docker-compose.yml** file, and clicked on "Compose Up". *An alternative would've been to run `docker-compose up` in the terminal.  
- The containers were successfully started 
![started container](https://user-images.githubusercontent.com/105195327/221348897-ce7b6f18-4ae2-4e39-a0c5-42a610384c59.png)  
- Frontend was served and communicating with the backend.  
![Screenshot_20230225_121134](https://user-images.githubusercontent.com/105195327/221354628-f6011cd5-f325-4b73-9c8a-5a25b1c8dbb7.png)

---
## Add an endpoint to the application
- I clicked on the open api icon 
- I right clicked on the existing openapi and selected "add path", and a section was created below the existing commands.  
![new api for notification](https://user-images.githubusercontent.com/105195327/221354669-5db9a557-27dc-440b-901f-d1115f0d035f.png)  

- I added description and set a tag to allow me group endpoints under activities.  
- I set it to return application/json, i set a reference, and committed my changes. 
![open api update](https://user-images.githubusercontent.com/105195327/221354693-7d20273c-8a86-4318-8b53-0d4e37a83011.png)  

---
## Creating The Notification Feature For Frontend and Backend

### Backend 
- I went to the app.py file in the backend-flask directory  
- I created a parameter for my notifications in the app.py file  
![notifications api](https://user-images.githubusercontent.com/105195327/221357021-833e3a7a-699e-4c08-87e0-0b05fc74bb14.png)  

- In the backend-flask directory, i created a **notifications_activities.py** file in the services directory. 
- I added an import statement for notifications  
- I opened the notifications_activities.py file and using home_activities as a guide i inputted some data  
![notifications activities](https://user-images.githubusercontent.com/105195327/221357091-91778e9c-ca51-40df-b940-0d2af5f7741d.png)  

- I visited the notifications endpoint and got an error  
![error trying to run notifications](https://user-images.githubusercontent.com/105195327/221357101-a3ad2db0-fc4c-48dd-a01f-2048a32fd082.png)  

- I fixed the error by changing app.route definitions in the app.py file to **"data_notifications()"** and this fixed the problem.  
![notifications api working](https://user-images.githubusercontent.com/105195327/221357111-9fac2dc2-3e24-48b5-bcbf-3d8227725de7.png)  

### Frontend
- I went to the frontend directory and opened the **"App.js"** file. 
- I created the path for my notifications feed page and added the import statement. 
- I created a **"NotificationsFeedPage.js"** file in pages directory and using the **"HomeFeedPage.js"** as a guide i inputted the required data. 
- I created a **"NotificationsFeedPage.css"** file.  
- I saved my changes and refreshed the web address and my changes were seen.  
  ![Screenshot_20230225_142333](https://user-images.githubusercontent.com/105195327/221359283-644b7c40-e8c5-41e1-aee6-e97468035f6b.png)  
---
## Adding DynamoDB Local and Postgres
- I opened my dockercompose.yml file  
- I integrated the postgre and DynamoDB commands in it.  
![Screenshot_20230225_145021](https://user-images.githubusercontent.com/105195327/221361133-98f25425-a429-493c-a739-54218aa7d7c8.png)  

### DynamoDB Local 
> services:  
  dynamodb-local:  
    # https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa  
    # We needed to add user:root to get this working.  
    user: root  
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"  
    image: "amazon/dynamodb-local:latest"  
    container_name: dynamodb-local  
    ports:  
      - "8000:8000"  
    volumes:  
      - "./docker/dynamodb:/home/dynamodblocal/data"  
    working_dir: /home/dynamodblocal  


### Postgre 
> services:  
  db:  
    image: postgres:13-alpine  
    restart: always  
    environment:  
      - POSTGRES_USER=postgres  
      - POSTGRES_PASSWORD=password  
    ports:  
      - '5432:5432'  
    volumes:  
      - db:/var/lib/postgresql/data  


### Volume
> volumes:
  db:
    driver: local

- I opened the necessary ports and i ran docker-compose up. 
![Screenshot_20230225_145710](https://user-images.githubusercontent.com/105195327/221361154-8e450dd3-1fcc-4770-92c5-ba509e954b3f.png)  

- All containers were successfully created.  
![Screenshot_20230225_145850](https://user-images.githubusercontent.com/105195327/221361167-6ec45aca-788a-4cde-892d-7b1f943fe23f.png)  

### Install postgre client library in gitpod
- I added the code below to my gitpod.yml file
>   - name: postgres  
    init: |  
      curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg  
      echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list  
      sudo apt update  
      sudo apt install -y postgresql-client-13 libpq-dev  

- I copied and pasted the first 3 commands needed to install posgre client, one by one, an ran them in the terminal.  
- I ran the last line of command  
- I typed **"psql -Upostgres --host localhost"** to see if it worked and it did.  So we know it's working. 


- 