from tkinter import Tk
from gui import SteganographyApp

def main():
    root = Tk()
    app = SteganographyApp(root)

    # Add a refresh button to call the refresh method in the GUI
    root.after(0, lambda: app.refresh())  # Ensures refresh happens after the GUI is initialized

    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

# from tkinter import Tk
# from gui import SteganographyApp
#
# if __name__ == "__main__":
#     root = Tk()
#     app = SteganographyApp(root)
#     root.mainloop()
