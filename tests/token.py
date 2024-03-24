import secrets

def generate_secure_token(length=32):
    """
    Generate a secure token.
    - length: Length of the token. Default is 32 bytes.
    Returns a hexadecimal string representation of the token.
    """
    return secrets.token_hex(length)

# Example usage
secure_token = generate_secure_token()
print(secure_token)
