# What is it
Casual Word Game (CWG) is a text based game where you try to guess a word based on it's definition. It is easy to pick up, has an educational element to it and boosts your general knowledge and vocabulary, plus it's just fun to play.

# Getting Started

If you are interested in the project just fork the repo and develop further. Would love to see your proposed changes and enhancements.  
Running the game is a simple matter of unpacking one of the archives in the `distributions` folder and double clicking the CWG file. The game runs in the terminal and the player controls it through text commands.

# Prerequisites

To edit or add source code all you need is a code editor/IDE and an operating system with _Python v3.7_ installed.

# Build and deployment

A typical build of the CWG's source is done via the _PyInstaller_ tool. You can install it by:
```
pip install pyinstaller
```
or upgrade it:
```
pip install --upgrade pyinstaller
```

Then it's a matter of choosing the preferred options...  
* `-n` - the name of the package
* `-D` or `-F` - the type of distibution: `single directory` or `single file` respectively.
* `--add-data` - adds the required extra non-binary files
* `-p` - the path to search for dependencies
...and running the command
```
pyinstaller -n <name_of_the_build> -<build_type>D|F --add-data <path_to_data>:<destination_of_data> -p <dir_name> <module_name>.py    
```

# Contribution

https://github.com/ivi-dev/CWG/blob/master/CONTRIBUTING.md

# Code of Conduct

https://github.com/ivi-dev/CWG/blob/master/CODE_OF_CONDUCT.md

# Authors

[Iliyan Videv](mailto:videviliyan@gmail.com)

# License

This project is licensed under the **MIT License**.  
https://github.com/ivi-dev/CWG/blob/master/LICENSE
