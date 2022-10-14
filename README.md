### Fully dockerized Book Search application

#### here is the [demo url](https://dc-homework.herokuapp.com/)

#### App Supports 
 - Searching books by ISBN number (10 digit or 13 digit) 
 - Authorization/Registration (Social login with **Gmail** and **Facebook** is supported)
 - Forgot password feature 
 - Storing encrypted passwords

### How book search works 
When user tries to search for specific book, system first checks if such book exists in DB, 
if not, it uses public Google Book API service to fetch book metadata and saves it in DB, so next time 
it won't have to query API for same book 

### Some quick notes about app 
 - ISBN number is validated in both frontend and backend
 - ISBN validation is divided into two parts:
   - Validating common pattern with RegEx
   - Check Digit validation
 - When recovering password, link is instantly given to user on the page and email is not sent

### To run with `docker`
 - run `docker-compose up`

### To run without `docker`
 - activate `virtualenv` 
 - run `pip install -r requirements.txt`
 - run `python manage.py migrate`
 - run `python manage.py runserver`

### To use Google Book API service
   - Go to [Google console](https://console.cloud.google.com/)
   - Pick a project or create new one and get into it
   - Go to `Credentials` section from left-hand side 
   - Create new `API key`
   - Copy that `API key` and paste it in .env file with key: `BOOK_API_TOKEN` e.i (BOOK_API_TOKEN=<YOUR_TOKEN>)

### To setup social login with Facebook 
   - Go to [facebook developers page](https://developers.facebook.com/)
   - Go to `My Apps` and pick an app or create new one and get into it
   - Go to `Settings > basic` and configure `App Domains` (This must include your app's domain. if developing locally, add `localhost`) and at the bottom press `Add platform`, choose `Website` and add `Site URL`, such as `http://localhost:8000`
   - Then configure `Redirect URLs`  from `Facebook Login > Settings` page (This step is not mandatory if developing locally, e.i using `localhost` as a domain)
   - Copy `App ID` and `App Secret` from `Settings > Basic` page and paste them in .env file with keys: `SOCIAL_AUTH_FACEBOOK_KEY` and `SOCIAL_AUTH_FACEBOOK_SECRET`

### To setup social login with Gmail
   - Go to [Google console](https://console.cloud.google.com/)
   - Pick a project or create new one and get into it
   - Go to `Credentials` section from left-hand side
   - Create `OAuth Client ID` by pressing `+ CREATE CREDENTIALS` at the top and selecting `OAuth Client ID`
   - When creating `OAuth Client ID`
     - Add your app url under `Authorized JavaScript origins` , such as `http://localhost:8000`
     - Add redirect url under `Authorized redirect URIs`. Redirect url must have such pattern: `${APP_URL}/accounts/google/login/callback/`, for example: `http://localhost:8000/accounts/google/login/callback/`
   - After creating `OAuth Client ID` grab `Client ID` and `Client secret` and save somewhere, we'll need them for next step
   - Go to your app's admin panel, choose `Social applications` table, and add a record 
      - In the `Provider` field, choose `Google`
      - In the `Client id` field, paste `Client ID` you have copied
      - In the `Secret key` field, paste `Client secret` you have copied and press save

### Some screenshots from app

#### search book
![Admin panel](https://raw.githubusercontent.com/ll-bat/dc-homework/master/static/images/search-book.png)
![Admin panel](https://raw.githubusercontent.com/ll-bat/dc-homework/master/static/images/search-book-v2.png)

#### Invalid ISBN 
![Admin panel](https://raw.githubusercontent.com/ll-bat/dc-homework/master/static/images/invalid-isbn.png)

#### ISBN section 
![Admin panel](https://raw.githubusercontent.com/ll-bat/dc-homework/master/static/images/isbn-description.png)

#### Login page 
![Admin panel](https://raw.githubusercontent.com/ll-bat/dc-homework/master/static/images/login-page.png)

#### Reset password 
![Admin panel](https://raw.githubusercontent.com/ll-bat/dc-homework/master/static/images/reset-password.png)

#### Sign up
![Admin panel](https://raw.githubusercontent.com/ll-bat/dc-homework/master/static/images/sign-up.png)

