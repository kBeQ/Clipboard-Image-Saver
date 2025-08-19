# Clipboard Image Saver

<p align="center">
  <img src="docs/Ico_ClipboardImageSaverApp.png" alt="Application Icon" width="128"/>
</p>

![Clipboard Example](docs/ClipboardExample.png)
A compact Windows utility built with Python and Tkinter to instantly save images from your clipboard.

![Application Screenshot](docs/app_screenshot.png)


## Features

-   **One-Click Insta-Save:** Instantly save the clipboard image to a predefined folder (defaults to Downloads).
-   **Save As... Dialog:** Standard save dialog for choosing a specific name and location.
-   **Persistent Settings:** Remembers your preferences and window position in a `ClipboardSaver.ini` file.
-   **Icon-Based UI:** Clean, compact interface with intuitive icons.
-   **Settings Menu:**
    -   "Always on Top" toggle.
    -   Set custom default folders for both "Save As" and "Insta-Save".


## Typical Workflow

The real power of this app is speed. It turns the multi-step process of saving a screenshot into a simple two-click action.

1.  **Snip:** Use the Windows Snipping Tool (`Win` + `Shift` + `S`) to capture any part of your screen.

    <img src="docs/ClipboardExample.png" alt="Example of a snipped image" width="400"/>

2.  **Save:** Click the **Insta-Save** button on the app.

3.  **Done:** The image is instantly saved with a timestamped filename in your chosen 'Insta-Save' folder (defaults to Downloads).


### Prerequisites
- Python 3.x
- `pillow` and `pyinstaller` libraries. You can install them using pip: