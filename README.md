# Downloads Folder Organiser
A lightweight Python script that declutters your Downloads folder by sorting files and directories into categorised subdirectories based on their file extensions.

## Features
- Custom Categories: Define your own folder names and file extensions using a simple config.toml file.

- Smart Folder Handling: Generic folders are moved to a designated directory, while macOS .app bundles are smartly categorised as Installers.

- Collision Protection: Never overwrites files. If a file with the same name already exists in the destination, it safely renames the new file (e.g., file_1.txt).

- Dry Run Mode: Preview exactly what the script would do without actually moving any files.

- Ignore Active Downloads: Easily configure the script to ignore files currently being downloaded (like .crdownload or .part).

## Prerequisites
Python 3.11 or higher (Required for the built-in tomllib module).

## Setup

1. Clone this repo 
2. Configure *config.toml* as needed.
3. Run *main.py*
