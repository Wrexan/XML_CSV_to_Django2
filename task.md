THE TEST
JUNIOR PYTHON DEVELOPER

Create a web application on the Django 4.1 framework. The application must match XML and
CSV files with user information. You need to collect a complete set of user data. The XML data
file contains first_name and last_name of the user, while the CSV file includes username,
password, and date_joined.
The files may contain data in round and square brackets, they should be ignored. There may
also be information about some users in CSV, but there’s none in XML, or vice versa. These
users should also be ignored.
The collected information (except for the password) should be visible on the main page of the
web app, it can only be accessed through authorization when the user is an admin. Users
must be able to log in, and they must be displayed in the Django admin panel. On this page,
we recommend using Bootstrap 5. It should look clear and readable on desktop, phone, and
tablet.
There should also be a logout button. The administrator must be able to start data collection
and select a data source.
Extra credit assignments:
- In the XML file, there is a link to the user's avatar. You need to expand the user model, add a
field for the avatar, and show it on the user data page.
- Create unit tests to test the logic of data collection.
Required files:
https://drive.google.com/drive/folders/1LiVUbRWof8TyHj2SXoRwqDCgotHjSoQB?usp=sharing.
The test task must be uploaded to GitHub and include instructions for running. The choice of
the database and other libraries is up to you. Also, write down how much time you spent on it.