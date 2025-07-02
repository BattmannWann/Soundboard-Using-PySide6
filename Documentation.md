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
    3.9 sounddevice
    3.10 soundfile
    3.11 shutil
    3.12 numpy
    3.13 mutagen
    3.14 getpass

4. General Code

    4.1 Lines ... - ... in tower_of_babel2.py
    4.2 settings.json
    4.3 python_testing.py
    4.4 requirements.txt
    4.5 media/
    4.6 sounds/
    4.7 trimmed_sounds/


5. How to run the soundboard using the Command Line Interface (CLI)

    5.1 Initialisation/Requirements
    5.2 Setup


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

#### 2.1.1 __init__(main_app)

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
    This has been stored in a variable called `main_app`. **The argument passed is also called main_app**


#### 2.1.2 save()

This method implements the functionality for saving the currently entered settings when a user presses the save button mentioned above. It does this in two ways:

    1. In `main_app` there is a dictionary that stores the application's settings called `settings`. Rather than constantly reading from a file, the application reads from the JSON file on opening and any changes while using the app modify the `settings` dictionary. This means that the application can change its settings dynamically and efficiently, avoiding repeated reads from a file.   

    2. These changes are written to a JSON file such that the next time the application is run, the settings have been made retainable. A call will be made by calling the main application's method `main_app.save_settings()` which will be elaborated in ***2.3.8***. 

After such, a window is then presented to the user to assert that the changes have been successful; if they haven't, then since these operations have been wrapped in a "try-except" block then the exception will open a notification window to address this and to provide an error message.

To prevent error, the user may press save without changing any settings, where the app will simply do nothing when no changes have been made. 


#### 2.1.3 closeEvent(event)

This method is an override of PySide6's closeEvent() method defined for its classes (specifically this is for the QWidget class). This provides additional control over what the system should do when a window is closed. Default `closeEvent()` will handle the control back over to the main window (or to whatever window it's predecessor was when looking at the stack chain). 

Here, it is configured to ensure that the main window is re-shown as once it is hidden it needs to be explicitly called with `.show()`. It then calls the super class (QWidget) and calls its `closeEvent()` method such that the original functionality is then implemented correctly. This is achieved using the passed in argument `event` which ensures that the main method version closes the correct event occurrence. 


### 2.2 Methods in the EditFiles Class

#### 2.2.1 __init__(main_app)

This constructor takes in as an argument `main_app` which is the reference to the `MainWindow` instance. 

The constructor for this class hides the main application's window and then displays another. This other window is contained within a grid layout that features a scrollable area for when the sounds get larger than the amount that can be displayed within the 1300 x 800 window. Displaying the sounds available are handled by the class' `load_sound_options()` function. 

The reason that this logic has been abstracted is such that when sounds are modified these changes are reflected in the window. Simply, the method can be called again whenever a change has been made. 

The only other notable segment of this method is the `button_to_options_mapping()` variable. This is a dictionary that maps each sound to its corresponding option buttons as seen on screen. This is updated at the loop found in the `load_sound_options()` method. 


#### 2.2.2 closeEvent(event)

This is implemented in the same way as it is in Settings (see 2.1.3).


#### 2.2.3 load_sound_options()

This is the main method of this class that loads all sounds available in the sound board, listing:

    - Their associated emoji/picture
    - The duration of the sound
    - Options for each sound; deletion, renaming, and editing the duration

As such the table headings are **Emoji**, **Name**, **Duration** and **Options**.

The sounds are formatted into a table, which has been achieved by using a grid layout. FIrstly, this method determines whether the grid has been initiated, if so, it removes any widgets found. This functionality has been implemented to account for changes to the sound options; every time there is a deletion, a change of name, or change of length, the window needs to correctly display the amendments. However, with so many elements, it becomes hard to update accordingly as this would require locating the widget within the grid and updating its contents. In solving this problem, this method was the easiest and most efficient way to ensure that the table remains up to date. 

The sounds themselves have been placed into a scrollable area to ensure that the space is used wisely. 

