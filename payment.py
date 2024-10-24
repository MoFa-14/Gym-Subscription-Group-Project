#!C:\Users\44731\AppData\Local\Programs\Python\Python311\python.exe


import cgi
import cgitb
import mysql.connector
import random

cgitb.enable()

# Function to generate a unique mID
def generate_mid(cursor):
    while True:
        # Generate a random mID between 10000 and 99999
        mID = random.randint(10000, 99999)
        # Check if the generated mID already exists in the finfo table
        cursor.execute("SELECT mID FROM finfo WHERE mID = %s", (mID,))
        # If mID does not exist, it's unique, so return it
        if not cursor.fetchone():
            return mID

# Establish connection to the database
connection = mysql.connector.connect(
 host='localhost',
    database='gp2',
    user='root',
    password='1234')
cursor = connection.cursor()

# Retrieve email from the session or a previous form (assuming email is passed as a form parameter for simplicity)
form = cgi.FieldStorage()
email = form.getvalue('email')  # Assuming email is passed as a parameter

# Check if the email exists in pinfo but not in finfo
select_query = "SELECT email FROM pinfo WHERE email = %s"
# Execute the select query with the email parameter
cursor.execute(select_query, (email,))
# Fetch the result of the select query
pinfo_result = cursor.fetchone()

# Check if the email exists in finfo
cursor.execute("SELECT mID FROM finfo WHERE email = %s", (email,))
finfo_result = cursor.fetchone()

if not pinfo_result:
    # If email does not exist in pinfo table, display an error message
    print("Content-type: text/html")
    print()
    print("<html><body><h2>Error: Invalid email!</h2><p>Please enter your correct email.</p></body></html>")
elif finfo_result:
    # If email exists in finfo table, display an error message
    print("Content-type: text/html")
    print()
    print("<html><body><h2>Error: Duplicate email!</h2><p>Your email has already been used. Please enter a different email.</p></body></html>")
else:
    # email exists in pinfo but not in finfo, proceed with generating mID
    mID = generate_mid(cursor)
    # Insert the new mID and email into the finfo table
    insert_query = "INSERT INTO finfo (mID, email) VALUES (%s, %s)"
    # Execute the insert query with the generated mID and email
    cursor.execute(insert_query, (mID, email))
    # Commit the new entry to the database
    connection.commit()

    # Retrieve subscription information including cost from sinfo table
    sinfo_query = "SELECT cost FROM sinfo WHERE email = %s"
    cursor.execute(sinfo_query, (email,))
    subscription_cost = cursor.fetchone()

    # HTML content to confirm subscription and offer navigation
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Subscription Confirmation</title>
    </head>
    <body>
    <link rel="stylesheet" href="MemIdsignup.css">
    <!-- top page -->
    <div class="m_top inclusive">
        <div class="logo">
            <h1>FITFUSION</h1>
        </div>
    </div>
        <div>
            <div class="container">
            <h2>You have successfully subscribed with us!</h2>
            <p style="font-size: 24px; font-weight: bold;">Your membership ID is: {}</p>
            <p>Subscription Cost: {}</p>
            <a href="index.html">
                <button type="submit">Return to Homepage</button>
                      <a>
            </form>
        </div>
    </body>
    </html>
    """.format(mID, subscription_cost[0])

    print("Content-type: text/html")
    print()
    print(html_content)

# Close database connection
cursor.close()
connection.close()
