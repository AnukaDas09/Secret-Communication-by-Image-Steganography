# refresh2.py

def clear_gui_fields(app):
    """Clears the text box, image box, and secret key entry box."""
    # Clear the message text box
    app.message_text.delete('1.0', 'end')

    # Clear the image box
    app.image_label.config(image='')
    app.image_label.image = None  # Reset the image reference

    # Reset the image path
    app.image_path = None

    # Clear the secret key entry box
    app.secret_key.delete(0, 'end')


# from tkinter import Tk
# from gui import SteganographyApp
#
#
# def refresh_gui():
#     root = Tk()
#     app = SteganographyApp(root)
#
#     # Calling the refresh method to clear all fields
#     app.refresh()
#
#     # Run the application
#     root.mainloop()
#
#
# if __name__ == "__main__":
#     refresh_gui()
