# coding : utf-8


#####################################################################################
# IMPORT DES LIBRAIRIES ET DE NOS CLASSES                                             #
#####################################################################################
import pygame
import math
from file_class.game import Game
from file_class.connexion import Connexion
from file_class.keyboard import Keyboard_f
from file_class.sql_request import SQL_request
pygame.init()


#####################################################################################
# INSTANCE DES VARIABLES                                                            #
#####################################################################################
email_user= "herbet.hadrien@gmail.com"
password_user = "herbet"
# ! def si le jeux est en cour
running = True
# ! set font big
#middle_font = pygame.font.Font(None, 40)
#little_font = pygame.font.Font(None, 20)

# ! set width and height
width_screen = 1600
height_screen = 900

# ? vérifie si email et password sont dans la BDD
#email_check = SQL_request.check_email(email_user)
#password_check = SQL_request.check_password(password_user)

#####################################################################################
# GENERATION DES OBJET DE LA HOMEPAGE                                               #
#####################################################################################

# ! generer la fenêtre du jeu
pygame.display.set_caption("Projet 2")
screen = pygame.display.set_mode((width_screen, height_screen), pygame.FULLSCREEN)

# ! importer et charger le background
background = pygame.image.load('assets/bg2.jpg')
background = pygame.transform.scale(background, (width_screen, height_screen))




#####################################################################################
# INSTANCE DES CLASSES                                                              #
#####################################################################################

# ? init la classe connexion
connexion = Connexion(width_screen, height_screen)
menu = connexion.list_home_object
SQL_request = SQL_request()
# ? init la classe keyboard
keyboard_touch = Keyboard_f()
# ! init la classe Game
game = Game(width_screen, height_screen)



#####################################################################################
# BOUCLE DES FRAME                                                                  #
#####################################################################################

# ! boucle tant que running est vrai
while running:


    # ! verifier si le jeu a commence ou ou pas
    if game.game_launch:
        # ! appliquer le background
        screen.blit(game.background, (0,0))
        # ! déclencher les instructions de la partie
        game.update(screen)
    # ! si le jeu n'est pas lancer
    else:
        # ! appliquer le background
        connexion.update(screen)
    # ! update le screen
    pygame.display.flip()

    # ! si le joueur ferme cette fenêtre
    for event in pygame.event.get():
        # ! check que l'event est le fait de fermer la fenêtre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Le jeu se ferme")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if connexion.list_home_object[0].rect.collidepoint(event.pos):
                connexion.list_home_object[0].change_image('assets/input_ok.PNG')
                connexion.list_home_object[1].change_image('assets/input_ko.PNG')
            
            if connexion.list_home_object[1].rect.collidepoint(event.pos):
                connexion.list_home_object[1].change_image('assets/input_ok.PNG')
                connexion.list_home_object[0].change_image('assets/input_ko.PNG')

            if connexion.list_home_object[4].rect.collidepoint(event.pos):
                connexion.test_login(SQL_request)

                if connexion.email_check and connexion.password_check:
                    game.game_launch = True
                elif not connexion.email_check or connexion.password_check:
                    connexion.login_false = True
            
            if game.game_launch and game.player_select == False:
                for button in game.button_play:
                    if button.rect.collidepoint(event.pos):
                        player_choose = button.lauch_player()
                        game.lauch_player_choice(player_choose)


        elif event.type == pygame.KEYDOWN:

            # ! si touche echap
            if event.key == 27:
                running = False
                pygame.quit()
                print("Le jeu se ferme")

            # ! si la touche tab
            elif event.key == 9:
                if connexion.list_home_object[0].can_write:
                    connexion.list_home_object[1].change_image('assets/input_ok.PNG')
                    connexion.list_home_object[0].change_image('assets/input_ko.PNG')

                elif connexion.list_home_object[1].can_write:
                    connexion.list_home_object[0].change_image('assets/input_ok.PNG')
                    connexion.list_home_object[1].change_image('assets/input_ko.PNG')

                elif connexion.list_home_object[0].can_write == False and connexion.list_home_object[0].can_write == False:
                    connexion.list_home_object[0].change_image('assets/input_ok.PNG')
                    connexion.list_home_object[1].change_image('assets/input_ko.PNG')

            # ? si la touche entrée
            elif event.key == 13 or event.key == 271:
                connexion.test_login(SQL_request)

                if connexion.email_check and connexion.password_check:
                    game.start(connexion.user_playing)
                elif not connexion.email_check or connexion.password_check:
                    connexion.login_false = True



            # ? si on appuie sur la touche back space
            elif event.key == 8 and connexion.list_home_object[0].can_write:
                connexion.return_mail_user()

            elif event.key == 8 and connexion.list_home_object[1].can_write:
                connexion.return_password_user()


            # ? sinon toute les touches
            else:
                if connexion.list_home_object[0].can_write:
                    connexion.write_mail_user(keyboard_touch.key_pressed(event.key))
                if connexion.list_home_object[1].can_write:
                    connexion.write_password_user(keyboard_touch.key_pressed(event.key))

