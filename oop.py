import jwt
import datetime

# Secret key used for signing the token
secret_key = "your_secret_key"

# Payload containing the claims for the token
payload = {
    'sub': 'user123',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
    'iss': 'your_issuer',
}

# Generate the JWT token
token = jwt.encode(payload, secret_key, algorithm='HS256')
print("Generated token:", token)

# Decode and verify the JWT token
try:
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
    print("Decoded token:", decoded_token)
except jwt.ExpiredSignatureError:
    print("Token has expired.")
except jwt.InvalidTokenError:
    print("Invalid token.")
