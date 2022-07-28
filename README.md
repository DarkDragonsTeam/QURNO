# QURNO News/Technology Web Application
Greetings and courtesy to all of you dear colleagues and friends of the DarkDragons team. We came back with another repository/project. This time of the public and free type. QURNO is a blog-based web application that can be used in any way you like. A product, a repository, a project and of course a tutorial! At QURNO you can read and write about anything but general technical news. Of course, QURNO is designed in such a way that you can learn in it. We have given you enough information, documents and comments to fully understand what is happening at QURNO. In fact, QURNO is a blog-based website that is really fully developed, QURNO has been trying to bring the best features of a blog-based website. QURNO under the Free, Open Source and Copyleft licenses
 GPL (GNU GENERAL PUBLIC LICENSE) Version 3 has been released, which means you can develop and distribute it any way you want. What are you waiting for? Let's go and get more acquainted with QURNO and install it :)

<span style="color: red;">
In the hope of freeing our beloved IRAN from sanctions<3</span>

***

## What is QURNO developed with?
We have tried to develop QURNO with the most modern technologies in the world. In fact, with technologies that make QURNO safe, fast and light.

### Server/Back-End development
* Django 

Django is a web application development framework for Python that allows you to develop projects as quickly as possible with the utmost security and processing speed.

### Database development
Database is a regular member in software development science. It is very important to know what database you are using, because the speed of development and processing speed of your work is very much dependent on it.

* PostgreSQL

PostgreSQL database system and DBMS is a powerful engine that you can use to process very large data. Running QURNO on PostgreSQL is recommended.

* SQLite

SQLite is a small, optimized engine that you can use for QURNO development and fast viewing. SQLite does not require any special installation or additional work, you just need to install the relevant libraries to use it.

### Design/Client/Front-End development
One of the most important parts of QURNO and software development in general is the design and appearance section. Strong communication with the user is mostly done through the appearance of the software. At QURNO, we strive to design a beautiful and simple user interface with the utmost creativity and thinking, which is both user-friendly and beautiful.

* Creative CSS and SCSS!

In fact, many parts of the site design have been done with CSS and SCSS. CSS and SCSS do not require much skill, you just need to be creative to be able to create a beautiful user interface.

* Bootstrap

We used bootstrap framework technology in CSS to accelerate QURNO development. Bootstrap can be a great option for large projects.

* JavaScript but to a certain extent!

We all know that the web is meaningless without JavaScript. JavaScript is a kind of web design spirit, but it should be used enough. Too much JavaScript in a website reduces processing speed, software security and boredom. We have used it enough to give a special spirit to our project.

***

## What are the features of QURNO?

### QURNO can be a tutorial!
Most of the clean development rules are followed in QURNO, while everywhere it is commented so that the user can safely develop QURNO and, of course, learn the related technologies!

### QURNO is safe
All security protocols (to the best of our knowledge and facilities) have been followed in QURNO. We have also complied with database security standards.

### QURNO is fast
There are several requirements for the high processing speed of a software, most of which we have met. Despite the high speed in Django itself, we have tried to follow the protocols related to processing speed.

### In general, QURNO standard has been developed
There are many rules for clean development. We have tried to comply with most of them and of course we have succeeded. For example, we have complied with the PEP8 standard in Python coding.

### QURNO has little dependence
Most software today requires a lot of files and resources to run. Fortunately, QURNO does not depend much on many resources, and most features are internally designed. But to observe the principle of cooperation in a community, we have used external packages and modules.

### QURNO is Dockerized
We have developed QURNO with Docker so that you can use it in any type and wherever you want. The Docker system is great and important, try to learn it, we have given enough information about Docker in the project files.

### QURNO launches fast
It is enough to be familiar with the installation to be able to set up QURNO. The easier solution, though, is to use Docker's lovely system and service.

### QURNO has permanent support
The DarkDragons team is responsible for the ongoing protection and support of QURNO and is ready to accept any criticism, development or distribution from you dear ones.

***