Another notable section here are the vertical and horizontal line separators. Unfortunately, the same widget cannot be added to a layout more than once, and thus, more than one variable has to be created. To ensure that the DRY principle has been adhered to, the creation of vertical and horizontal separators was abstracted into a method that returns the appropriate widget. These variables ensure that the table structure is made visible to the user, aiding in readability. 

The for loop utilises a dictionary from the main app which contains records of every sound available in the application. Each key corresponds to the name of a sound and its values holding the relevant information; in this case all it needs is the sound's duration. 

In every iteration a remove, rename, and edit button are created and added to the current row. To ensure that each sound is mapped correctly to each button, this is where the `button_to_options_mapping` dictionary comes into play. 

Lastly, to appropriately add each widget in the correct grid line, there is an iterated variable `curr_grid` which increments in each iteration. This is simple, but ensures that each widget is placed on a different line each time. 


#### 2.2.4 create_vertical_separator()

This widget comes from `QFrame()` which can be customised to set orientation, shadow and colour accoridngly. To stretch the frame over all the columns, in `load_sound_options()` the `addWidget()` method which is apart of the layout allows for negative indices that indicate it should stretch over the whole layout space. Each vertical separator has been placed accordingly between each widget, orientated using the `alignment` argument. 


#### 2.2.5 create_horizontal_separator() 

This widget is implemented the exact same way as 2.2.4 but in `.setFrameShape()` QFrame.HLine is used instead of QFrame.VLine. It is implemented in the same way into the layout as well. 


#### 2.2.6 delete_sound(name)

This method takes in as an argument the name of the sound such that any reference required uses the correct name, without additional calls being made; the title of the window uses the sound's name, for instance. 

This method implements the functionality for the delete button, found in the options section. When clicked on, the user is immediately greeted with a warning pop-up, prompting the user to confirm that they actually want to delete the sound. If so, they need to press "Yes". This uses the operating system to remove the sound from the folder, wrapped in a try-except block to ensure that if any errors occur the user is prompted and given an appropriate error message to explain why. 


#### 2.2.7 rename_sound(name)

Takes in the name of the sound as an argument. This ensures that any reference for the name of the sound is correct. 

This method opens another window, that allows the user to enter the new name they wish to provide for the given sound. As before, if the user presses save without entering anything into the text box, then the sound remains unchanged. This is the same if the user presses cancel. **Only** if the user enters valid text and presses save will the sound be renamed. 

This logic is again wrapped in a try-except block to ensure that if any errors occur, the user is informed accordingly. 

The save logic is detailed in the method `save_rename()`.


#### 2.2.8 save_rename(original)

This method takes in as an argument the original name for the sound, such that the following is possible:

    The path of the sound is retrieved from the main app's `sound_buttons` dictionary, such that the operating system can correctly identify the sound and rename it on the system itself. This ensures that the change is permanent. 

On a successful or unsuccessful operation, the user is prompted by a pop-up box to inform them accordingly, as the logic is wrapped within a try-except block. 

On a successful operation, both the `main_app.load_sounds()` and `load_sound_options()` methods are called to ensure that the application then displays the changes everywhere. 

The rename window is then closed at the end. 


#### 2.2.9 edit_sound_length(name, duration)

The taken arguments are name (to ensure the sound can be referenced) and duration to display appropriately the duration of the sound (along with constraints on how the length of the sound can be changed).

This method creates a new window to display the name of the sound the user is editing, and a double handled slider to allow the user to select the segment of the sound they want to keep. 

After adjusting the sliders, the user can preview the segment of the sound they have selected. 

On pressing save, the sound is saved as a copy to ensure that if the user later wants to revert the sound back to its original state then this is made possible. This logic is handled by creating a sound with the same name into the `trimmed_sounds/` directory. When the logic in the main application iterates over the sounds directory, it will first check if the sound with the same name exits in `trimmed_sounds/`. If so, then this version takes priority and is loaded in instead. This however, only happens on application start. To ensure that the changes take immediate effect, the path value is modified for the key of the sound in the `main_app.sound_buttons` dictionary. This will make more sense as to why when understanding the logic of `2.3.3` and of `2.3.9`. 

