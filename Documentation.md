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

    - The purpose of the application
    - An overview of entire implementation
    - Each Class
    - Each method within each class
    - Each import and library used
    - How to run the soundboard using the CLI

***This is a non-exhaustive list, so please refer to the contents section for a more detailed summary.***

Regarding how to use the soundboard itself, please refer to the [User Guide](). 

I will format this documentation such that you may use the links provided in the contents section to navigate through this document quickly. Copies of this may also be found in the wiki, however, I myself find it useful to have a copy in the code. 

---

## Contents

1. Purpose of the Application

2. Implementation Overview

3. Classes

    3.1 Settings
    3.2 EditFiles
    3.3 MainWindow
    3.4 MultiDevicePlayer

4. Methods

    4.1 Methods in class Settings

        4.1.1 __init__()
        4.1.2 save()


    4.2 Methods in class EditFiles

        4.2.1 __init__()
        4.2.2 load_sound_options()
        4.2.3 create_vertical_separator()
        4.2.4 create_horizontal_separator()
        4.2.5 delete_sound()
        4.2.6 rename_sound()
        4.2.7 save_rename()
        4.2.8 edit_sound_length()
        4.2.9 length_slider_val_changed()
        4.2.10 preview_sound()
        4.2.11 trim_sound()
        4.2.12 save_length()
        4.2.13 revert_sound()
        4.2.14 change_emoji()
        4.2.15 remove_emoji()

    4.3 Methods in class MainWindow

        4.3.1 __init__()
        4.3.2 set_volume()
        4.3.3 get_duration()
        4.3.4 load_sounds()
        4.3.5 build_home_view()
        4.3.6 add_files()
        4.3.7 edit_files()
        4.3.8 settings_config()
        4.3.9 save_settings()
        4.3.10 closeEvent()

    4.4 Methods in class MultiDevicePlayer

        4.4.1 __init__()
        4.4.2 play_sound()
        4.4.3 _play_on_device()
        4.4.4 _match_channels()
        4.4.5 stop()

5. Imports and Libraries

    5.1 PySide6.QtCore
    5.2 PySide6.QtGui
    5.3 PySide6.QtWidgets
    5.4 superqt
    5.5 sys
    5.6 os
    5.7 json
    5.8 threading
    5.9 sounddevice
    5.10 soundfile
    5.11 shutil
    5.12 numpy
    5.13 mutagen
    5.14 getpass

6. General Code

    6.1 Lines 1166 - 1175 in tower_of_babel2.py
    6.2 settings.json
    6.3 python_testing.py
    6.4 requirements.txt
    6.5 media/
    6.6 sounds/
    6.7 unedited_sounds/
    6.8 button_images.json
    6.9 themes/
    6.10 fonts/


7. How to run the soundboard using the Command Line Interface (CLI)

    7.1 Initialisation/Requirements
    7.2 Setup


---

## 1. Purpose

The purpose of this application is to provide a soundboard alternative to the one provided by Discord. This application hosts all the main features provided by discord, and a few extras, such as:

    - **Adding sound files**: This can be done using the application, much like Discord. However, Discord limits users on the length of the sound you choose, whereas, this is not a limitation in the app. 

    - **Customising the Sounds**: Much like Discord, all the sounds can be renamed, given an emoji/icon, deleted, and trimmed (users can select a specific segment of the sound uploaded to be played). A difference in this application is that the whole sound can be used, with any segment being open to be chosen, along with the option to choose any image file for the sound itself. 

    - **Stopping Sounds**: Unlike in Discord, the sounds can be stopped (i.e. playback stops) by the user at any given time. 


---

## 2. Implementation Overview

The application has been developed using `PySide6` for the graphical user interface (GUI) and using a variety of libraries such as `sounddevice`, `os`, and `sys` to handle audio playback and the manipulation of the sound files.

The application has been developed in such a way that is uses "tabs" to navigate to each section, much like a modern application; i.e. the user presses a button, and the window navigates smoothly to a new page, without opening another window. This is handled by changing the `QMainWindow`'s, what is referred to as, **Central Widget**. Each new page of the application is an instance of a class, so when the user wants to look at, for example, the settings page, the `Settings` instance is loaded as the central widget. 

