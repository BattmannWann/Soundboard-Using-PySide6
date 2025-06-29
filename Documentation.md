# Documentation for Soundboard

### Written and Maintained by Rhys Stewart


## Preface

While the code itself does follow the "self-documenting" convention laid out by professional software standards, the following will provide an in-depth overview of each
segment of the codebase, such that any possible discrepancy or misunderstanding is covered. 

Since the codebase is quite large, I feel it important to have produced this document to help lessen the load. Having to read thousands of lines of code is very cumbersome, 
even if the code is well written. 


## What to expect

The documentation will provide detailed discussion over:

    - Each Class
    - Each method within each class
    - Each import and library used
    - How to run the soundboard using the CLI

Regarding how to use the soundboard itself, please refer to the [User Guide](). 

I will format this documentation such that you may use the links provided in the contents section to navigate through this document quickly. Copies of this may also be found in the wiki, however, I myself find it useful to have a copy in the code. 


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
