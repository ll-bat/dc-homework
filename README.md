### Fully dockerized Book Search application 

#### Supports 
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


### Some screenshots

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

