To run the application you must set up the front end and backend in seperate terminals.



For the frontend run these commands in this order:


Navigate to the frontend folder with: cd frontend (assuming you're in the root folder)

Then install all the dependencies with: npm install

Start up the server with: npm run dev



For the backend run these commands in this order:


Navigate to the frontend folder with: cd backend (assuming you're in the root folder)

Next, install all the dependencies: pip install -r requirements.txt

Create the database using python manage.py makemigrations

And python manage.py migrate

Start up the backend server: python manage.py runserver

Now you can navigate to http://localhost:5173/ to access the web application.


There is a moderator account with the following credentials:

Username: admin

Password: 123