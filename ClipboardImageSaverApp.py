import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab
import os
import sys
import json
from datetime import datetime

# --- Configuration Manager ---
class ConfigManager:
    def __init__(self, filename="settings.json"):
        self.base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        self.filepath = os.path.join(self.base_path, filename)
        self.settings = self._load_settings()

    def _load_settings(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Define default user downloads folder
            downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
            return {
                'default_folder': os.path.expanduser("~/Desktop"),
                'always_on_top': False,
                'quick_save_folder': downloads_folder # New setting for Insta Save
            }

    def get(self, key):
        return self.settings.get(key)

    def set(self, key, value):
        self.settings[key] = value
        with open(self.filepath, 'w') as f:
            json.dump(self.settings, f, indent=4)

# --- Main Application ---
class ClipboardImageSaverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard Saver")
        # Widen the window for the fourth button
        self.root.geometry("240x80")
        self.root.configure(bg="#333333")
        self.root.resizable(False, False)

        self.config = ConfigManager()
        
        self.always_on_top_var = tk.BooleanVar(value=self.config.get('always_on_top'))
        self.root.attributes('-topmost', self.always_on_top_var.get())
        self.destination_folder = self.config.get('default_folder')

        base_path = self.config.base_path
        
        try:
            self.root.iconbitmap(os.path.join(base_path, "Ico_ClipboardImageSaverApp.ico"))
        except Exception as e:
            print(f"Failed to load window icon: {e}")

        try:
            FIXED_ICON_SIZE = (48, 48)
            img_folder = Image.open(os.path.join(base_path, "icon_folder.png")).resize(FIXED_ICON_SIZE, Image.Resampling.LANCZOS)
            img_save = Image.open(os.path.join(base_path, "icon_save.png")).resize(FIXED_ICON_SIZE, Image.Resampling.LANCZOS)
            img_settings = Image.open(os.path.join(base_path, "icon_settings.png")).resize(FIXED_ICON_SIZE, Image.Resampling.LANCZOS)
            img_dwnld = Image.open(os.path.join(base_path, "icon_dwnld.png")).resize(FIXED_ICON_SIZE, Image.Resampling.LANCZOS)
            
            self.folder_icon = ImageTk.PhotoImage(img_folder)
            self.save_icon = ImageTk.PhotoImage(img_save)
            self.settings_icon = ImageTk.PhotoImage(img_settings)
            self.dwnld_icon = ImageTk.PhotoImage(img_dwnld)
        except Exception as e:
            messagebox.showerror("Icon Error", f"Could not load button icons.\nError: {e}")
            sys.exit()

        # Configure all four columns
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # --- Widgets ---
        self.select_dest_button = tk.Button(root, image=self.folder_icon, command=self.select_destination_folder, bg="#333333", relief=tk.FLAT, bd=0, activebackground="#444444")
        self.select_dest_button.grid(row=0, column=0, sticky="nsew")

        self.save_as_button = tk.Button(root, image=self.save_icon, command=self.save_as, bg="#333333", relief=tk.FLAT, bd=0, activebackground="#444444")
        self.save_as_button.grid(row=0, column=1, sticky="nsew")
        
        # New Insta Save Button
        self.insta_save_button = tk.Button(root, image=self.dwnld_icon, command=self.insta_save, bg="#333333", relief=tk.FLAT, bd=0, activebackground="#444444")
        self.insta_save_button.grid(row=0, column=2, sticky="nsew")

        self.settings_button = tk.Menubutton(root, image=self.settings_icon, bg="#333333", relief=tk.FLAT, bd=0, activebackground="#444444")
        self.settings_button.grid(row=0, column=3, sticky="nsew")

        self.settings_menu = tk.Menu(self.settings_button, tearoff=0, bg="#555555", fg="white")
        self.settings_menu.add_checkbutton(label="Always on Top", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Set 'Save As' Folder...", command=self.set_default_directory)
        self.settings_menu.add_command(label="Set 'Insta-Save' Folder...", command=self.set_quick_save_directory)
        self.settings_button['menu'] = self.settings_menu

        self.status_bar = tk.Label(root, text=os.path.basename(self.destination_folder), bg="#222222", fg="white", anchor="w", padx=5)
        self.status_bar.grid(row=1, column=0, columnspan=4, sticky="ew")

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

    def select_destination_folder(self):
        folder_path = filedialog.askdirectory(title="Change Current 'Save As' Folder", initialdir=self.destination_folder)
        if folder_path:
            self.destination_folder = folder_path
            self.status_bar.config(text=os.path.basename(folder_path))

    def save_as(self):
        try:
            default_filename = datetime.now().strftime("IMG_%Y%m%d_%H%M%S.png")
            save_path = filedialog.asksaveasfilename(
                initialdir=self.destination_folder, initialfile=default_filename,
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
            quick_save_folder = self.config.get('quick_save_folder')
            os.makedirs(quick_save_folder, exist_ok=True)
            
            filename = datetime.now().strftime("IMG_%Y%m%d_%H%M%S.png")
            save_path = os.path.join(quick_save_folder, filename)

            image = ImageGrab.grabclipboard()
            if image is None:
                raise ValueError("No image found on clipboard.")
            
            image.save(save_path, "PNG")

            # Give user feedback on the status bar
            original_text = os.path.basename(self.destination_folder)
            self.status_bar.config(text=f"Saved to {os.path.basename(quick_save_folder)}!")
            self.root.after(2500, lambda: self.status_bar.config(text=original_text))

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardImageSaverApp(root)
    root.mainloop()