This means that every time a page is navigated to, the class rebuilds itself through its supplementary loading methods. This decision was taken as every time a change is made to the application, the changes are loaded dynamically and immediately. The instance stays singular, but it's main content reloaded. While this may have a larger overhead, this ensures the application stays up-to-date at any given time, to reflect user changes. At any given time, there is not a large quantity of data to load or manipulate regardless.


## 3. Classes

### 3.1 Settings

The first class covered here is **Settings**. Settings, as the name implies, allows the user to customise the soundboard to a certain extent. This class is a subclass of QWidget, which gives it the abilities of `QWidget` and allows for personalisation. 

Settings allows the user to:

    - Change the default output (audio device such as headphones or a speaker) and input (microphone device) 
    - Change the default volume setting of sounds (this changes the actual volume of the sound and **NOT** the device volume)
    - Change the displayed username

Clicking on the settings button on the main window's toolbar will change the central widget to a `Settings` class instance instead of the `MainWindow` instance. If any of the options presented are changed, the system will only maintain these changes after the user presses the save button. If there are no issues, the user will be presented with a success pop-up message; otherwise, the user is presented with an error message pop-up, the includes an appropriate error message to instruct the user on what the problem is. 


### 3.2 EditFiles

EditFiles is also a subclass of `QWidget`.

This class allows the user to view all the sounds available in the soundboard, and do the following:

    - Edit the assigned emoji/picture (either change it to a new one or remove it)
    - Remove the sound
    - Rename the sound
    - Edit the sound's length

The edit files button is also found on the main window's toolbar, which will change the central widget presented on the screen once pressed. Each sound is presented to the user in a table format, with appropriate headers and status tips to indicate what the user can do. 


### 3.3 MainWindow

This class is the main body of the soundboard, which hosts the soundboard and toolbar for navigating to the settings, adding files, and editing files pages. Unlike the other classes, this class is instead a subclass of the `QMainWidget` class, which allows personalisation of the library's main window application class. 

The sounds are arranged in a scrollable box to allow the flow and design to not become cramped or too large. 

The window contains a section that greets the user and as part of the toolbar the user can change the volume of the sounds dynamically using the slider. To hear a sound, the user has to click on the button labelled with the name they are looking for. 

To handle use cases, when the main window is opened for the first time, the user will be greeted with a message stating that there are currently no sounds, and they must be added using the button in the toolbar. 

An additional button that can be found on the toolbar is the `Stop Sound(s)` button, which will stop any current playback. The sound buttons can be pressed several times, with the sounds overlapping each other if so. 


### 3.4 MultiDevicePlayer

This class is used to abstract out the audio playback onto the devices. This way the threads are contained and managed in a single environment, allowing fine-tuning to how the threads are handled. 

It allows the audio to be formatted before playback and allows for instantaneous interruption of the threads if the user presses `Stop Sound(s)`.


## 4. Methods

This section will go into explicit detail as to what each method within each class is implementing and achieving. This will help explain design choices and aid in debugging. 


### 4.1 Methods in the Settings Class

#### 4.1.1 __init__(main_app)

This is the class constructor, which handles the following operations:

    - Make the title of the window "Settings".

    - Create a main layout to add sub-layouts into; in this case the settings window opts for a grid layout.

    - Widgets are then added to the grid layout

    - The first row features a label detailing the dropdown box next to it is to select the default output audio device.

    - The second row features a label detailing the dropbox next to it is for the default input device.

    - The following row allows the user to alter the default volume setting for all of the sounds; labelled appropriately

    - The last row allows the user to change the username presented by the system. The username is collected by the `getpass` library and is the device's default username setting. 

    - A save button to allow the user to permanently change the application's settings. This is achieved through reading and writing to a JSON file called `settings.json`

    - To access the occurrence of `MainWindow`, it has been passed as an argument when creating the Settings class. This way any relevant variables and methods can be accessed and called. Thus, calling a method within the MainWindow class will appropriately make the changes required.
    This has been stored in a variable called `main_app`. **The argument passed is also called main_app**


#### 4.1.2 save()

This method implements the functionality for saving the currently entered settings when a user presses the save button mentioned above. It does this in two ways:

    1. In `main_app` there is a dictionary that stores the application's settings called `settings`. Rather than constantly reading from a file, the application reads from the JSON file on opening and any changes while using the app modify the `settings` dictionary. This means that the application can change its settings dynamically and efficiently, avoiding repeated reads from a file.   

    2. These changes are written to a JSON file such that the next time the application is run, the settings have been made retainable. A call will be made by calling the main application's method `main_app.save_settings()` which will be elaborated in ***4.3.8***. 

