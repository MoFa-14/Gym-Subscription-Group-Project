#!C:\Users\44731\AppData\Local\Programs\Python\Python311\python.exe

import cgi
import cgitb
import mysql.connector # Import the MySQL connector module to interact with the MySQL database

cgitb.enable()

# lists of prices for different services and memberships
ugym_membership_prices = {    
    "super_off_peak": {
        "gym_access": 16,
        "swimming_pool": 15,
        "classes": 10,
        "massage_therapy": 25,
        "physiotherapy": 20
    },
    "off_peak": {
        "gym_access": 21,
        "swimming_pool": 15,
        "classes": 10,
        "massage_therapy": 25,
        "physiotherapy": 20
    },
    "anytime": {
        "gym_access": 30,
        "swimming_pool": 15,
        "classes": 10,
        "massage_therapy": 25,
        "physiotherapy": 20
    }
}

ugym_no_membership_prices = {
    "joining_fee": 10,
    "swimming_pool": 25,
    "classes": 20,
    "massage_therapy": 30,
    "physiotherapy": 25
}

power_zone_membership_prices = {
    "super_off_peak": {
        "gym_access": 13,
        "swimming_pool": 12.5,
        "classes": 0,
        "massage_therapy": 25,
        "physiotherapy": 25
    },
    "off_peak": {
        "gym_access": 19,
        "swimming_pool": 12.5,
        "classes": 0,
        "massage_therapy": 25,
        "physiotherapy": 25
    },
    "anytime": {
        "gym_access": 24,
        "swimming_pool": 12.5,
        "classes": 0,
        "massage_therapy": 25,
        "physiotherapy": 25
    }
}

power_zone_no_membership_prices = {
    "joining_fee": 30,
    "swimming_pool": 20,
    "classes": 20,
    "massage_therapy": 30,
    "physiotherapy": 30
}

# Function to calculate the total cost with membership for uGym
def calculate_total_cost_with_membership_ugym(timing, services, is_student=False, age=None):
    # Calculate total cost by summing up joining fee and gym access fee for the selected timing
    total_cost = ugym_no_membership_prices["joining_fee"] + ugym_membership_prices[timing]["gym_access"]
    
    # Check if the user is a student, aged between 16-25, or above 66 years old
    if is_student or (age is not None and 16 <= age <= 25) or (age is not None and age > 66):
        # Assign discount percentage based on user's eligibility: 20% for students or users aged 16-25, 15% for users above 66
        discount_percentage = 0.80 if is_student or (age is not None and 16 <= age <= 25) else 0.85
        # Apply discount to total cost if user meets discount criteria
        total_cost *= discount_percentage
    
    # Iterate over selected services
    for service in services:
        if (is_student or (age is not None and 16 <= age <= 25) or (age is not None and age > 66)) and service != "massage_therapy" and service != "physiotherapy":
            # Apply discount to the service if the user meets the criteria
            total_cost += 0.80 * ugym_membership_prices[timing][service] if is_student or (age is not None and 16 <= age <= 25) else 0.85 * ugym_membership_prices[timing][service]
        else:
            # If the user is not eligible for a discount or the service is massage therapy or physiotherapy,
            # add the regular price of the service to the total cost
            total_cost += ugym_membership_prices[timing][service]
    
    # Return the calculated total cost
    return total_cost

# Function to calculate the total cost without membership for uGym
def calculate_total_cost_without_membership_ugym(timing, services, is_student, age=None):
    # Initialize total cost to 0
    total_cost = 0
    # Retrieve gym access cost based on selected timing
    gym_access_cost = ugym_membership_prices[timing]["gym_access"]
    
    # Apply discounts based on student status or age
    if is_student or (age is not None and 16 <= age <= 25) or (age is not None and age > 66):
        # Assign discount percentage based on user's eligibility: 20% for students or users aged 16-25, 15% for users above 66
        discount_percentage = 0.80 if is_student or (age is not None and 16 <= age <= 25) else 0.85
        # Calculate total cost with discounts for gym access
        total_cost += gym_access_cost * discount_percentage
        
        # Apply discount to other services (excluding physiotherapy and massage therapy)
        for service in services:
            if service not in ["physiotherapy", "massage_therapy"]:
                # Apply discount to the service
                total_cost += ugym_no_membership_prices[service] * discount_percentage
            else:
                # Add regular price of physiotherapy or massage therapy to total cost (no discount applied)
                total_cost += ugym_no_membership_prices[service]
    else:
        # No discounts applied, calculate total cost without discounts
        total_cost += gym_access_cost
        # Add regular prices of selected services to total cost
        for service in services:
            total_cost += ugym_no_membership_prices[service]
    
    # Return the calculated total cost
    return total_cost

