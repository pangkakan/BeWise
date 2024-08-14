from controllers.db import create_connection

class User:
    def __init__(self, username, password, email, cur, conn, logger,):
        self.cur = cur
        self.conn = conn
        self.logger = logger
        self.username = username
        self.password = password
        self.email = email

    def save_user(self):
        try:
            self.cur.execute("""
                INSERT INTO user_data (username, password, email) VALUES (%s, %s, %s)""",
                            (self.username, self.password, self.email))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"Failed to save user {self.username}: {e}")
            return False

    @classmethod
    def get_by_email_and_password(cls, email, password, cur, conn, logger):
        try:
            cur.execute("SELECT username, password, email FROM user_data WHERE email = %s AND password = %s", (email, password))
            row = cur.fetchone()
            if row:
                return cls(username=row[0], password=row[1], email=row[2], cur=cur, conn=conn, logger=logger)
            return None
        except Exception as e:
            logger.error(f"Failed to fetch user by email {email} and password: {e}")
            return None

    @classmethod
    def get_by_email(cls, email, cur, conn, logger):
        try:
            cur.execute("SELECT username, password, email FROM user_data WHERE email = %s", (email,))
            row = cur.fetchone()
            if row:
                return cls(username=row[0], password=row[1], email=row[2], cur=cur, conn=conn, logger=logger)
            return None
        except Exception as e:
            logger.error(f"Failed to fetch user by email {email}: {e}")
            return None

    @classmethod
    def get_by_username(cls, username, cur, conn, logger):
        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM user_data WHERE username = %s", (username,))
            user_id = cur.fetchone()
            return user_id[0] if user_id else None
        except Exception as e:
            logger.error(f"Error fetching user ID for {username}: {e}")
            conn.rollback()
            return None
        finally:
            cur.close()
    
    @staticmethod
    def authenticate(email, password, cur, conn):
        cur = conn.cursor
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cur.execute(query, (email, password))
        result = cur.fetchone()
        if result:
            return User(result)
        return None

    def update_username(self, new_username):
        try:
            self.cur.execute("UPDATE user_data SET username = %s WHERE username = %s", (new_username, self.username))
            self.conn.commit()
            self.username = new_username
            return True
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"Failed to update username for {self.username}: {e}")
            return False

    def update_email(self, new_email):
        try:
            self.cur.execute("UPDATE user_data SET email = %s WHERE username = %s", (new_email, self.username))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"Failed to update email for {self.username}: {e}")
            return False

    def update_password(self, new_password):
        try:
            self.cur.execute("UPDATE user_data SET password = %s WHERE username = %s", (new_password, self.username))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"Failed to update password for {self.username}: {e}")
            return False

    def delete_user(self):
        try:
            self.cur.execute("DELETE FROM user_data WHERE username = %s", (self.username,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"Failed to delete account for {self.username}: {e}")
            return False

    def verify_password(self, provided_password):
        return self.password == provided_password