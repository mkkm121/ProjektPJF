# Restaurant Project
Simple resturant application using the Python Flask micro-framework.

Table of contents:
<li><a href="#Overview">Overview</a></li>
<li><a href="#Technologies">Technologies</a></li>
<li><a href="#Look">Look</a></li>
<li><a href="#Instalation">Instalation</a></li>

# Overview
In this project, a simple web application for restaurants was created. The software allows you to log in, register, manage your account and place orders for customers. The customer can pay by card using the Stripe API. The admin, i.e. the restaurant employee, has full control over orders. So it can cancel or change the state of client requests.

# Technologies

Core components:
<li>Python flask application</li>
<li>SQLAlchemy Database</li>
<li>HTML/CSS</li>
<li>Stripe API</li>

# Look
Home page
![image](https://i.postimg.cc/nLkLrs1k/obraz-2022-01-27-160259.png)
Offer page
![image](https://i.postimg.cc/0jdvWFHC/obraz-2022-01-27-160443.png)
Ordering
![image](https://i.postimg.cc/tCkyh06q/obraz-2022-01-27-160523.png)
Cart
![image](https://i.postimg.cc/HsRzvnXB/obraz-2022-01-27-160640.png)
Contact page
![image](https://i.postimg.cc/LXWg4YHW/obraz-2022-01-27-160822.png)
Account page
![image](https://i.postimg.cc/RFWQTzhj/obraz-2022-01-27-160849.png)
Admin panel
![image](https://i.postimg.cc/mD3ZJPPM/Zrzut-ekranu-2022-01-27-160949.png)

# Instalation
Before running, install all packages using the command:
```
$ pip install -r requirements.txt
```
Then start the application
```
$ python run.py
```
