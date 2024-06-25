import os
import subprocess
import customtkinter
from tkinter import filedialog, messagebox, StringVar


class ProjectSetupApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Project Setup")
        self.geometry("900x650")
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
        self.project_name_label.pack(pady=10)

        self.project_name_entry = customtkinter.CTkEntry(
            self,
            width=300,
            font=self.font,
            border_width=2,
            border_color="grey",
            bg_color="#05040A",
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
        self.dir_label.pack(pady=10)

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
            text_color="white",
            font=self.font,
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
        self.main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Create a canvas to hold the options frame
        self.canvas = customtkinter.CTkCanvas(self.main_frame, bg="#05040A")
        self.canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Add scrollbars
        self.scroll_y = customtkinter.CTkScrollbar(self.main_frame, orientation="vertical", command=self.canvas.yview)
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        self.scroll_x = customtkinter.CTkScrollbar(self.main_frame, orientation="horizontal", command=self.canvas.xview)
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        # Options for folders and files
        self.options_frame = customtkinter.CTkFrame(
            self.canvas,
            bg_color="#05040A",
            fg_color="#05040A",
            corner_radius=10,
            border_width=1,
            border_color="#7F8AB5",
        )

        self.canvas.create_window((0, 0), window=self.options_frame, anchor="nw")

        self.option_vars = {
            ".gitignore": customtkinter.StringVar(),
            "CHANGELOG.rst": customtkinter.StringVar(),
            "CONTRIBUTING.rst": customtkinter.StringVar(),
            "docs/index.rst": customtkinter.StringVar(),
            "LICENSE": customtkinter.StringVar(),
            "README.rst": customtkinter.StringVar(),
            "requirements.txt": customtkinter.StringVar(),
            "setup.py": customtkinter.StringVar(),
            "my_project/__init__.py": customtkinter.StringVar(),
            "my_project/module.py": customtkinter.StringVar(),
            "tests/__init__.py": customtkinter.StringVar(),
            "tests/test_module.py": customtkinter.StringVar(),
        }

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
            checkbox.grid(row=row, column=0, sticky="w", pady=10, padx=6)
            row += 1

        # Update the canvas scroll region
        self.options_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Preview label
        self.preview_label = customtkinter.CTkLabel(
            self.main_frame,
            text="",
            bg_color="#05040A",
            fg_color="#05040A",
            text_color="white",
            font=self.font,
            justify="left",
            anchor="w",
        )
        self.preview_label.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.main_frame.columnconfigure(2, weight=1)  # Make the preview expand

        # Create project button
        self.create_button = customtkinter.CTkButton(
            self,
            text="Create Project",
            width=400,
            height=60,
            command=self.create_project,
            bg_color="#05040A",
            border_width=2,
            fg_color="#1D1A29",
            text_color="white",
            corner_radius=10,
            font=self.font,
        )
        self.create_button.pack(pady=10)

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
        preview_text = f"{project_name}/\n"
        preview_text += "├── .gitignore\n" if self.option_vars[".gitignore"].get() == "on" else ""
        preview_text += "├── CHANGELOG.rst\n" if self.option_vars["CHANGELOG.rst"].get() == "on" else ""
        preview_text += "├── CONTRIBUTING.rst\n" if self.option_vars["CONTRIBUTING.rst"].get() == "on" else ""
        preview_text += "├── docs\n" if self.option_vars["docs/index.rst"].get() == "on" else ""
        preview_text += "│   └── index.rst\n" if self.option_vars["docs/index.rst"].get() == "on" else ""
        preview_text += "├── LICENSE\n" if self.option_vars["LICENSE"].get() == "on" else ""
        preview_text += "├── README.rst\n" if self.option_vars["README.rst"].get() == "on" else ""
        preview_text += "├── requirements.txt\n" if self.option_vars["requirements.txt"].get() == "on" else ""
        preview_text += "├── setup.py\n" if self.option_vars["setup.py"].get() == "on" else ""
        preview_text += "├── my_project\n" if self.option_vars["my_project/__init__.py"].get() == "on" or self.option_vars["my_project/module.py"].get() == "on" else ""
        preview_text += "│   ├── __init__.py\n" if self.option_vars["my_project/__init__.py"].get() == "on" else ""
        preview_text += "│   └── module.py\n" if self.option_vars["my_project/module.py"].get() == "on" else ""
        preview_text += "└── tests\n" if self.option_vars["tests/__init__.py"].get() == "on" or self.option_vars["tests/test_module.py"].get() == "on" else ""
        preview_text += "    ├── __init__.py\n" if self.option_vars["tests/__init__.py"].get() == "on" else ""
        preview_text += "    └── test_module.py\n" if self.option_vars["tests/test_module.py"].get() == "on" else ""

        self.preview_label.configure(text=preview_text)


if __name__ == "__main__":
    app = ProjectSetupApp()
    app.mainloop()

