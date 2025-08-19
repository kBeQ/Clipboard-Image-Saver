import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab
import os
import sys
import configparser
from datetime import datetime

class ConfigManager:
    """Handles loading, saving, and providing default settings from an .ini file."""
    def __init__(self, filename="ClipboardSaver.ini"):
        self.base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        self.filepath = os.path.join(self.base_path, filename)
        self.config = configparser.ConfigParser()
        self._load_or_create_settings()

    def _load_or_create_settings(self):
        if not os.path.exists(self.filepath):
            self.config.add_section('Settings')
        else:
            self.config.read(self.filepath)

        # Define all default settings in one place for easy management
        defaults = {
            'default_folder': os.path.expanduser("~/Desktop"),
            'always_on_top': False,
            'quick_save_folder': os.path.join(os.path.expanduser('~'), 'Downloads'),
            'window_geometry': "",
            'window_size_index': 2
        }
        
        for key, value in defaults.items():
            if not self.config.has_option('Settings', key):
                self.set(key, value)

    def get(self, key):
        if key in ['always_on_top']:
            return self.config.getboolean('Settings', key)
        if key in ['window_size_index']:
            return self.config.getint('Settings', key)
        return self.config.get('Settings', key)

    def set(self, key, value):
        self.config.set('Settings', key, str(value))
        with open(self.filepath, 'w') as configfile:
            self.config.write(configfile)