Before loading the window, the sound is checked to be lesser than one second. If it is, then a warning pop-up box is displayed to the user to inform them that editing a sound that is less than one second is prohibited as there are not enough audio frames to perform such an action - it doesn't make much sense as the user wouldn't get much benefit from it. 

If the sound's duration is greater than one, then the slider step is set to 0.1s and the range of the slider set from 1.0s to the duration of the sound. 

To revert the sound back to its original, the revert button can be found in this same window. 


#### 2.2.10 length_slider_val_changed(value)

As an argument, the value is passed by the `.connect` method to ensure proper handling. 

This method implements the logic that whenever the slider is changed the value in the label to indicate where the audio segment is, is changed. This value is rounded to 2 decimal places as any further are irrelevant to the user. 


#### 2.2.11 preview_sound(name, slider)

This method takes the name of the sound and the slider object instance as arguments. The name ensures that the sound can be referenced and found properly, and the slider object instance ensures that its current values can be obtained. 

The method also contains a doc string to explain some of the more complicated logic that may not be clear on first glance. To avoid wasting time, here is the information presented:

``` 

    Each sound has been stored as a numpy array. This, using this knowledge we can splice the sound array to edit its length as follows:
        
        - Each row in the data array is ONE AUDIO FRAME.
        - The number of frames per second is determined by the SAMPLERATE
        - Thus, to trim our audio, we do 
            
            trimmed_length = samplerate * number_of_seconds
            trimmed_data = data[:trimmed_data]
                
        - So, if we want the first 5 seconds, substitute 'number_of_seconds' with 5. 
            
        - Here, we have a double handled slider, so we can splice using a start and stop value
            
            trimmed_start = samplerate * handle_1
            trimmed_end = samplerate * handle_2
                
            trimmed_sound = data[trimmed_start:trimmed_end]

```

Contained within this method is additional logic to disable the buttons present on the window, such that when the sound is playing, the logic doesn't try and subsume the current actions. This prevents errors from occurring also. 

This method doesn't actually play the sound however, and simply serves as a support function to avoid errors and aid `trim_sound()`. 


#### 2.2.12 trim_sound(name, slider)

This method takes as arguments name, and slider which have been explained in `preview_sound()` and have been taken directly from this method. This is where the logic described in the docstring of `preview_sound()` is implemented, and if the preview sound button has been pressed, then the audio will be played as part of this function. 

This decision was taken to prevent repetition of code. To play the sound, the data needs to be spliced, and to save the modification of the sound the data also needs to be sliced. This is where the `previewed` variable flag initialised in `edit_sound_length()` becomes relevant. If it is set to true, then preview sound has been pressed and the sound needs to be played. Otherwise, the data just needs to be spliced. 

Once the data has been spliced, it is saved in the `trimmed_sounds` dictionary found in `edit_sound_length()`. This way, if the user decides to save the modified version of the sound, then the data is there to be written. Otherwise, when the method exits, the data is lost, ensuring memory space is not being wasted. 


#### 2.2.13 save_length(name)

Takes as an argument the name of the sound to ensure proper referencing of the sound being modified. 

This method prompts the user with a pop-up box to refer the state of the operation. If successful or not, the user will be greeted with the appropriate information depending on the outcome. This is handled by a try-except block. 


#### revert_sound(name)

This method takes in as an argument the name of the sound to ensure that proper referencing and finding of the sound is possible. 

Under a try-except block, the user will be prompted with a success or failure method depending on successful/unsuccessful operation. 

On a successful operation, the sound is found in the `trimmed_sounds/` directory and deleted. Then, the main application window and the edit files window sound options are updated to reflect this change. 


### 2.3 Methods in the MainWindow Class

#### 2.3.1 __init__()

