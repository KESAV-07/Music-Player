#login page
from settings import *
import pygame
import tkinter as tk
from tkinter import messagebox
import csv
import os

class loginpage:

    def __init__(self, display):
        pygame.init()
        self.display = display

    #tk window pop up
    def show_message(self, message):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Message", message)
        root.destroy()
    #creates and stores in csv file
    def check_csv(self, file_name='users.csv'):
        if not os.path.exists(file_name):
            with open(file_name, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["username", "password"])
                writer.writeheader()
    


    def save_user_data(self, username, password):
        self.check_csv()

        # Check if the user already exists in 'users.csv'
        with open('users.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            users = {row['username']: row['password'] for row in reader}

        if username in users:
            # Check if the password matches
            if users[username] == password:
                self.show_message("Login successful!")
                return True
            else:
                self.show_message("Wrong password!")
                return False
        else:
            # Register the new user by appending to 'users.csv'
            with open('users.csv', mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["username", "password"])
                writer.writerow({"username": username, "password": password})
            self.show_message("User registered successfully!")

            # Create a folder for the user in the specified directory
            user_dir = r"C:\Users\aravi\OneDrive\Desktop\a;;\kesav\music_player\user"
            user_folder_path = os.path.join(user_dir, username)
    
            # Create the user directory if it does not exist
            if not os.path.exists(user_folder_path):
                os.makedirs(user_folder_path)

            # Create an empty 'liked_songs.csv' file inside the user folder
            liked_songs_file = os.path.join(user_folder_path, "liked_songs.csv")
            with open(liked_songs_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["song_id", "song_name", "artist"])  # Add headers if needed

            return True


    def run(self):
        running = True
        clock = pygame.time.Clock()

        text_font = pygame.font.SysFont("Uni Sans", 38)
        input_font = pygame.font.SysFont("Uni Sans", 28)

        #login button
        login_header = text_font.render("LOGIN", True, (238, 235, 227))
        login_rect = login_header.get_rect()
        login_rect.center = (SCREENSIZE[0] // 2, SCREENSIZE[1] // 2 + SCREENSIZE[1] // 3 + 25)

        #username
        username_header = text_font.render("ENTER USERNAME ", True, (238, 235, 227))
        username_rect = username_header.get_rect()
        username_rect.center = (SCREENSIZE[0] // 2, SCREENSIZE[1] // 2 - 120)

        #password
        password_header = text_font.render("ENTER PASSWORD", True, (238, 235, 227))
        password_rect = password_header.get_rect()
        password_rect.center = (SCREENSIZE[0] // 2, SCREENSIZE[1] // 2 + 60)

        username_input_rect = pygame.Rect(SCREENSIZE[0] // 2 - 300, SCREENSIZE[1] // 2 - 60, 600, 40)
        password_input_rect = pygame.Rect(SCREENSIZE[0] // 2 - 300, SCREENSIZE[1] // 2 + 120, 600, 40)

        username_text = ''
        password_text = ''
        caret_position_username = 0
        caret_position_password = 0
        input_active_username = False
        input_active_password = False
        caret_visible_username = True
        caret_visible_password = True
        caret_blink_time = 500
        last_blink_time = pygame.time.get_ticks()

        login_button_rect = pygame.Rect(SCREENSIZE[0] // 2 - 75, SCREENSIZE[1] // 2 + SCREENSIZE[1] // 3, 150, 50)

        while running:
            self.display.fill((23, 23, 23))

            mouse_pos = pygame.mouse.get_pos()
            #cross button hover effect
            if (SCREENSIZE[0] - 30) <= mouse_pos[0] <= (SCREENSIZE[0] - 30) + 30 and 0 <= mouse_pos[1] <= 30:
                pygame.draw.rect(self.display, (255, 0, 0), (SCREENSIZE[0] - 30, 0, 30, 30), border_radius=3)
            else:
                pygame.draw.rect(self.display, (55, 55, 55), (SCREENSIZE[0] - 30, 0, 30, 30), border_radius=3)

            pygame.draw.line(self.display, (255, 255, 255), (SCREENSIZE[0] - 28, 2), (SCREENSIZE[0] - 2, 28))
            pygame.draw.line(self.display, (255, 255, 255), (SCREENSIZE[0] - 2, 2), (SCREENSIZE[0] - 28, 28))

            # login button effects
            if login_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]: 
                    login_button_color = (45, 45, 45)  
                else:
                    login_button_color = (45, 45, 45)  
            else:
                login_button_color = (75, 75, 75)  

            pygame.draw.rect(self.display, login_button_color, login_button_rect)

            self.display.blit(login_header, login_rect)
            self.display.blit(username_header, username_rect)
            self.display.blit(password_header, password_rect)

            username_color = (45, 45, 45) if input_active_username else (65, 65, 65)
            password_color = (45, 45, 45) if input_active_password else (65, 65, 65)

            pygame.draw.rect(self.display, username_color, username_input_rect, border_radius=5)
            pygame.draw.rect(self.display, password_color, password_input_rect, border_radius=5)

            username_rendered = input_font.render(username_text, True, (255, 255, 255))

            #displays the password as *
            password_rendered = input_font.render('*' * len(password_text), True, (255, 255, 255))

            self.display.blit(username_rendered, (username_input_rect.x + 10, username_input_rect.y + 5))
            self.display.blit(password_rendered, (password_input_rect.x + 10, password_input_rect.y + 5))

            #pointer stuff
            current_time = pygame.time.get_ticks()
            if current_time - last_blink_time > caret_blink_time:
                caret_visible_username = not caret_visible_username
                caret_visible_password = not caret_visible_password
                last_blink_time = current_time

            if caret_visible_username and input_active_username:
                text_width_username = input_font.size(username_text[:caret_position_username])[0]
                caret_x_username = username_input_rect.x + 10 + text_width_username
                pygame.draw.line(self.display, (255, 255, 255), (caret_x_username, username_input_rect.y + 5), 
                                 (caret_x_username, username_input_rect.y + 35), 2)

            if caret_visible_password and input_active_password:
                text_width_password = input_font.size(password_text[:caret_position_password])[0]
                caret_x_password = password_input_rect.x + 10 + text_width_password
                pygame.draw.line(self.display, (255, 255, 255), (caret_x_password, password_input_rect.y + 5), 
                                 (caret_x_password, password_input_rect.y + 35), 2)

            #events handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                #mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:

                        #cross button to quit
                        if pygame.Rect(SCREENSIZE[0] - 30, 0, 30, 30).collidepoint(mouse_pos):
                            running = False  
                            break

                        #login button to login
                        if login_button_rect.collidepoint(mouse_pos): 

                            if not username_text and not password_text:
                                self.show_message("Please enter both username and password.")
                            elif not username_text:
                                self.show_message("Please enter username.")
                            elif not password_text:
                                self.show_message("Please enter password.")
                            else:
                                if self.save_user_data(username_text, password_text):
                                    running = False


                        #pointer to switch whether username or passwrod input
                        if username_input_rect.collidepoint(mouse_pos):
                            input_active_username = True  
                            input_active_password = False  
                            caret_position_username = len(username_text)
                        elif password_input_rect.collidepoint(mouse_pos):
                            input_active_password = True  
                            input_active_username = False  
                            caret_position_password = len(password_text)
                
                #keyboard events
                if event.type == pygame.KEYDOWN:
                    if input_active_username:

                        #backspace , removing the char to left of caret and moves caret 1 steb back
                        if event.key == pygame.K_BACKSPACE:
                            if caret_position_username > 0:
                                username_text = username_text[:caret_position_username - 1] + username_text[caret_position_username:]
                                caret_position_username -= 1

                        #enter
                        elif event.key == pygame.K_RETURN:
                            input_active_username = False  

                        #moving the caret left
                        elif event.key == pygame.K_LEFT:
                            if caret_position_username > 0:
                                caret_position_username -= 1  
                        #moving the caret right
                        elif event.key == pygame.K_RIGHT:
                            if caret_position_username < len(username_text):
                                caret_position_username += 1 
                         #username input 
                        else:
                            if len(username_text) < 25:
                                username_text = username_text[:caret_position_username] + event.unicode + username_text[caret_position_username:]
                                caret_position_username += 1

                    elif input_active_password:
                        if event.key == pygame.K_BACKSPACE:
                            if caret_position_password > 0:
                                password_text = password_text[:caret_position_password - 1] + password_text[caret_position_password:]
                                caret_position_password -= 1
                        elif event.key == pygame.K_RETURN:
                            input_active_password = False  
                        elif event.key == pygame.K_LEFT:
                            if caret_position_password > 0:
                                caret_position_password -= 1  
                        elif event.key == pygame.K_RIGHT:
                            if caret_position_password < len(password_text):
                                caret_position_password += 1  
                        else:
                            if len(password_text) < 10:
                                password_text = password_text[:caret_position_password] + event.unicode + password_text[caret_position_password:]
                                caret_position_password += 1

            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    SCREENSIZE = (1280, 720)
    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    login = loginpage(screen)
    login.run()