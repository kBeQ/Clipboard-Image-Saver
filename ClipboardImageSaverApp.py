import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab
import os
import sys

class ClipboardImageSaverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard Image Saver")
        # Make the window more compact
        self.root.geometry("150x80")
        self.root.configure(bg="#333333")

        # --- Resolve Paths for Icon and Images ---
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        
        # Set the main window icon
        try:
            icon_path = os.path.join(base_path, "Ico_ClipboardImageSaverApp.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to load window icon: {e}")

        # --- Load Button Icons ---
        try:
            self.icon_folder = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "icon_folder.png")))
            self.icon_save = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "icon_save.png")))
        except Exception as e:
            messagebox.showerror("Icon Error", f"Could not load button icons (e.g., icon_folder.png).\n\nError: {e}")
            sys.exit()

        # --- UI Layout using .grid() ---
        # Configure the grid to expand horizontally
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # --- Widgets ---
        # Button to select destination folder
        self.select_dest_button = tk.Button(
            root, image=self.icon_folder, command=self.select_destination_folder,
            bg="#555555", relief=tk.FLAT, borderwidth=0, highlightthickness=0
        )
        self.select_dest_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Button to save as PNG
        self.save_as_button = tk.Button(
            root, image=self.icon_save, command=self.save_as,
            bg="#555555", relief=tk.FLAT, borderwidth=0, highlightthickness=0
        )
        self.save_as_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Status Bar for destination folder
        self.destination_folder = os.path.expanduser("~/Desktop")
        self.status_bar = tk.Label(
            root, text=os.path.basename(self.destination_folder),
            bg="#222222", fg="white", anchor="w"
        )
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

    def select_destination_folder(self):
        folder_path = filedialog.askdirectory(title="Saving to:")
        if folder_path:
            self.destination_folder = folder_path
            # Update status bar to show only the folder name for compactness
            self.status_bar.config(text=os.path.basename(folder_path))
            print(f"Destination folder set to: {folder_path}")

    def save_as(self):
        try:
            # Generate a default filename based on the current date and time
            default_filename = datetime.now().strftime("IMG_%Y%m%d_%H%M%S.png")

            save_path = filedialog.asksaveasfilename(
                initialdir=self.destination_folder,
                initialfile=default_filename,
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                title="Save Clipboard Image As..."
            )
            if not save_path:
                return

            image = ImageGrab.grabclipboard()
            if image is None:
                raise ValueError("No image found on clipboard.")

            image.save(save_path, "PNG")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardImageSaverApp(root)
    root.mainloop()