After such, a window is then presented to the user to assert that the changes have been successful; if they haven't, then since these operations have been wrapped in a "try-except" block then the exception will open a notification window to address this and to provide an error message.

To prevent error, the user may press save without changing any settings, where the app will simply do nothing when no changes have been made. 


### 4.2 Methods in the EditFiles Class

#### 4.2.1 __init__(main_app)

This constructor takes in as an argument `main_app` which is the reference to the `MainWindow` instance. 

This page is contained within a grid layout that features a scrollable area for when the sounds get larger than the amount that can be displayed within the 1300 x 800 window. Displaying the sounds available are handled by the class' `load_sound_options()` function. 

The reason that this logic has been abstracted is such that when sounds are modified these changes are reflected in the window. Simply, the method can be called again whenever a change has been made. 

The only other notable segment of this method is the `button_to_options_mapping()` variable. This is a dictionary that maps each sound to its corresponding option buttons as seen on screen. This is updated at the loop found in the `load_sound_options()` method. 


#### 4.2.2 load_sound_options()

This is the main method of this class that loads all sounds available in the sound board, listing:

    - Their associated emoji/picture
    - Options to remove and / or set the emoji/picture
    - The duration of the sound
    - Options for each sound; deletion, renaming, and editing the duration

As such the table headings are **Emoji**, **Name**, **Duration** and **Options**.

The sounds are formatted into a table, which has been achieved by using a grid layout. Firstly, this method determines whether the grid has been initiated, if so, it removes any widgets found. This functionality has been implemented to account for changes to the sound options; every time there is a deletion, a change of name, or change of length, the window needs to correctly display the amendments. However, with so many elements, it becomes hard to update accordingly as this would require locating the widget within the grid and updating its contents. In solving this problem, this method was the easiest and most efficient way to ensure that the table remains up to date. 

The sounds themselves have been placed into a scrollable area to ensure that the space is used wisely. 

Another notable section here are the vertical and horizontal line separators. Unfortunately, the same widget cannot be added to a layout more than once, and thus, more than one variable has to be created. To ensure that the DRY principle has been adhered to, the creation of vertical and horizontal separators was abstracted into a method that returns the appropriate widget. These variables ensure that the table structure is made visible to the user, aiding in readability. 

The for loop utilises a dictionary from the main app which contains records of every sound available in the application. Each key corresponds to the name of a sound and its values holding the relevant information; in this case all it needs is the sound's duration. 

In every iteration a remove, rename, edit button, set icon, and remove icon buttons are created and added to the current row. To ensure that each sound is mapped correctly to each button, this is where the `button_to_options_mapping` dictionary comes into play. 

Lastly, to appropriately add each widget in the correct grid line, there is an iterated variable `curr_grid` which increments in each iteration. This is simple, but ensures that each widget is placed on a different line each time. 


#### 4.2.3 create_vertical_separator()

This widget comes from `QFrame()` which can be customised to set orientation, shadow and colour accoridngly. To stretch the frame over all the columns, in `load_sound_options()` the `addWidget()` method which is apart of the layout allows for negative indices that indicate it should stretch over the whole layout space. Each vertical separator has been placed accordingly between each widget, orientated using the `alignment` argument. 


#### 4.2.4 create_horizontal_separator() 

This widget is implemented the exact same way as 2.2.4 but in `.setFrameShape()` QFrame.HLine is used instead of QFrame.VLine. It is implemented in the same way into the layout as well. 


#### 4.2.5 delete_sound(name)

This method takes in as an argument the name of the sound such that any reference required uses the correct name, without additional calls being made; the title of the window uses the sound's name, for instance. 

This method implements the functionality for the delete button, found in the options section. When clicked on, the user is immediately greeted with a warning pop-up, prompting the user to confirm that they actually want to delete the sound. If so, they need to press "Yes". This uses the operating system to remove the sound from the folder, wrapped in a try-except block to ensure that if any errors occur the user is prompted and given an appropriate error message to explain why. 


#### 4.2.6 rename_sound(name)

Takes in the name of the sound as an argument. This ensures that any reference for the name of the sound is correct. 

