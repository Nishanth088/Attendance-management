import bcrypt

password = b"admin123"

hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print(hashed.decode())