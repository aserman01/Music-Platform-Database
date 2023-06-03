#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 18:24:59 2023

@author: aniltanaktan
"""
import sqlite3
import PySimpleGUI as sg 
from datetime import datetime, timedelta

con = sqlite3.connect('Project.db')
cur = con.cursor()

# global variables
login_user_name = -1
login_user_type = -1

#for testing
#username_input = "Appi40"


def window_login():
    layout = [[sg.Text('Welcome to DataBabe’s Spotify. Please enter your information.')],
              [sg.Text('Username:',size=(20,1))], [sg.Input(size=(20,1), key='id')],
         		[sg.Text('Password:',size=(20,1))], [sg.Input(size=(20,1), key='password')],
          		[sg.Button('Login'), sg.Exit()]]
    return sg.Window('Main Window', layout)

def Menu():
    layout = [[sg.Text(f"Welcome, {login_user_name}!")],
              [sg.Button("Tracks")], 
              [sg.Button("Albums")],
              [sg.Button("Profile")],
              [sg.Button("History")], 
              [sg.Button("Logout")]]
    
    return sg.Window('Menu', layout)

def window_ArtistMenu():
	#artist için kullanılacak ekran
    layout = [[sg.Text('Welcome ' + login_user_name)],
              [sg.Button('Statistics')],
              [sg.Button('Your Tracks')],
              [sg.Button('Logout')]]
    return sg.Window('Artist Menu', layout)

def window_UserHist():
    cur.execute("SELECT T.NAME, H.TIMESTAMP FROM HISTORY H, TRACK T WHERE T.TRACKID = H.TRACKID AND H.USERNAME = ? ORDER BY H.TIMESTAMP DESC", (login_user_name,))
    user_history = [f"{row[0]}: {row[1]}" for row in cur.fetchall()]
    
    layout = [[sg.Text("User History")],
              [sg.Listbox(user_history, size=(50, 10))],
              [sg.Button("Return to Menu")]]
    
    return sg.Window('User History', layout)


def window_showtracks(values):
    cur.execute("SELECT DISTINCT U.NAME FROM ARTIST A, USERS U WHERE A.USERNAME = U.USERNAME")
    artists = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT DISTINCT Genre FROM Track")
    genres = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT T.NAME, GROUP_CONCAT(U.NAME, ', '), T.Genre FROM USERS U, TRACK T, CREATES_T C, ARTIST A WHERE U.USERNAME = A.USERNAME and T.TRACKID = C.TRACKID AND C.USERNAME = A.USERNAME GROUP BY T.NAME")
    tracks = [[row[0], row[1], row[2]] for row in cur.fetchall()]
    cur.execute("SELECT P.NAME FROM PLAYLIST P, USERS U WHERE P.USERNAME = U.USERNAME AND P.USERNAME = ?", (login_user_name,))
    playlists = [row[0] for row in cur.fetchall()]  # Create playlists variable

    layout = [[sg.Text("Filter by Artists:"), sg.Combo(artists, key="-ARTIST-")],
              [sg.Text("Filter by Genre:"), sg.Combo(genres, key="-GENRE-"), sg.Button("Filter"), sg.Button("Reset Filter")],
              [sg.Text("Tracks:")],
              [sg.Listbox(tracks, size=(50, 10), key="-TRACK-")],
              [sg.Combo(playlists, key="-PLAYLIST-"), sg.Button("Add to Playlist")],
              [sg.Button("Return to Menu"), sg.Button("Play")]]
    
    return sg.Window("Tracks", layout)


def window_ArtistTracks():
    query = """
        SELECT T.NAME, GROUP_CONCAT(U.NAME, ', ')
        FROM TRACK T
        INNER JOIN CREATES_T C ON T.TRACKID = C.TRACKID
        INNER JOIN USERS U ON C.USERNAME = U.USERNAME
        WHERE T.TRACKID IN (
            SELECT TRACKID
            FROM CREATES_T
            WHERE USERNAME = ?
        )
        GROUP BY T.NAME
    """
    cur.execute(query, (login_user_name,))
    tracks = cur.fetchall()

    layout = [
        [sg.Text('Artist Tracks')],
        [sg.Listbox(tracks, size=(50, 10), key='-TRACK-')],
        [sg.Button('Create New Track'), sg.Button('Create New Album')],
        [sg.Button('Return to Menu '), sg.Button('Update')]
    ]

    return sg.Window('Artist Tracks', layout)

	
def window_Albums():
    
    albums = []
    
    for row in cur.execute('''SELECT DISTINCT U.Name, A.Name 
                              FROM USERS U, ALBUM A, IS_IN I
                              WHERE I.ALBUMID = A.ALBUMID
                              AND U.USERNAME = I.USERNAME '''):
        albums.append(row)
    
    layout = [[sg.Text('Album List:'), sg.Combo(albums, size=(38,7), key='album'), sg.Button('List Tracks')],
              [sg.Listbox((), size=(50,10), key='-TRACK-')],
              [sg.Button('Play'), sg.Button('Return to Menu')]]

    return sg.Window('Albums', layout)

def window_statistic(values):
    today = datetime.today()
    lessthanonemonth = today - timedelta(days=30)
    
    tracksstat = []
    for row in cur.execute('''SELECT T.NAME, COUNT(*) AS PLAYS
                              FROM TRACK T, CREATES_T CT, ARTIST A, HISTORY H
                              WHERE  H.TRACKID = CT.TRACKID AND CT.USERNAME = A.USERNAME AND T.TRACKID = CT.TRACKID AND A.USERNAME = ? and H.TIMESTAMP >= ?
                              GROUP BY T.TRACKID''', (login_user_name, lessthanonemonth)):
        tracksstat.append(( row[0],row[1]))


    layout = [[sg.Text('Your Statistics for Last 30 Days:')],
              [sg.Listbox(tracksstat, size=(40, 5))],
              [sg.Button('Return to Menu ')]]

    return sg.Window('Statistics', layout)


def window_Profile():
    followers = []
    for row in cur.execute('''SELECT F.FOLLOWER_USERNAME
                              FROM STANDART S, FOLLOWS F
                              WHERE S.USERNAME = F.FOLLOWEE_USERNAME AND S.USERNAME = ? ''', (login_user_name,)):
        followers.append(row[0])
    
    following = []
    for row in cur.execute('''SELECT F.FOLLOWEE_USERNAME
                              FROM STANDART S, FOLLOWS F 
                              WHERE S.USERNAME = F.FOLLOWER_USERNAME AND S.USERNAME = ? ''', (login_user_name,)):
        following.append(row[0])
    
    notfollowing = []
    for row in cur.execute('''SELECT USERNAME
                              FROM STANDART
                              WHERE USERNAME <> ?''', (login_user_name,)):
        notfollowing.append(row[0])
     
    my_playlist = []
    for row in cur.execute('''SELECT NAME
                              FROM PLAYLIST
                              WHERE USERNAME = ?''', (login_user_name,)):
        my_playlist.append(row[0])
    
    
    
    liked_playlist = []
    for row in cur.execute('''SELECT NAME
                              FROM PLAYLIST P, LIKES L
                              WHERE P.PLAYLISTID = L.PLAYLISTID AND L.USERNAME = ?''', (login_user_name,)):
        liked_playlist.append(row[0])
    
    layout = [[sg.Text('Your Followers:'),sg.Text('                 You Are Following:')],
              [sg.Listbox(followers, size=(20, 5)), sg.Listbox(following, size=(20, 5))],
              [sg.Text('Look for users'), sg.Combo(notfollowing, key='fuser')],
              [sg.Button('Follow'), sg.Button('Go to Profile')],
              [sg.Text('My Playlists:'),sg.Text('                 Liked Playlists:')],
              [sg.Listbox(my_playlist, size=(20, 5)), sg.Listbox(liked_playlist, size=(20, 5))],
              [sg.Button('Show Content of Playlist'), sg.Button('Create New Playlist')],
              [sg.Button('Return to Menu')]]

    return sg.Window('Profile', layout)

def window_show_content(values):
    
    name = values[2][0]
    for row in cur.execute('''SELECT P.PLAYLISTID
                              FROM PLAYLIST P
                              WHERE P.NAME = ? ''', (name,)):
        playlistid = row[0] 
    
    tracks_in_playlist = []
    for row in cur.execute('''SELECT T.NAME
                              FROM PLAYLIST P, INCLUDES I, TRACK T
                              WHERE P.PLAYLISTID = I.PLAYLISTID AND T.TRACKID = I.TRACKID AND P.PLAYLISTID = ?''', (playlistid,)):
        tracks_in_playlist.append(row[0])
    
    layout = [[sg.Text('Tracks in Playlist')],
              [sg.Listbox(tracks_in_playlist, size=(20, 5))],
              [sg.Button('Return to Profile')]]

    return sg.Window('Tracks in Playlist', layout)



def window_Create_New_Playlist():
    layout = [[sg.Text('Create New Playlist')],
              [sg.Text('Playlist Name:',size=(20,1))], [sg.Input(size=(20,1), key='playlist_name')],
              [sg.Combo(['Visible', 'Private'], key = 'privacy' )],
              [sg.Button('Create Playlist')],
              [sg.Button('Return to Profile')]]

    return sg.Window('Create New Playlist', layout)

def window_GoToProfile(values):
    playlists = []
    fuser = values['fuser']
    
    if fuser == '':
        sg.popup('Please choose an user.')

    else: 
        for row in cur.execute('''SELECT NAME, USERNAME
FROM PLAYLIST
WHERE (USERNAME = ? OR PLAYLISTID IN (
    SELECT PLAYLISTID
    FROM LIKES
    WHERE USERNAME = ?
  ))
  AND VISIBILITY = 'V'
''', (fuser, fuser)):
            playlists.append((row[0],'by', row[1]))                           
                            
    layout = [[sg.Text(f"{fuser}'s Profile")],
              [sg.Text('Playlists:')],
              [sg.Listbox(playlists, size=(40, 10), key='-PLAYLIST-'), sg.Button('Show Playlist'), sg.Button('Like Playlist')],
              [sg.Button('Return to your Profile')]]
    
    return sg.Window('Go to Profile', layout)


def window_CreateAlbum():
    cur.execute("""
        SELECT T.NAME, GROUP_CONCAT(U.NAME, ', ')
        FROM TRACK T
        INNER JOIN CREATES_T C ON T.TRACKID = C.TRACKID
        INNER JOIN USERS U ON C.USERNAME = U.USERNAME
        WHERE T.TRACKID IN (
            SELECT TRACKID
            FROM CREATES_T
            WHERE USERNAME = ?
        )
        GROUP BY T.NAME
    """, (login_user_name,))
    tracks = cur.fetchall()
    
    layout = [[sg.Text('Album Name:'), sg.Input(key='-ALBUM_NAME-')],
              [sg.Text('Select Tracks:')],
              [sg.Listbox(tracks, size=(30, 6), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, key='-SELECTED_TRACKS-')],
              [sg.Button('Create'), sg.Button('Cancel')]]
    return sg.Window('Create an album', layout)

def button_UpdateTrack(values):
    track = values['-TRACK-']
    
    
    
    if track:
        cur.execute("SELECT * FROM TRACK WHERE name=?", (track[0][0],))
        track_info = list(cur.fetchone())

        if track_info:
            track_name = sg.popup_get_text('Enter the new track name:')
            track_genre = sg.popup_get_text('Enter the new track genre:')
            track_length = sg.popup_get_text('Enter the new track length (minutes in the form 3.12, 2.0 etc):')
            release_date = sg.popup_get_text('Enter the new release date (YYYY-MM-DD):')
            
            
            cur.execute("SELECT * FROM TRACK WHERE NAME = ?", (track_name,))
            existing_track = cur.fetchone()
            if existing_track:
                sg.popup("A track with the same name already exists. Please choose a different track name.")
                return
            
            if track_name:
                track_info[2] = track_name
            if track_genre:
                track_info[1] = track_genre
            if track_length:
                try:
                    track_length = float(track_length)
                except ValueError:
                    sg.popup('Invalid track length. Please enter length in the form 3.12, 2.0, etc.')
                    return
                track_info[4] = track_length
            if release_date:
                try:
                    release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
                except ValueError:
                    sg.popup('Invalid release date format. Please enter the release date in the format YYYY-MM-DD.')
                    return
                track_info[3] = release_date.strftime('%Y-%m-%d')

            cur.execute("UPDATE TRACK SET name=?, length_S=?, genre=?, rel_date=? WHERE name=?",
                           (track_info[2], track_info[4], track_info[1], track_info[3], track[0][0]))
            con.commit()
            sg.popup('Track information updated successfully.')
        
    else:
        sg.popup('Please choose a track to update.')
    return window_ArtistTracks()       

def button_CreateAlbum(values):
    
    album_name = values['-ALBUM_NAME-']
    selected_t = values['-SELECTED_TRACKS-']
    
    if not album_name:
        sg.popup('Please enter the album name.')
        return
    
    if not selected_t:
        sg.popup('Please select at least one track.')
        return
    if not album_name and selected_t:
        sg.popup('Please enter the album name and select at least one track.')
        return
    
    release_date = datetime.today().strftime('%Y-%m-%d')
    cur.execute("SELECT MAX(ALBUMID) FROM ALBUM")
    album_id = cur.fetchone()[0] + 1
    cur.execute("INSERT INTO ALBUM (name, ALBUMID, release) VALUES (?, ?, ?)", (album_name, album_id, release_date))
    
    # Insert the selected tracks into the album_tracks table
    for track in selected_t:
        cur.execute("SELECT TRACKID FROM TRACK WHERE name=?", (track[0],))
        track_id = cur.fetchone()[0]
        cur.execute("INSERT INTO IS_IN (ALBUMID, TRACKID, USERNAME) VALUES (?, ?, ?)", (album_id, track_id, login_user_name))
    
    con.commit()
    sg.popup('Album created successfully.')

def button_LikePlaylist(values):
    playlist_dict = values['-PLAYLIST-']
    
    #the list is not empty, i.e. all the indices are accessible
    if playlist_dict and playlist_dict[0]:
            playlist = values['-PLAYLIST-'][0][0]
            cur.execute("SELECT PLAYLISTID FROM PLAYLIST WHERE NAME = ?", (playlist,))
            playlistid = cur.fetchone()[0]
            
            uniq = cur.execute("SELECT COUNT(*) FROM LIKES WHERE PLAYLISTID = ? AND USERNAME = ?", (playlistid, login_user_name)).fetchone()[0]
            if uniq == 0: 
                cur.execute('INSERT INTO LIKES (PLAYLISTID, USERNAME) VALUES (?, ?)', (playlistid, login_user_name))
                sg.popup('The playlist', playlist, 'has been added to your liked playlists')
            else:
                sg.popup('You have already liked this playlist.')
                
    else: 
        sg.popup('Choose a playlist first.')
        
def button_ShowPlaylist(values):
    playlist_dict = values['-PLAYLIST-']
    
    if playlist_dict and playlist_dict[0]:
        playlist = values['-PLAYLIST-'][0][0]
        tracks = []
        for row in cur.execute('''SELECT T.NAME FROM TRACK T, PLAYLIST P, INCLUDES I 
                    WHERE T.TRACKID = I.TRACKID AND P.PLAYLISTID = I.PLAYLISTID 
                    AND P.NAME = ?''', (playlist,)):
                    tracks.append(row)
                    
        track_list = ''
        for track in tracks:
            track_list += track[0] + '\n'
        sg.popup(f"The tracks in the playlist '{playlist}':\n{track_list}")
        
    else: 
        sg.popup('Choose a playlist first.')
        
def button_GoToProfile(values):
    global window
    fuser = values['fuser']
    if fuser == '':
        sg.popup('Please choose an user.')
    else:
        window.close()
        window = window_GoToProfile(values)

def button_create_playlist(values):
    
    name = values['playlist_name']
    privacy_value = values['privacy']
    
    my_playlist = []
    
    for row in cur.execute('''SELECT NAME
                              FROM PLAYLIST
                              WHERE USERNAME = ? ''', (login_user_name,)):
        my_playlist.append(row[0])
    
    if name and privacy_value:
        if name in my_playlist:
            sg.popup('You already have a playlist with this name.')
        else:
            cur.execute('INSERT INTO PLAYLIST (NAME, VISIBILITY, USERNAME) VALUES(?, ?, ?)', (name, privacy_value[0], login_user_name))
    elif name:
        sg.popup('Please select a visibility preference.')
    elif privacy_value:
        sg.popup('Please enter a playlist name.')
    else:
        sg.popup('Please enter a playlist name and select a visibility preference.')

    
def button_follow(values):
    
    following = []
    for row in cur.execute('''SELECT F.FOLLOWEE_USERNAME
                              FROM STANDART S, FOLLOWS F 
                              WHERE S.USERNAME = F.FOLLOWER_USERNAME AND S.USERNAME = ? ''', (login_user_name,)):
        following.append(row[0])
        
    fuser = values['fuser']
    if fuser == '':
        sg.popup('Please choose an user.')
    elif fuser in following:
        sg.popup('You are already following this user!')
    else:
        
        username = login_user_name
        fusername = fuser
        cur.execute('INSERT INTO FOLLOWS (FOLLOWER_USERNAME, FOLLOWEE_USERNAME) VALUES (?, ?)', (username, fusername))
        window["fuser"].update(values=fuser)

def button_addtoplaylist(values):
    selected_track = values['-TRACK-']  # Get the selected track from the listbox
    selected_playlist = values['-PLAYLIST-']  # Get the selected playlist from the combo box
    
    if selected_track and selected_track[0]:
        selected_track = selected_track[0]
    
    if selected_track and selected_playlist:
        playlist_name = selected_playlist
        cur.execute("SELECT PLAYLISTID FROM PLAYLIST WHERE NAME = ? AND USERNAME = ?", (playlist_name, login_user_name))
        playlist_row = cur.fetchone()

        if playlist_row:
            playlist_id = playlist_row[0]  # Get the playlist ID

            track_name, collaborator_names, genre = selected_track

            cur.execute("SELECT TRACKID FROM TRACK WHERE NAME = ? AND Genre = ?", (track_name, genre))
            track_row = cur.fetchone()

            if track_row:
                track_id = track_row[0]  # Get the track ID


                cur.execute("SELECT * FROM INCLUDES WHERE TRACKID = ? AND PlaylistID = ?", (track_id, playlist_id))
                if cur.fetchone():
                    sg.popup("Song already exists in the playlist.", title="Error")
                else:              
                    cur.execute("INSERT INTO INCLUDES (TRACKID, PLAYLISTID) VALUES (?, ?)", (track_id, playlist_id))
                    sg.popup('Track added to playlist successfully!')
                
                
                
            else:
                sg.popup('The selected track does not exist.')
        else:
            sg.popup('The selected playlist does not exist.')
    else:
        sg.popup('Please select a track and a playlist.')

    return window_showtracks(values)


def button_create_track():
    track_name = sg.popup_get_text('Enter the track name:')
    track_genre = sg.popup_get_text('Enter the track genre:')
    track_length = sg.popup_get_text('Enter the track length (minutes in the form 3.12, 2.0 etc):')
    release_date = sg.popup_get_text('Enter the release date (YYYY-MM-DD):')
    artist_name = sg.popup_get_text('Enter the collaborative artist name (leave blank if none):')
    collaborator_username = None

    if track_name and track_genre and track_length and release_date:
        result = None
        
        try:
            track_length = float(track_length)
        except ValueError:
            sg.popup('Invalid track length. Please enter lenght in the form 3.12, 2.0 etc.')
            return

        try:
            release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
        except ValueError:
            sg.popup('Invalid release date format. Please enter the release date in the format YYYY-MM-DD.')
            return
        
        if artist_name:
            cur.execute("SELECT USERNAME FROM USERS WHERE NAME = ?", (artist_name,))
            result = cur.fetchone()
            
            if result:
                collaborator_username = result[0]
            else:
                sg.popup("The specified artist does not exist.")
                return
        
        cur.execute("SELECT * FROM TRACK WHERE NAME = ?", (track_name,))
        existing_track = cur.fetchone()
        if existing_track:
            sg.popup("A track with the same name already exists. Please choose a different track name.")
            return
        
        cur.execute("INSERT INTO TRACK (NAME, GENRE, LENGTH_S, REL_DATE) VALUES (?, ?, ?, ?)",
                (track_name, track_genre, track_length, release_date))
        track_id = cur.lastrowid

        if collaborator_username:
            cur.execute("INSERT INTO CREATES_T (TRACKID, USERNAME) VALUES (?, ?)",
                    (track_id, collaborator_username))

        cur.execute("INSERT INTO CREATES_T (TRACKID, USERNAME) VALUES (?, ?)",
                (track_id, login_user_name))
        
        con.commit()
        sg.popup('Track created successfully!')
    
    else:
        sg.popup('Invalid track details!')
    
    
    return window_ArtistTracks()


def button_list_tracks(values):
    
    album = values['album']
    if album == '':
        sg.popup('Please choose an album.')
    else:
        album_name = album[1]
        
        tracks = []
        
        for row in cur.execute('SELECT T.NAME FROM TRACK T, IS_IN I, ALBUM A WHERE I.TRACKID = T.TRACKID AND I.ALBUMID = A.ALBUMID AND A.NAME = ?', (album_name,)):
            tracks.append(row)
        
        window.Element('-TRACK-').Update(values=tracks)


def button_play(values):
    tracks = values["-TRACK-"]

  
    todaysDate = datetime.today()
    todaysDate_str = todaysDate.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('''SELECT NAME FROM HISTORY H, TRACK T, CREATES_T C WHERE H.TRACKID = T.TRACKID and T.TRACKID = C.TRACKID and C.USERNAME = ? AND H.TIMESTAMP = ?''', (login_user_name, todaysDate_str))
  
    row = cur.fetchone()
    cur.execute('SELECT MAX(HISTORYID) FROM HISTORY')
    row = cur.fetchone()
    
    if tracks != []:
        if len(tracks) == 1:
            sg.popup('Now playing,', (tracks[0][0]))
            cur.execute("SELECT TRACKID FROM TRACK WHERE NAME = ?", (tracks[0][0],))
            trackid = cur.fetchone()[0]  
        
        else:
            sg.popup('Now playing,', (tracks[0][0]), tracks[0][1])
            cur.execute("SELECT TRACKID FROM TRACK WHERE NAME = ?", (tracks[0][0],))
            trackid = cur.fetchone()[0]  
            
        if row is None:
        # this is when there is no user in the system
            new_id = 1
        else:
            new_id = row[0] + 1

        username = login_user_name
    
        cur.execute('INSERT INTO HISTORY (HISTORYID, TIMESTAMP, TRACKID, USERNAME) VALUES (?, ?, ?, ?)', (new_id, todaysDate_str, trackid, username))
            
    elif tracks == []:
        sg.popup('Choose a track first.')


def button_filter(values):
    artist = values["-ARTIST-"]
    genre = values["-GENRE-"]
    query = "SELECT T.NAME FROM USERS U, TRACK T, CREATES_T C, ARTIST A WHERE U.USERNAME = A.USERNAME and T.TRACKID = C.TRACKID AND C.USERNAME = A.USERNAME"
    params = []
    
    if artist:
        query += " AND U.NAME = ?"
        params.append(artist)
        
    if genre:
        query += " AND T.GENRE = ?"
        params.append(genre)
    
    if not (genre or artist):
        sg.popup('Choose a genre or artist first.')
        return
        
    cur.execute(query, params)
    tracks = [[row[0]] for row in cur.fetchall()]  # Each song in its own row
    window["-TRACK-"].update(values=tracks)



def button_login(values):

    global login_user_name
    global login_user_type
    global window
    
    uname = values['id']
    upass = values['password']
    if uname == '':
        sg.popup('Username cannot be empty!')
    elif upass == '':
        sg.popup('Password cannot be empty!')
    else:
        # first check if this is a valid user
        cur.execute('SELECT USERNAME FROM USERS WHERE USERNAME = ? AND PASSWORD = ?', (uname,upass))
        row = cur.fetchone()
        
        if row is None:
            sg.popup('Username or password is wrong!')
        else:
            # this is some existing user, let's keep the ID of this user in the global variable
            login_user_name = row[0]
            # let's first check if this is a standard user
            cur.execute('SELECT USERNAME FROM STANDART WHERE USERNAME = ?', (uname,))
            row_standart = cur.fetchone()
            
            if row_standart is None:
                # let's check for artist
                cur.execute('SELECT USERNAME FROM ARTIST WHERE USERNAME = ?', (uname,))
                row_artist = cur.fetchone()
                if row_artist is None:
                    # this is not a teacher also, then there should be some problem with the DB
                    # since we expect a user to be either a student or a teacher
                    sg.popup('User type error! Please contact the admin.')
                else:
                    # this is an artist
                    login_user_type = 'Artist'
                    sg.popup('Welcome, ' + login_user_name + ' (Artist)')
                    window.close()
                    window = window_ArtistMenu()
            else:
                # this is a standart user
                    login_user_type = 'Standart_User'
                    sg.popup('Welcome, ' + login_user_name + ' (User)')
                    window.close()
                    window = Menu()

window = window_login()

while True:
    event, values = window.read()
    if event == 'Login':
        button_login(values)
        
    elif event == 'Return to Menu':
        window.close()
        window = Menu()

    elif event == 'Return to Menu ':
        window.close()
        window = window_ArtistMenu()
        
    elif event == 'Tracks':
        window.close()
        window =  window_showtracks(values)

    elif event == 'History':
        window.close()
        window = window_UserHist()

    elif event == 'Albums':
        window.close()
        window = window_Albums()

    elif event == 'Statistics':
        window.close()
        window = window_statistic(values)

    elif event == 'Your Tracks':
        window.close()
        window = window_ArtistTracks()

    elif event == 'List Tracks':
        button_list_tracks(values)

    elif event == 'Create New Track':
        button_create_track()
        window.close()
        window = window_ArtistTracks()

    elif event == 'Profile':
        window.close()
        window = window_Profile()

    elif event == 'Go to Profile':
        button_GoToProfile(values)

    elif event == 'Return to your Profile':
        window.close()
        window = window_Profile()

    elif event == 'Logout':
    # set login user global parameters
        login_user_id = -1
        login_user_name = -1
        login_user_type = -1
        window.close()
        window = window_login()

    elif event == 'Filter':
        button_filter(values)

    elif event == 'Play':
        button_play(values)

    elif event == 'Add to Playlist':
        button_addtoplaylist(values)

    elif event == 'Follow':
        button_follow(values)
        window.close()
        window = window_Profile()

    elif event == 'Like Playlist':
        button_LikePlaylist(values)

    elif event == 'Show Playlist':
        button_ShowPlaylist(values)

    elif event == 'Reset Filter':
        window.close()
        window = window_showtracks(values)

    elif event == sg.WIN_CLOSED:
        break
    
    elif event == 'Create New Album':
        window.close()
        window = window_CreateAlbum()
    
    elif event == 'Create':
        button_CreateAlbum(values)
        window.close()
        window = window_ArtistTracks()
    
    elif event == 'Cancel':
        window.close()
        window = window_ArtistTracks()
        
    elif event == 'Update':
        button_UpdateTrack(values)
        window.close()
        window = window_ArtistTracks()

    elif event == 'Create New Playlist':
        window.close()
        window = window_Create_New_Playlist()

    elif event == 'Return to Profile':
        window.close()
        window = window_Profile()

    elif event == 'Create Playlist':
        button_create_playlist(values)
        con.commit()
        window.close()
        window = window_Profile()

    elif event == 'Exit':
        window.close()

    elif event == 'Show Content of Playlist':
        if values[2] == []:
            sg.popup('Choose a playlist first')
        else:
            window.close()
            window = window_show_content(values)

window.close()

con.commit()
con.close()
