from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import  Button, PhotoImage
from PIL import Image, ImageTk
import os
import functions
import refresh2

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('750x520')
        self.root.config(bg='white')
        self.root.title("Steganography Application")
        # self.refresh_icon = PhotoImage(file="refresh_logo.png")
        img_icon = Image.open("refresh_logo.png")  # Replace with your image path
        img_resized = img_icon.resize((30, 30), Image.Resampling.LANCZOS)  # Resize to 30x30 pixels
        self.refresh_icon = ImageTk.PhotoImage(img_resized)
        self.image_path = None
        self.hidden_image = None

        self.setup_gui()

    def setup_gui(self):
        self.root.resizable(True, True)
        # Logo
        try:
            logo = PhotoImage(file='logo.png')
            Label(self.root, image=logo, bd=0, bg='grey').place(x=70, y=0)
            self.root.logo = logo  # To prevent garbage collection
        except:
            Label(self.root, text="Steganography App", font="impact 25 bold", bg="black", fg="red").place(x=190, y=0)

        # Heading
        Label(self.root, text='Secret Communication by Image Steganography', font='impack 16 bold', bg='white',
              fg='dark blue').place(x=150, y=22)

        # Label(self.root, text='Hiding Message', font='impack 30 bold', bg='white', fg='dark blue').place(x=260, y=12)

        # Frame 1 (Image Display)
        f1 = Frame(self.root, width=250, height=220, bd=5, bg='sea green')
        f1.place(x=50, y=100)
        self.image_label = Label(f1, bg='sea green')
        self.image_label.place(x=0, y=0)

        # Frame 2 (Text Input)
        f2 = Frame(self.root, width=320, height=220, bd=5, bg='light grey')
        f2.place(x=330, y=100)
        self.message_text = Text(f2, font='arial 15 bold', wrap=WORD)
        self.message_text.place(x=0, y=0, width=310, height=210)

        # Secret Key Entry
        Label(self.root, text='Enter Secret Key', font='10', bg='white', fg='black').place(x=260, y=330)
        self.secret_key = Entry(self.root, bd=2, font='impact 10 bold',bg='light grey', show='*')
        self.secret_key.place(x=245, y=360)

        # Buttons
        Button(self.root, text='Open Image', bg='blue', fg='white', font='arial 12 bold', cursor='hand2',
               command=self.open_image).place(x=60, y=417)
        Button(self.root, text='Save Image', bg='green', fg='white', font='arial 12 bold', cursor='hand2',
               command=self.save_image).place(x=190, y=417)
        Button(self.root, text='Hide Data', bg='red', fg='white', font='arial 12 bold', cursor='hand2',
               command=self.hide_data).place(x=380, y=417)
        Button(self.root, text='Show Data', bg='orange', fg='white', font='arial 12 bold', cursor='hand2',
               command=self.reveal_data).place(x=510, y=417)

        button_x = 670  # Align right edges
        button_y = 20   # Place above the white box (adjust as needed)

        # Create the refresh button and bind it to the refresh method
        Button(self.root,image=self.refresh_icon, bg='grey',cursor='hand2',
               command=lambda: refresh2.clear_gui_fields(self)).place(x=button_x, y=button_y)

        #lambda: refresh2.clear_gui_fields(self)) , bg='teal'

    def open_image(self):
        """Open and display an image."""
        self.image_path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title='Select Image File',
            filetypes=(('Image Files', '*.png;*.jpg;*.jpeg'), ('All Files', '*.*'))
        )
        if self.image_path:
            try:
                global img
                img = Image.open(self.image_path)
                img = img.resize((240, 210), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                self.image_label.configure(image=img)
                self.image_label.image = img
            except Exception as e:
                messagebox.showerror("Error", f"Unable to open image: {str(e)}")

    def hide_data(self):
        """Hide the message in the image with a password."""
        if not self.image_path:
            messagebox.showerror("Error", "Please open an image first.")
            return
        message = self.message_text.get(1.0, END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message to hide.")
            return

        password = self.secret_key.get().strip()
        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return

        try:
            self.hidden_image = functions.hide_message(self.image_path, message, password)
            messagebox.showinfo("Success", "Message hidden successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_image(self):
        """Save the image with the hidden message."""
        if self.hidden_image:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png")]
            )
            if save_path:
                try:
                    functions.save_image(self.hidden_image, save_path)
                    messagebox.showinfo("Success", "Image saved successfully.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "No message hidden to save.")

    def reveal_data(self):
        """Reveal the hidden message with a password."""
        if not self.image_path:
            messagebox.showerror("Error", "Please open an image first.")
            return
        password = self.secret_key.get().strip()
        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return

        try:
            message = functions.reveal_message(self.image_path, password)
            if message:
                self.message_text.delete(1.0, END)
                self.message_text.insert(END, message)
                messagebox.showinfo("Success", "Message revealed successfully.")
            else:
                messagebox.showerror("Error", "No hidden message found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh(self):
        """Clears the text box, image box, and secret key entry box."""
        # Clear the message text box
        self.message_text.delete('1.0', END)

        # Clear the image box
        self.image_label.config(image='')
        self.image_label.image = None  # Reset the image reference

        # Reset the image path
        self.image_path = None

        # Clear the secret key entry box
        self.secret_key.delete(0, END)




# from tkinter import *
# from tkinter import filedialog, messagebox
# from PIL import Image, ImageTk
# import os
# import functions
#
#
# class SteganographyApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.geometry('750x520')
#         self.root.config(bg='black')
#         self.root.title("Steganography Application")
#
#         self.image_path = None
#         self.hidden_image = None
#
#         self.setup_gui()
#
#     def setup_gui(self):
#         # Logo
#         try:
#             logo = PhotoImage(file='logo.png')
#             Label(self.root, image=logo, bd=0, bg='black').place(x=190, y=0)
#             self.root.logo = logo  # To prevent garbage collection
#         except:
#             Label(self.root, text="Steganography App", font="impact 25 bold", bg="black", fg="red").place(x=190, y=0)
#
#         # Heading
#         Label(self.root, text='Secret Message', font='impact 30 bold', bg='black', fg='red').place(x=260, y=12)
#
#         # Frame 1 (Image Display)
#         f1 = Frame(self.root, width=250, height=220, bd=5, bg='purple')
#         f1.place(x=50, y=100)
#         self.image_label = Label(f1, bg='purple')
#         self.image_label.place(x=0, y=0)
#
#         # Frame 2 (Text Input)
#         f2 = Frame(self.root, width=320, height=220, bd=5, bg='white')
#         f2.place(x=330, y=100)
#         self.message_text = Text(f2, font='arial 15 bold', wrap=WORD)
#         self.message_text.place(x=0, y=0, width=310, height=210)
#
#         # Secret Key Entry
#         Label(self.root, text='Enter Secret Key', font='10', bg='black', fg='yellow').place(x=260, y=330)
#         self.secret_key = Entry(self.root, bd=2, font='impact 10 bold', show='*')
#         self.secret_key.place(x=245, y=360)
#
#         # Buttons
#         Button(self.root, text='Open Image', bg='blue', fg='white', font='arial 12 bold', cursor='hand2',
#                command=self.open_image).place(x=60, y=417)
#         Button(self.root, text='Save Image', bg='green', fg='white', font='arial 12 bold', cursor='hand2',
#                command=self.save_image).place(x=190, y=417)
#         Button(self.root, text='Hide Data', bg='red', fg='white', font='arial 12 bold', cursor='hand2',
#                command=self.hide_data).place(x=380, y=417)
#         Button(self.root, text='Show Data', bg='orange', fg='white', font='arial 12 bold', cursor='hand2',
#                command=self.reveal_data).place(x=510, y=417)
#
#         button_x = 650  # Align right edges
#         button_y = 50   # Place above the white box (adjust as needed)
#
#         # Create the button
#         Button(self.root, text='Refresh', bg='grey', fg='white', font='arial 12 bold', cursor='hand2').place(x=button_x, y=button_y)
#
#
#     def open_image(self):
#         """Open and display an image."""
#         self.image_path = filedialog.askopenfilename(
#             initialdir=os.getcwd(),
#             title='Select Image File',
#             filetypes=(('Image Files', '*.png;*.jpg;*.jpeg'), ('All Files', '*.*'))
#         )
#         if self.image_path:
#             try:
#                 global img
#                 img = Image.open(self.image_path)
#                 img = img.resize((240, 210), Image.Resampling.LANCZOS)
#                 img = ImageTk.PhotoImage(img)
#                 self.image_label.configure(image=img)
#                 self.image_label.image = img
#             except Exception as e:
#                 messagebox.showerror("Error", f"Unable to open image: {str(e)}")
#
#     def hide_data(self):
#         """Hide the message in the image with a password."""
#         if not self.image_path:
#             messagebox.showerror("Error", "Please open an image first.")
#             return
#         # global message
#         message = self.message_text.get(1.0, END).strip()
#         if not message:
#             messagebox.showerror("Error", "Please enter a message to hide.")
#             return
#
#         password = self.secret_key.get().strip()
#         if not password:
#             messagebox.showerror("Error", "Please enter a password.")
#             return
#
#         try:
#             self.hidden_image = functions.hide_message(self.image_path, message, password)
#             messagebox.showinfo("Success", "Message hidden successfully.")
#         except Exception as e:
#             messagebox.showerror("Error", str(e))
#
#     def save_image(self):
#         """Save the image with the hidden message."""
#         if self.hidden_image:
#             save_path = filedialog.asksaveasfilename(
#                 defaultextension=".png",
#                 filetypes=[("PNG Files", "*.png")]
#             )
#             if save_path:
#                 try:
#                     functions.save_image(self.hidden_image, save_path)
#                     messagebox.showinfo("Success", "Image saved successfully.")
#                 except Exception as e:
#                     messagebox.showerror("Error", str(e))
#         else:
#             messagebox.showerror("Error", "No message hidden to save.")
#
#     def reveal_data(self):
#         """Reveal the hidden message with a password."""
#         if not self.image_path:
#             messagebox.showerror("Error", "Please open an image first.")
#             return
#         global password
#         password = self.secret_key.get().strip()
#         if not password:
#             messagebox.showerror("Error", "Please enter a password.")
#             return
#
#         try:
#             global message
#             message = functions.reveal_message(self.image_path, password)
#             if message:
#                 self.message_text.delete(1.0, END)
#                 self.message_text.insert(END, message)
#                 messagebox.showinfo("Success", "Message revealed successfully.")
#             else:
#                 messagebox.showerror("Error", "No hidden message found.")
#         except Exception as e:
#             messagebox.showerror("Error", str(e))
#
#     def refresh(self):
#         """Clears the text box, image box, and secret key entry box."""
#         # Clear the message text box
#         self.message_text.delete('1.0', END)
#
#         # Clear the image box
#         self.image_label.config(image='')
#         self.image_label.image = None  # Reset the image reference
#
#         # Reset the image path
#         self.image_path = None
#
#         # Clear the secret key entry box
#         self.secret_key.delete(0, END)
#
#     # def refresh(self):
#     #     """Clears the text box, image box, and secret key entry box."""
#     #     # Clear the text box
#     #     message.delete('1.0', END)
#     #     # Clear the image box by displaying a blank or default placeholder
#     #     img.config(image='')  # Assuming image_label is the widget displaying the image
#     #     # Clear the secret key entry box
#     #     password.delete(0, END)
#
#     # def hide_data(self):
#     #     """Hide the message in the image."""
#     #     if not self.image_path:
#     #         messagebox.showerror("Error", "Please open an image first.")
#     #         return
#     #
#     #     message = self.message_text.get(1.0, END).strip()
#     #     if not message:
#     #         messagebox.showerror("Error", "Please enter a message to hide.")
#     #         return
#     #
#     #     try:
#     #         self.hidden_image = functions.hide_message(self.image_path, message)
#     #         messagebox.showinfo("Success", "Message hidden successfully.")
#     #     except Exception as e:
#     #         messagebox.showerror("Error", str(e))
#
#
#     # def reveal_data(self):
#     #     """Reveal the hidden message."""
#     #     if not self.image_path:
#     #         messagebox.showerror("Error", "Please open an image first.")
#     #         return
#     #
#     #     try:
#     #         message = functions.reveal_message(self.image_path)
#     #         if message:
#     #             self.message_text.delete(1.0, END)
#     #             self.message_text.insert(END, message)
#     #             messagebox.showinfo("Success", "Message revealed successfully.")
#     #         else:
#     #             messagebox.showerror("Error", "No hidden message found.")
#     #     except Exception as e:
#     #         messagebox.showerror("Error", str(e))
