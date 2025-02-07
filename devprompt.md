# Development Prompt

Generate the following:

A simple desktop application that can run on the Linux desktop (ensure compatibility with Open SUSE Tumbleweed + KDE at least).

Use PyQt6 for the GUI.

Functionalities:

- User provides the base of their Github repositories on this computer. Default to ~/Git. This setting should persist between sessions (so ensure memory stoage).
- User pastes a Github repository URL in its browser-native format. E.g: https://github.com/danielrosehill/Open-That-Repo.

User hits "find repo"

Then:

- The utility attempts to find the repository on the user's computer. It does this by parsing through the Github repos from the base configured and trying to identify matches. Matches are repositories in which that repository is configured as a remote. The program should attempt to exclude "matches" that are due to submodule matches. 

The GUI presents its output in a format like this:

- The local path 
- An "Open Repo" button. When this is clicked the local repo will be opened in VS Code (syntax = code + local path)