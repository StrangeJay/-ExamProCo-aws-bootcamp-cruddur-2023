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
---

## Install AWS Amplify
# - I went to look for the frontend code for cognito. 
- I went to my frontend directory, then i ran `npm i aws-amplify --save` to install amplify on my terminal. The **--save** adds it to the package.json file.  
- I checked my package.json file to be sure it was added to the package.  

## Configure Amplify 

- I copied the code `import { Amplify } from 'aws-amplify';
` to my App.js file.  


- I added the commands below to the App.js file, right below the import statements.  

```
Amplify.configure({
  "AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,
  "aws_cognito_identity_pool_id": process.env.REACT_APP_AWS_COGNITO_IDENTITY_POOL_ID,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,
  "oauth": {},
  Auth: {
    // We are not using an Identity Pool
    // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
    region: process.env.REACT_APP_AWS_PROJECT_REGION,           // REQUIRED - Amazon Cognito Region
    userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,         // OPTIONAL - Amazon Cognito User Pool ID
    userPoolWebClientId: process.env.REACT_APP_AWS_CLIENT_ID,   // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
  }
});
```

- I copied the commands below to the frontend section of my dockerfile, and i'm going to fill the values in.  
- I got the user pool ID from my user pool page  


- I got the client side ID by clicking into my user pool, navigating to *App Integration**, and scrolling down to **App analytics**  


---
## Conditionally show components based on if we're logged in or logged out 

### Starting with our HomeFeedPage 
- I navugated to my HomeFeedPage.js file and added `import { Auth } from 'aws-amplify';` import statement.  

- I was going to set a react state to manage a users variable/object. That'll say Usernname, Email, PhoneNumber... That'll be displayed.  I was going to add `const [user, setUser] = React.useState(null);` to my HomeFeedPage.js, in the section with other const statement. but it was already there.  

- I checked to see if i had the **checkAuth** code in my HomeFeedPage.js, and i replaced the existing one, with the one below.  

#### Update ProfileInfo.js   
```
import { Auth } from 'aws-amplify';
```
- I used the line above to replace the cookie import line.   


- I removed the remaining cookie signout line.   


### Signin Page 
- First i decided to compose up to make sure my configurations have been perfect so far. After creating the containers i went to the frontend URL and it was blank.  



- I went back to my App.js file and corrected some typo. I composed down and composed up again, and the frontend was working fine.  



#### Signin Page
- I went to my SigninPage.js file and replaced the import cookie line with `import { Auth } from 'aws-amplify';`  

- I replaced the onsubmit code with the one below.  
```
const onsubmit = async (event) => {
  setErrors('')
  event.preventDefault();
  try {
    Auth.signIn(email, password)
      .then(user => {
        localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
        window.location.href = "/"
      })
      .catch(err => { console.log('Error!', err) });
  } catch (error) {
    if (error.code == 'UserNotConfirmedException') {
      window.location.href = "/confirm"
    }
    setCognitoErrors(error.message)
  }
  return false
}
```


- 

