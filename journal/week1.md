# Week 1 — App Containerization 

## Contenarize Backend 

### Run Python 
- I changed directory to the **backend-flask** directory
- I ran `pip3 install -r requirements.txt` to install the necessary requirements
- I ran the code `python3 -m flask run --host=0.0.0.0 --port=4567` 
- I went to the address on `exposed ports` but kept getting 404 error from the server 
- ![exposed ports](https://user-images.githubusercontent.com/105195327/221190009-690bfd01-9f57-44bd-a774-949fcc176f4a.png)  

![not found url](https://user-images.githubusercontent.com/105195327/221189534-19281e49-4311-4695-b0f2-cae97a3ca286.png)  

- I unlocked the 4567 port and made it public, and tried again, this time i got a different error  
![internal server error](https://user-images.githubusercontent.com/105195327/221190136-ee1b6d0a-1981-4d52-bc0e-8a3ee38f5800.png)  

- I was receiving a 404 error in the terminal
![404 error](https://user-images.githubusercontent.com/105195327/221190502-f32e218b-1490-48ce-abd5-22516ecbf105.png)  

- I saved the frontend and backend url as environment variables 
- I made sure i appended `/api/activities/home` to the url 
- I unlocked the port on the port tab

### Add a Dockerfile
- I created a Dockerfile file in the **backend-flask** directory. 
- I inputed the neccesary commands needed to run my Dockerfile.  
![Screenshot_20230223_130152](https://user-images.githubusercontent.com/105195327/220917090-cbbccaf3-76b8-49ae-807b-554eda20b384.png)

- I added comments to my Dockerfile to better understand how what is going on, things being copied, and things being installed on the host OS, and things being installed in the container.  


