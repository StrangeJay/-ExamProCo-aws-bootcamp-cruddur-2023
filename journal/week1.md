# Week 1 — App Containerization 

## Contenarize Backend 

### Run Python 
- I changed directory to the **backend-flask** directory
- I ran `pip3 install -r requirements.txt` to install the necessary requirements
- I ran the code `python3 -m flask run --host=0.0.0.0 --port=4567` 
- I went to the address but kept getting 404 error from the server 
- I saved the frontend and backend url as environment variables
- I made sure i appended `/api/activities/home` to the url 
- I unlocked the port on the port tab

### Add a Dockerfile
- I created a Dockerfile file in the **backend-flask** directory. 
- I inputed the neccesary commands needed to run my Dockerfile.  
![Screenshot_20230223_130152](https://user-images.githubusercontent.com/105195327/220917090-cbbccaf3-76b8-49ae-807b-554eda20b384.png)

- I added comments to my Dockerfile to better understand how what is going on, things being copied, and things being installed on the host OS, and things being installed in the container.  