This is the core of the application. The constructor essentially sets up the entire application. To ease reading, here is what is achieved (within relevance):

    - The settings are retrieved from the `settings.json` file and stored in the `settings` dictionary; ONLY IF `settings.json` exists, otherwise a set of default settings are stored in the dictionary instead. 

    - The username of the user is retrieved using `getpass` and stored in the settings dictionary.

    - The overall layout used is a box layout, that contains a grid, and a scroll area within the grid. This allows a layout hierarchy. 

    - The sounds are loaded and formatted correctly using the `load_sounds()` method (see 2.3.3)

    - The toolbar is created and relevant buttons associated with the methods to implement them

    - The appearance of the window is also configured here (window title, size, visual separators, etc...)


#### 2.3.2 set_volume(value)

The argument passed here, value, is the value of the slider at the point in time that it has been moved (if the slider was moved to value 50, then 50 is passed into the method). This logic is used whenever a change is detected. 

The volume value is stored in the settings dictionary. The value stored is divided by 100 as the logic to actually change the volume of a sound requires the value to be a fraction. To see what actually happens, see `2.3.9`

As the sounds are being modified directly, the `load_sounds()` method needs to be called such that when the sound is played, the desired outcome is achieved. 


#### 2.3.3 load_sounds()

This method initialises by clearing all sounds in the grid at that moment. This is to implement any changes made to the sounds during the run-time of the application. 

Next, if the directory to hold the sounds doesn't exist, then it is created by the app, and an appropriate display message is shown to the user to prompt them to add sound files using the `add_files` button in the toolbar. Similar logic is used when there are no files in the directory. The directory could have been created, but if the application is restarted, then the same message needs to be displayed to the user. 

