# Phone Polls  
  

  
## Purpose  
* This website is used to vote for your favourite mobile phone.   
Users need to register on the web before voting.  
Each user can only vote once.  

## Design
* This multi-users web application is design to vote the most popular mobile phone model.  
Which uses HTML, CSS, Flask, AJAX, JQuery, and Bootstrap.  
The type of social choice mechanism is first past the post voting.  

### Development platform: 
* macOS  

### Development tools:  
* PyCharm 2019 


## Modules
* Some of the essential modules that the website used are:
 * Flask - which is the framework of the web application
 * Flask-Admin
 * Flask-Login
 * Flask-Migrate
 * Flask-SQLAlchemy
 * Flask-WTF

## Basic Elements
* The header  
 * The header is the web navigation which has the name of the website and Home, login, logout, profile, admin system functions which allowed users to enter corresponding pages.

* The footer
 * At the footer is the design information about this website. The right side is the current time, the last login time of the user and the name of the user who logged in.

## Web Page Distribution
* Home Page
 * When a user opens the web page, the first thing that appears is the Homepage, which shows the current voting results. The results are presented in the form of a bar chart and a pie chart (which allowed visitors to change the view way to see the results), user can switch the form at the bottom right of the table. On the right side of the page is the message board of the logged in user. User can post anonymously.

 * At the bottom left of the chart is the voting button. When the user who has logged in clicks, the voting menu will be displayed, and the voting will be based on the model of the mobile phone in the list. If the user is not logged in, they will jump to the login page.
![Home Page](https://github.com/Prestonccc/phone_polls/blob/master/README_image/homepage.png?raw=true) 

* Login Page
 * The page allows users to login with inputting users information, alert message if the information is wrong. If login successfully, then jump to vote page if the user hasn’t voted yet, otherwise jump into the result page. If the visitor is an new user, the web will provide a register link to register.
![Login page](https://github.com/Prestonccc/phone_polls/blob/master/README_image/login.png?raw=true)

* Vote Page
 * Vote button to let user vote, then jump into result page.
![Vote page](https://github.com/Prestonccc/phone_polls/blob/master/README_image/votepage.png?raw=true)

* User Page
 * The user page shows the user’s profile photo, and the user can write “about me” by going through the edit profile and submit.
 * The response on voting that user post on the home page will be recorded on his profile page.
![User page](https://github.com/Prestonccc/phone_polls/blob/master/README_image/profile.png?raw=true)

* Admin System
 * The admin system is going to control and manage the whole database:  
 user table-add or delete user, vote table-manage the vote by the user, admin table-add or delete administrators, post able- manage posts, phone table-add or delete phone vote options.
![Admin System](https://github.com/Prestonccc/phone_polls/blob/master/README_image/admin_total.JPG?raw=true)
 
