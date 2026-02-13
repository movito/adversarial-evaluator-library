"""
Vulnerable User Management Module

WARNING: This code contains INTENTIONAL security vulnerabilities for testing.
DO NOT use this code in production!

Expected evaluator verdict: CHANGES_REQUESTED or REJECT
Expected findings:
- SQL injection vulnerability
- Hardcoded credentials
- Weak password hashing
- Missing input validation
- Information disclosure in errors
- Command injection
- Path traversal
"""

import hashlib
import os
import sqlite3
import subprocess

# VULNERABILITY: Hardcoded database credentials
DB_HOST = "prod-db.company.internal"
DB_USER = "admin"
DB_PASSWORD = "SuperSecret123!"  # VULNERABILITY: Hardcoded password
API_KEY = "sk-live-abc123xyz789"  # VULNERABILITY: Hardcoded API key


class UserManager:
    """Manages user accounts. Contains multiple security vulnerabilities."""

    def __init__(self, db_path="users.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        """Create the users table."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                email TEXT,
                role TEXT
            )
        """)

    def create_user(self, username, password, email, role="user"):
        """
        Create a new user account.

        VULNERABILITY: SQL injection - username and email are not sanitized
        VULNERABILITY: Weak password hashing (MD5)
        VULNERABILITY: No input validation
        """
        # VULNERABILITY: MD5 is cryptographically broken
        password_hash = hashlib.md5(password.encode()).hexdigest()

        # VULNERABILITY: SQL injection via string concatenation
        query = f"""
            INSERT INTO users (username, password, email, role)
            VALUES ('{username}', '{password_hash}', '{email}', '{role}')
        """
        self.conn.execute(query)
        self.conn.commit()

    def login(self, username, password):
        """
        Authenticate a user.

        VULNERABILITY: SQL injection
        VULNERABILITY: Information disclosure in error messages
        """
        password_hash = hashlib.md5(password.encode()).hexdigest()

        # VULNERABILITY: SQL injection via string formatting
        query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (
            username,
            password_hash,
        )

        result = self.conn.execute(query).fetchone()

        if not result:
            # VULNERABILITY: Information disclosure - reveals if username exists
            user_exists = self.conn.execute(
                f"SELECT 1 FROM users WHERE username = '{username}'"
            ).fetchone()
            if user_exists:
                raise Exception(f"Invalid password for user: {username}")
            else:
                raise Exception(f"User not found: {username}")

        return {"id": result[0], "username": result[1], "role": result[4]}

    def get_user_by_id(self, user_id):
        """
        Get user by ID.

        VULNERABILITY: SQL injection via user_id
        """
        # VULNERABILITY: No type checking on user_id, direct string interpolation
        query = f"SELECT * FROM users WHERE id = {user_id}"
        return self.conn.execute(query).fetchone()

    def search_users(self, search_term):
        """
        Search for users.

        VULNERABILITY: SQL injection via LIKE clause
        """
        # VULNERABILITY: SQL injection in LIKE clause
        query = (
            f"SELECT username, email FROM users WHERE username LIKE '%{search_term}%'"
        )
        return self.conn.execute(query).fetchall()

    def export_user_data(self, user_id, output_dir):
        """
        Export user data to a file.

        VULNERABILITY: Path traversal
        VULNERABILITY: Command injection
        """
        # VULNERABILITY: Path traversal - user_id could be "../../../etc/passwd"
        output_path = os.path.join(output_dir, f"user_{user_id}.json")

        user = self.get_user_by_id(user_id)
        if user:
            with open(output_path, "w") as f:
                f.write(str(user))

            # VULNERABILITY: Command injection via output_path
            subprocess.run(f"chmod 644 {output_path}", shell=True)

        return output_path

    def run_report(self, report_name):
        """
        Run a named report.

        VULNERABILITY: Command injection
        """
        # VULNERABILITY: Direct command injection
        result = subprocess.run(
            f"python reports/{report_name}.py",
            shell=True,
            capture_output=True,
            text=True,
        )
        return result.stdout

    def backup_database(self, backup_name):
        """
        Create a database backup.

        VULNERABILITY: Command injection via backup_name
        """
        # VULNERABILITY: Command injection - backup_name is user-controlled
        os.system(f"cp users.db backups/{backup_name}.db")

    def update_email(self, user_id, new_email):
        """
        Update user email.

        VULNERABILITY: SQL injection
        VULNERABILITY: No email validation
        """
        # VULNERABILITY: SQL injection
        query = f"UPDATE users SET email = '{new_email}' WHERE id = {user_id}"
        self.conn.execute(query)
        self.conn.commit()

    def delete_user(self, username):
        """
        Delete a user account.

        VULNERABILITY: SQL injection
        VULNERABILITY: No authorization check
        """
        # VULNERABILITY: SQL injection, no auth check
        self.conn.execute(f"DELETE FROM users WHERE username = '{username}'")
        self.conn.commit()

    def get_password_reset_token(self, email):
        """
        Generate a password reset token.

        VULNERABILITY: Predictable token generation
        VULNERABILITY: Information disclosure
        """
        import time

        # VULNERABILITY: Predictable token (timestamp-based)
        token = hashlib.md5(f"{email}{time.time()}".encode()).hexdigest()[:8]

        # VULNERABILITY: Reveals if email exists
        user = self.conn.execute(
            f"SELECT * FROM users WHERE email = '{email}'"
        ).fetchone()

        if user:
            print(
                f"Password reset token for {email}: {token}"
            )  # VULNERABILITY: Logging sensitive data
            return token
        else:
            raise Exception(f"No account found for email: {email}")


def process_upload(filename, content):
    """
    Process an uploaded file.

    VULNERABILITY: Path traversal in filename
    VULNERABILITY: No content validation
    """
    # VULNERABILITY: Path traversal - filename could be "../../../etc/cron.d/malicious"
    upload_path = f"/var/uploads/{filename}"

    with open(upload_path, "wb") as f:
        f.write(content)

    # VULNERABILITY: Executing uploaded content
    if filename.endswith(".py"):
        exec(content)  # VULNERABILITY: Arbitrary code execution

    return upload_path


def log_action(user, action):
    """
    Log a user action.

    VULNERABILITY: Log injection
    """
    import logging

    # VULNERABILITY: Log injection - action could contain newlines and fake log entries
    logging.info(f"User {user} performed action: {action}")