This method opens another window, that allows the user to enter the new name they wish to provide for the given sound. As before, if the user presses save without entering anything into the text box, then the sound remains unchanged. This is the same if the user presses cancel. **Only** if the user enters valid text and presses save will the sound be renamed. 

This logic is again wrapped in a try-except block to ensure that if any errors occur, the user is informed accordingly. 

The save logic is detailed in the method `save_rename()`.


#### 4.2.7 save_rename(original)

This method takes in as an argument the original name for the sound, such that the following is possible:

    The path of the sound is retrieved from the main app's `sound_buttons` dictionary, such that the operating system can correctly identify the sound and rename it on the system itself. This ensures that the change is permanent. 

On a successful or unsuccessful operation, the user is prompted by a pop-up box to inform them accordingly, as the logic is wrapped within a try-except block. 

On a successful operation, both the `main_app.load_sounds()` and `load_sound_options()` methods are called to ensure that the application then displays the changes everywhere. 

The rename window is then closed at the end. 


#### 4.2.8 edit_sound_length(name, duration)

The taken arguments are name (to ensure the sound can be referenced) and duration to display appropriately the duration of the sound (along with constraints on how the length of the sound can be changed).

This method creates a new window to display the name of the sound the user is editing, and a double handled slider to allow the user to select the segment of the sound they want to keep. 

After adjusting the sliders, the user can preview the segment of the sound they have selected. 

On pressing save, the sound is moved to another directory to ensure that if the user later wants to revert the sound back to its original state then this is made possible. This logic is handled by first moving the sound into the `unedited_sounds/` directory, and then placing the modified sound in its place into the `sounds/` directory. 

To ensure that the changes take immediate effect, the path value is modified for the key of the sound in the `main_app.sound_buttons` dictionary. This will make more sense as to why when understanding the logic of `3.3.3` and of `3.3.9`. 

Before loading the window, the sound is checked to be lesser than one second. If it is, then a warning pop-up box is displayed to the user to inform them that editing a sound that is less than one second is prohibited as there are not enough audio frames to perform such an action - it doesn't make much sense as the user wouldn't get much benefit from it. 

If the sound's duration is greater than one, then the slider step is set to 0.1s and the range of the slider set from 1.0s to the duration of the sound. 

To revert the sound back to its original, the revert button can be found in this same window. 


#### 4.2.9 length_slider_val_changed(value)

As an argument, the value is passed by the `.connect` method to ensure proper handling. 

This method implements the logic that whenever the slider is changed the value in the label to indicate where the audio segment is, is changed. This value is rounded to 2 decimal places as any further are irrelevant to the user. 


#### 4.2.10 preview_sound(name, slider)

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


#### 4.2.11 trim_sound(name, slider)

This method takes as arguments name, and slider which have been explained in `preview_sound()` and have been taken directly from this method. This is where the logic described in the docstring of `preview_sound()` is implemented, and if the preview sound button has been pressed, then the audio will be played as part of this function. 

This decision was taken to prevent repetition of code. To play the sound, the data needs to be spliced, and to save the modification of the sound the data also needs to be sliced. This is where the `previewed` variable flag initialised in `edit_sound_length()` becomes relevant. If it is set to true, then preview sound has been pressed and the sound needs to be played. Otherwise, the data just needs to be spliced. 

Once the data has been spliced, it is saved in the `trimmed_sounds` dictionary found in `edit_sound_length()`. This way, if the user decides to save the modified version of the sound, then the data is there to be written. Otherwise, when the method exits, the data is lost, ensuring memory space is not being wasted. 


#### 4.2.12 save_length(name)

Takes as an argument the name of the sound to ensure proper referencing of the sound being modified. 

This method prompts the user with a pop-up box to refer the state of the operation. If successful or not, the user will be greeted with the appropriate information depending on the outcome. This is handled by a try-except block. 


#### 4.2.13 revert_sound(name)

This method takes in as an argument the name of the sound to ensure that proper referencing and finding of the sound is possible. 

Under a try-except block, the user will be prompted with a success or failure method depending on successful/unsuccessful operation. 

On a successful operation, the sound is found in the `trimmed_sounds/` directory and deleted. Then, the main application window and the edit files window sound options are updated to reflect this change. 


#### 4.2.14 change_emoji(name, emoji)

This method provides the functionality to change the emoji for a particular sound. This will prompt the user with the device's file explorer, to allow them to choose a file. 

