# Clipboard Image Saver

<p align="center">
  <img src="docs/Ico_ClipboardImageSaverApp.png" alt="Application Icon" width="128"/>
</p>

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


## Use Cases

### 1. Instant Screenshots
This is the classic workflow. It turns saving a screenshot into a simple two-click action.

1.  **Snip:** Use the Windows Snipping Tool (`Win` + `Shift` + `S`) to capture any part of your screen.

    <img src="docs/ClipboardExample.png" alt="Example of a snipped image" width="400"/>

2.  **Save:** Click the **Insta-Save** button on the app.

    <img src="icon_dwnld.png" alt="Download Icon">

3.  **Done:** The image is instantly saved with a timestamped filename in your chosen 'Insta-Save' folder (defaults to Downloads).


### 2. Affinity Photo / Photoshop

![Affinity Photo](docs/Affinity.png)
![NiceCat](docs/NiceCat.png)

^ I want ^ this specific layer to be saved as it's own file.

I can simply select it in Affinity Photo >> Ctrl+C to copy >> click the app's download button and...

![In The Downloads](docs/InTheDownloads.png)

TADAA!! The layer is immediately saved as a new, perfectly cropped PNG file.
> **Important Note:** The saved image will have the exact resolution as it appears on your canvas. If you copy a 100x100 pixel layer, you get a 100x100 pixel PNG. This is perfect for exporting assets for web or app development.