import bcrypt
import re
import smtplib
from email.message import EmailMessage


registered_emails = []
users = []

class User:
    def __init__(self,name,email, password):
        self.name = name
        self.email = email
        self.password = password

    def create_user(name, email, password):
        if email in registered_emails:
            raise ValueError("E-Mail-Adresse existiert bereits!")
        user = User(name, email, password)
        users.append(user)
        registered_emails.append(email)
        return user

    def delete_user(email):
        global users, registered_emails
        if email not in registered_emails:
            print(f"User mit E-Mail {email} existiert nicht.")
            return False

        registered_emails.remove(email)

        users = [users for user in users if user.email !=email]
        print(f"User mit E-Mail {email} wurde erfolgreich gelöscht.")
        return True

create_user("Michael", "michael@example.com", "password123")
delete_user("michael@example.com")
delete_user("nichtvorhanden@example.com")