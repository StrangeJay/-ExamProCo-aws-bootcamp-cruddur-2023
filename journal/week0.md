# Week 0 — Billing and Architecture

## Create An Admin User
- Create an IAM user 
Sign into the `AWS Management Console` and open the [IAM console](https://us-east-1.console.aws.amazon.com/iam/?region=us-east-1#)  
![iam](https://user-images.githubusercontent.com/105195327/219350512-d689198f-0848-4087-a487-dafa89ba89c5.png)  

- Create a new IAM user and `enable console access` for the user  
![Iam User](https://user-images.githubusercontent.com/105195327/219351897-b55f4116-afa0-4aea-82e0-d0d26c32c7e6.png)

- Create a new `Admin group` and grant the group `Administrator Access` 
 ![Screenshot_20230216_122355](https://user-images.githubusercontent.com/105195327/219352415-1527cea6-da71-431b-a94f-97ec0cb2767b.png)   
- Select the check mark next to the `Aministrator group`, and click Next: Review and Create   
- Choose `create user`  
- Download the CSV with the credentials  
- Return to user list and click on the user name  
- Click on `Security Credentials` and `Create access key`   
![Screenshot_20230216_123223](https://user-images.githubusercontent.com/105195327/219354157-11a3b15d-2dba-49af-b463-7d3481172826.png)   
   
- Choose `AWS CLI Access` and click on create Access key  
- Download the CSV with the credentials   
-Setup Multi Factor Authentication (MFA) for your new user, this is best practice.  
- Sign out of root user and sign in as the new IAM user  
---
## Install and verify the AWS CLI 
- Follow the instructions on the [AWS Command Line Interface Documentation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)  
- Copy and paste the command needed to install the CLI on your respective device. I am using Linux so i followed the instructions for Linux systems. 
- Run the following commands, one at a time to avoid any problems. Copying it all at once might work too, but sometimes it's better to do it line by line to get the expected results.  
`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"`  
`unzip awscliv2.zip`   
`sudo ./aws/install`   

### Setting up ENV Variable 
- I could've used **aws configure** to set up the CLI, but i set up my environment variable with gitpod instead. 
- Create a file and copy and type these commands into the file  
`export AWS_ACCESS_KEY_ID="<your access id"`   
`export AWS_SECRET_ACCESS_KEY="<your access key>`   
`export AWS_DEFAULT_REGION="<region>`   

- Copy and paste the commands into your gitpod terminal one at a time.   
- Confirm if you set it right by typing `env | grep AWS_` this should show you the copied details.   
- Type `aws sts get-caller-identity` and it should show your User Id, Acoount and Arn.   
- Tell gitpod to remember these credentials next time you open your workspace. by typing the following commands.  
`gp env AWS_ACCESS_KEY_ID=""`   
`gp env AWS_SECRET_ACCESS_KEY=""`   
`gp env AWS_DEFAULT_REGION=us-east-1`   

- Add a script to your gitpod.yml file to make sure that everytime we start up our workspace it loads these settings and we don't have to do it all over again.  
![updated YAML file](https://user-images.githubusercontent.com/105195327/219480714-6b68e57d-8188-4f2b-81ea-2dc43890f833.png)   
---