This is wrapped in a try-except block to ensure that if the operation is or isn't successful, the user is notified with a pop-up box to convey the appropriate message. 

The images are stored in a JSON file called `button_images.json` such that the images are retained and reloaded on an application close and restart. This functionality is handled by the main application's `save_icons()` function.


#### 4.2.15 remove_emoji(name)

This method will provide the user the ability to remove any image set for a sound. If one is not already set, a pop-up message will inform the user of this. There are also pop-up boxes for a successful or unsuccessful removal.

To ensure each entry in the table features the same spacing, what this function actually does is replace the emoji with a placeholder which is the same colour as the background. 


### 4.3 Methods in the MainWindow Class

#### 4.3.1 __init__()

This is the core of the application. The constructor essentially sets up the entire application. To ease reading, here is what is achieved (within relevance):

    - The settings are retrieved from the `settings.json` file and stored in the `settings` dictionary ONLY IF `settings.json` exists, otherwise a set of default settings are stored in the dictionary instead. 

    - The username of the user is retrieved using `getpass` and stored in the settings dictionary.

    - The overall layout used is a box layout, that contains a grid, and a scroll area within the grid. This allows a layout hierarchy. 

    - The sounds are loaded and formatted correctly using the `build_home_view()` method, which inside calls `load_sounds()`.

    - The toolbar is created and relevant buttons associated with the methods to implement them

    - The appearance of the window is also configured here (window title, size, visual separators, etc...)

    - The class which handles sound playback is created here, such that it can be referred to at any point (as it is created as a class member)



#### 4.3.2 set_volume(value)

The argument passed here, `value`, is the value of the slider at the point in time that it has been moved (if the slider was moved to value 50, then 50 is passed into the method). This logic is used whenever a change is detected. 

The volume value is stored in the settings dictionary. The value stored is divided by 100 as the logic to actually change the volume of a sound requires the value to be a fraction. To see how it is used, see `4.4.2`.

As the sounds are being modified directly, the `load_sounds()` method needs to be called such that when the sound is played, the desired outcome is achieved. 


#### 4.3.3 get_duration(path, file)

This helper function takes in the path of the sound and returns the sound's duration, rounded to 2 decimal places. If there are any issues in retrieving this information, the duration is set to `None` and the calling method handles the logic from there. 


#### 4.3.4 load_sounds()

Firstly, if the directory to hold the sounds doesn't exist, then it is created by the app, and an appropriate display message is shown to the user to prompt them to add sound files using the `add_files` button in the toolbar. Similar logic is used when there are no files in the directory as the directory could have been created, but if the application is restarted, then the same message needs to be displayed to the user. 

The for loop of this method initialises/formats all of the sound files. It achieves the following:

    - Creates the name of the sound file by splitting the relative path and taking only the first part (for example of a file called 'Sound.mp3', the name is then 'Sound')

    - Other details of the file are then collated; this includes duration, and an image

    - A button is created for the sound, placing on it the name of the sound (up to a maximum of 40 characters for space reasons otherwise the buttons can become quite messy) and is associated with the appropriate data for its method; the path of the sound, and the volume of the sound is passed through to the method on creation, such that when it is called, the information is already there. 


#### 4.3.5 build_home_view()

This method handles the logic for building and displaying the sounds grid on the home page. This has been abstracted out of the constructor as when information about the sounds, on indeed if the sounds themselves change, these changes can be reflected on a reload; simply, this function is recalled.

It does the following:

    - Sets the window's size

    - Creates the layouts, along with the widget storing all the content, which is placed inside the main layout inside a scroll area

    - Displays the welcome message to the user

    - Calls the `load_sounds()` method, which handles the creation of the buttons. 

    - Sets the *theme* of the window, by reading from a `.qss` file.


#### 4.3.6 add_files()

This implements the functionality of adding files to the soundboard. It does this by utilising the file browser of the device, allowing the user to add multiple files at once. However, it is restricted to `.mp3` and `.wav` files only. 

After any files have been added, the `load_sounds()` method is then called to display the added files to the soundboard. 


#### 4.3.7 edit_files()

This links the edit files button on the toolbar to its relevant class. This will create the class object and show the window the the user. The rest of the implementation details can then be found following section `3.2`.


#### 4.3.8 settings_config()

