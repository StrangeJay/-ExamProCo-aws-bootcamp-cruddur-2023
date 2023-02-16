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
