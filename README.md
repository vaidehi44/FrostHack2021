 # Online Education Platform for Institutes
 
 Effective online eduaction has become must now. So it is necessary for schools and institutes to have their own platforms which would help in organized and effective learning and teaching experience for students, teachers and schools. Considering this, during Frosthack 2021, I have tried to develop this website which includes some basic functionalities which the platform should serve.
 Basically, I have built three portals - Admin, Student and Teacher. Description for them is as follows -
 
 Admin portal - Allows admin to upload/update timetables for each class as excel files, upload/update lecture links for each class, make new announcements or remove previous ones.
 
 Student portal - Allows student to access his/her class timetable and link(every class would have only one link and timetable), see the announcements made by the admin, see the assignments give by teacher and an option for submitting the assignment.
 
 Teacher portal - Allows teacher to access his/her timetable, class links for each class, option to give new assignments or close previous ones and see the noticeboard.
 
 Website has been built using Django. It can be run on local machine by following the steps given in next section.
 
 # Installation guide
 
 ### Step 1 : Clone this repository
 Go to the folder where you want to install the code and then run -
 `git clone https://github.com/vaidehi44/FrostHack2021.git`
 ### Step 2 : Create and activate a virtual environment
 Make sure you have python, pip and virtualenv installed. For creating and activating the environment(in windows) run-
 ```
 python -m venv virtenv
 virtenv\scripts\activate
 ```
 
 ### Step 3 : Install the dependencies
 Enter the project repository('FrostHack2021') and run 
 `pip install -r requirements.txt`
 
 ### Step 4 : Generate a secret key 
Make a new file named 'secrets.sh' in the root repository. Generate a secret key for Django from http://www.miniwebtool.com/django-secret-key-generator/ and paste the key in 'secrets.sh' file -

 `export SECRET_KEY='<secret_key>'`
 
 ### Step 5 : Run the migrations commands - 
 ```
 python manage.py migrate
 python manage.py makemigrations
 python manage.py migrate
 ```
 
 ### Step 6 : Run the server
 `python manage.py runserver`
 
 Go on http://127.0.0.1:8000/portals. If everything went well, you should be able to see the login options for all the three portals. You can login to any portal using the credentials given in next section. To make your own new users, use the admin site of Django (http://127.0.0.1:8000/admin).
 
 ## User credentials - 
 Admin portal: username - `admin`
 
 Student portal:
 usernames - `student1`, `student2`
 
 Teacher portal:
 usernames - `teacher1`, `teacher2`
 
 Password for all the users is - `Pass@123`
 
 
