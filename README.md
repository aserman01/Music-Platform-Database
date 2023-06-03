# Music-Platform-Database

This is a Python-based Spotify-like Online Music Platform application that utilizes a SQLite database to manage user accounts, tracks, albums, playlists, and user activity history. It provides features for both regular users and artists.

## Prerequisites

- Python 3.x
- PySimpleGUI library
- SQLite3

## Installation

1. Clone the repository to your local machine.
2. Install the required dependencies using the following command:
'''
pip install PySimpleGUI
'''
3. Make sure you have SQLite3 installed on your machine. If not, you can download it from the official SQLite website (https://www.sqlite.org/download.html) and follow the installation instructions.
4. Run the **'Project.db'** script to create the SQLite database.
5. Run the **'Online_Music_Platform.py'** script to start the application.


## Features

- User Authentication: Users can log in with their username and password.
- User Menu: Provides options for accessing tracks, albums, user profile, activity history, and logging out.
- Artist Menu: Additional menu options specific to artists, such as track statistics and managing their own tracks.
- Tracks: Allows users to browse and filter tracks by artist and genre, add tracks to playlists, and play tracks.
- Albums: Displays a list of albums and their associated tracks.
- User Profile: Shows user information, followers, following, playlists, and liked playlists. Users can also follow/unfollow other users and explore their profiles.
- User History: Displays the user's activity history, including recently played tracks.
- Statistics: Shows track statistics for the last 30 days, including the number of plays.
- Create New Playlist: Allows users to create a new playlist with a name and privacy setting (visible or private).
- Show Content of Playlist: Displays the tracks within a selected playlist.
- Create New Album: Enables artists to create a new album by selecting existing tracks.
- Update Track: Allows artists to update track information, such as name, genre, length, and release date.
- Like Playlist: Enables users to like a playlist.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