This links the settings button on the toolbar to its relevant class. This will create the settings class object and then show the window to the user. The rest of the implementation details can then be found in section `3.1`


#### 4.3.9 save_settings()

This method allows the settings altered by the user to be written to the json file for permanence. 

If there is an issue when this method is called, the user is greeted with an error pop-up box with relevant error details. 


#### 4.3.10 closeEvent(event)

This method is passed the relevant event such that after any personalisation is achieved, the real method handles the closing logic properly. 

The addition here is that when the main window is closed, any sound that is currently playing is stopped, using the `MultiDevicePlayer` class method `stop()`.



### 4.4 Methods class MultiDevicePlayer

#### 4.4.1 __init__()

The constructor for this class is rather small, initialising a stop thread variable called `stop_event`, and a list to store threads to be run, called `threads`.


#### 4.4.2 play_sound(path, devices, volume = 1.0)

This function handles gathering and manipulating the data for playback, and creates the threads required for playing through the input and output devices. The created threads are stored into `self.threads`.

The threads are given the target function `_play_on_device` which is responsible for actually playing the audio, and the corresponding arguments required for this function (which have been curated at the start of this function).


#### 4.4.3 _play_on_device(data, samplerate, device)

This function is responsible for playing the audio through the devices. This is handled by the `sounddevice`'s `OutputStream`.

As using threads and outputs can be erroneous, this logic has been wrapped in a try-except block, which will inform the user with a pop-up box if there are any issues on playback. 

The playback is handled by a while loop, which writes the data to the output stream. This way, if the user presses `Stop Sound(s)` (in the toolbar), the sound can be interrupted at any time. This is handled by an if-statement which will check if the `self.stop_event` has been set (i.e. the user has willed the sounds to stop using `Stop Sound(s)`). If it has been set, playback will stop immediately, otherwise the sound will continue to play until there is no more data to be written (this is why the break condition for the while loop is checking that the current index within the chunk of data to be written is less than the length of the data, otherwise there is no further data to be written).


#### 4.4.4 _match_channels(data, max_channels)

This function will down/up mix the audio to match the selected device's channels. If there are too many or too little, this will ensure that there are less errors produced in runtime. 


#### 4.4.5 stop()

This function signals all threads to stop playback by setting the `self.stop_event` using `.set()`.

---

## 5. Imports and Libraries

This section will go into detail on the libraries and imports that have been chosen. It will not, however, teach how to use these  libraries, this section is for the sole intent of informing a developer which have been used such that they can become familiar with the system and research that of which they do not know. 

To begin with, the most important library used in this application is PySide6. PySide6 is a modern Python GUI library that is build on the foundations of the C++ library Qt. 


### 5.1 PySide6.QtCore
This module provides core non-GUI functionality used by PySide6 applications, such as timers, signals and slots, file handling, and date/time utilities. It is used for handling lower-level tasks and application logic that doesn't involve direct user interface elements. 

