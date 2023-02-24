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


- I realised the container image name has to be the last point so i flipped the command a bit and ran `docker run --rm -p 4567:4567 -it -e FRONTEND_URL -e BACKEND_URL backend -flask`  
- It was successful 
- I could've used the command `docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask` and then i wouldn't have had to set the frontend and backend environment variable first like i did.  
- I went to my exposed ports to make sure port 4567 is open and public, i visited the web address with the necessary endpoint and i was taken to a functioning page.  



