# Week 0 — Billing and Architecture

## Create An Admin User
- I created an IAM user 
Signed into the `AWS Management Console` and opened the [IAM console](https://us-east-1.console.aws.amazon.com/iam/?region=us-east-1#)  
![iam](https://user-images.githubusercontent.com/105195327/219350512-d689198f-0848-4087-a487-dafa89ba89c5.png)  

- I created a new IAM user and `enable console access` for the user  
![Iam User](https://user-images.githubusercontent.com/105195327/219351897-b55f4116-afa0-4aea-82e0-d0d26c32c7e6.png)

- I created a new `Admin group` and granted the group `Administrator Access` 
 ![Screenshot_20230216_122355](https://user-images.githubusercontent.com/105195327/219352415-1527cea6-da71-431b-a94f-97ec0cb2767b.png)   
- I selected the check mark next to the `Aministrator group`, and clicked Next: Review and Create   
- I chose `create user`  
- Downloaded the CSV with the credentials  
- Returned to user list and clicked on the user name  
- Clicked on `Security Credentials` and `Create access key`   
![Screenshot_20230216_123223](https://user-images.githubusercontent.com/105195327/219354157-11a3b15d-2dba-49af-b463-7d3481172826.png)   
   
- I chose `AWS CLI Access` and clicked on create Access key  
- Downloaded the CSV with the credentials   
- Setup Multi Factor Authentication (MFA) for my new user, this is best practice.  
- Signed out of root user and signed in as the new IAM user  
---
## Install and verify the AWS CLI 
- I followed the instructions on the [AWS Command Line Interface Documentation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)  
- Copy and paste the command needed to install the CLI on your respective device. *I am using Linux so i followed the instructions for Linux systems.* 
- Run the following commands, one at a time to avoid any problems. *Copying it all at once might work too, but sometimes it's better to do it line by line to get the expected results.*  
`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"`  
`unzip awscliv2.zip`   
`sudo ./aws/install`   

### Setting up ENV Variable 
- I could've used **aws configure** to set up the CLI, but i set up my environment variable with gitpod instead. 
- I created a file and typed these commands into the file  
`export AWS_ACCESS_KEY_ID="<your access id"`   
`export AWS_SECRET_ACCESS_KEY="<your access key>`   
`export AWS_DEFAULT_REGION="<region>`   

- Copied and pasted the commands into my gitpod terminal one at a time.   
- Confirmed if i set it right by typing `env | grep AWS_` *this should me the copied details.*   
- Typed `aws sts get-caller-identity` and it outputed my User Id, Acoount and Arn.   
- Told gitpod to remember these credentials next time i open your workspace. by typing the following commands.  
`gp env AWS_ACCESS_KEY_ID=""`   
`gp env AWS_SECRET_ACCESS_KEY=""`   
`gp env AWS_DEFAULT_REGION=us-east-1`   

- Added a script to my gitpod.yml file to make sure that everytime i start up my workspace it loads these settings and i don't have to do it all over again.  
![updated YAML file](https://user-images.githubusercontent.com/105195327/219480714-6b68e57d-8188-4f2b-81ea-2dc43890f833.png)   
- Commited the changes 
- Double checked by going to my repo and confirming the changes were applied.  
- exited gitpod and re-entered gitpod to test if the script works and everything gets setup immediately the workspace is loaded   
---
## Enabling Billing 
- Turn on Billing Alerts to recieve alerts. 
- I went to my AWS management console  
- Searched for billing 
![AWS biling](https://user-images.githubusercontent.com/105195327/219485504-7351eba7-e179-4649-ac64-53d61f8db964.png)


- I encountered a permissions error because i was signed in as my IAM user so i logged out and signed in as root user  
- I went to the billing page, and under `Billing Preferences` i choose `Receive Billing Alerts`  
- i also chose to receive free tier usage alert under the **Cost Management Preferences**  
- I clicked on `Save Preferences`   
---
## Creating a billing alarm
**Create SNS Topic**  

- We need to create an SNS topic before we can create an alarm. The SNS topic is what will send us an alert when we get overbilled.  

- [create aws sns topic](https://docs.aws.amazon.com/cli/latest/reference/sns/create-topic.html)   

- I used the AWS CLI Command reference document as a guide 
![create topic](https://user-images.githubusercontent.com/105195327/219489445-6fded97a-3fb0-4fc4-b6e4-b1cff409927e.png)   

- Created an SNS Topic by typing the following command  
`aws sns create-topic --name billing-alarm`  
*it outputed the ARN assigned to the created topic*  
- I copied and pasted this code and substituted the necessary credentials.  
> aws sns subscribe \
      --topic-arn="<TopicARN>" \
      --protocol=email \
      --notification-endpoint=<your@email.com>  
      
- Kept getting an error message `aws: error: the following arguments are required: --protocol`  when i tried copying all at once, so i did it one at a time.  
![subscription](https://user-images.githubusercontent.com/105195327/219496133-2b91477d-1418-4e9e-b016-18901d0eb249.png)  
- I got a mail asking me to confirm the subscription and i clicked confirm and received a "subscription confirmed" message.  
- I went to the management console to confirm the creation of my SNS topic 
![created billing ish](https://user-images.githubusercontent.com/105195327/219497007-0ab0b37c-e5c2-4e31-b7d7-5a01044b9027.png)   
---
## Create an alarm
I went to this [tutorial](https://aws.amazon.com/premiumsupport/knowledge-center/cloudwatch-estimatedcharges-alarm/) to find how to create my alarm  
- create an alarm configuration as a json file 
- Call the PutMetricAlarm API:  `aws cloudwatch put-metric-alarm --cli-input-json file://alarm_config.json`  
- I went to my management console to confirm the creation of my alarm  
---
## Creating a budget using the AWS CLI
- I went to the AWS CLI page and clicked on the **command reference** documentation and found instructions for [creating a budget](https://docs.aws.amazon.com/cli/latest/reference/budgets/create-budget.html)  
 - Following the instructions on the page, i created 2 json named "budget.json" and "notifications-with-subscribers.json" 
 - I copied and pasted the necessary json code
 - I read through it and made the necessary changes to set my budget limit and threshold.  
 - I copied the command below to make the necessary changes to folder and account ID: 
 > aws budgets create-budget \
       --account-id 111122223333 \
       --budget file://budget.json \
       --notifications-with-subscribers file://notifications-with-subscribers.json   

- i got my account ID by typing `aws sts get-caller-identity --query Account`  then i inputed my account ID at the appropriate place.  
- i saved my Account id as an environment variable to make it easier to get later, by running the following code `export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)`. Now when i type `env | grep AWS_ACCOUNT_` it outputs my account ID to the terminal. 
- I saved the account ID permanently so i can see it next time I i login without having to re-run all these command. `gp env AWS_ACCOUNT_ID="<Account ID>"
- I pasted the above code in my terminal and ran it.  
- There was no output(which is usually a good indicator that it worked) 
- I went to my management console and checked the budget page and my created budget was there.  
 ![budget completion](https://user-images.githubusercontent.com/105195327/219722136-5dfcfa9b-7b28-40b9-8f6d-399e8a248252.png)  

---
## My Conceptual diagram 
[My crudder conceptual diagram](https://lucid.app/lucidchart/98375dfe-4833-4761-9915-4f0f1f4305c8/edit?viewport_loc=-1849%2C-124%2C1598%2C732%2C0_0&invitationId=inv_bbfc422f-3940-4692-9bd3-879087da10c9)  
 
 ![My Crudder Conceptual Diagram](https://user-images.githubusercontent.com/105195327/219723694-8b0f58f8-0ebd-4c23-9b9b-a52cced04802.png)  

 ---
 ## My logical diagram 
  [My crudder logical diagram](https://lucid.app/lucidchart/95da8a08-80d3-4b01-9b66-d932e19b7752/edit?viewport_loc=324%2C43%2C1769%2C811%2C0_0&invitationId=inv_3b1d18de-5ee0-4d22-bf14-70c3f56ac398) 
 
 ![My Crudder Logical Diagram](https://user-images.githubusercontent.com/105195327/219723669-dd8987e1-87de-4c10-8911-c55b1281a642.png)
---
 