## Developers and stakeholders
QURNO was developed by DarkDragons, but its main developer is [Navid Rahimzadeh](https://www.github.com/navidrahimzadeh), a developer and programmer of mobile, cross-platform and web.

For various reasons, it has been decided not to mention DarkDragons collaborators in this project.

***

## QURNO installation
As standard, two installation methods are suggested by DarkDragons.
* Docker System
* Classic Setup

### Docker System
Setting up with Docker will allow you to quickly and hassle-free access to the project and its resources. Just install Docker on your operating system and run Docker Desktop.

To run the project in Docker, just enter the following commands in order.

First we tell Docker to pull project structure images.
```commandline
docker pull python:latest
docker pull postgres:latest
```

These two commands allow Docker to install and run Image Python and PostgreSQL software.

In the next command, we tell Docker to launch our project-specific image.
```commandline
docker build .
```

Docker has now created a custom image for our project. You can combine this image with the PostgreSQL software image.

Now we need to use Docker Compose to attach your project image to Image of PostgreSQL.

```commandline
docker-compose up
```

And over! The project is now ready to run on [127.0.0.1](http://127.0.0.1:8000) (on port 8000). You can use the ***docker-compose exec web (python manage.py COMMAND)*** command to manage project-related commands.

For example:
```commandline
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

#### Docker Tips
* Your environmental variables are stored in the docker-compose.yaml file. Be careful to keep this file correct.
* Docker is under sanctions in Iran, Cuba, North Korea, Sudan and several other countries, beware.
* Be sure to read the docker-compose.yaml file and the dockerfile file. There is a convincing explanation.

### Classic installation
To install a classic project, you must first have PostgreSQL installed. Although installing PostgreSQL is not mandatory, it is best to do so.

Now you have two options:
* Project installation with SQLite
* Project installation with PostgreSQL

#### SQLite

If you want to install the project with SQLite, your work is not very annoying. Enough ***(Comment or delete psycopg2-binary and psycopg2 packages - in the requirements.txt file)*** and then enter the following command.
```commandline
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The required QURNO packages are now installed. It's time to set the environmental variables for QURNO and Django.

To set environmental variables in CMD:
```cmd
set SECRET_KEY=YOUR SECRET_KEY
```

To set environmental variables in PowerShell:
```powershell
$env:SECRET_KEY = "YOUR SECRET_KEY"
```

To set environmental variables in Unix Terminals:
```bash
export SECRET_KEY=YOUR SECRET_KEY
```

```commandline
python manage.py migrate
python manage.py runserver
```
[127.0.0.1:8000](https://127.0.0.1:8000)

And the whole project is now (SQLite dependent) executable.

#### PostgreSQL
Getting started with PostgreSQL is a bit more complicated. You should now have PostgreSQL installed on your system, which we hope it will be, because installing PostgreSQL is really troublesome.

We expect you to complete all the installation of PostgreSQL.

Now launch a new database and enter your details in it. (Preferably do this with a new ROLE in the PostgreSQL database.)

Convert your database profile to environmental variables. (With the following characteristics)

* DATABASE_NAME = "Enter the name of the database created"
* DATABASE_ROLE = "Enter the name of the ROLE with which you created the database."
* DATABASE_ROLE_PASSWORD = "Enter the ROLE password with which you created the database."
* Enter your SECRET_KEY with these values.

You can run these values in different commandlines as follows. 

In CMD:
```cmd
set SECRET_KEY=YOUR SECRET_KEY
set DATABASE_NAME=Enter the name of the database created.
set DATABASE_ROLE=Enter the name of the ROLE with which you created the database.
set DATABASE_ROLE_PASSWORD=Enter the ROLE password with which you created the database.
```

In PowerShell:
```powershell
$env:SECRET_KEY = "YOUR SECRET_KEY"
$env:DATBASE_NAME="Enter the name of the database created."
$env:DATABASE_ROLE = "Enter name of ROLE with which you created the database."
$env:DATABASE_ROLE_PASSWORD = "Enter the ROLE password with which you created the database."
```

In Bash:
```bash
export SECRET_KEY=YOUR SECRET_KEY
export DATABASE_NAME=Enter the name of the database created.
export DATABASE_ROLE=Enter the name of the ROLE with which you created the database.
export DATABASE_ROLE_PASSWORD=Enter the ROLE password with which you created the database.
```

<span style="color:red;">Note: By default, we assume that you are using the Docker system. In the Docker system, the database runs on the db host by default, but in PostgreSQL the original version is not. Change the host in DATABASES - default to 127.0.0.1 (or any other host you created). (Preferably convert the values of the hosts to an environmental variable. ***Especially in the production phase***.)</span>

<mark>Now you need to install the required packages in addition to the PostgreSQL adapter. This is important because PostgreSQL has two psycopg2 and psycopg2-binary adapters. Psycopg2 is actually a complete adapter, but psycopg2-binary, as its name implies, only works. The "requirements.txt" file also mentions this, first test whether psycopg2 works or not, if you find that it does not work, disable (comment) psycopg2 and enable psycopg2-binary.</mark>

```commandline
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Now that all the environment variables are set, ***(without closing the current Shell)*** Open another Shell and test whether the connection is secure.

```commandline
python manage.py check
```

If all goes well, be happy, because for the first time you will definitely get into trouble and need a lot of research. In general, setting up Django and PostgreSQL for a novice will not be easy, so do not despair.

***

## License
The license for this project is GNU GPL version three. You can manipulate, redistribute and rewrite this project and repository. You are generally free to do whatever you want with it. DarkDragons will give you this permission.

If you want to know more about the structure of GNU GPL, you can read the LICENSE.txt file in this basic directory.

***

<span style="font-size: 40px;">Thanks for reading this README</span>
 
 
<span style="font-size: 40px;">DarkDragons Team</span>
