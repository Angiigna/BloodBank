import random
import string
import pandas as pd
from datetime import datetime, timedelta



BloodTypes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'Any Compatible Type']

Cities = [
    'Puducherry', 'Chennai', 'Banglore', 'Cochin', 'Hyderabad',
    'Kozhikode', 'Thiruchirapalli', 'Madurai', 'Thiruvananthapuram', 'Manglore'
]



def random_phone():
    return "".join(random.choices(string.digits, k=10))


def random_date(start=None, end=None):
    """Generate a random date between start and end."""
    if start is None:
        start = datetime(2020, 1, 1)
    if end is None:
        end = datetime(2025, 1, 1)

    delta = end - start
    int_delta = delta.days
    random_day = random.randrange(int_delta)
    return start + timedelta(days=random_day)


def random_name():
    fname = [
        'Sivangi', 'Nayana', 'Abhiya', 'Gokul', 'Parvathy', 'Abhijith', 'Ananya', 'Karthik', 'Lakshmi',
        'Arjun', 'Meera', 'Yusuf', 'Vishnu', 'Diya', 'Rohan', 'Zoya', 'Aarav', 'Ishita', 'Dev',
        'Anika', 'Sai', 'Nishant', 'Riya', 'Aditya', 'Tara', 'Kabir', 'Mira', 'Sherin', 'Zair',
        'Minha', 'Reynash', 'Azan', 'Aman', 'Aisha'
    ]

    lname = [
        'Shah', 'Patel', 'Kumar', 'Reddy', 'Singh', 'Gupta', 'Mehta', 'Nair', 'Iyer', 'Das',
        'Chatterjee', 'Verma', 'Kapoor', 'Malhotra', 'Chaudhary', 'Joshi', 'Bose', 'Saxena', 'Trivedi', 'Sharma'
    ]

    return random.choice(fname) + " " + random.choice(lname)


def random_email(name):
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
    name_part = ''.join(name.lower().split())
    number_part = str(random.randint(10, 99))
    domain = random.choice(domains)
    return f"{name_part}{number_part}@{domain}"



def generate_user(n):
    users = []
    for i in range(1, n + 1):
        name = random_name()
        users.append({
            "id": i,
            "email": random_email(name),
            "first_name": name,
            "password": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
            "is_donor": random.choice([True, False])
        })

    return pd.DataFrame(users)


def generate_donor(users_df):
    donors = []
    donor_id = 1

    donor_users = users_df[users_df["is_donor"] == True]

    for _, row in donor_users.iterrows():
        donors.append({
            "id": donor_id,
            "user_id": row["id"],
            "blood_type": random.choice(BloodTypes),
            "age": random.randint(18, 60),
            "contact_number": random_phone(),
            "last_donation_date": random_date(),
            "city": random.choice(Cities)
        })
        donor_id += 1

    return pd.DataFrame(donors)


def generate_request(users_df, n):
    requests = []
    for i in range(1, n + 1):
        requests.append({
            "id": i,
            "requester_id": random.choice(users_df["id"]),
            "patient_name": random_name(),
            "blood_type_needed": random.choice(BloodTypes),
            "units_needed": random.randint(1, 9),
            "contact_number": random_phone(),
            "status": random.choice(['Pending', 'Completed']),
            "city": random.choice(Cities)
        })
    return pd.DataFrame(requests)


def generate_interactions(donors_df, requests_df, n_interactions=1000):
    interactions = []

    for i in range(1, n_interactions + 1):

        donor = donors_df.sample(1).iloc[0]
        req = requests_df.sample(1).iloc[0]

        # Base probability
        p = 0.1

        # Boost probability
        if donor["city"] == req["city"]:
            p += 0.2
        if donor["blood_type"] == req["blood_type_needed"]:
            p += 0.3
        if donor["age"] < 40:
            p += 0.1
        if req["units_needed"] == 1:
            p += 0.1

        response = "Completed" if random.random() < p else "No Response"

        interactions.append({
            "id": i,
            "donor_id": donor["id"],
            "request_id": req["id"],
            "interaction_date": random_date(),
            "status": response
        })

    return pd.DataFrame(interactions)


if __name__ == "__main__":
    users = generate_user(500)
    donors = generate_donor(users)
    requests = generate_request(users, 700)
    interactions = generate_interactions(donors, requests, 1000)

    users.to_csv("synthetic_users.csv", index=False)
    donors.to_csv("synthetic_donors.csv", index=False)
    requests.to_csv("synthetic_requests.csv", index=False)
    interactions.to_csv("synthetic_interactions.csv", index=False)

    print("Synthetic data generated and saved to CSV files.")
