import random
import string
import pickle
import os
import tkinter as tk
import customtkinter
import pyperclip


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.search_value = ""
        self.passwords = self.load_passwords()
        self.title("Password Manager")
        self.geometry("700x450")
        self.resizable(False, False)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Password Manager",
                                                             compound="left", font=("Poppins", 14))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.view_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="View Passwords",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"), anchor="w",
                                                   command=self.view_button_event, font=("Poppins", 14))
        self.view_button.grid(row=1, column=0, sticky="ew")

        self.add_frame_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Add Password",
                                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"),
                                                        anchor="w", command=self.add_frame_button, font=("Poppins", 14))
        self.add_frame_button.grid(row=2, column=0, sticky="ew")

        self.generate_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                       border_spacing=10, text="Generate Password",
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                       hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.generate_button_event,
                                                       font=("Poppins", 14))
        self.generate_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event,
                                                                font=("Poppins", 14))
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create add frame
        self.add_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.add_frame.grid_columnconfigure(0, weight=1)

        self.service_input = customtkinter.CTkEntry(self.add_frame, placeholder_text="Service", font=("Poppins", 18))
        self.service_input.grid(row=1, column=0, padx=20, pady=(100, 0))

        self.username_input = customtkinter.CTkEntry(self.add_frame, placeholder_text="Username", font=("Poppins", 18))
        self.username_input.grid(row=2, column=0, padx=20, pady=(15, 7))

        self.password_input = customtkinter.CTkEntry(self.add_frame, placeholder_text="Password", font=("Poppins", 18))
        self.password_input.grid(row=3, column=0, padx=20)

        self.add_button = customtkinter.CTkButton(self.add_frame, text="Add Password", font=("Poppins", 18),
                                                  command=lambda: self.add_password(self.service_input.get(),
                                                                                    self.username_input.get(),
                                                                                    self.password_input.get()))
        self.add_button.grid(row=4, column=0, padx=20, pady=10)

        # create generate frame
        self.generate_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.generate_frame.grid_columnconfigure(0, weight=1)

        self.new_pw = customtkinter.CTkLabel(self.generate_frame, text=''.join(
            random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20)),
                                             font=("Poppins", 18))
        self.new_pw.grid(row=1, column=0, padx=20, pady=(150, 0))

        self.slider = customtkinter.CTkSlider(self.generate_frame, from_=1, to=40, number_of_steps=40)
        self.slider.bind("<B1-Motion>", lambda event: self.generate_password(int(self.slider.get())))
        self.slider.bind("<ButtonRelease-1>", lambda event: self.generate_password(int(self.slider.get())))

        self.slider.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.copy_button = customtkinter.CTkButton(self.generate_frame, text="Copy", font=("Poppins", 12),
                                                   command=lambda: pyperclip.copy(self.new_pw.cget("text")))
        self.copy_button.grid(row=4, column=0, padx=20, pady=10)
        self.view_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.view_frame.grid_columnconfigure(0, weight=1)
        self.show_view_frame()

        # select default frame
        self.select_frame_by_name("view")

    def save_passwords(self):
        with open("passwords.p", "wb") as f:
            pickle.dump(self.passwords, f)

    def load_passwords(self):
        if os.path.getsize("passwords.p") == 0:
            return {}
        with open("passwords.p", "rb") as f:
            return pickle.load(f)

    def show_view_frame(self, back_button=None, error_label=None, service_label=None, username_label=None,
                        password_label=None, copy_button=None):
        if back_button:
            back_button.grid_remove()
        if service_label:
            service_label.grid_remove()
        if username_label:
            username_label.grid_remove()
        if password_label:
            password_label.grid_remove()
        if error_label:
            error_label.grid_remove()
        if copy_button:
            copy_button.grid_remove()
        # create view frame
        prompt_label = customtkinter.CTkLabel(self.view_frame, text="Search for the service to get login details",
                                              font=("Poppins", 12))
        prompt_label.grid(row=1, column=0, padx=20, pady=(150, 0))
        search_bar = customtkinter.CTkEntry(self.view_frame, placeholder_text="Amazon, Google, Twitter etc...",
                                            font=("Poppins", 18), width=500)
        search_bar.grid(row=2, column=0, padx=20, pady=10)
        search_button = customtkinter.CTkButton(self.view_frame, text="Search", font=("Poppins", 14),
                                                command=lambda: self.show_info(prompt_label, search_button, search_bar,
                                                                               search_bar.get()))
        search_button.grid(row=3, column=0, padx=20, pady=10)

    def show_info(self, prompt_label, search_button, search_bar, search_value):
        prompt_label.grid_remove()
        search_bar.grid_remove()
        search_button.grid_remove()

        service_label = None
        username_label = None
        password_label = None
        error_label = None
        copy_button = None

        if search_value.lower() in list(map(str.lower, self.passwords.keys())):
            search_value = search_bar.get().strip()
            lowercase_search_value = search_value.lower()
            username = ""
            password = ""
            service = ""
            for key in self.passwords.keys():
                if key.lower() == lowercase_search_value:
                    username = self.passwords[key][0]
                    password = self.passwords[key][1]
                    service = key
            service_label = customtkinter.CTkLabel(self.view_frame, text=service, font=("Poppins", 18))
            service_label.grid(row=2, column=0, padx=20, pady=(100, 0))
            username_label = customtkinter.CTkLabel(self.view_frame, text="Username: " + username, font=("Poppins", 18))
            username_label.grid(row=3, column=0, padx=20, pady=10)
            password_label = customtkinter.CTkLabel(self.view_frame, text="Password: " + password, font=("Poppins", 18))
            password_label.grid(row=4, column=0, padx=20, pady=10)
            copy_button = customtkinter.CTkButton(self.view_frame, text="Copy Password", font=("Poppins", 12), command=lambda: pyperclip.copy(password))
            copy_button.grid(row=5, column=0, padx=20, pady=10)
        else:
            error_label = customtkinter.CTkLabel(self.view_frame, text=search_value + " not found",
                                                 font=("Poppins", 18))
            error_label.grid(row=2, column=0, padx=20, pady=(100, 0))

        back_button = customtkinter.CTkButton(self.view_frame, text="Back", font=("Poppins", 18),
                                              command=lambda: self.show_view_frame(back_button, error_label,
                                                                                   service_label, username_label,
                                                                                   password_label, copy_button))
        back_button.grid(row=1, column=0, padx=20, pady=10)

    def generate_password(self, length):
        characters = string.ascii_letters + string.digits + string.punctuation
        length = int(length)
        password = ''.join(random.choice(characters) for i in range(length))
        self.new_pw.configure(text=password)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.view_button.configure(fg_color=("gray75", "gray25") if name == "view" else "transparent")
        self.add_frame_button.configure(fg_color=("gray75", "gray25") if name == "add" else "transparent")
        self.generate_button.configure(fg_color=("gray75", "gray25") if name == "generate" else "transparent")

        # show selected frame
        if name == "view":
            self.view_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.view_frame.grid_forget()
        if name == "add":
            self.add_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.add_frame.grid_forget()
        if name == "generate":
            self.generate_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.generate_frame.grid_forget()

    def add_password(self, service, username, password):
        self.passwords[service.lower()] = [username, password]
        self.service_input.delete(0, "end")
        self.username_input.delete(0, "end")
        self.password_input.delete(0, "end")

    def view_button_event(self):
        self.select_frame_by_name("view")

    def add_frame_button(self):
        self.select_frame_by_name("add")

    def generate_button_event(self):
        self.select_frame_by_name("generate")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == '__main__':
    app = App()
    app.mainloop()
    app.save_passwords()
