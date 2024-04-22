# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 04/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
import os
import re

from argon2 import PasswordHasher

class PasswordHandler:
    def __init__(self):
        self.ph = PasswordHasher()

    def generate_salt(self):
        # Menghasilkan salt yang aman
        return os.urandom(16)

    def hash_password(self, password, salt=None):
        # Jika tidak ada salt yang diberikan, generate salt baru


        if salt is None:
            salt = self.generate_salt()

        # Hash password menggunakan argon2b dan salt
        hashed_password = self.ph.hash(password, salt=salt)
        return hashed_password, salt

    def verify_password(self, password, hashed_password, salt):
        # Verifikasi password menggunakan argon2b dan salt yang diberikan
        try:
            self.ph.verify(hashed_password, password)
            return True
        except:
            return False

    def validate_password_string(self, password):
        if password is None:
            res = {
                'message': "password must be at least 8 characters",
                'success': False
            }
            return res
        if len(password) < 8 or password is None:
            res = {
                'message': "password must be at least 8 characters",
                'success': False
            }
            return res
        # At least one uppercase letter
        if not re.search(r'[A-Z]', password):
            res = {
                'message': "Password must be at least one uppercase letter",
                'success': False
            }
            return res

        # At least one lowercase letter
        if not re.search(r'[a-z]', password):
            res = {
                'message': "Password must be at least one lowercase letter",
                'success': False
            }
            return res

            # At least one digit

        # At least one special character
        if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', password):
            res = {
                'message': "Password must be at least one special character",
                'success': False
            }
            return res

            # No spaces allowed
        if ' ' in password:
            res = {
                'message': "Password must be at least 8 character",
                'success': False
            }
            return res

            # If all checks pass, the password is valid
        return {'success': True}

    def validate_username_string(self, username):
        if username is None:
            res = {
                'message': "Username must be at least 8 characters",
                'success': False
            }
            return res
        if len(username) < 8 or username is None:
            res = {
                'message': "Username must be at least 8 characters",
                'success': False
            }
            return res
        # At least one uppercase letter

        # At least one special character
        if re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', username):
            res = {
                'message': "username cannot contain special character",
                'success': False
            }
            return res

            # No spaces allowed
        if ' ' in username:
            res = {
                'message': "username must be at least 8 character",
                'success': False
            }
            return res

            # If all checks pass, the password is valid
        return {'success': True}