# Function to calculate the total cost with membership for Power Zone
def calculate_total_cost_with_membership_power_zone(timing, services, is_student=False, age=None):
    # Initialize total cost with the joining fee and gym access fee
    total_cost = power_zone_no_membership_prices["joining_fee"] + power_zone_membership_prices[timing]["gym_access"]
    
    # Apply discounts based on student status or age
    if is_student or (age is not None and 16 <= age <= 25) or (age is not None and age > 66):
        # Assign discount percentage based on user's eligibility: 15% for students or users aged 16-25, 20% for users above 66
        discount_percentage = 0.85 if is_student or (age is not None and 16 <= age <= 25) else 0.80
        # Apply discount to total cost if user meets discount criteria
        total_cost *= discount_percentage
    
    # Iterate over selected services
    for service in services:
        # Apply discount for selected services (excluding massage therapy and physiotherapy)
        if (is_student or (age is not None and 16 <= age <= 25) or (age is not None and age > 66)) and service != "massage_therapy" and service != "physiotherapy":
            # Multiply the original price by the discount percentage to apply the discount
            total_cost += discount_percentage * power_zone_membership_prices[timing][service]
        else:
            # If the user is not eligible for a discount or the service is massage therapy or physiotherapy,
            # add the regular price of the service to the total cost
            total_cost += power_zone_membership_prices[timing][service]
    
    # Return the calculated total cost
    return total_cost

# Function to calculate the total cost without membership for Power Zone
def calculate_total_cost_without_membership_power_zone(timing, services, is_student=False, age=None):
    # Initialize total cost to 0
    total_cost = 0
    # Retrieve gym access cost based on selected timing
    gym_access_cost = power_zone_membership_prices[timing]["gym_access"]
    
    # Apply discounts based on student status or age
    if is_student or (age is not None and 16 <= age <= 25) or (age is not None and age > 66):
        # Assign discount percentage based on user's eligibility: 15% for students or users aged 16-25, 20% for users above 66
        discount_percentage = 0.85 if is_student or (age is not None and 16 <= age <= 25) else 0.80
        # Calculate total cost with discounts for gym access
        total_cost += gym_access_cost * discount_percentage
        
        # Apply discount to other services (excluding physiotherapy and massage therapy)
        for service in services:
            if service not in ["physiotherapy", "massage_therapy"]:
                # Apply discount to the service
                total_cost += power_zone_no_membership_prices[service] * discount_percentage
            else:
                # Add regular price of physiotherapy or massage therapy to total cost (no discount applied)
                total_cost += power_zone_no_membership_prices[service]
    else:
        # No discounts applied, calculate total cost without discounts
        total_cost += gym_access_cost
        # Add regular prices of selected services to total cost
        for service in services:
            total_cost += power_zone_no_membership_prices[service]
    
    # Return the calculated total cost
    return total_cost

# Retrieve form data
form = cgi.FieldStorage()
name = form.getvalue("name")
surname = form.getvalue("surname")
email = form.getvalue("email")
timing = form.getvalue("timing")
services = form.getlist("services")
is_student = "is_student" in form
age = int(form.getvalue("age")) if "age" in form and form.getvalue("age").isdigit() else None
membership_option = form.getvalue("membership")

# Establish connection to the database
connection = mysql.connector.connect(
 host='localhost',
    database='gp2',
    user='root',
    password='1234')

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Adjusting the way membership_bool is determined
if membership_option == "with_membership":
    membership_bool = 1
else:
    membership_bool = 0

# Define a SQL select query based on email
select_query = "SELECT * FROM pinfo WHERE email = %s"
# Execute the select query with the email parameter
cursor.execute(select_query, (email,))
# Fetch the result of the select query
existing_user = cursor.fetchone()

# Check if the user already exists in the database
if existing_user:
    # Update pinfo record for the existing user with the provided information
    update_pinfo_query = "UPDATE pinfo SET name=%s, surname=%s, age=%s, student=%s WHERE email=%s"
    # Execute the update query with the provided information
    cursor.execute(update_pinfo_query, (name, surname, age, is_student, email))
else:
    # Insert a new pinfo record for the new user
    insert_pinfo_query = "INSERT INTO pinfo (name, surname, age, email, student) VALUES (%s, %s, %s, %s, %s)"
    # Execute the insert query with the provided information
    cursor.execute(insert_pinfo_query, (name, surname, age, email, is_student))

# Update or insert into sinfo table
swimming_pool = 'swimming_pool' in services
classes = 'classes' in services
massage = 'massage_therapy' in services
physiotherapy = 'physiotherapy' in services

