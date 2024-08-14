from bottle import request, redirect, response
from models.user import User

def register():
    """
    Handles user registration.
    """
    username = request.forms.get('name-reg')
    email = request.forms.get('email-reg')
    password = request.forms.get('password-reg')

    print(f"Registering user: {username}, {email}")

    user = User(username=username, password=password, email=email)
    try:
        user.save_user()
        print("User registered successfully")
        return "Success"
    except Exception as e:
        print(f"Error during registration: {e}")
        # Print the traceback for better understanding
        import traceback
        traceback.print_exc()
        return "Failed"

def login():
    email = request.forms.get('email-login')
    password = request.forms.get('password-login')

    print(f"Form data - Email: {email}, Password: {password}")

    if not email or not password:
        print("Email or password not provided")
        return None

    user = User.get(email)  # Assuming this fetches a user by email

    if user:
        print(f"User found: {user.username}, verifying password...")
        if user.verify_password(password):
            print("Password verification successful")
            return user
        else:
            print("Password verification failed")
            return None
    else:
        print("User not found")
        return None

