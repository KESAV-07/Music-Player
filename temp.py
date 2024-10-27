#display
from math import ceil
import tkinter as tk
from token import COMMA
import customtkinter as customtk
from PIL import Image, ImageTk
import pygame
from music import *
from search import search_songs
import os
from download import download_song
from functools import partial

customtk.set_appearance_mode("System")
customtk.set_default_color_theme("blue")

root = customtk.CTk()
root.title("Music Player")
root.geometry("1280x720")
frames = []

pygame.mixer.init()
pygame.display.init()
screen = pygame.display.set_mode((1, 1), pygame.NOFRAME)

# Background image
background_image = Image.open("img/blackgradbg.png")
background_image = background_image.resize((1920, 1080), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Bottom frame
bottom_frame = customtk.CTkFrame(master=root, width=1280, height=100, corner_radius=0, bg_color="black", fg_color="#000000")
bottom_frame.place(x=0, y=550)

#top frame
bottom_frame = customtk.CTkFrame(master=root, width=1280, height=50, corner_radius=0, bg_color="black", fg_color="#000000")
bottom_frame.place(x=0, y=0)

# Left frame
left_frame = customtk.CTkFrame(master=root, width=300, height=500, corner_radius=10, bg_color="#000000", fg_color="#191414",border_color="#000000",border_width=4)
left_frame.place(x=0, y=50)
playlist_text = tk.Label(left_frame,text="Your Playlist",fg="white",bg="#191414",font=(" Circular Std",22))
playlist_text.place(x=130,y=30)

# Right frame
right_frame = customtk.CTkFrame(master=root, width=300, height=500, corner_radius=10, bg_color="#000000", fg_color="#191414",border_color="#000000",border_width=4)
right_frame.place(x=980, y=50)
select_buttons=[]
download_buttons=[]
#main frame
def create_frames(num_frames):
    global frames
    frames.clear()  # Clear existing frames
    for i in range(num_frames):  # Create new frames
        frame = customtk.CTkFrame(master=root, width=515, height=35, corner_radius=20, fg_color="#000000", bg_color="#3C3D37")
        frames.append(frame)
        frame.place(relx=0.3, rely=0.15 + (i * 0.07))  
        
        select_image1 = Image.open("img/playbuttonwhite2.png")
        select_image1 = select_image1.resize((25,25), Image.LANCZOS)
        select_image_tk1 = ImageTk.PhotoImage(select_image1)
        music = search_results[i]
        f = partial(downloadAndPlay,music)
        select_button = customtk.CTkButton(master=root, image=select_image_tk1,command=f, text="", width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=5,hover_color="#1F282C")
        select_button.place(relx=0.315, rely=0.176 + (i*0.07), anchor=tk.CENTER)
        select_buttons.append(select_button)
        '''
        download_image1 = Image.open("img/download.png")
        download_image1 = download_image1.resize((25,25), Image.LANCZOS)
        download_image_tk1 = ImageTk.PhotoImage(download_image1)
        download_button = customtk.CTkButton(master=root, image=download_image_tk1,command=mute_music, text="", width=25, height=25, bg_color="#030201", fg_color="black",corner_radius=5,hover_color="#1F282C")
        download_button.place(relx=0.68, rely=0.176 + (i*0.07), anchor=tk.CENTER)
        download_buttons.append(download_button)
        '''
def downloadAndPlay(music):
    song_name = download_song(music.title,music.artist)
    list_songs.clear()
    list_songs.append(f'music/{song_name}.wav')
    next_song()

# Song list
list_songs = []
list_covers = ["bg.png"]
n = 0

# Song name label
song_name_label = tk.Label(root, text="", bg="#000000", fg="white", font=("Circular", 18))
song_name_label.place(relx=0.14, rely=0.92, anchor=tk.CENTER)

# Progress bar variable
progressbar = None
song_length = 0  

# Song play/pause state
song_playing = False  # Initially no song is playing
current_volume = 0.5  # default volume


pygame.mixer.music.set_endevent(pygame.USEREVENT)

def on_search():
    query = search_input.get()  # Get the song name  from the input box
    search_song(query)  # Call the search function from search.py

def update_progress():
    
    if pygame.mixer.music.get_busy() and song_length > 0:  # to  ensure there's a song playing
        current_position = pygame.mixer.music.get_pos() / 1000  # Get position in seconds
        slider.set(current_position / song_length)  # Update seek bar
    root.after(200, update_progress)  # Call this function again after 200 milliseconds

def play_pause_music():
    global song_playing

    if song_playing:  
        pygame.mixer.music.pause()  # Pause the song
        song_playing = False  # Update the state to not playing
        create_play_button()  # Switch to the play button
    else:
        if pygame.mixer.music.get_pos() > 0:  # If a song is paused, resume it
            pygame.mixer.music.unpause()  # Resume the song
            song_playing = True  # Update the state to playing
            create_pause_button()  # Switch to the pause button
        else:
            play_music()  # Start a new song if no song was playing before

def play_music():
    global n, song_length, song_playing, song_duration_label  
    try:
        song_name = list_songs[n]
    except:
        pass
    pygame.mixer.music.load(song_name)
    pygame.mixer.music.play(loops=0)
    pygame.mixer.music.set_volume(current_volume)  # Set the volume to the current volume level

    song_playing = True  
    create_pause_button()  # Show pause button when the song is playing

    # Update the song length and song name label
    song_length = pygame.mixer.Sound(song_name).get_length()  # Get the length of the song in seconds
    song_name_label.config(text=song_name[6:-4],wraplength=400)  # Update song name

    # Convert song length to minutes:seconds format
    song_duration = f"{int(song_length // 60)}:{int(song_length % 60):02d}"
    
    # Update the song duration label on the window
    song_duration_label.config(text=f"{song_duration}")  # Update song duration label
    print(song_duration)  # Optional print for debugging

    slider.set(0)  # Initialize slider to 0
    update_progress()  # Start updating the seek bar
    n = (n + 1) % len(list_songs)  # Loop back to the first song after the last one
    create_like_button()
    create_loop_button()
    create_lyricsoff_button()

# Somewhere in your initialization code, you'll need to create the `song_duration_label`
song_duration_label = tk.Label(root, text="0:00",fg="white",bg="black",font="circular 14")  # Initial placeholder text
song_duration_label.place(relx=0.66,rely=0.865) 



def pause_music():
    """This function pauses the music."""
    pygame.mixer.music.pause()
    create_play_button()
    global song_playing
    song_playing = False  # Set the state to not playing

def seek_music(position):
    """Seek to a specific position in the song."""
    global song_length
    if song_length > 0:  # Ensure the song length is valid
        new_position = position * song_length  # Get the new position in seconds
        pygame.mixer.music.set_pos(new_position)  # Set the new position in seconds
        slider.set(position)  # Keep the slider updated after seeking

def prev_song():
    """Play the previous song in the list."""
    global n
    n = (n - 2) % len(list_songs)  # Go to the previous song, loop if needed
    play_music()

def next_song():
    """Play the next song in the list."""
    play_music()

def volume(value):
    """Set the volume of the music."""
    global current_volume
    current_volume = float(value)  # Store the current volume level
    pygame.mixer.music.set_volume(current_volume)  # Apply the volume change to the currently playing music

def homepage():
    global frames
    # Clear existing frames before displaying new results
    for frame in frames:
        frame.destroy()  
    create_frames(10)
def like_music():
    create_liked_button()

def unlike_music():
    create_like_button()

def loop_music():
    create_looped_button()

def looped_music():
    create_loop_button()

def lyricson_mode():
    create_lyricson_button()

def lyricsoff_mode():
    create_lyricsoff_button()

def mute_music():
    """Mute the music and set the volume slider to 0."""
    pygame.mixer.music.set_volume(0)  # Mute the audio
    volume_slider.set(0)  # Bring the slider to 0
    create_volumeoff_button()  # Switch to the muted button

def unmute_music():
    """Unmute the music and restore the previous volume level."""
    pygame.mixer.music.set_volume(current_volume)  # Restore the audio to the previously set volume
    volume_slider.set(current_volume)  # Restore the slider to the current volume level
    create_volumeon_button()  # Switch to the volume on button

# Create play, previous, and next buttons 
def create_play_button():
    play_image1 = Image.open("img/playbuttonwhite2.png")
    play_image1 = play_image1.resize((60, 60), Image.LANCZOS)
    play_image_tk1 = ImageTk.PhotoImage(play_image1)
    play_button = customtk.CTkButton(master=root, image=play_image_tk1, text="", command=play_pause_music, width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=5,hover_color="#1F282C")
    play_button.place(relx=0.500, rely=0.950, anchor=tk.CENTER)

def create_pause_button():
    pause_image1 = Image.open("img/pausebutton.png")
    pause_image1 = pause_image1.resize((60, 60), Image.LANCZOS)
    pause_image_tk1 = ImageTk.PhotoImage(pause_image1)
    pause_button = customtk.CTkButton(master=root, image=pause_image_tk1, text="", command=play_pause_music, width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=5,hover_color="#1F282C")
    pause_button.place(relx=0.500, rely=0.950, anchor=tk.CENTER)



def create_prev_button():
    prev_image = Image.open("img/prevgreybutton.png")
    prev_image = prev_image.resize((25, 25), Image.LANCZOS)
    prev_image_tk = ImageTk.PhotoImage(prev_image)
    prev_button = customtk.CTkButton(master=root, image=prev_image_tk, text="", command=prev_song, width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=15,hover_color="#1F282C")
    prev_button.place(relx=0.460, rely=0.950, anchor=tk.CENTER)

def create_next_button():
    next_image = Image.open("img/nextgreybutton.png")
    next_image = next_image.resize((25, 25), Image.LANCZOS)
    next_image_tk = ImageTk.PhotoImage(next_image)
    next_button = customtk.CTkButton(master=root, image=next_image_tk, text="", command=next_song, width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=15,hover_color="#1F282C")
    next_button.place(relx=0.540, rely=0.950, anchor=tk.CENTER)

def create_like_button():
    like_image1 = Image.open("img/heartwhitebutton.png")
    like_image1 = like_image1.resize((30, 30), Image.LANCZOS)
    like_image_tk1 = ImageTk.PhotoImage(like_image1)
    like_button = customtk.CTkButton(master=root, image=like_image_tk1, text="", command=like_music, width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=5,hover_color="#1F282C")
    like_button.place(relx=0.25, rely=0.91880, anchor=tk.CENTER)
    return like_button

def create_liked_button():
    
    liked_image1 = Image.open("img/heartredbutton.png")
    liked_image1 = liked_image1.resize((35, 35), Image.LANCZOS)
    liked_image_tk1 = ImageTk.PhotoImage(liked_image1)
    liked_button = customtk.CTkButton(master=root, image=liked_image_tk1, text="",command=unlike_music, width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=5,hover_color="#1F282C")
    liked_button.place(relx=0.25, rely=0.91880, anchor=tk.CENTER)

def create_lyricsoff_button():
    
    lyricsoff_image1 = Image.open("img/lyricsoffbutton.png")
    lyricsoff_image1 =lyricsoff_image1.resize((30, 30), Image.LANCZOS)
    lyricsoff_image_tk1 = ImageTk.PhotoImage(lyricsoff_image1)
    lyricsoff_button = customtk.CTkButton(master=root, image=lyricsoff_image_tk1, text="",command=lyricson_mode, width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=5,hover_color="#1F282C")
    lyricsoff_button.place(relx=0.6, rely=0.950, anchor=tk.CENTER)

def create_lyricson_button():
    
    lyricson_image1 = Image.open("img/lyricsonbutton.png")
    lyricson_image1 =lyricson_image1.resize((35, 35), Image.LANCZOS)
    lyricson_image_tk1 = ImageTk.PhotoImage(lyricson_image1)
    lyricson_button = customtk.CTkButton(master=root, image=lyricson_image_tk1, text="",command=lyricsoff_mode, width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=5,hover_color="#1F282C")
    lyricson_button.place(relx=0.6, rely=0.950, anchor=tk.CENTER)


def create_loop_button():
    loop_image1 = Image.open("img/loopbutton.png")
    loop_image1 = loop_image1.resize((30, 30), Image.LANCZOS)
    loop_image_tk1 = ImageTk.PhotoImage(loop_image1)
    loop_button = customtk.CTkButton(master=root, image=loop_image_tk1, text="",command=loop_music, width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=5,hover_color="#1F282C")
    loop_button.place(relx=0.4, rely=0.950, anchor=tk.CENTER)

def create_looped_button():
    looped_image1 = Image.open("img/loopedbutton.png")
    looped_image1 = looped_image1.resize((35,35), Image.LANCZOS)
    looped_image_tk1 = ImageTk.PhotoImage(looped_image1)
    looped_button = customtk.CTkButton(master=root, image=looped_image_tk1, text="",command=looped_music, width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=5,hover_color="#1F282C")
    looped_button.place(relx=0.4, rely=0.950, anchor=tk.CENTER)

def create_volumeon_button():

    volume_image1 = Image.open("img/soundon.png")
    volume_image1 = volume_image1.resize((30,30), Image.LANCZOS)
    volume_image_tk1 = ImageTk.PhotoImage(volume_image1)
    volume_button = customtk.CTkButton(master=root, image=volume_image_tk1,command=mute_music, text="", width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=5,hover_color="#1F282C")
    volume_button.place(relx=0.8, rely=0.960, anchor=tk.CENTER)

def create_volumeoff_button():
    volumeoff_image1 = Image.open("img/soundoffbutton.png")
    volumeoff_image1 = volumeoff_image1.resize((30,30), Image.LANCZOS)
    volumeoff_image_tk1 = ImageTk.PhotoImage(volumeoff_image1)
    volumeoff_button = customtk.CTkButton(master=root, image=volumeoff_image_tk1,command=unmute_music, text="", width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=5,hover_color="#1F282C")
    volumeoff_button.place(relx=0.8, rely=0.960, anchor=tk.CENTER)

def create_home_button():
    home_image1 = Image.open("img/homewhitebutton.png")
    home_image1 = home_image1.resize((40,40), Image.LANCZOS)
    home_image_tk1 = ImageTk.PhotoImage(home_image1)
    home_button = customtk.CTkButton(master=root, image=home_image_tk1, command= homepage,text="", width=25, height=25, bg_color="#030201", fg_color="#030201",corner_radius=5,hover_color="#1F282C")
    home_button.place(relx=0.97, rely=0.04, anchor=tk.CENTER)


def search():
    global search_entry  # Declare search_entry as global to make it accessible in on_search

    big_frame = customtk.CTkFrame(root, bg_color="#3c3c3c", fg_color="#000000", border_width=0, corner_radius=0, width=680, height=50)
    big_frame.place(relx=0.50, rely=0.1, anchor='center')

    border_frame = customtk.CTkFrame(root, bg_color="#191414", fg_color="transparent", border_width=2, corner_radius=10, width=400, height=50)
    border_frame.place(relx=0.5, rely=0.085, anchor='center') 

    search_entry = customtk.CTkEntry(
        root,
        width=390,
        fg_color="transparent",
        bg_color="#191414",
        font=("Circular", 20),
        border_color="#191414",
        placeholder_text="What do you want to play?"
    )
    search_entry.place(relx=0.347, rely=0.068)

    # Bind the 'Enter' key to the on_search function
    search_entry.bind("<Return>", on_search)

def display_results(search_results):
    global frames
    # Clear existing frames before displaying new results
    for frame in frames:
        frame.destroy()  # Destroy old frames
    create_frames(len(search_results))  # Create new frames for the new results

    # Loop through search results and assign each result to a frame
    for x, result in enumerate(search_results):
        if x < len(frames):  # Ensure you don't exceed the number of frames available
            main_frame = frames[x]
            
            # Create a label inside the frame to display the result
            label = customtk.CTkLabel(
                master=main_frame,
                text=f"Song: {result.title}, Artist: {result.artist}, Album: {result.album}",
                font=("Circular std",11),
                width=475,
                text_color="white",
                fg_color="#000000",  
                wraplength=400  # fits the result within the frame width
            )
            
            label.pack(padx=20, pady=5)  

def on_search(event=None):
    global search_results
    query = search_entry.get()  # Get the input from the entry box
    if query.strip():  # Check if the input is not empty
        print(f"Search Query: {query}")  # Print the query to the terminal
        # Call the actual search function from search.py
        search_results = search_songs(query)  # Assuming perform_search is the function from search.py
        display_results(search_results)

    
search()

# Volume Slider
def create_volume_slider():
    global volume_slider
    volume_slider = customtk.CTkSlider(master=root, from_=0, to=1, command=volume, 
                                         width=200, height=15, bg_color="#000000", 
                                         button_color="#FAF9F6", fg_color="#3c3c3c", 
                                         button_hover_color="white", progress_color="#1DB954")
    volume_slider.place(relx=0.82, rely=0.95)  # Adjust the placement
    volume_slider.set(current_volume)  # Set the slider to the current volume

def create_slider():
    global slider
    slider = customtk.CTkSlider(master=root, from_=0, to=1, command=seek_music, 
                                 width=400, height=15, bg_color="#000000", 
                                 button_color="#FAF9F6", fg_color="#3c3c3c", 
                                 button_hover_color="white", progress_color="#1DB954")
    slider.place(relx=0.34, rely=0.87) 

create_home_button()
create_volumeon_button()
create_play_button()
create_prev_button()
create_next_button()
create_slider()
create_volume_slider()
root.mainloop()