import base64
from stegano import lsb
from cryptography.fernet import Fernet

def generate_key(password):
    """Generate a Fernet key from a password."""
    key = base64.urlsafe_b64encode(password.ljust(32)[:32].encode())
    return key

def encrypt_message(message, password):
    """Encrypt a message using a password."""
    key = generate_key(password)
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    # Convert encrypted bytes to Base64 string
    return base64.urlsafe_b64encode(encrypted_message).decode()

def decrypt_message(encrypted_message, password):
    """Decrypt a Base64-encoded encrypted message using a password."""
    key = generate_key(password)
    fernet = Fernet(key)
    # Decode Base64 string back to bytes
    encrypted_message_bytes = base64.urlsafe_b64decode(encrypted_message)
    return fernet.decrypt(encrypted_message_bytes).decode()

def hide_message(image_path, message, password):
    """Hide an encrypted message in an image."""
    try:
        encrypted_message = encrypt_message(message, password)
        hidden_image = lsb.hide(image_path, encrypted_message)
        return hidden_image
    except Exception as e:
        raise Exception(f"Error hiding message: {e}")

def reveal_message(image_path, password):
    """Reveal and decrypt a hidden message from an image."""
    try:
        encrypted_message = lsb.reveal(image_path)
        if encrypted_message is None:
            raise Exception("No hidden message found.")
        return decrypt_message(encrypted_message, password)
    except Exception as e:
        raise Exception(f"Error revealing message: {e}")

def save_image(image, output_path):
    """Save the modified image to the specified output path."""
    try:
        image.save(output_path)
        return True
    except Exception as e:
        raise Exception(f"Error saving image: {e}")


# from stegano import lsb
# from cryptography.fernet import Fernet
#
# def generate_key(password):
#     """Generate a key from the password."""
#     return Fernet(Fernet.generate_key())
#
# def encrypt_message(message, password):
#     """Encrypt a message using a password."""
#     key = generate_key(password)
#     fernet = Fernet(key)
#     return fernet.encrypt(message.encode())
#
# def decrypt_message(encrypted_message, password):
#     """Decrypt a message using a password."""
#     key = generate_key(password)
#     fernet = Fernet(key)
#     return fernet.decrypt(encrypted_message).decode()
#
# def hide_message(image_path, message, password):
#     """Hide an encrypted message in an image."""
#     try:
#         encrypted_message = encrypt_message(message, password)
#         hidden_image = lsb.hide(image_path, encrypted_message)
#         return hidden_image
#     except Exception as e:
#         raise Exception(f"Error hiding message: {e}")
#
# def reveal_message(image_path, password):
#     """Reveal and decrypt a hidden message from an image."""
#     try:
#         encrypted_message = lsb.reveal(image_path)
#         if encrypted_message is None:
#             raise Exception("No hidden message found.")
#         return decrypt_message(encrypted_message, password)
#     except Exception as e:
#         raise Exception(f"Error revealing message: {e}")
# def save_image(hidden_image, save_path):
#     """Save the image with the hidden message."""
#     try:
#         hidden_image.save(save_path)
#     except Exception as e:
#         raise Exception(f"Error saving image: {e}")
