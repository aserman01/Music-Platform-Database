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
- User Menu: Provides options for accessing tracks, albums, user profile, and activity history.
- Artist Menu: Additional options specific to artists, such as track statistics and managing their own tracks.
- Browse and Filter Tracks: Users can explore and filter tracks by artist and genre, add them to playlists, and play them.
- View Albums: Displays a list of albums and their associated tracks.
- User Profile: Shows user information, followers, following, playlists, and liked playlists. Users can follow/unfollow others and explore their profiles.
- User History: Displays the user's activity history, including recently played tracks.
- Track Statistics: Artists can view statistics for their tracks, such as play count.
- Create Playlists: Users can create new playlists with a name and privacy setting.
- View Playlist Contents: Displays the tracks within a selected playlist.
- Create Albums: Artists can create new albums by selecting existing tracks.
- Update Track Information: Artists can update track details like name, genre, length, and release date.
- Like Playlists: Users can like playlists to show their appreciation.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