# Initialize variables for selected gym and least cost
selected_gym = None
least_cost = None

if membership_option == "with_membership":
    # Calculate total cost with membership for both gyms
    total_cost_with_membership_ugym = calculate_total_cost_with_membership_ugym(timing, services, is_student, age)
    total_cost_with_membership_power_zone = calculate_total_cost_with_membership_power_zone(timing, services, is_student, age)
    
    # Compare the total costs and select the least expensive option
    if total_cost_with_membership_ugym < total_cost_with_membership_power_zone:
        selected_gym = "uGym"
        least_cost = total_cost_with_membership_ugym
    else:
        selected_gym = "Power Zone"
        least_cost = total_cost_with_membership_power_zone
    
    # Generate message recommending the selected gym with membership
    message = f"If you're looking for the best value for your selected facilities ,<br> we recommend joining <br><span class='selected-gym'>{selected_gym}</span><br>Enjoy your membership and make the most out of your fitness journey!"
else:
    # Calculate total cost without membership for both gyms
    total_cost_without_membership_ugym = calculate_total_cost_without_membership_ugym(timing, services, is_student, age)
    total_cost_without_membership_power_zone = calculate_total_cost_without_membership_power_zone(timing, services, is_student, age)

    # Select the gym with the least cost
    if total_cost_without_membership_ugym < total_cost_without_membership_power_zone:
        selected_gym = "uGym"
        least_cost = total_cost_without_membership_ugym
    else:
        selected_gym = "Power Zone"
        least_cost = total_cost_without_membership_power_zone

    # Generate message recommending the selected gym without membership
    message = f"If you're looking for the best value for your selected facilities,<br>, we recommend considering joining<br> <span class='selected-gym'>{selected_gym}</span><br> without membership. You can still enjoy our facilities at a competitive price!"

# Check if a subscription record exists for this email in sinfo
select_sinfo_query = "SELECT * FROM sinfo WHERE email = %s"
# Execute the select query with the email parameter
cursor.execute(select_sinfo_query, (email,))
# Fetch the result of the select query
existing_sinfo = cursor.fetchone()

# inserting or updating sinfo table
if existing_sinfo:
    # Update the existing sinfo record for the user
    update_sinfo_query = """
    UPDATE sinfo SET timing=%s, membership=%s, gym=%s, swimming_pool=%s, classes=%s, massage=%s, physiotherapy=%s, cost=%s WHERE email=%s
    """
    # Execute the update query with the provided information
    cursor.execute(update_sinfo_query, (timing, membership_bool, selected_gym, swimming_pool, classes, massage, physiotherapy, least_cost, email))
else:
    # Insert a new sinfo record for the user
    insert_sinfo_query = """
    INSERT INTO sinfo (email, timing, membership, gym, swimming_pool, classes, massage, physiotherapy, cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    # Execute the insert query with the provided information
    cursor.execute(insert_sinfo_query, (email, timing, membership_bool, selected_gym, swimming_pool, classes, massage, physiotherapy, least_cost))

# Commit changes to the database
connection.commit()

# Create a summary header displaying user's selected information
summary_header = f"""
<h1 style="font-size: 20px;">Summary of Your Selection:</h1>
<ul>
    <li >Name: {name} {surname}</li>
    <li>Email: {email}</li>
    <li>Age: {age}</li>
    <li>Membership: {'With' if membership_option == "with_membership" else 'Without'}</li>
    <li>Student: {'Yes' if is_student else 'No'}</li>
    <li>Timing: {timing}</li>
    <li>Selected Facilities:</li>
    <ul>
        {''.join([f'<li>{service}</li>' for service in services])}
    </ul>
</ul>
"""

#  the summary header with the message and total cost
html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gym Membership Recommendation</title>

</head>
<body>
<link rel="stylesheet" href="gd.css">
 <!-- top page -->
    <div class="m_top inclusive">
        <div class="logo">
            <h1>FITFUSION</h1>
        </div>
    </div>


<div class="middle inclusive">
    <div class="default">
      <h1>Your Ideal Gym Membership Recommendation</h1>
      <div>
        {summary_header}
      </div>
      <p>{message}</p>
      <p class= "total-cost">Total Cost: &pound;{least_cost}</p>
      <form action="payment.html" method="post">
        <button type="submit">Continue</button>
      </form>
      <button onclick="goBack()">Go Back and Edit</button>
    </div>
  </div>

  <script>
    function goBack() {{
      window.history.back();
    }}
  </script>
</body>
</html>
"""

print("Content-type:text/html\r\n\r\n")
print(html)

# Close the cursor and connection
cursor.close()
connection.close()