import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageGrab
import os
import sys
from datetime import datetime


class ClipboardImageSaverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard Image Saver")
        self.root.geometry("400x160")

        # Dynamically resolve the icon path
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "Ico_ClipboardImageSaverApp.ico")

        # Attempt to set the icon dynamically
        try:
            self.root.iconbitmap(icon_path)  # Set the icon for taskbar & window
        except Exception as e:
            print(f"Failed to load the icon dynamically: {e}")

        # Apply dark mode
        self.root.configure(bg="#333333")

        # Display the current destination folder dynamically
        self.destination_folder = os.path.expanduser("~/Desktop")
        self.label = tk.Label(
            root,
            text=f"Current destination folder: {self.destination_folder}",
            bg="#333333",
            fg="white",
            wraplength=400,
        )
        self.label.pack(pady=10)

        # Button to select destination folder
        self.select_dest_button = tk.Button(
            root,
            text="Change Destination Folder",
            command=self.select_destination_folder,
            bg="#555555",
            fg="white",
        )
        self.select_dest_button.pack(pady=5)

        # Button to save as PNG in the destination folder
        self.save_as_button = tk.Button(
            root,
            text="Save As...",
            command=self.save_as,
            bg="#555555",
            fg="white",
        )
        self.save_as_button.pack(pady=5)

    def select_destination_folder(self):
        folder_path = filedialog.askdirectory(title="Saving to:")
        if folder_path:
            self.destination_folder = folder_path
            self.label.config(
                text=f"Current destination folder: {self.destination_folder}"
            )
            print(f"Destination folder set to: {folder_path}")
        else:
            print("No folder selected.")

    def save_as(self):
        try:
            save_path = filedialog.asksaveasfilename(
                initialdir=self.destination_folder,
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                title="Save Clipboard Image As..."
            )
            if not save_path:
                print("Save canceled by user.")
                return

            image = ImageGrab.grabclipboard()
            if image is None:
                raise ValueError("No image found on clipboard.")

            image.save(save_path, "PNG")
            print(f"Image saved to: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            print(f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardImageSaverApp(root)
    root.mainloop()
