import os
import json
import subprocess
import customtkinter
from tkinter import filedialog, messagebox, StringVar


class ProjectSetupApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Project Setup")
        self.geometry("550x700")
        self.config(bg="#05040A")

        self.font = ("Dubai", 16)  # Définir une police plus lisible

        # Project name entry
        self.project_name_label = customtkinter.CTkLabel(
            self,
            text="Project Name:",
            bg_color="#05040A",
            fg_color="#05040A",
            text_color="white",
            font=self.font,
        )
        self.project_name_label.pack(pady=10)

        self.project_name_entry = customtkinter.CTkEntry(
            self, width=300, font=self.font
        )
        self.project_name_entry.pack(pady=5)

        # Directory selection
        self.dir_label = customtkinter.CTkLabel(
            self,
            text="Select Directory:",
            bg_color="#05040A",
            fg_color="#05040A",
            text_color="white",
            font=self.font,
        )
        self.dir_label.pack(pady=10)

        self.dir_button = customtkinter.CTkButton(
            self,
            text="Browse",
            command=self.browse_directory,
            fg_color="#4e4e4e",
            text_color="white",
            corner_radius=10,
            font=self.font,
        )
        self.dir_button.pack(pady=5)

        self.dir_path = StringVar()
        self.dir_path_label = customtkinter.CTkLabel(
            self,
            textvariable=self.dir_path,
            bg_color="#05040A",
            fg_color="#05040A",
            text_color="white",
            font=self.font,
        )
        self.dir_path_label.pack(pady=5)

        # Options for folders and files
        self.options_frame = customtkinter.CTkFrame(
            self,
            bg_color="#05040A",
            fg_color="#05040A",
            corner_radius=10,
            border_width=1,
            border_color="#7F8AB5",
        )
        self.options_frame.pack(pady=20, padx=20, fill="both", expand="yes")

        self.option_vars = {
            "docs": customtkinter.StringVar(),
            "tests": customtkinter.StringVar(),
            "README.md": customtkinter.StringVar(),
            "requirements.txt": customtkinter.StringVar(),
            "setup.py": customtkinter.StringVar(),
        }

        for option in self.option_vars:
            customtkinter.CTkCheckBox(
                self.options_frame,
                text=option,
                variable=self.option_vars[option],
                onvalue="on",
                offvalue="off",
                bg_color="#05040A",
                fg_color="#4e4e4e",
                text_color="white",
                font=self.font,
            ).pack(anchor="w")

        # Create project button
        self.create_button = customtkinter.CTkButton(
            self,
            text="Create Project",
            command=self.create_project,
            fg_color="#4e4e4e",
            text_color="white",
            corner_radius=10,
            font=self.font,
        )
        self.create_button.pack(pady=20)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_path.set(directory)

    def create_project(self):
        project_name = self.project_name_entry.get()
        base_dir = self.dir_path.get()
        if not project_name or not base_dir:
            messagebox.showerror(
                "Error", "Please specify a project name and directory."
            )
            return

        project_path = os.path.join(base_dir, project_name)
        os.makedirs(project_path, exist_ok=True)

        if self.option_vars["docs"].get() == "on":
            os.makedirs(os.path.join(project_path, "docs"), exist_ok=True)

        if self.option_vars["tests"].get() == "on":
            os.makedirs(os.path.join(project_path, "tests"), exist_ok=True)
            with open(os.path.join(project_path, "tests", "__init__.py"), "w") as f:
                f.write("")

        if self.option_vars["README.md"].get() == "on":
            with open(os.path.join(project_path, "README.md"), "w") as f:
                f.write(f"# {project_name}")

        if self.option_vars["requirements.txt"].get() == "on":
            with open(os.path.join(project_path, "requirements.txt"), "w") as f:
                f.write("")

        if self.option_vars["setup.py"].get() == "on":
            with open(os.path.join(project_path, "setup.py"), "w") as f:
                f.write(
                    f"""from setuptools import setup, find_packages

setup(
    name="{project_name}",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
)
"""
                )

        messagebox.showinfo("Success", f"Project {project_name} created successfully!")

        # Specify the full path to code.exe
        code_path = (
            r"C:\\Users\\Salon\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        )
        subprocess.run([code_path, project_path])


if __name__ == "__main__":
    app = ProjectSetupApp()
    app.mainloop()
