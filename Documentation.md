# Documentation for Soundboard

### Written and Maintained by Rhys Stewart

---

## Preface

While the code itself does follow the "self-documenting" convention laid out by professional software standards, the following will provide an in-depth overview of each
segment of the codebase, such that any possible discrepancy or misunderstanding is covered. 

Since the codebase is quite large, I feel it important to have produced this document to help lessen the load. Having to read thousands of lines of code is very cumbersome, 
even if the code is well written. 

---


## What to expect

The documentation will provide detailed discussion over:

    - Each Class
    - Each method within each class
    - Each import and library used
    - How to run the soundboard using the CLI

Regarding how to use the soundboard itself, please refer to the [User Guide](). 

I will format this documentation such that you may use the links provided in the contents section to navigate through this document quickly. Copies of this may also be found in the wiki, however, I myself find it useful to have a copy in the code. 

---

## Contents

1. Classes

    1.1 Settings
    1.2 EditFiles
    1.3 MainWindow

2. Methods

    2.1 Methods in class Settings

        2.1.1 __init__()
        2.1.2 save()
        2.1.3 closeEvent()

    2.2 Methods in class EditFiles

        2.2.1 __init__()
        2.2.2 closeEvent()
        2.2.3 load_sound_options()
        2.2.4 create_vertical_separator()
        2.2.5 create_horizontal_separator()
        2.2.6 delete_sound()
        2.2.7 rename_sound()
        2.2.8 save_rename()
        2.2.9 edit_sound_length()
        2.2.10 length_slider_val_changed()
        2.2.11 preview_sound()

    2.3 Methods in class MainWindow

        2.3.1 __init__()
        2.3.2 set_volume()
        2.3.3 load_sounds()
        2.3.4 add_files()
        2.3.5 edit_files()
        2.3.6 settings_config()
        2.3.7 stop_sounds()
        2.3.8 save_settings()
        2.3.9 play_sound()
        2.3.10 closeEvent()

3. Imports and Libraries

    3.1 PySide6.QtCore
    3.2 PySide6.QtGui
    3.3 PySide6.QtWidgets
    3.4 superqt
    3.5 sys
    3.6 os
    3.7 json
    3.8 threading
    3.9 pygame
    3.10 sounddevice
    3.11 soundfile
    3.12 shutil
    3.13 numpy
    3.14 mutagen
    3.15 getpass

4. General Code

    4.1 Lines ... - ... in tower_of_babel2.py
    4.2 settings.json
    4.3 python_testing.py
    4.4 requirements.txt
    4.5 media/
    4.6 sounds/


5. How to run the soundboard using the Command Line Interface (CLI)

    5.1 Initialisation/Requirements
    5.2 Setup
    5.3 Using the CLI to run the soundboard

---

## 1. Classes

### 1.1 Settings

The first class covered here is **Settings**. Settings, as the name implies, allows the user to customise the soundboard to a certain extent. This class is a subclass of QWidget, which gives it the abilities of `QWidget` and allows for personalisation. 

Settings allows the user to:

    - Change the default input (audio device such as headphones or a speaker) and output (microphone device) 
    - Change the default volume setting of sounds (this changes the actual volume of the sound and **NOT** the device volume)
    - Change the displayed username

Clicking on the settings button on the main window's toolbar will open a new window and close the main window. If the user wishes not to alter the settings, on closing the window, the main window will automatically reopen. This is the same for saving the settings but first a confirmation box appears to alert the user whether their changes have been successful or not; in an unsuccessful case the box should display a helpful error message.


### 1.2 EditFiles

EditFiles is also a subclass of `QWidget`.

This class allows the user to view all the sounds available in the soundboard, and do the following:

    - Edit the assigned emoji/picture
    - Remove the sound
    - Rename the sound
    - Edit the sound's length

The edit files button is also found on the main window's toolbar, and on clicking the button it will open a new window and close the main. Each sound is listed as part of a table, to aid readability. As before, closing this window will then automatically reopen the main window.


