# What is it
Casual Word Game (CWG) is a text based game where you try to guess a word based on it's definition. It is meant to be easy to pick up, has an educational element to it and boosts your general knowledge and vocabulary, plus it's just fun to play.  
The other main purpose of the CWG project is to serve as an entry point into the world of the Python programming language. Fresh and creative ideas for good, clean code and tidy file ordering are always welcome and encouraged.

# Download and installation
You can download a copy of the game to play from [here](https://github.com/ivi-dev/CWG/releases). Be aware that some of the releases are for a particular operating system. If that doesn't work for you, please request a specific build from the maintainers if you cannot build the source yourself that is.
To install just extract the archive into a convenient location on your machine and double click on the _CWG_ file.

# Getting Started

If you are interested in the project just fork the repo and develop further. Would love to see your proposed changes and enhancements.

# Prerequisites

To edit/add source code or to debug it all you need is a code editor/IDE and an operating system with _Python v3.7_ installed.  

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

A more detailed overview and instructions are available at: [PyInstaller Manual](https://pyinstaller.readthedocs.io/en/stable/usage.html#mac-os-x-specific-options)

# Contribution

[Contributing guidelines](https://github.com/ivi-dev/CWG/blob/master/CONTRIBUTING.md)

# Code of Conduct

[Code of Conduct](https://github.com/ivi-dev/CWG/blob/master/CODE_OF_CONDUCT.md)

# Authors

[Iliyan Videv](mailto:videviliyan@gmail.com)

# License

This project is licensed under the **MIT License**.  
[LICENSE](https://github.com/ivi-dev/CWG/blob/master/LICENSE)
