#!C:\Users\44731\AppData\Local\Programs\Python\Python311\python.exe

import cgi
import cgitb
import mysql.connector # Import the MySQL connector module to interact with the MySQL database

cgitb.enable()

# Retrieve email from the session or a previous form (assuming email is passed as a form parameter for simplicity)
form = cgi.FieldStorage()
email = form.getvalue('email')  # Assuming email is passed as a parameter

# Establish connection to the database
connection = mysql.connector.connect(
 host='localhost',
    database='gp2',
    user='root',
    password='1234')


cursor = connection.cursor()

# Fetching information from pinfo table
pinfo_query = "SELECT name, surname, age, student FROM pinfo WHERE email = %s"
cursor.execute(pinfo_query, (email,))
pinfo_info = cursor.fetchone()

# Fetching information from sinfo table
sinfo_query = "SELECT timing, membership, gym, swimming_pool, classes, massage, physiotherapy, cost FROM sinfo WHERE email = %s"
cursor.execute(sinfo_query, (email,))
sinfo_info = cursor.fetchone()

# Fetching information from finfo table
finfo_query = "SELECT mID FROM finfo WHERE email = %s"
cursor.execute(finfo_query, (email,))
finfo_info = cursor.fetchone()

# Displaying the fetched information to the user
print("Content-type:text/html\r\n\r\n")
print('<!DOCTYPE html>')
print('<html lang="en">')
print('<head>')
print('<meta charset="UTF-8">')
print('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
print('<title>Personal Information</title>')
print('<style>')
print('.container {')
print('    width: 50%; /* Adjust the width as needed */')
print('    margin: 50px auto 0; /* Add margin to the top of the container */')
print('    background-color: red; /* Set background color to red */')
print('    padding: 20px; /* Add padding for spacing */')
print('    box-sizing: border-box; /* Include padding in the width */')
print('}')
print('h1, h2, p {')
print('    color: black;')
print('    text-align: center;')
print('}')
print('body {')
print('    background-image: url("img/feature-2.jpg");')
print('    background-size: cover;')
print('    background-position: center;')
print('    font-family: Arial, sans-serif; /* Setting a fallback font */')
print('    margin: 0;')
print('    padding: 0;')
print('    font-size: 16px; /* Default font size for the entire body */')
print('}')
print('</style>')
print('</head>')
print('<body>')
print('<div class="container">')

if pinfo_info:
    print("<h1>Personal Information</h1>")
    print(f"<p>Name: {pinfo_info[0]}</p>")
    print(f"<p>Surname: {pinfo_info[1]}</p>")
    print(f"<p>Age: {pinfo_info[2]}</p>")
    print(f"<p>Student: {'Yes' if pinfo_info[3] else 'No'}</p>")  
    if finfo_info:
        print(f"<p>Membership ID: {finfo_info[0]}</p>")
    else:
        print("<p>You did not complete your subscription with us.<br> Please, pay for your subscription in order to get a membership ID.</p>")
else:
    print("<p>No personal information found for the provided email.</p>")

if sinfo_info:
    print("<h2>Subscription Information</h2>")
    print(f"<p>Timing: {sinfo_info[0]}</p>")
    print(f"<p>Membership: {'With' if sinfo_info[1] else 'Without'}</p>")
    print(f"<p>Gym: {sinfo_info[2]}</p>")
    print(f"<p>Swimming Pool: {'Yes' if sinfo_info[3] else 'No'}</p>")
    print(f"<p>Classes: {'Yes' if sinfo_info[4] else 'No'}</p>")
    print(f"<p>Massage Therapy: {'Yes' if sinfo_info[5] else 'No'}</p>")
    print(f"<p>Physiotherapy: {'Yes' if sinfo_info[6] else 'No'}</p>")
    print(f"<p>Cost: {sinfo_info[7]}</p>")
else:
    print("<p>No subscription information found for the provided email.</p>")

# Add a button to return to the homepage
print('<form action="gym_recommendation.html" method="get">')
print('<button type="submit">Return to Homepage</button>')
print('</form>')
print('</div>')
print('</body>')
print('</html>')

# Commit the new entry to the database
connection.commit()

# Close database connection
cursor.close()
connection.close()