The for loop of this method initialises/formats all of the sound files. It achieves the following:

    - Creates the name of the sound file by splitting the relative path and taking only the first part (for example of a file called 'Sound.mp3', the name is then 'Sound')

    - If the name of the file exists in the `trimmed_sounds` directory, then this version is used over the original (due to the request of the user modifying the sound's duration)

    - Other details of the file are then collated; this includes duration, and an image

    - A button is created for the sound, placing on it the name of the sound (up to a maximum of 40 characters for space reasons) and is associated with the appropriate data for its method; the path of the sound, and the volume of the sound is passed through to the method on creation, such that when it is called, the information is already there. 

    - The button is then placed on the grid in groups of two

    - Lastly, a record of the button is stored in the `sound_buttons` dictionary. This dictionary has the following values: `path`, `emoji_path`, and `duration`.



#### 2.3.4 add_files()

This implements the functionality of adding files to the soundboard. It does this by utilising the file browser of the device, allowing the user to add multiple files at once. However, it is restricted to `.mp3` and `.wav` files only. 

After any files have been added, the `load_sounds()` method is then called to display the added files to the soundboard. 


#### 2.3.5 edit_files()

This links the edit files button on the toolbar to its relevant class. This will create the class object and show the window the the user. The rest of the implementation details can then be found following section `2.2`.


#### 2.3.6 settings_config()

This links the settings button on the toolbar to its relevant class. This will create the settings class object and then show the window to the user. The rest of the implementation details can then be found in section `2.1`


#### 2.3.7 stop_sounds()

This method implements the logic for the `Stop Sounds` button found in the toolbar. 

This will simply stop playing any sound that is currently playing at that moment in time. 


#### 2.3.8 save_settings()

This method allows the settings altered by the user to be written to the json file for permanence. 

If there is an issue when this method is called, the user is greeted with an error pop-up box with relevant error details. 


#### 2.3.9 play_sound(path, volume_level = 1.0)

Passed to this method is the path for the sound and the volume level for said sound (by default this is set to full volume if no preference exists). 

This method is implemented through a sub-method within it, called `_play`. 

To have the sound play both through the default input and output, this function utilises threads, which is why there is a need of a sub-method. When each thread is called, `_play` is executed. 

`_play`'s logic is wrapped within a try-execute block that will produce an error message if something goes wrong. This is useful to let the user know that there has been a problem with playing a sound through one of their chosen audio channels. 


#### 2.3.9 closeEvent(event)

Like the previous `closeEvent()` overrides, this method is passed the relevant event such that after any personalisation is achieved, the real method handles the closing logic properly. 

The addition here is that when the main window is closed, any sound that is currently playing is stopped. 


---

## 3. Imports and Libraries

This section will go into detail on the libraries and imports that have been chosen. It will not, however, teach how to use these  libraries, this section is for the sole intent of informing a developer which have been used such that they can become familiar with the system and research that of which they do not know. 

To begin with, the most important library used in this application is PySide6. PySide6 is a modern Python GUI library that is build on the foundations of the C++ library Qt. 


### 3.1 PySide6.QtCore
This module provides core non-GUI functionality used by PySide6 applications, such as timers, signals and slots, file handling, and date/time utilities. It is used for handling lower-level tasks and application logic that doesn't involve direct user interface elements. 

In this case, the application requires methods [QSize](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QSize.html#more) and [Qt](https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html). 


### 3.2 PySide6.QtGui
This module contains classes for windowing system integration, 2D graphics, basic imaging, fonts, and input events. It's responsible for handling icons, key events, and rendering graphics within the app.

The application imports [QAction](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QAction.html), [QIcon](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QIcon.html), [QPixmap](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPixmap.html), [QIntValidator](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QIntValidator.html)


### 3.3 PySide6.QtWidgets
This is the main module used for building the graphical user interface. It contains the various UI components such as windows, buttons, labels, sliders, and layouts used to construct the application's interface.

This is the largest and most foundational import. These will be listed but only the overall [Widgets](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/) link will be provided here.

The imports are: 

    - QApplication
    - QCheckBox
    - QLabel
    - QMainWindow
    - QStatusBar
    - QToolBar
    - QWidget
    - QVBoxLayout
    - QHBoxLayout
    - QGridLayout
    - QPushButton
    - QFileDialog
    - QMessageBox
    - QComboBox
    - QScrollArea 
    - QSlider
    - QLineEdit
    - QFrame


### 3.4 superqt
This is an extended Qt widgets package that includes advanced and customizable components that go beyond the standard PySide6 offerings. For example, it includes the QRangeSlider, which allows users to select a range rather than a single value on a slider — a feature used in this application. 

See the relevant documentation online [here](https://pypi.org/project/superqt/).


### 3.5 sys
The sys module is used to access system-specific parameters and functions. In this application, it may be used to handle command-line arguments or to exit the application safely.


### 3.6 os
The os module provides a portable way of interacting with the operating system. It is used for file and directory management, environment information, and checking system paths. It plays a key role in accessing, creating, and modifying files and folders.


### 3.7 json
The json module is used for parsing and writing JSON files. This is commonly used in the application to save and load settings such as volume or user-specific configurations.


### 3.8 threading
The threading module is used to run background tasks concurrently with the main application. This is important in GUI applications to ensure the interface remains responsive while long-running tasks (like sound playback or file operations) are being processed.


### 3.9 sounddevice
This module is used to play and record sound using NumPy arrays. It allows low-latency interaction with audio devices and is essential for real-time sound playback in the application.


### 3.10 soundfile
soundfile provides support for reading and writing sound files. It is used in conjunction with NumPy to load audio data into memory for processing or slicing.


### 3.11 shutil
This module offers high-level file operations such as copying and deleting files. It is used when the user moves, renames, or removes files within the soundboard directory.


### 3.12 numpy
NumPy is used for numerical operations, especially for manipulating audio data loaded from files. It enables slicing, analysing, and modifying sound waveforms in array format. 


### 3.13 mutagen
Mutagen is a Python module to handle audio metadata. It is used in this application to extract information such as sound duration, file tags, or encoding details for sound files like MP3 or WAV.

As this is not a common import, see more details [here](https://mutagen.readthedocs.io/en/latest/user/gettingstarted.html).


### 3.14 getpass
The getpass module is used to securely retrieve the current user's login name. In this application, it is to simply retrieve the user's username. 

---

## 4. General Code

This section is to cover any small segments of code/files that have not been handled by the previous sections. This section will be relatively small, but it is important to cover all bases. 


### 4.1 Lines ... - ... in tower_of_babel2.py

These lines are in the general scope of the program, which in a class based application such as this one, it may be referred to as the main program. 

Here, the main application is initialised, creating a `MainWindow` instance and then executing the application to run and display it on the host's machine. 


### 4.2 settings.json

This file is responsible for the data permanence of user preference. Whenever a user alters a system setting, the configuration is stored in this file. 

When read in python, this is converted to a dictionary with the following keys:

    - volume
    - default_input_info
    - default_output_info
    - default_output
    - default_input
    - username


### 4.3 python_testing.py

This file is kept simply for testing purposes. Sometimes when testing out a new feature it is much simpler to extract out the logic and test it on a small scale before integration. I will keep this file such that if another developer decides to develop the application further, a testing file already exists. 

Therefore, this is solely a file for convenience. 


### 4.4 requirements.txt

This project has been configured to support the use of a virtual environment. Therefore, this text file contains all requirements for the application to run. 


### 4.5 media/

The `media/` directory contains ALL images/icons used in the application. 


### 4.6 sounds/

The `sounds/` directory holds ALL sound files used in the application. Whenever the user uploads sound files, this is where they are stored. 


### 4.7 trimmed_sounds/

This directory holds any sounds that have been modified in length. This allows the user to easily revert back to the original sound's duration, without having to modify the original sound whatsoever. This helps maintain data integrity.


---

## 5. How to run the soundboard using the Command Line Interface (CLI)

### 5.1 Initialisation/Requirements

The following is a list of prerequisites before continuing:

    - Git has been installed successfully on your machine

    - There is a suitable version of Python that has been installed. For this application Python version 3.10+ is advised. 

    - pip installer is present and usable on your machine. This can often be bundled together when using Python's install wizard

    - When installing Python using the Wizard, make sure it is added to your PATH variable for the system.

    - You are somewhat familiar with your machines terminal interface and commands. Extensive or expert knowledge is NOT required however.

    - For editing any files, an appropriate IDE should be installed (this is entirely up to the developer of course, vim is applauded). Recommended choice is VS Code.

Once the above has been confirmed/resolved, you may continue.

Before running the application, it is strongly advised that a virtual environment (venv) is created before execution. 

To do this depends on the environment that you are using. Likely, is that this is a wWindows machine, so the following will explain how to achieve this for Windows. For other operating systems, I recommend researching how to create a python virtual environment.


### 5.2 Setup

Steps:

    1. Open your favourite terminal (I recommend the installing the [Windows terminal app](https://apps.microsoft.com/detail/9N0DX20HK701?hl=en-us&gl=GB&ocid=pdpshare) as this is a convenient way to manage different kinds of terminals in one place)

    2. Navigate to the directory that you wish to download and work on the project in. Recommendation: Use something along the lines of `C:\Users\username\Documents\Projects...`

    3. Then, clone the repository using git, e.g.

        ```bash
        > git clone https://github.com/BattmannWann/Soundboard-Using-PySide6.git
    
        ```

    4. Then move into the cloned project directory 

        ```bash
        cd Soundboard-Using-PySide6
        ```

    5. Create the Python virtual environment in this directory:

        ```bash
        python -m venv venv

        ```

    6. On successful creation, you should then be able to execute the following to activate the environment:

        ```bash
        .\venv\Scripts\activate
        ```

    7. Next, navigate into the `Soundboard/` directory and install the project's requirements into the virtual environment using pip:

        ```bash
        cd Soundboard\
        pip install -r .\requirements.txt
        ```

    8. Now, you should be able to run the application as follows:

        ```bash
        python .\tower_of_babel2.py
        ```

If there are any issues with these steps, then ensure to consult your terminal as it will instruct you what is wrong. If there are any ambiguities, Google and ChatBots can be very helpful in solving discrepancies. 





