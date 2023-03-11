# Week 3 — Decentralized Authentication 

## Create user pool on AWS 
- I went to my AWS management console, searched for **Amazon Cognito** and clicked into it.  ![create user pool](https://user-images.githubusercontent.com/105195327/224273651-e778ad11-d0ed-40a1-a5e7-7d2bc5b2052e.png)  

- I saw 2 options for provider types, ""Cognito User Pool"" and ""Federated Identity Providers**  
![Authentication Providers](https://user-images.githubusercontent.com/105195327/224278181-e3e74ba3-a99a-4698-ba54-5462126c43dc.png)  


> **Note** "Cognito user pool" is for when you're making a web application and you want to add login and signup, and manage it externally. While federated identity providers, is when you want to be able to login using a social identity from another provider. With user pool you can add different methods of identity providers, but federated is a little different. 

- I checked the option to log in with **user name** and **email.**  
- I set password policy to default    
![Password policy](https://user-images.githubusercontent.com/105195327/224280889-959ea303-7c11-4fe3-ba37-77ad1899ef44.png)  

- I left the option to use MFA unchecked, to save and prevent spend.  
![MFA](https://user-images.githubusercontent.com/105195327/224281027-e64de56f-78c3-4741-8414-91a43712da72.png)  

- I enabled self account recovery to allow users recover their accounts by themselves without having to email me to reset it for them.  

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
 ![aws amplify installation](https://user-images.githubusercontent.com/105195327/224457063-c7d2ed45-ae2f-4bcf-b48f-025bc71fe5d9.png)  

## Configure Amplify 

- I copied the code `import { Amplify } from 'aws-amplify';
` to my App.js file.  
![amplify in AppJs](https://user-images.githubusercontent.com/105195327/224457087-a6aadf44-6b7f-469a-bb1e-5576d63dd4ec.png)  

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
![dockerfile amplify ish](https://user-images.githubusercontent.com/105195327/224457146-a2a0edd2-5646-4277-8a71-718d745296d0.png)  

- I got the user pool ID from my user pool page  
![user pool ID](https://user-images.githubusercontent.com/105195327/224457163-55c3d93c-8c57-499d-b0b1-20ec48656acd.png)  

- I got the client side ID by clicking into my user pool, navigating to *App Integration**, and scrolling down to **App analytics**  
![app client id 1st](https://user-images.githubusercontent.com/105195327/224457190-2452f080-df05-47b8-953a-b2faeb0a1596.png)  

![app client id](https://user-images.githubusercontent.com/105195327/224457207-e2429711-2482-4779-9d06-30909d4997b7.png)  

---
## Conditionally show components based on if we're logged in or logged out 

### Starting with our HomeFeedPage 
- I navigated to my HomeFeedPage.js file and added `import { Auth } from 'aws-amplify';` import statement.  

- I was going to set a react state to manage a users variable/object. That'll say Username, Email, PhoneNumber... That'll be displayed.  I was going to add `const [user, setUser] = React.useState(null);` to my HomeFeedPage.js, in the section with other const statement. but it was already there.  
![react state](https://user-images.githubusercontent.com/105195327/224457326-2d6640bd-1133-4fb6-91ba-f768c8f1d136.png)  

- I checked to see if i had the **checkAuth** code in my HomeFeedPage.js, and i replaced the existing one, with the one below.  
![checkAuth](https://user-images.githubusercontent.com/105195327/224475274-25bcf267-0752-4fd7-9249-8d1bf9982cec.png)   

#### Update ProfileInfo.js   
```
import { Auth } from 'aws-amplify';
```
- I used the line above to replace the cookie import line.   
![profileInfo replacement](https://user-images.githubusercontent.com/105195327/224475321-21f2614c-dc99-4c9e-b9e1-fe705f42c179.png)  

- I removed the remaining cookie signout line.   
![cookie replacement line](https://user-images.githubusercontent.com/105195327/224475264-71b74365-24c6-4ebd-bb82-e8cbcd26e8ce.png)


### Signin Page 
- First i decided to compose up to make sure my configurations have been perfect so far. After creating the containers i went to the frontend URL and it was blank.  
![blank frontend](https://user-images.githubusercontent.com/105195327/224475404-03d09074-08a0-4d2c-80c1-8140c81b0d77.png)  

- I went back to my App.js file and corrected some typo. I composed down and composed up again, and the frontend was working fine.  
![frontend working](https://user-images.githubusercontent.com/105195327/224475413-6931599b-26f1-4873-8994-cc4e85e593cc.png)  

#### Signin Page
- I went to my SigninPage.js file and replaced the import cookie line with `import { Auth } from 'aws-amplify';`  
![signin page](https://user-images.githubusercontent.com/105195327/224475437-f8eaa353-5241-4e3d-9ad7-99e640b45b78.png)  

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

![signin paage on submit](https://user-images.githubusercontent.com/105195327/224475458-f9f1e155-221c-4483-89d3-f49dc93efa45.png)  

- I saved and went back to the frontend URL, i tried signing in a user that doesn't exist and i got an error saying **"Error! NotAuthorizedException: Incorrect username or password."** while inspecting the page.  
![no user error](https://user-images.githubusercontent.com/105195327/224475482-3d707b8d-5fc0-44dd-b0b0-b4cf991cffd5.png)  

- The error was expected, but i wanted it to give the error message on the signin page. I went back to check my code.  

- I made some changes and tried it again. This time it worked.  
![signin error showing at log in](https://user-images.githubusercontent.com/105195327/224475511-0c241188-ce1b-4123-89c6-6f325917010c.png)  

- Went to my user pool on AWS to add a user.  
![create user](https://user-images.githubusercontent.com/105195327/224475517-b4e6b65c-b24d-4d50-a18c-2d91ab7d1ddc.png)  

![created the user details](https://user-images.githubusercontent.com/105195327/224475539-1f1d8f5c-097d-4e2b-9cb5-6fb07581e0d7.png)  

- I tried signing in to confirm the user is recognised, but i got an error.  
![error for created user signin](https://user-images.githubusercontent.com/105195327/224475548-12cc567a-54bb-4286-8ebc-937bf14d2f03.png)

- I went back to my code to do some investigations and find out what's wrong.  
---
#### Fix
- This line of code was what caused the error, because i haven't set the token yet. I will leave it as it is for now, and find a quick fix to continue testing.  

- I googled a fix for the problem and found one [here](https://stackoverflow.com/questions/40287012/how-to-change-user-status-force-change-password) 

```
aws cognito-idp admin-set-user-password \
  --user-pool-id <your-user-pool-id> \
  --username <username> \
  --password <password> \
  --permanent
```


- I went to my terminal and ran this code `aws cognito-idp admin-set-user-password --username jay_kaneki --password Testing123. --user-pool-id us-east-1_oIWpVFT2R --permanent` 
then i went back to try it out and it worked.  

- I clicked on signout and i was successfully signed out. 

- I remembered the username section said "@handle" instead of the actual users handle because we didn't select "prefered username" as an attribute. We would fix that.  

- I went to my created user, set a name and set additional attribute and a value.  

- I signed back in and the user handle was there.  

- I signed out, went back to my user to delete that user because i want to create the signup function next, so we can add our user with the signup button.  
---

## Signup Page
- I went to my SignupPage.js file to implement my codes. 

- i replaced the import cookie line with `import { Auth } from 'aws-amplify';` like i did for the signin page. 

- I replaced the **onsubmit** section with the code below.  

```
const onsubmit = async (event) => {
  event.preventDefault();
  setErrors('')
  try {
    const { user } = await Auth.signUp({
      username: email,
      password: password,
      attributes: {
        name: name,
        email: email,
        preferred_username: username,
      },
      autoSignIn: { // optional - enables auto sign in after user is confirmed
        enabled: true,
      }
    });
    console.log(user);
    window.location.href = `/confirm?email=${email}`
  } catch (error) {
      console.log(error);
      setErrors(error.message)
  }
  return false
}
```


### Confirmation Page
- I went to my ConfirmationPage.js file, i replaced the import cookie line with `import { Auth } from 'aws-amplify';` 