In this case, the application requires methods [QSize](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QSize.html#more) and [Qt](https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html). 


### 5.2 PySide6.QtGui
This module contains classes for windowing system integration, 2D graphics, basic imaging, fonts, and input events. It's responsible for handling icons, key events, and rendering graphics within the app.

The application imports [QAction](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QAction.html), [QIcon](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QIcon.html), [QPixmap](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPixmap.html), [QIntValidator](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QIntValidator.html)


### 5.3 PySide6.QtWidgets
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


### 5.4 superqt
This is an extended Qt widgets package that includes advanced and customizable components that go beyond the standard PySide6 offerings. For example, it includes the QRangeSlider, which allows users to select a range rather than a single value on a slider — a feature used in this application. 

See the relevant documentation online [here](https://pypi.org/project/superqt/).


### 5.5 sys
The sys module is used to access system-specific parameters and functions. In this application, it may be used to handle command-line arguments or to exit the application safely.


### 5.6 os
The os module provides a portable way of interacting with the operating system. It is used for file and directory management, environment information, and checking system paths. It plays a key role in accessing, creating, and modifying files and folders.


### 5.7 json
The json module is used for parsing and writing JSON files. This is commonly used in the application to save and load settings such as volume or user-specific configurations.


### 5.8 threading
The threading module is used to run background tasks concurrently with the main application. This is important in GUI applications to ensure the interface remains responsive while long-running tasks (like sound playback or file operations) are being processed.


### 5.9 sounddevice
This module is used to play and record sound using NumPy arrays. It allows low-latency interaction with audio devices and is essential for real-time sound playback in the application.


### 5.10 soundfile
soundfile provides support for reading and writing sound files. It is used in conjunction with NumPy to load audio data into memory for processing or slicing.


### 5.11 shutil
This module offers high-level file operations such as copying and deleting files. It is used when the user moves, renames, or removes files within the soundboard directory.


### 5.12 numpy
NumPy is used for numerical operations, especially for manipulating audio data loaded from files. It enables slicing, analysing, and modifying sound waveforms in array format. 


### 5.13 mutagen
Mutagen is a Python module to handle audio metadata. It is used in this application to extract information such as sound duration, file tags, or encoding details for sound files like MP3 or WAV.

As this is not a common import, see more details [here](https://mutagen.readthedocs.io/en/latest/user/gettingstarted.html).


### 5.14 getpass
The getpass module is used to securely retrieve the current user's login name. In this application, it is to simply retrieve the user's username. 

---

## 6. General Code

This section is to cover any small segments of code/files that have not been handled by the previous sections. This section will be relatively small, but it is important to cover all bases. 


### 6.1 Lines 1166 - 1175 in tower_of_babel2.py

These lines are in the general scope of the program, which in a class based application such as this one, it may be referred to as the main program. 

Here, the main application is initialised, creating a `MainWindow` instance and then executing the application to run and display it on the host's machine. 

Additionally, the fonts used for the application are initialised here.


### 6.2 settings.json

This file is responsible for the data permanence of user preference. Whenever a user alters a system setting, the configuration is stored in this file. 

When read in python, this is converted to a dictionary with the following keys:

    - volume
    - default_input_info
    - default_output_info
    - default_output
    - default_input
    - username


### 6.3 python_testing.py

This file is kept simply for testing purposes. Sometimes when testing out a new feature it is much simpler to extract out the logic and test it on a small scale before integration. I will keep this file such that if another developer decides to develop the application further, a testing file already exists. 

Therefore, this is solely a file for convenience. Once the application is ready for deployment, this will be removed.


### 6.4 requirements.txt

This project has been configured to support the use of a virtual environment. Therefore, this text file contains all requirements for the application to run. 


### 6.5 media/

The `media/` directory contains ALL images/icons used in the application. 


### 6.6 sounds/

The `sounds/` directory holds ALL sound files used in the application. Whenever the user uploads sound files, this is where they are stored. 


### 6.7 unedited_sounds/

This directory holds the unmodified versions of sounds after they have been edited. This allows the user to easily revert back to the original sound's duration, without having to modify the original sound whatsoever, maintaining data integrity.


### 6.8 button_images.json

This file holds the file paths for any sound that has been allocated an image. Thus, when the application loads the sounds, if the `button_icons` variable contains a key with the same name as a button, the button is given the previously set image. 


### 6.9 themes/

This directory stores all the `.qss` files needed for styling the application. There is a file for each page in the application. 

**QSS** uses CSS syntax and is of CSS version 2.


### 6.10 fonts/

This directory stores all the fonts that can be used by the application.

---

## 7. How to run the soundboard using the Command Line Interface (CLI)

### 7.1 Initialisation/Requirements

The following is a list of prerequisites before continuing:

    - Git has been installed successfully on your machine

    - There is a suitable version of Python that has been installed. For this application Python version 3.10+ is required. 

    - pip installer is present and usable on your machine. This can often be bundled together when using Python's install wizard

    - When installing Python using the wizard, make sure it is added to your PATH variable for the system.

    - You are somewhat familiar with your machines terminal interface and commands. Extensive or expert knowledge is NOT required however.

    - For editing any files, an appropriate IDE should be installed (this is entirely up to the developer of course, vim is applauded). Recommended choice is VS Code.

Once the above has been confirmed/resolved, you may continue.

Before running the application, it is strongly advised that a virtual environment (venv) is created before execution. 

To do this depends on the environment that you are using. Likely, is that this is a Windows machine, so the following will explain how to achieve this for Windows. For other operating systems, I recommend researching how to create a python virtual environment.


### 7.2 Setup

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

Otherwise, please raise an issue on GitHub or email me directly using `battmannwann@gmail.com`.

---

# Thank you for reading the documentation.





