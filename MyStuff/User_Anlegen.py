import bcrypt
import re
import smtplib
import os
from dotenv import load_dotenv
from datetime import datetime
from email.message import EmailMessage

load_dotenv()  # Lädt Umgebungsvariablen aus .env-Datei

# "Datenbank" als Dictionary mit Email als Key
users_by_email = {}


class User:
    def __init__(self, name, email, password):
        if email in users_by_email:
            raise ValueError("E-Mail-Adresse existiert bereits!")

        if not self.is_name_valid(name):
            raise ValueError("Der Benutzername muss zwischen 3 und 20 Zeichen lang sein.")

        if not self.is_password_secure(password):
            raise ValueError("Das Passwort entspricht nicht den Sicherheitsanforderungen.")

        self.name = name
        self.email = email
        self.password_hash = self.hash_password(password)
        self.created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.updated_at = self.created_at  # Initial = erstellt

    def is_name_valid(self, name):
        return 3 <= len(name) <= 20

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password_to_check):
        return bcrypt.checkpw(password_to_check.encode('utf-8'), self.password_hash)

    def is_password_secure(self, password):
        return (
            len(password) >= 10
            and re.search(r"[A-Z]", password)
            and re.search(r"[a-z]", password)
        )

    def update_password(self, new_password):
        if not self.is_password_secure(new_password):
            raise ValueError("Das neue Passwort erfüllt die Anforderungen nicht.")
        self.password_hash = self.hash_password(new_password)
        self.updated_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        print(f"Passwort für {self.email} wurde aktualisiert am {self.updated_at}.")

    def __str__(self):
        return (
            f"Username: {self.name}\n"
            f"E-Mail: {self.email}\n"
            f"Erstellt am: {self.created_at}\n"
            f"Zuletzt aktualisiert am: {self.updated_at}"
        )


def send_welcome_email(to_email, username):
    msg = EmailMessage()
    msg['Subject'] = 'Willkommen zu deinem neuen Account!'
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = to_email

    msg.set_content(f"""
    Hallo {username},

    vielen Dank für deine Registrierung! Dein Account wurde erfolgreich erstellt.

    Wir freuen uns, dich an Bord zu haben.

    Viele Grüße,
    Dein Team
    """)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
            smtp.send_message(msg)
            print(f"Willkommensmail an {to_email} wurde versendet.")
    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {e}")


def create_user(name, email, password):
    if email in users_by_email:
        raise ValueError("E-Mail-Adresse existiert bereits!")
    user = User(name, email, password)
    users_by_email[email] = user
    send_welcome_email(email, name)
    print(f"User {email} erfolgreich erstellt.")
    return user


def delete_user(email):
    if email not in users_by_email:
        print(f"User mit E-Mail {email} existiert nicht.")
        return False
    del users_by_email[email]
    print(f"User mit E-Mail {email} wurde erfolgreich gelöscht.")
    return True


# Beispiel-Test
try:
    user1 = create_user("Michael", "michael@example.com", "Maultaschenwurst92")
    print(user1)
except ValueError as e:
    print(e)

# Passwort aktualisieren:
try:
    user1.update_password("NeuesSicheresPasswort99")
except Exception as e:
    print(e)

# Löschen:
delete_user("michael@example.com")
delete_user("nichtvorhanden@example.com")