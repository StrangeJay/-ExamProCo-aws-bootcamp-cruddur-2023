# Week 3 — Decentralized Authentication 

## Create user pool on AWS 
- I went to my AWS management console, searched for **Amazon Cognito** and clicked into it.  ![create user pool](https://user-images.githubusercontent.com/105195327/224273651-e778ad11-d0ed-40a1-a5e7-7d2bc5b2052e.png)  

- I saw 2 options for provider types, ""Cognito User Pool"" and ""Federated Identity Providers**  
![Authentication Providers](https://user-images.githubusercontent.com/105195327/224278181-e3e74ba3-a99a-4698-ba54-5462126c43dc.png)  


> **Note** "Cognito user pool" is for when you're making a web application and you want to add login and signup, and manage it externally. While federated identity providers, is when you want to be able to login using a social identity from another provider. With user pool you can add different methods of identity providers, but federated is a little different. 

- I checked the option to log in with **user name** and **email.**  
- I set password polict to default    
![Password policy](https://user-images.githubusercontent.com/105195327/224280889-959ea303-7c11-4fe3-ba37-77ad1899ef44.png)  

- I left the option to use MFA unchecked, to save and prevent spend.  
![MFA](https://user-images.githubusercontent.com/105195327/224281027-e64de56f-78c3-4741-8414-91a43712da72.png)  

- I enabled self account recovery to allow users revover their accounts by themselves without having to email me to reset it for them.  

- I chose only email as the delivery method for recovery message, because it cost money to use SMS and i don't want to incure spend. Email costs less and right now is free because my free tier covers it and my Amazon SES grants me 62,000 Outbound messages per month.     
![password recovery](https://user-images.githubusercontent.com/105195327/224283434-8e80f7be-4bce-411e-92b9-ccc3d7ada17c.png)  
- On the next page, i left everything on default, then for the **"required attribute"** all i selected was **"name"**  
![attribute change](https://user-images.githubusercontent.com/105195327/224288305-928f2858-ed74-4a09-851b-013357b44605.png)  

> **Note** When an attribute is selected, it can't be changed(only the value changes) so make sure what you're selecting is what you actually want.  

- Next page required me to make a selection between sending email with Amazon SES or Cognito. SES is the recommended, but it involves extra setting(which requires having a domain name) that we would do much later, for now, we would be using Cognito.  
![content message delivery](https://user-images.githubusercontent.com/105195327/224290216-24ec66eb-3d69-40e8-b1bc-fd850804aa2b.png)  
*Cognito allows you send 50 messages, that's very low, which is why i might change the settings later.*  

- On the next page i set App client name and user pool name, then i left everything else as default.  
- My user pool was successfully created. 


