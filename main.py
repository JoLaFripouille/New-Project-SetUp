import os
import subprocess
import customtkinter
from tkinter import filedialog, messagebox, StringVar, Text


class ProjectSetupApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Project Setup")
        self.geometry("550x710")
        self.config(bg="#05040A")

        self.font_label = customtkinter.CTkFont(family="Dubai", size=20)
        self.font = customtkinter.CTkFont(family="Dubai", size=16)

        # Project name entry
        self.project_name_label = customtkinter.CTkLabel(
            self,
            text="Project Name:",
            bg_color="#05040A",
            fg_color="#05040A",
            text_color="white",
            font=self.font_label,
        )
        self.project_name_label.pack(pady=5)

        self.project_name_entry = customtkinter.CTkEntry(
            self,
            width=300,
            font=self.font,
            border_width=2,
            border_color="grey",
            bg_color="#05040A",
            justify= 'center'
        )
        self.project_name_entry.pack(pady=5)

        # Directory selection
        self.dir_label = customtkinter.CTkLabel(
            self,
            text="Select Directory",
            bg_color="#05040A",
            fg_color="#05040A",
            text_color="white",
            font=self.font_label,
        )
        self.dir_label.pack(pady=5)

        self.dir_button = customtkinter.CTkButton(
            self,
            text="Browse",
            command=self.browse_directory,
            bg_color="#05040A",
            border_width=2,
            fg_color="#1D1A29",
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
            text_color="grey",
            font=("Dubai", 12),
        )
        self.dir_path_label.pack(pady=5)

        # Frame for options and preview
        self.main_frame = customtkinter.CTkFrame(
            self,
            bg_color="#05040A",
            fg_color="#05040A",
            corner_radius=10,
            border_width=1,
            border_color="#7F8AB5",
        )
        self.main_frame.pack(pady=5, padx=30, fill="both", expand=True)

        # Options for folders and files
        self.option_vars = {
            ".gitignore": customtkinter.StringVar(),
            "docs/index.rst": customtkinter.StringVar(),
            "README.rst": customtkinter.StringVar(),
            "requirements.txt": customtkinter.StringVar(),
            "setup.py": customtkinter.StringVar(),
            "my_project/__init__.py": customtkinter.StringVar(),
            "my_project/module.py": customtkinter.StringVar(),
            "tests/__init__.py": customtkinter.StringVar(),
            "tests/test_module.py": customtkinter.StringVar(),
            "images/": customtkinter.StringVar(),
        }

        self.options_frame = customtkinter.CTkScrollableFrame(
            self.main_frame,
            bg_color="transparent",
            fg_color="#05040A",
            height=360,
            corner_radius=15,
            border_color="#7F8AB5",
        )
        self.options_frame.grid(row=0, column=0, padx=3, pady=3, sticky="ns")

        row = 0
        for option in self.option_vars:
            checkbox = customtkinter.CTkCheckBox(
                self.options_frame,
                text=option,
                variable=self.option_vars[option],
                onvalue="on",
                offvalue="off",
                bg_color="#05040A",
                fg_color="#1D1A29",
                text_color="white",
                font=self.font,
                command=self.update_preview,
            )
            checkbox.grid(row=row, column=0, sticky="w", pady=6, padx=8)
            row += 1

        # Textbox for preview
        self.preview_textbox = Text(
            self.main_frame,
            bg="#05040A",
            fg="white",
            font=("Courier", 12),
            wrap="none",
            state="disabled"
        )
        self.preview_textbox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.main_frame.columnconfigure(1, weight=1)  # Make the preview expand

        # Create project button
        self.create_button = customtkinter.CTkButton(
            self,
            text="Create Project",
            width=450,
            height=60,
            command=self.create_project,
            bg_color="#05040A",
            border_width=2,
            fg_color="#1D1A29",
            text_color="white",
            corner_radius=10,
            font=self.font,
        )
        self.create_button.pack(pady=20)

        self.update_preview()

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

        for option, var in self.option_vars.items():
            if var.get() == "on":
                path_parts = option.split('/')
                sub_path = project_path
                for part in path_parts:
                    sub_path = os.path.join(sub_path, part)
                    if '.' not in part:
                        os.makedirs(sub_path, exist_ok=True)
                    else:
                        with open(sub_path, 'w') as f:
                            if part == "README.rst":
                                f.write(f"# {project_name}")

        messagebox.showinfo("Success", f"Project {project_name} created successfully!")

        # Specify the full path to code.exe
        code_path = r"C:\\Users\\Salon\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        if os.path.exists(code_path):
            subprocess.run([code_path, project_path])
        else:
            messagebox.showerror(
                "Error", "VS Code executable not found. Please ensure it is installed."
            )

    def update_preview(self):
        project_name = self.project_name_entry.get() or "my_project"
        self.preview_textbox.configure(state="normal")
        self.preview_textbox.delete("1.0", "end")
        self.preview_textbox.insert("end", f"{project_name}/\n", "project")
        if self.option_vars[".gitignore"].get() == "on":
            self.preview_textbox.insert("end", "├── .gitignore\n", "file")
        if self.option_vars["docs/index.rst"].get() == "on":
            self.preview_textbox.insert("end", "├── docs\n", "folder")
            self.preview_textbox.insert("end", "│   └── index.rst\n", "file")
        if self.option_vars["README.rst"].get() == "on":
            self.preview_textbox.insert("end", "├── README.rst\n", "file")
        if self.option_vars["requirements.txt"].get() == "on":
            self.preview_textbox.insert("end", "├── requirements.txt\n", "file")
        if self.option_vars["setup.py"].get() == "on":
            self.preview_textbox.insert("end", "├── setup.py\n", "file")
        if self.option_vars["my_project/__init__.py"].get() == "on" or self.option_vars["my_project/module.py"].get() == "on":
            self.preview_textbox.insert("end", "├── my_project\n", "folder")
            if self.option_vars["my_project/__init__.py"].get() == "on":
                self.preview_textbox.insert("end", "│   ├── __init__.py\n", "file")
            if self.option_vars["my_project/module.py"].get() == "on":
                self.preview_textbox.insert("end", "│   └── module.py\n", "file")
        if self.option_vars["tests/__init__.py"].get() == "on" or self.option_vars["tests/test_module.py"].get() == "on":
            self.preview_textbox.insert("end", "└── tests\n", "folder")
            if self.option_vars["tests/__init__.py"].get() == "on":
                self.preview_textbox.insert("end", "    ├── __init__.py\n", "file")
            if self.option_vars["tests/test_module.py"].get() == "on":
                self.preview_textbox.insert("end", "    └── test_module.py\n", "file")
        if self.option_vars["images/"].get() == "on":
                    self.preview_textbox.insert("end", "├── images/\n", "folder")

        self.preview_textbox.configure(state="disabled")

        self.preview_textbox.tag_configure("project", foreground="green")
        self.preview_textbox.tag_configure("folder", foreground="pink")
        self.preview_textbox.tag_configure("file", foreground="violet")


if __name__ == "__main__":
    app = ProjectSetupApp()
    app.mainloop()