class ClipboardImageSaverApp:
    def __init__(self, root):
        self.root = root
        self.config = ConfigManager()

        self.SIZE_OPTIONS = [
        ("Tiny (140x65)", "140x65", 32),
        ("Small (170x75)", "170x75", 40),
        ("Medium (200x85)", "200x85", 48),
        ("Large (250x110)", "250x110", 60),
        ("X-Large (520x230)", "520x230", 120),
        ("Huge (720x320)", "720x320", 170)
        ]

        # Break down the setup process into logical steps
        self._setup_variables()
        self._setup_window()
        self._load_assets()
        self._create_widgets()
        self._create_menus()
        
    def _setup_variables(self):
        """Initialize all necessary variables from the config."""
        self.size_index_var = tk.IntVar(value=self.config.get('window_size_index'))
        self.always_on_top_var = tk.BooleanVar(value=self.config.get('always_on_top'))
        self.destination_folder = self.config.get('default_folder')
        self.base_path = self.config.base_path

    def _setup_window(self):
        """Configure the main window's properties."""
        self.root.title("Clipboard Saver")
        self.root.configure(bg="#333333")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.attributes('-topmost', self.always_on_top_var.get())
        
        # Apply the initial size and position
        current_size_index = self.size_index_var.get()
        _, geometry, _ = self.SIZE_OPTIONS[current_size_index]
        saved_pos = self.config.get('window_geometry')
        if saved_pos and '+' in saved_pos:
            pos = saved_pos.split('+')[1:]
            self.root.geometry(f"{geometry}+{pos[0]}+{pos[1]}")
        else:
            self.root.geometry(geometry)

    def _load_icon(self, filename, size):
        """A helper function to load and resize an image, reducing repetition."""
        path = os.path.join(self.base_path, filename)
        img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def _load_assets(self):
        """Load and prepare all image assets."""
        try:
            self.root.iconbitmap(os.path.join(self.base_path, "Ico_ClipboardImageSaverApp.ico"))
            
            # Load original images once to prevent re-reading from disk
            self.original_save_img = Image.open(os.path.join(self.base_path, "icon_save.png"))
            self.original_dwnld_img = Image.open(os.path.join(self.base_path, "icon_dwnld.png"))
            self.original_settings_img = Image.open(os.path.join(self.base_path, "icon_settings.png"))

            # Load menu icons (these don't need to be reloaded)
            self.menu_save_icon = self._load_icon("icon_save.png", (16, 16))
            self.menu_dwnld_icon = self._load_icon("icon_dwnld.png", (16, 16))
            
            # Create the main button icons at the initial size
            initial_icon_size = self.SIZE_OPTIONS[self.size_index_var.get()][2]
            self._update_button_icons(initial_icon_size)

        except Exception as e:
            messagebox.showerror("Icon Error", f"Could not load assets.\nError: {e}")
            sys.exit()

    def _create_widgets(self):
        """Create and place all the main UI widgets."""
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # A helper to create buttons with common styling
        def create_button(image, command, column, is_menu=False):
            common_opts = {"bg": "#333333", "relief": tk.FLAT, "bd": 0, "activebackground": "#444444"}
            ButtonClass = tk.Menubutton if is_menu else tk.Button
            button = ButtonClass(self.root, image=image, **common_opts)
            if not is_menu:
                button.config(command=command)
            button.grid(row=0, column=column, sticky="nsew")
            return button

        self.save_as_button = create_button(self.save_icon, self.save_as, 0)
        self.insta_save_button = create_button(self.dwnld_icon, self.insta_save, 1)
        self.settings_button = create_button(self.settings_icon, None, 2, is_menu=True)

        self.status_bar = tk.Label(self.root, text=os.path.basename(self.destination_folder), bg="#222222", fg="white", anchor="w", padx=5)
        self.status_bar.grid(row=1, column=0, columnspan=3, sticky="ew")

    def _create_menus(self):
        """Create and configure the settings dropdown and its sub-menus."""
        self.settings_menu = tk.Menu(self.settings_button, tearoff=0, bg="#555555", fg="white")
        self.settings_button['menu'] = self.settings_menu
        
        self.settings_menu.add_checkbutton(label="Always on Top", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        
        size_menu = tk.Menu(self.settings_menu, tearoff=0, bg="#555555", fg="white")
        for index, (label, _, _) in enumerate(self.SIZE_OPTIONS):
            size_menu.add_radiobutton(label=label, variable=self.size_index_var, value=index, command=self.apply_new_size)
        self.settings_menu.add_cascade(label="Window Size", menu=size_menu)

        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Set 'Save As' Folder...", image=self.menu_save_icon, compound=tk.LEFT, command=self.set_default_directory)
        self.settings_menu.add_command(label="Set 'Insta-Save' Folder...", image=self.menu_dwnld_icon, compound=tk.LEFT, command=self.set_quick_save_directory)

    def _update_button_icons(self, size):
        """Resizes the main button icons and applies them."""
        self.save_icon = ImageTk.PhotoImage(self.original_save_img.resize((size, size), Image.Resampling.LANCZOS))
        self.dwnld_icon = ImageTk.PhotoImage(self.original_dwnld_img.resize((size, size), Image.Resampling.LANCZOS))
        self.settings_icon = ImageTk.PhotoImage(self.original_settings_img.resize((size, size), Image.Resampling.LANCZOS))
        
        # This check prevents errors during the initial setup
        if hasattr(self, 'save_as_button'):
            self.save_as_button.config(image=self.save_icon)
            self.insta_save_button.config(image=self.dwnld_icon)
            self.settings_button.config(image=self.settings_icon)

    # --- Event Handlers and Core Logic ---
    def apply_new_size(self):
        new_index = self.size_index_var.get()
        _, new_geometry, new_icon_size = self.SIZE_OPTIONS[new_index]
        
        pos = self.root.geometry().split('+')[1:]
        self.root.geometry(f"{new_geometry}+{pos[0]}+{pos[1]}")
        
        self._update_button_icons(new_icon_size)
        self.config.set('window_size_index', new_index)

    def on_closing(self):
        self.config.set('window_geometry', self.root.geometry())
        self.root.destroy()

    def toggle_always_on_top(self):
        is_on_top = self.always_on_top_var.get()
        self.root.attributes('-topmost', is_on_top)
        self.config.set('always_on_top', is_on_top)

    def set_default_directory(self):
        folder_path = filedialog.askdirectory(title="Select 'Save As' Folder")
        if folder_path:
            self.destination_folder = folder_path
            self.status_bar.config(text=os.path.basename(folder_path))
            self.config.set('default_folder', folder_path)
            messagebox.showinfo("Settings Saved", f"'Save As' folder set to:\n{folder_path}")

    def set_quick_save_directory(self):
        folder_path = filedialog.askdirectory(title="Select 'Insta-Save' Folder")
        if folder_path:
            self.config.set('quick_save_folder', folder_path)
            messagebox.showinfo("Settings Saved", f"'Insta-Save' folder set to:\n{folder_path}")

    def save_as(self):
        try:
            filename = datetime.now().strftime("IMG_%Y%m%d_%H%M%S.png")
            save_path = filedialog.asksaveasfilename(
                initialdir=self.destination_folder, initialfile=filename,
                defaultextension=".png", filetypes=[("PNG files", "*.png")]
            )
            if not save_path: return
            image = ImageGrab.grabclipboard()
            if image is None: raise ValueError("No image found on clipboard.")
            image.save(save_path, "PNG")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insta_save(self):
        try:
            folder = self.config.get('quick_save_folder')
            os.makedirs(folder, exist_ok=True)
            filename = datetime.now().strftime("IMG_%Y%m%d_%H%M%S.png")
            save_path = os.path.join(folder, filename)
            image = ImageGrab.grabclipboard()
            if image is None: raise ValueError("No image found on clipboard.")
            image.save(save_path, "PNG")
            
            original_text = os.path.basename(self.destination_folder)
            self.status_bar.config(text=f"Saved to {os.path.basename(folder)}!")
            self.root.after(2500, lambda: self.status_bar.config(text=original_text))
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardImageSaverApp(root)
    root.mainloop()