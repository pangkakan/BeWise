





def check_if_empty_input(prompt):
    """
    Function which checks that the user input is not left empty.
    Argument,
    prompt = user input (str)
    """
    while True:
        user_input = input(prompt)
        if len(user_input) <= 0:
            print("\nFältet får inte lämnas tomt. Var vänlig försök igen.")
        else:
            return user_input



def register(conn):
    """
    In this function the user can register a new account by inserting the requested necessary user details.
    The user details are then controlled with various conditions and checked against existing user details to avoid creation of duplicate accounts.
    """
    cur = conn.cursor()

    new_email = check_if_empty_input("Mejladress: ")
    cur.execute(
        '''
            SELECT * FROM users 
            WHERE email = %s
        ''', (new_email,)
    )

    email_exists = cur.fetchone()
    if email_exists is None or email_exists[0] != new_email:
        new_password = check_if_empty_input("Lösenord: ")
        new_fname= check_if_empty_input("Förnamn: ")
        new_lname = check_if_empty_input("Efternamn: ")

        new_phone_nr = input("Telefonnummer: ")
        while len(new_phone_nr) != 10 or new_phone_nr.isdigit() == False:
            print("Ditt telefonnummer måste bestå av 10 siffror.")
            new_phone_nr = input("Skriv ditt telefonnummer: ")

        new_address = check_if_empty_input("Skriv din gatuadress: ")
        new_city = check_if_empty_input("Vilken stad bor du i? ")
        new_country = check_if_empty_input("Vilket land bor du i? ")

        cur.execute(
            '''
                INSERT INTO users 
                VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, False) 
            ''', (new_email, new_password, new_fname, new_lname, new_phone_nr, new_address, new_city, new_country)
        )
        conn.commit()

        print(f"\n{new_fname}, du är nu registrerad! \nLogga in för att börja shoppa!")

    else:
        print("\nEmailen är redan registrerad. \nVar vänlig logga in för att börja shoppa!")



def login(conn):
    """
    Function through which users can login to their accounts using a saved email and password.

    Returns,
    False (boolean) if the user is not yet registered
    user_email (str) if the user is registered
    """
    cur = conn.cursor()

    print("Ange dina användaruppgifter nedan")

    user_email = check_if_empty_input("\nMejladress: ")

    cur.execute(
        '''
            SELECT email, password, f_name 
            FROM users WHERE users.email=%s
        ''', (user_email,)

    )
    existing_user = cur.fetchone()

    if existing_user is None:
        print("Användaren existerar inte")
        user_choice = input("\nÖnskar du registrera dig? (ja/nej) ")
        user_choice = user_choice.lower()

        if user_choice == "ja":
            register()
            return False

        else:
            return False

    user_password = check_if_empty_input("Lösenord: ")

    while existing_user[1] is not None and existing_user[1] != user_password:
        print("\nFel lösenord. Försök igen.")
        user_password = check_if_empty_input("Lösenord: ")

    else:
        print(f'\nVälkommen {existing_user[2]}! \nDu är nu inloggad')
        return user_email