### 1.3 MainWindow

This class is the main body of the soundboard, which hosts the soundboard and toolbar for navigating to the settings, adding files, and editing files. Unlike the other classes, this class is instead a subclass of the `QMainWidget` class, which allows personalisation of the library's main window application class. 

The sounds are arranged in a scrollable box to allow the flow and design to not become cramped or too large. 

The window contains a section that greets the user and as part of the toolbar the user can change the volume of the sounds dynamically using the slider. To hear a sound, the user has to click on the button labelled with the name they are looking for. 

To handle use cases, when the main window is opened for the first time, the user will be greeted with a message stating that there are currently no sounds, and they must be added using the button in the toolbar. 



## 2. Methods

This section will go into explicit detail as to what each method within each class is implementing and achieving. This will help explain design choices and aid in debugging. 


### 2.1 Methods in the Settings Class

#### 2.1.1 __init__()

The class constructor initialises the settings window and closes the main window to prevent the screen from getting too crowded. In this initialisation, it will add the following to the screen:

    - Make the title of the window "Settings".

    - Create a main layout to add sub-layouts into; in this case the settings window opts for a grid layout.

    - Widgets are then added to the grid layout

    - The first row features a label detailing the dropdown box next to it is to select the default input audio device.

    - The second row features a label detailing the dropbox next to it is for the default output device.

    - The following row allows the user to alter the default volume setting for all of the sounds; labelled appropriately

    - The last row allows the user to change the username presented by the system. The username is collected by the getpass library and is the device's default username setting. 

    - A save button to allow the user to permanently change the application's settings. This is achieved through reading and writing to a JSON file called `settings.json`

    - To access the occurrence of MainWindow, it has been passed as an argument when creating the Settings class. This way any relevant variables and methods can be accessed and called. Thus, calling a method within the MainWindow class will appropriately make the changes required.
    This has been stored in a variable called `main_app`.


#### 2.1.2 save()

This method implements the functionality for saving the currently entered settings when a user presses the save button mentioned above. It does this in two ways:

    1. In `main_app` there is a dictionary that stores the application's settings called `settings`. Rather than constantly reading from a file, the application reads from the JSON file on opening and any changes while using the app modify the `settings` dictionary. This means that the application can change its settings dynamically and efficiently, avoiding repeated reads from a file.   

    2. These changes are written to a JSON file such that the next time the application is run, the settings have been made retainable. A call will be made by calling the main application's method `main_app.save_settings()` which will be elaborated in ***2.3.8***. 

After such, a window is then presented to the user to assert that the changes have been successful; if they haven't, then since these operations have been wrapped in a "try-except" block then the exception will open a notification window to address this and to provide an error message.

To prevent error, the user may press save without changing any settings, where the app will simply do nothing when no changes have been made. 


#### 2.1.3 closeEvent()

This method is an override of PySide6's closeEvent() method defined for its classes (specifically this is for the QWidget class). This provides additional control over what the system should do when a window is closed. Default `closeEvent()` will handle the control back over to the main window (or to whatever window it's predecessor was when looking at the stack chain). 

Here, it is configured to ensure that the main window is reshown as once it is hidden it needs to be explicitly called with `.show()`. It then calls the super class (QWidget) and calls its `closeEvent()` method such that the original functionality is then implemented correctly. 


### 2.2 Methods in the EditFiles Class

#### 2.2.1 __init__()

The constructor for this class hides the main application's window and then displays another. This other window is contained within a grid layout that features a scrollable area for when the sounds get larger than the amount that can be displayed within the 1300 x 800 window. Displaying the sounds available are handled by the class' `load_sound_options` function. 

The reason that this logic has been abstracted is such that when sounds are modified these changes are reflected in the window. Simply, the method can be called again whenever a change has been made. 

The only other notable segment of this method is the `button_to_options_mapping()` variable.



