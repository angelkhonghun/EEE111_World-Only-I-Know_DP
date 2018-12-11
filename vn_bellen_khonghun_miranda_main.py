#Bellen, Enrique III M. 2018-01015
#Khong Hun, Angelica 2018-04502
#Miranda, Jerimiah 2018-01845
import pygame, time, datetime, pickle, inspect
#player
class player():
    def __init__(self, stats = 0, willpower = 0, persuasion = 0, courage = 0, endurance = 0, optimism = 0):
        self.stats = stats
        self.willpower = willpower
        self.courage = courage
        self.persuasion = persuasion
        self.endurance = endurance
        self.optimism = optimism

#images
class picture(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file) #loads the image file
        self.rect = self.image.get_rect() #get rectangle of image

class background(picture):
    def __init__(self, image_file): 
        picture.__init__(self, "assets/" + image_file) #call picture initializer
        self.rect.left, self.rect.top = [0,0] #location of background image

class character(picture):
    def __init__(self, image_file):
        picture.__init__(self, "assets/" + image_file) #call picture initializer
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.43), int(self.image.get_height()*0.43))) #scale down the character images
        self.rect = self.image.get_rect() #get rectangle of image after scaling down
        self.rect.center = [500,300] #location of character in screen

class character_decision(picture):
    def __init__(self, image_file):
        picture.__init__(self, "assets/" + image_file) #call picture initializer
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.43), int(self.image.get_height()*0.43))) #scale down the character images
        self.rect = self.image.get_rect() #get rectangle of image after scaling down
        self.rect.center = [700,300] #location of character in screen

class textbox(picture):
    def __init__(self, message, italic = False, bold = True):
        picture.__init__(self, "assets/images/boxes/textbox.png") #call picture initializer
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.90), int(self.image.get_height()*0.90))) #scale down the textbox image
        self.rect = self.image.get_rect() #get rectangle of image after scaling down
        #text
        font = pygame.font.SysFont('Arial', 20, bold, italic) #text format
        words = [word.split(' ') for word in message.splitlines()]  # 2D array where each row is a list of words
        space = font.size(' ')[0]  # the width of a space
        max_width, max_height = self.image.get_size() #get dimensions of image
        max_width -= 85 #right margin
        pos = [self.rect.left + 100 ,self.rect.top + 60] #left margin, top margin
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, pygame.Color('black'))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  #reset the x
                    y += word_height  # start on new row
                self.image.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  #reset the x
            y += word_height  #start on new row
        self.rect.center = [500,500]

class namebox(picture):
    def __init__(self,message):
        picture.__init__(self, "assets/images/boxes/namebox.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.70), int(self.image.get_height()*0.90)))
        self.rect = self.image.get_rect()
        self.rect.right,self.rect.top = [950,350]
        image_width = self.rect.size[0]
        image_height = self.rect.size[1]        
        self.font = pygame.font.SysFont("ChopinScript", 35)
        self.textSurf = self.font.render(message, 1, pygame.Color('black'))
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = [image_width/2, image_height/2 + 10]
        self.image.blit(self.textSurf, self.textRect)

class decisionbox(picture):
    def __init__(self, message, italic = False, bold = True):
        picture.__init__(self, "assets/images/boxes/decisionbox.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.80), int(self.image.get_height()*0.80)))
        self.rect = self.image.get_rect()
        font = pygame.font.SysFont('Arial', 20, bold, italic)
        #text
        words = [word.split(' ') for word in message.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = self.image.get_size()
        max_width -= 10
        pos = [self.rect.left + 45, self.rect.top + 100]
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, pygame.Color('black'))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.image.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
        self.rect.left, self.rect.top = [20,10]

class button(picture):
    def __init__(self, message, location):
        picture.__init__(self, "assets/images/boxes/button.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*1.75), int(self.image.get_height()*1.75)))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        image_width = self.rect.size[0]
        image_height = self.rect.size[1]        
        self.font = pygame.font.SysFont("NORMAL", 10)
        self.textSurf = self.font.render(message, 1, (208, 113 ,4))
        text_width = self.textSurf.get_width()
        text_height = self.textSurf.get_height()
        self.image.blit(self.textSurf, [image_width/2 - text_width/2, image_height/2 - text_height/2])

class button_hover(picture):
    def __init__(self, message, location):
        picture.__init__(self, "assets/images/boxes/button-hover.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*1.75), int(self.image.get_height()*1.75)))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        image_width = self.rect.size[0]
        image_height = self.rect.size[1]        
        self.font = pygame.font.SysFont("NORMAL", 10)
        self.textSurf = self.font.render(message, 1, pygame.Color('white'))
        text_width = self.textSurf.get_width()
        text_height = self.textSurf.get_height()
        self.image.blit(self.textSurf, [image_width/2 - text_width/2, image_height/2 - text_height/2])

class load_button(picture):
    def __init__(self, location):
        picture.__init__(self, "assets/images/boxes/namebox.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.93), int(self.image.get_height()*0.93)))
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = location

class shopbox(picture):
    def __init__(self, message, italic = False, bold = True):
        picture.__init__(self, "assets/images/boxes/decisionbox.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.80), int(self.image.get_height()*0.80)))
        self.rect = self.image.get_rect()
        font = pygame.font.SysFont('ChopinScript', 35)
        word_surface = font.render("Welcome to the Shop!", 0, pygame.Color('black'))
        pos = [self.rect.left + 45, self.rect.top + 100]
        x, y = pos
        self.image.blit(word_surface, (x, y))
        #text
        font = pygame.font.SysFont('Arial', 20, bold, italic) 
        words = [word.split(' ') for word in message.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = self.image.get_size()
        max_width -= 30
        pos = [self.rect.left + 45, self.rect.top + 150]
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, pygame.Color('black'))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.image.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
        self.rect.right, self.rect.top = [980,10]

class shop_button(picture):
    def __init__(self, image, location):
        picture.__init__(self, image)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.5), int(self.image.get_height()*0.5)))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class shop_button_caption(picture):
    def __init__(self, message, location):
        picture.__init__(self, "assets/images/boxes/namebox.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.93), int(self.image.get_height()*0.93)))
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = location
        image_width = self.rect.size[0]
        image_height = self.rect.size[1]        
        self.font = pygame.font.SysFont("ChopinScript", 35)
        self.textSurf = self.font.render(message, 1, pygame.Color('black'))
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = [image_width/2, image_height/2 + 10]
        self.image.blit(self.textSurf, self.textRect)

class transparent_black():
    def __init__(self, width, height, location, alpha):
        self.surf = pygame.Surface((width,height))  #the size of your rect
        self.surf.set_alpha(alpha) # alpha level
        self.surf.fill((0,0,0)) #this fills the entire surface
        self.rect = location

#text
class text(pygame.sprite.Sprite):
    def __init__(self, message, font, size, color, bold, italic):
        self.font = pygame.font.SysFont(font, size, bold, italic)
        self.textSurf = self.font.render(message, 1, color)
        self.rect = self.textSurf.get_rect()
        
class main_button(text):
    def __init__(self, message, location, width, height):
        text.__init__(self, message, "Normal", 15, pygame.Color('white'), False, False)
        self.rect.right, self.rect.top = [location[0] + width - 15, location[1] + 10]

class decision_button(text):
    def __init__(self, message, location, width, height):
        text.__init__(self, message, "Arial", 20, pygame.Color('black'), True, False)
        self.rect.center = [location[0] + width/2, location[1] + height/2]

class load_text(text):
    def __init__(self, message, color, location, width, height):
        text.__init__(self, message, "ChopinScript", 27, color, False, False)
        self.rect.center = [location[0] + width/2, location[1] + height/2 + 10]

#music & sounds
class music():
    def __init__(self, music, loop):
        self.music = pygame.mixer.music.load("assets/" + music)
        self.play = pygame.mixer.music.play(loop)

class sound():
    def __init__(self, sound, loop = 0):
        self.sound = pygame.mixer.Sound("assets/" + sound)
        self.play = pygame.mixer.Sound.play(self.sound, loop)

#main game
class window(object):
    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        self.screen = pygame.display.set_mode((1000,650))
        self.screen.fill((255,255,255))
        self.clock = pygame.time.Clock()
        pygame.display.update()
        logo = pygame.image.load('assets/images/logo.png')
        pygame.display.set_icon(logo)
        pygame.display.set_caption('World Only I Know')
        pygame.display.update()

    def button_menu(self, message, location, action = None, background = None, scene = None, player = None):
        button_down = button(message, location)
        button_down_hover = button_hover(message, location)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if location[0] + button_down.rect.size[0] > mouse[0] > location[0] and location[1] + button_down.rect.size[1] > mouse[1] > location[1]:
            self.screen.blit(button_down_hover.image, button_down_hover.rect)
            if click[0] == 1 and action != None:
                if action == self.load_game:
                    action(background)
                elif action == self.save_game:
                    action(background, scene)
                elif action == self.shop:
                    action(background, player)
                elif action == "back":
                    return 0
                else:
                    action()

        else:
            self.screen.blit(button_down.image, button_down.rect)

    def main_menu(self, message, location, action = None, background = None, player = None):
        width = 200
        height = 40
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if location[0] + width > mouse[0] > location[0] and location[1] + height > mouse[1] > location[1]:
            main_holder = transparent_black(width, height, location, 128)
            self.screen.blit(main_holder.surf, main_holder.rect)
            if click[0] == 1 and action != None:
                if action == self.load_game:
                    action(background)
                elif action == self.scene1:
                    action(0,player)
                else:
                    action()
        main_button_right = main_button(message, location, width, height)
        self.screen.blit(main_button_right.textSurf, main_button_right.rect)

    def decision_menu(self, message, location, action = None, count = None, player = None):
        width = 365
        height = 40
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if location[0] + width > mouse[0] > location[0] and location[1] + height > mouse[1] > location[1]:
            main_holder = transparent_black(width, height, location, 50)
            self.screen.blit(main_holder.surf, main_holder.rect)
            if click[0] == 1 and action != None:
                action(count, player)
             
        decision_center = decision_button(message, location, width, height)
        self.screen.blit(decision_center.textSurf, decision_center.rect)

    def load_menu(self, count, location):
        load = load_button(location)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        width = load.rect.size[0]
        height = load.rect.size[1]

        try:
            fh = open('assets/save_files/timestamps.txt','r')
        except:
            pass
        try:
            all_timestamp = fh.readlines()
            message = all_timestamp[count]
            message= message.strip()
            fh.close()
        except:
            message = ""

        self.screen.blit(load.image, load.rect)
        if location[0] + width > mouse[0] > location[0] and location[1] + height > mouse[1] > location[1]:
            timestamp = load_text(message, (46, 63, 83), location, width, height)
            self.screen.blit(timestamp.textSurf, timestamp.rect)
            if click[0] == 1:
                if message == "":
                    pass
                else:
                    self.load_scene(count)
        else:     
            timestamp = load_text(message, pygame.Color('black'), location, width, height)
            self.screen.blit(timestamp.textSurf, timestamp.rect)

    def overwrite_menu(self, count, location, new_timestamp, scene):
        load = load_button(location)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        width = load.rect.size[0]
        height = load.rect.size[1]

        fh = open('assets/save_files/timestamps.txt','r')
        all_timestamp = fh.readlines()
        message = all_timestamp[count]
        message= message.strip()
        fh.close()
        self.screen.blit(load.image, load.rect)
        if location[0] + width > mouse[0] > location[0] and location[1] + height > mouse[1] > location[1]:
            timestamp = load_text(message, (46, 63, 83), location, width, height)
            self.screen.blit(timestamp.textSurf, timestamp.rect)
            if click[0] == 1:
                return self.overwrite(count,new_timestamp, scene)
        else:     
            timestamp = load_text(message, pygame.Color('black'), location, width, height)
            self.screen.blit(timestamp.textSurf, timestamp.rect)       

    def overwrite(self, count, new_timestamp, scene):
        fh = open('assets/save_files/timestamps.txt','r')
        all_timestamp = fh.readlines()
        all_timestamp[count] = new_timestamp + "\n"
        fh = open('assets/save_files/timestamps.txt', 'w')
        fh.writelines(all_timestamp)
        fh.close()
        data = {"scene" : scene[0], "scene count": scene[1], "player": scene[2]}
        with open(("assets/save_files/save" + str(count) + ".txt"),'wb') as fh:
            pickle.dump(data,fh)
        return 0

    def load_scene(self, count):
        with open("assets/save_files/save" + str(count) + ".txt",'rb') as fh:
            data = pickle.load(fh)
        scene = "".join(("self.",data["scene"],"(",str(data['scene count']),",player(",str(data['player'].stats),",", str(data['player'].willpower),",", str(data['player'].persuasion),",", str(data['player'].courage),",", str(data['player'].endurance), ",", str(data['player'].optimism),"))"))
        eval(scene)

    def exit_game(self):
        pygame.quit()
        quit()

    def scene1(self, count = 0, player = 0):
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Water Lily.mp3", 1)
        scene1 = True
        instruction = textbox("Press space to continue.",True, False)
        self.screen.blit(instruction.image, instruction.rect)
        play = True
        while scene1:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1

            #backgrounds and sounds
            if count == 0:
                self.screen.fill((0,0,0))
                bg = background("images/backgrounds/FIRE.jpg")
                self.screen.blit(bg.image,bg.rect) 
                if play == True:
                    breath = sound("music/sound_effects/heavy_breathing.wav")
                    play = False

            elif count == 1:
                #bg = background("images/backgrounds/FIRE.jpg")
                self.screen.blit(bg.image,bg.rect)
                if play == False:
                    ambulance = sound("music/sound_effects/ambulance.wav")
                    play = True

            elif count >= 2:
                bg = background("images/backgrounds/FIRE.jpg")
                self.screen.blit(bg.image,bg.rect)   
            #button menu
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order
            if count == 0:
                instruction = textbox("Press spacebar to continue.", True, False)
                self.screen.blit(instruction.image, instruction.rect)

            if count == 1:
                father = character("images/characters/Tomiichi/Tomiichi3_upset3.png")
                name = namebox("Tomiichi")
                instruction = textbox("You’re going to be okay, sweetie. I’m going to take care of you.")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)

            if count >= 2:
                father = character_decision("images/characters/Tomiichi/Tomiichi3_upset3.png")
                decision = decisionbox("What will you tell to your father?", True)
                self.screen.blit(father.image, father.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("I'm scared, Dad.", [35,200], self.scene1_a, 1, player)
                self.decision_menu("Am I going to die?",[35,260], self.scene1_a, 2, player)
                self.decision_menu("I can't breathe.", [35,320], self.scene1_a, 3, player)

            pygame.display.update()
            self.clock.tick(60)

    def scene1_a(self, count, player):
        scene1_scared = True
        while scene1_scared:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.scene2(0,player)

            if count == 1:
                bg = background("images/backgrounds/FIRE.jpg")
                father = character("images/characters/Tomiichi/Tomiichi2.png")
                name = namebox("Tomiichi")
                dialogue = textbox("Don't be scared, my child. Help is on their way. Hang in there.")

            elif count == 2:
                bg = background("images/backgrounds/FIRE.jpg")
                father = character("images/characters/Tomiichi/Tomiichi2.png")
                name = namebox("Tomiichi")
                dialogue = textbox("You are not going to die, Kimiko. The best doctors will treat you and you'll be cured in no time.")

            elif count == 3:
                bg = background("images/backgrounds/FIRE.jpg")
                father = character("images/characters/Tomiichi/Tomiichi2.png")
                name = namebox("Tomiichi")
                dialogue = textbox("Relax, my child. Breathe in. Breathe out. \nIt'll only worsen your condition if you panic.")

            self.screen.blit(bg.image,bg.rect) 
            self.screen.blit(father.image, father.rect)
            self.screen.blit(dialogue.image, dialogue.rect)
            self.screen.blit(name.image, name.rect)   
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            pygame.display.update()
            self.clock.tick(60)

    def scene2(self, count, player):
        #pygame.mixer.Sound.stop(ambulance.sound)
        bg = background("images/backgrounds/bedroom_day.png")
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        scene2 = True
        #count = 0
        play = True
        while scene2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1

            #backgrounds and sounds
            if count == 0:
               self.screen.fill((0,0,0))
            if count == 1:
               self.screen.fill((0,0,0))

            if count >= 2:
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 1:
                name = namebox("Kimiko")
                instruction = textbox("Uh, what happened?")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                father = character("images/characters/Tomiichi/Tomiichi1_upset1.png")
                name = namebox("Tomiichi")
                instruction = textbox("You got into an accident, sweetie, but you’re okay now.")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Kimiko")
                instruction = textbox("Why do I feel different?")
                father = character("images/characters/Tomiichi/Tomiichi1_upset1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                father = character("images/characters/Tomiichi/Tomiichi1_upset1.png")
                name = namebox("Tomiichi")
                instruction = textbox("Well there were slight complications to the accident. For now, you are not allowed outside the house under any circumstances.")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Kimiko")
                instruction = textbox("What? But Why? What exactly happened? ")
                father = character("images/characters/Tomiichi/Tomiichi1_upset1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                father = character("images/characters/Tomiichi/Tomiichi1_upset1.png")
                name = namebox("Tomiichi")
                instruction = textbox("It’s complicated, sweetie. To make the long story short, the doctors had to operate on your heart, but don’t worry, there are caretakers here to look after you. They’ll give you everything you need. This is really difficult for me too, Kamiko. I think it’s best if we don’t question the doctors. We all just want what is best for you. ")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 7:
                self.scene3(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene3(self, count, player):
        bg = background("images/backgrounds/bedroom_day.png")
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        scene3 = True
        #count = 0
        play = True
        while scene3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1

            #backgrounds and sounds
            if count == 0:
               self.screen.fill((0,0,0))
            if count >= 1:
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("(I remember my accident so well. It has been a decade since then. I am 17 now. I hope I will be able to live normally again. I guess only time will tell.)")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                self.scene4(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene4(self, count, player):
        bg = background("images/backgrounds/stairs day.png")
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        scene4 = True
        #count = 0
        play = True
        while scene4:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1

            #backgrounds and sounds
            if count == 0:
               self.screen.fill((0,0,0))
            if count >= 1:
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 1:
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                name = namebox("Tomiichi")
                instruction = textbox("Kimiko, I’m going out of town for a business trip and I leave tonight. ")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("Can I come?")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                name = namebox("Tomiichi")
                instruction = textbox("Of course not, sweetie. It has already been ten years and not once have you left the house. Who knows what might happen? ")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("Exactly!! It’s high time that I get a feel of what the outside world is like")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                name = namebox("Tomiichi")
                instruction = textbox("But, the doctors haven’t cleared you yet. This is the end of the discussion. Behave, okay? I trust you.")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("Fine, whatever.")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                name = namebox("Tomiichi")
                instruction = textbox("I’ll see you soon.")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 8:
                self.scene5(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene5(self, count, player):
        bg = background("images/backgrounds/bedroom_day.png")
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        scene5 = True
        #count = 0
        play = True
        while scene5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Dad’s going to be gone a few days. I honestly think that nothing bad can happen. I’m sure it’s nothing about the outdoor air or anything health related because I always leave my windows open.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Kimiko")
                instruction = textbox("Maybe he’s just scared that he might lose me. I’ll be extra careful. I just want a few hours to explore the outdoors. But at the same time, what if there’s really something I should avoid?")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("This home has kept me safe for so long already. I’m sure this house won’t fail me now.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 3:
                decision = decisionbox("What will you do?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("GO TO THE KITCHEN", [35,200], self.scene5_a, 1, player)
                self.decision_menu("SNEAK OUT OF THE HOUSE ",[35,240], self.scene5_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene5_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene6a(0,player)
            elif count == 2:
                self.scene6b(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene6a(self, count, player):
        bg = background("images/backgrounds/kitchen day.png")
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("What? Why am I suddenly in the kitchen? I thought I wanted to explore beyond the walls of this house? I don’t remember feeling hungry. I just ate 30 minutes ago.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What will you do?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("GRAB A SNACK", [35,200], self.scene6_a, 1, player)
                self.decision_menu("SNEAK OUT OF THE HOUSE ",[35,240], self.scene6_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene6_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene7a(0,player)
            elif count == 2:
                self.scene6b(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene7a(self, count, player):
        bg = background("images/backgrounds/kitchen day.png")
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("That was oddly satisfying. Now I feel sleepy. Maybe I should lie down. What is happening to me? A minute ago I wanted to leave the house and now the thought of laying on the couch seems so inviting.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What will you do?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("GO TO THE LIVING ROOM", [35,200], self.scene7_a, 1, player)
                self.decision_menu("SNEAK OUT OF THE HOUSE ",[35,240], self.scene7_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene7_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene8a(0,player)
            elif count == 2:
                self.scene6b(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene8a(self, count, player):
        bg = background("images/backgrounds/sala day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player
            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Okay, so I guess I am really sleepy. Maybe the thought of the adventure in leaving the house was just in my subconscious.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What will you do?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("LAY ON THE COUCH", [35,200], self.scene8_a, 1, player)
                self.decision_menu("SNEAK OUT OF THE HOUSE ",[35,240], self.scene8_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene8_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene9a(0,player)
            elif count == 2:
                self.scene6b(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene9a(self, count, player):
        bg = background("images/backgrounds/sala night.png")
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("*Yawn* Oh! I fell asleep! What is happening to me? I feel like my mind is so clouded. I remember that dad went left for a business trip so I was supposed to leave the house, the next thing I know, I was eating, and now here I am. This is kind of creepy. I was never one to change my mind so quickly. All these years I always thought that I know what I want.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What will you do?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("CONTEMPLATE ON WHAT HAS HAPPENED", [35,200], self.scene9_a, 1, player)
                self.decision_menu("SNEAK OUT OF THE HOUSE ",[35,240], self.scene9_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene9_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene10a(0, player)
            elif count == 2:
                self.scene6b(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene10a(self, count, player):
        bg = background("images/backgrounds/sala day.png")
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I can’t seem to calm down. Maybe, I should go to my room. Something might be able to calm me down and help me decide. Or maybe, taking a walk will help me clear my mind. How frustrating?! Here I am again thinking about going out!")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What will you do?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("GO TO ROOM", [35,200], self.scene10_a, 1, player)
                self.decision_menu("SNEAK OUT OF THE HOUSE ",[35,240], self.scene10_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene10_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene11a(0,player)
            elif count == 2:
                self.scene6b(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene11a(self, count, player):
        bg = background("images/backgrounds/bedroom_day.png")
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("*pacing around* This is madness. Maybe something strange really is happening. Something is really messing with me… Or SOMEONE?! Hmmm… What am I thinking about right now?")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What am I thinking about right now?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("THIS IS ALL JUST A DREAM", [35,200], self.scene11_a, 1, player)
                self.decision_menu("LEAVING THE HOUSE",[35,240], self.scene11_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene11_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene12a1(0,player)
            elif count == 2:
                self.scene12a2(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene12a1(self, count, player):
        bg = background("images/backgrounds/bedroom_day.png")
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("If this is a dream, I should probably wake up and face reality.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("How do you wish to wake yourself up?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("PINCH YOURSELF", [35,200], self.scene12a1_a, 1, player)
                self.decision_menu("TALK TO YOURSELF",[35,240], self.scene12a1_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene12a1_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene12a1(0,player)
            elif count == 2:
                self.scene13a1(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene12a2(self, count, player):
        bg = background("images/backgrounds/bedroom_day.png")
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("That’s exactly what was on my mind. Guess I was just a little bit nervous in leaving the house. Guess I should get ready to go now. I’m sure dad will understand.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                self.scene6b(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene13a1(self, count, player):
        bg = background("images/backgrounds/bedroom_day.png")
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("This is all just a dream?! It’s not. Just so it’s clear, this is one of the most real life experiences I have ever had. I HAVE BEEN STUCK HERE FOR TEN YEARS! I’M SURE THIS REAL.")
                kimiko = character("images/characters/Kimiko (Daughter)/Kimiko7_angry3.png")
                self.screen.blit(kimiko.image, kimiko.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("Who are you?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("I AM YOU AND YOU ARE ME", [35,200], self.scene13a1_a, 1, player)
                if player.endurance == 5 and player.willpower == 5:
                    self.decision_menu("I AM A PLAYER FROM THE REAL WORLD",[35,240], self.scene13a1_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene13a1_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene14a1(0,player)
            elif count == 2:
                self.scene14a2(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene14a1(self, count, player):
        bg = None
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count == 0:
                bg = background("images/backgrounds/bedroom_day.png")
                self.screen.blit(bg.image,bg.rect)
            elif count >= 1:
                self.screen.fill((0,0,0))
                bg = background("images/backgrounds/crack.png")
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Who are you? Who am I? I think I am going crazy. This is not me… This is not me...  This is not me… This is not me… This is not me… This is not me… This is not me...")
                kimiko = character("images/characters/Kimiko (Daughter)/Kimiko3_upset2.png")
                self.screen.blit(kimiko.image, kimiko.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count > 0:
                self.credits()
            pygame.display.update()
            self.clock.tick(60)

    def scene14a2(self, count, player): #credit
        bg = None
        pygame.mixer.music.fadeout(1000)
        intro = music("music/background_music/Almost New.mp3", 1)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count == 0:
                bg = background("images/backgrounds/bedroom_day.png")
                self.screen.blit(bg.image,bg.rect)
            elif count >= 1:
                self.screen.fill((0,0,0))
                bg = background("images/backgrounds/crack.png")
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Player")
                instruction = textbox("Kimiko, this is only a game. You are in a visual novel. Nothing in your world is real. You are just a figment of imagination of the creators. I wish you the best.")
                kimiko = character("images/characters/Kimiko (Daughter)/Kimiko7_upset2.png")
                self.screen.blit(kimiko.image, kimiko.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count > 0:
                self.credits()
            pygame.display.update()
            self.clock.tick(60)

    #-------------------------------------------------------------------------------------------------------------------------------
    def scene6b(self, count, player):
        bg = background("images/backgrounds/house out day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Wow! I’m finally out of the house! I don’t think anything will happen to me. I feel fine. But, where do I go now? Wait! If I remember correctly, the city isn’t so far from here.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                self.scene7b(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene7b(self, count, player):
        bg = None
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                bg = background("images/backgrounds/cafe out day.png") #INSERT CITY BG HERE
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I’m finally in the city. I think I’m a bit tired though. Should I keep walking around? Or do I rest in that cafe?")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("Where will you go?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("GO TO THE CAFE ", [35,200], self.scene7b_a, 1, player)
                self.decision_menu("KEEP WALKING AROUND",[35,240], self.scene7b_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene7b_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene8b(0,player)
            elif count == 2:
                self.scene8c(0,player)
            pygame.display.update()
            self.clock.tick(60)

    #HACKER ROUTE HACKER ROUTE HACKER ROUTE HACKER ROUTE HACKER ROUTE HACKER ROUTE HACKER ROUTE HACKER ROUTE HACKER ROUTE 
    def scene8b(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player
            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Oh! There seems to be a lot of people. There is one free seat though. But some guy is occupying half the table.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What will you do?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("ASK IF YOU CAN SIT BESIDE HIM", [35,200], self.scene8b_a, 1, player)
                self.decision_menu("WAIT FOR AN EMPTY TABLE",[35,240], self.scene8b_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene8b_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene9b(0, player)
            elif count == 2:
                self.scene9d(0,player)
            pygame.display.update()
            self.clock.tick(60)
 
    def scene8c(self, count, player):
        bg = background("images/backgrounds/street day.png")#temporary bg
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player
            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Hmmm… This is nice. I can’t believe I’m finally out of the house.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("Which way will you turn? ")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("LEFT", [35,200], self.scene8c_a, 1, player)
                self.decision_menu("RIGHT",[35,240], self.scene8c_a, 1, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene8c_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene9c(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene9c(self, count, player):
        bg = background("images/backgrounds/street day.png")#temporary bg
        pygame.mixer.music.fadeout(1000)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("It seems like nothing is happening to me… I’m just going in circles… Is this pointless? Did I just waste my time?")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What will you do now?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("KEEP WALKING", [35,200], self.scene9c_a, 1, player)
                self.decision_menu("GO BACK HOME… MAYBE",[35,240], self.scene9c_a, 1, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene9c_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene10d(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene9b(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
               
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Um, hello there! Is this seat occupied?")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Takumi")
                instruction = textbox("No, it isn’t. Take a seat.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_happy4.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 2:
                decision = decisionbox("What will you do next?")
                takumi = character_decision("images/characters/Takumi (Hacker)/Takumi1_happy4.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("MAKE SMALL TALK WITH THE GUY", [35,200], self.scene9b_a, 1, player)
                self.decision_menu("STAY QUIET & WAIT FOR HIM TO LEAVE ",[35,240], self.scene9b_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene9b_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene10b(0, player)
            elif count == 2:
                self.scene9d(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene10b(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Hello!! What’s your name, mister?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_happy5.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Takumi")
                instruction = textbox("Takumi")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_happy5.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("Well, what brings you here today, mister Takumi?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_happy5.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Takumi")
                instruction = textbox("Just here to check out the players. I come here everyday.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_happy5.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("Players?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_happy5.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Takumi")
                instruction = textbox("Yea, the real ones. Are you real?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_happy5.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("Huh? What are you talking about?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_happy5.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                name = namebox("Takumi")
                instruction = textbox("Oh nothing. What’s your name?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_happy5.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 8:
                name = namebox("Kimiko")
                instruction = textbox("Oh it’s Kimiko?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_happy5.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 9:
                name = namebox("Takumi")
                instruction = textbox("Oh okay. I like it. And how about you, what brings you here?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_happy5.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 10:
                decision = decisionbox("What will you say?")
                takumi = character_decision("images/characters/Takumi (Hacker)/Takumi1_happy5.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("SHARE THE REAL REASON", [35,200], self.scene10b_a, 1, player)
                self.decision_menu("DON’T SHARE TOO MUCH",[35,240], self.scene10b_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene10b_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene11b(0, player)
            elif count == 2:
                self.scene11b2(0, player)
            pygame.display.update()
            self.clock.tick(60)

    # DONT FORGET 11b.2 DONT FORGET 11b.2 DONT FORGET 11b.2 DONT FORGET 11b.2 DONT FORGET 11b.2 DONT FORGET 11b.2 DONT FORGET 11b.2 DONT FORGET 11b.2 
    def scene11b(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Well… I have been stuck at home for 10 years. I haven’t been allowed to leave but I don’t really know why. All I know is that I got into an accident when I was little, and now I am here.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi3_happy4.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Takumi")
                instruction = textbox("Interesting… Ten years is a really long time. Well since you haven’t been outside in quite a while, you can ask me anything or even talk about anything you want.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi3_happy4.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 2:
                decision = decisionbox("What will you say?")
                takumi = character_decision("images/characters/Takumi (Hacker)/Takumi3_happy4.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("INVITE HIM TO YOUR HOUSE", [35,200], self.scene11b_a, 1, player)
                self.decision_menu("ASK ABOUT THE CITY",[35,240], self.scene11b_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene11b_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene12b(0, player)
            elif count == 2:
                self.scene11b2(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene12b(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Well… Do you want to see the house I was stuck in?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi3_happy1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Takumi")
                instruction = textbox("Like go there?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi3_happy1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("Yeah, sure.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi3_happy1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Takumi")
                instruction = textbox("Woah?! Um I mean, yea sure. When will this happen?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi3_happy1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("Now.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi3_happy1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Takumi")
                instruction = textbox("Oh okay. Let’s go?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi3_happy1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("Sure.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi3_happy1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 7:
                self.scene13b(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene13b(self, count, player):
        bg = background("images/backgrounds/house out day.png")#TENTATIVE BG NEEDS FATHER IN THE BG OR SOMETHING
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Oh look it’s my dad!")
                takumi = character("images/characters/Takumi (Hacker)/Takumi13_confused1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Takumi")
                instruction = textbox("Is he allowed to see me? What if he gets mad?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi13_confused1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 2:
                decision = decisionbox("What will you do?")
                takumi = character_decision("images/characters/Takumi (Hacker)/Takumi13_confused1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("RUN HOME & LEAVE TAKUMI THERE ", [35,200], self.scene13b_a, 1, player)
                self.decision_menu("TELL TAKUMI TO HIDE",[35,240], self.scene13b_a,1, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene13b_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene14b(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene14b(self, count, player):
        bg = background("images/backgrounds/sala day.png")
        pygame.mixer.music.fadeout(1000)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Hi dad! How did your business trip go?")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Tomiichi")
                instruction = textbox("It was fine. How about you, did you behave? ")
                father = character("images/characters/Tomiichi/Tomiichi2_smirk4.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("Yes I did. Of course.")
                father = character("images/characters/Tomiichi/Tomiichi2_smirk4.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Tomiichi")
                instruction = textbox("You should get some rest. You look tired.")
                father = character("images/characters/Tomiichi/Tomiichi2_smirk4.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("Yea, okay. See you.")
                father = character("images/characters/Tomiichi/Tomiichi2_smirk4.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 5:
                self.scene15b(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene15b(self, count, player):
        bg = background("images/backgrounds/bedroom_night.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Dad did not seem suspicious at all… Did he notice anything? Hmmm. And what should I do about Takumi? I just left him there. That was quite mean. Maybe if I go back to the coffee shop, he’d be there. He did say he goes there everyday. Or should I just stay home again so that dad will never find out what happened, and I’ll never get caught…")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What will you do?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("GO BACK TO CAFE TO MEET TAKUMI AGAIN", [35,200], self.scene15b_a, 1, player)
                self.decision_menu("STAY HOME AND NEVER SPEAK & THINK ABOUT IT",[35,240], self.scene15b_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    #DONT FORGER 15z DONT FORGER 15z DONT FORGER 15z DONT FORGER 15z DONT FORGER 15z DONT FORGER 15z DONT FORGER 15z DONT FORGER 15z 
    def scene15b_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene16b(0,player)
            elif count == 2:
                self.scene15z(o,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene16b(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox(" I’m so sorry I left you last time. My dad, you see, he’s just a little complicated.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset3.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Takumi")
                instruction = textbox("Yes I know. In fact, I know exactly what’s up…")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset3.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("What is it?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset3.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Takumi")
                instruction = textbox("You see, this is all just a game. Me? I exist in real life. I just sync my brain into the game and play in this world, but you, you’re not real. You’re not a human synced. You’re not an element in this game. I think you exist just for you dad. You died, you know, in your accident.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset3.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("How do you know all this?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset3.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Takumi")
                instruction = textbox("Well, in the real world, I am a hacker. I traced your house in an unplayable location on the map, and when I saw you in the cafe, I knew that you were from there, so I just needed to figure out why you existed. I broke into the game’s database/server and found everything I needed. Your dad, made this game and put you in it.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset3.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox(" But… This can’t be happening… Everything feels so real. You feel so real.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset3.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                name = namebox("Takumi")
                instruction = textbox("Your dad is about to find out that you’re gone and what you have been doing. He’s going to take you out of here forever. We should move quickly.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset3.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 8:
                name = namebox("Kimiko")
                instruction = textbox("What should we do? I’m scared.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset3.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 9:
                name = namebox("Takumi")
                instruction = textbox("I’ve got you. We have a few more minutes until you disappear. Where do you want to go?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset3.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 10:
                decision = decisionbox("Where will you go?")
                takumi = character_decision("images/characters/Takumi (Hacker)/Takumi1_upset3.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(decision.image, decision.rect)
                if player.persuasion == 5 and player.optimism == 5:
                    self.decision_menu("FAR AWAY FROM HERE", [35,200], self.scene16b_a, 1, player)
                self.decision_menu("SOMEWHERE SAFE",[35,240], self.scene16b_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene16b_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene17b(0, player)
            elif count == 2:
                self.scene17b2(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene17b(self, count, player):
        bg = None
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                #self.screen.fill((0,0,0))
                bg = background("images/backgrounds/16452741.jpg")
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 1:
                name = namebox("Takumi")
                instruction = textbox("I’ve brought you to the Beyond. Through this route we’ll be able to transport to different games I loved  while I was growing up so that your dad will never find us. We’re going on an adventure!")
                takumi = character("images/characters/Takumi (Hacker)/Takumi9_poker1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 2:
                self.credits()
            pygame.display.update()
            self.clock.tick(60)

    def scene17b2(self, count, player): #credit
        bg = background("images/backgrounds/IMG_3174.png")#TEMPORARY BG
        pygame.mixer.music.fadeout(1000)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Takumi")
                instruction = textbox("I think we’re safe here.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Kimiko")
                instruction = textbox("I feel kind of strange though")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Takumi")
                instruction = textbox("Oh no! I don’t think this place is safe enough. Quick! We better hurry to get somewhere safe.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Kimiko")
                instruction = textbox("Takumi, it’s fine. It’s okay. I accept it.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Takumi")
                instruction = textbox("What?")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Kimiko")
                instruction = textbox("I didn’t listen to my dad or whoever he is. I’m going to be deleted in this game. This is my fate. I already vanished once. It’s time for me to vanish permanently. Good bye.")
                takumi = character("images/characters/Takumi (Hacker)/Takumi1_upset1.png")
                self.screen.blit(takumi.image, takumi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 6:
                self.credits()
            pygame.display.update()
            self.clock.tick(60)

    #MODERATOR ROUTE MODERATOR ROUTE MODERATOR ROUTE MODERATOR ROUTE MODERATOR ROUTE MODERATOR ROUTE MODERATOR ROUTE MODERATOR ROUTE MODERATOR ROUTE MODERATOR ROUTE MODERATOR ROUTE 
    def scene9d(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("This is taking so long. It seems like no one is leaving anytime soon…")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What will you do next?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("KEEP WAITING", [35,200], self.scene9d_a, 1, player)
                self.decision_menu("GO BACK HOME",[35,240], self.scene9d_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene9d_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene10d(0,player)
            elif count == 2:
                self.scene10d2(0,player)
            pygame.display.update()
            self.clock.tick(60)

    #DONT FORGET 10d2 DONT FORGET 10d2 DONT FORGET 10d2 DONT FORGET 10d2 DONT FORGET 10d2 DONT FORGET 10d2 DONT FORGET 10d2 DONT FORGET 10d2 DONT FORGET 10d2 
    def scene10d(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Random Stranger")
                instruction = textbox("Hello! I can’t help but notice you all the way from over there. You look quite familiar… What’s your name?")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Kimiko")
                instruction = textbox("Oh um hi")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_happy7.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("This is kinda odd… Why did he approach me out of nowhere")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_happy7.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 3:
                decision = decisionbox("What will you do next?")
                hiroshi = character_decision("images/characters/Hiroshi (Moderator)/Hiroshi2_happy7.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("TALK TO HIM", [35,200], self.scene10d_a, 1, player)
                self.decision_menu("IGNORE HIM",[35,240], self.scene10d_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene10d_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene11d(0,player)
            elif count == 2:
                self.scene11f(0,player)
            pygame.display.update()
            self.clock.tick(60)

    #DONT FORGET 11f DONT FORGET 11f DONT FORGET 11f DONT FORGET 11f DONT FORGET 11f DONT FORGET 11f DONT FORGET 11f DONT FORGET 11f 
    def scene11d(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I’m Kimiko. What’s your name?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi3_happy2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Hiroshi")
                instruction = textbox("I’m Hiroshi")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi3_happy2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("Oh hello! Nice meeting you, I guess…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi3_happy2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Hiroshi")
                instruction = textbox("Do you wanna sit down with me and have a drink?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi3_happy2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 4:
                decision = decisionbox("What will you do next?")
                hiroshi = character_decision("images/characters/Hiroshi (Moderator)/Hiroshi3_happy2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("SIT DOWN AND HAVE A DRINK WITH HIROSHI", [35,200], self.scene11d_a, 1, player)
                self.decision_menu("SAY YOU HAVE TO GO",[35,240], self.scene11d_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene11d_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene12d(0, player)
            elif count == 2:
                self.scene11f(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene12d(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Hiroshi")
                instruction = textbox("You shouldn’t be here. It’s dangerous")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_troubled2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Kimiko")
                instruction = textbox("Uhh… (To herself) This is getting pretty strange. I don’t know if I should be scared or what?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_troubled2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 2:
                decision = decisionbox("What will you do next?")
                hiroshi = character_decision("images/characters/Hiroshi (Moderator)/Hiroshi2_troubled2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("ASK ABOUT WHAT HE MEANS", [35,200], self.scene12d_a, 1, player)
                self.decision_menu("LEAVE THE TABLE",[35,240], self.scene12d_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene12d_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene13d(0, player)
            elif count == 2:
                self.scene11f(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene11f(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I have to go now. I’m sorry. ")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_troubled2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Hiroshi")
                instruction = textbox("Oh okay…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_troubled2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 2:
                decision = decisionbox("Where will you go now?")
                hiroshi = character_decision("images/characters/Hiroshi (Moderator)/Hiroshi2_troubled2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("HOME", [35,200], self.scene11f_a, 1, player)
                self.decision_menu("JUST AWAY FROM HERE",[35,240], self.scene11f_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene11f_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene10d2(0, player)
            elif count == 2:
                self.scene11e(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene10d2(self, count, player):
        bg = background("images/backgrounds/outside_day.png") #tentative bg 
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Hmm… I guess to some extent my dad was right. I should not have gone out. There isn’t even anything to see. Should I still try to make the most out of this trip?")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What will you do next?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("NO… SO TAKE SHORT ROUTE", [35,200], self.scene10d2_a, 1, player)
                self.decision_menu("YES… MAYBE… SO TAKE THE LONG ROUTE",[35,240], self.scene10d2_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene10d2_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene11d2(0, player)
            elif count == 2:
                self.scene11e(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene11d2(self, count, player):
        bg = background("images/backgrounds/outside_day.png") #tentative bg 
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Hmmm… It seems like there’s this unsettling feeling at the back of my mind… I wonder how I should feel right now?")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What are you feeling right now?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("WORRIED", [35,200], self.scene11d2_a, 1, player)
                self.decision_menu("CAREFREE BECAUSE DAD LOVES ME",[35,240], self.scene11d2_a, 1, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene11d2_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene12d2(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene12d2(self, count, player):
        bg = background("images/backgrounds/street day.png") #tentative bg 
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player
            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox(" I guess it doesn’t matter what I feel… All that matters is how I deal with all this…")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What are you going to do now?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("GET SOMETHING FOR REMEMBRANCE", [35,200], self.scene12d2_a, 1, player)
                self.decision_menu("HURRY HOME SO DAD WON’T FIND OUT",[35,240], self.scene12d2_a, 1, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene12d2_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene13d2(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene13d2(self, count, player):
        bg = background("images/backgrounds/house out day.png") #tentative bg 
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I guess that is what I should do so this trip won’t be so bad… Hmm… Oh! I’m already near home… There’s dad!! Guess I should hurry and enter from the back so dad won’t see me.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                self.scene14d3(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene14d3(self, count, player):
        bg = background("images/backgrounds/stairs day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Oh hi dad! You’re back! How was everything!!")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Tomiichi")
                instruction = textbox("Good, good! And you, how did you spend your time?")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("I didn’t do much… As always.")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Tomiichi")
                instruction = textbox("You okay? You look like something is bothering you…")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("Oh, It’s nothing…")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Tomiichi")
                instruction = textbox("Are you sure? You know you can talk to me about anything…")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("Uh well…")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 7:
                decision = decisionbox("What are you going to say?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("NOTHING", [35,200], self.scene14d3_a, 1, player)
                self.decision_menu("ASK ABOUT THE OUTSIDE WORLD",[35,240], self.scene14d3_a, 1, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene14d3_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene15d21(0, player)
            if count == 2:
                self.scene15d22(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene15d21(self, count, player):
        bg = background("images/backgrounds/stairs day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Oh it’s nothing… Really I’m fine.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Tomiichi")
                instruction = textbox("Okay, if you say so…")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("Yea. Nothing to worry about.")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                self.screen.fill((0,0,0))
            if count >= 4:
                self.scene15z(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene15d22(self, count, player):
        bg = background("images/backgrounds/stairs day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Oh well… I just wanted to ask…")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Tomiichi")
                instruction = textbox("What is it?")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("What is it like in the outside world? ")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Tomiichi")
                instruction = textbox("Why do you want to know so bad? Are you planning anything bad?")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("Of course not dad… You know, ten years is just A LOT.")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Tomiichi")
                instruction = textbox("Well yea, I get your point, but honey, you’re really not missing out on anything.")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("If you say so…")
                father = character("images/characters/Tomiichi/Tomiichi4_smirk1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                self.screen.fill((0,0,0))
            if count >= 8:
                self.scene15z(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene13d(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player
            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Care to explain what you meant?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_smirk2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Hiroshi")
                instruction = textbox("You first!! What do you wanna talk about? I feel like there’s something on your mind after so long…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_smirk2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("That’s weird. What does he even mean by so long? Does he know about my 10 years?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_smirk2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 3:
                decision = decisionbox("What will you talk about?")
                hiroshi = character_decision("images/characters/Hiroshi (Moderator)/Hiroshi2_smirk2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("ASK ABOUT HIROSHI INSTEAD", [35,200], self.scene13d_a, 1, player)
                self.decision_menu("TALK ABOUT ACCIDENT",[35,240], self.scene13d_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene13d_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene14d(0, player)
            elif count == 2:
                self.scene14d2(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene14d(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I just wanna get to know as much people as I can really…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Hiroshi")
                instruction = textbox("Oh yea? Well I think 10 years is just too long… The world wants to hear more about you, Kimiko.")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("Huh? Ten years of what?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Hiroshi")
                instruction = textbox("Being trapped at home?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("How did you know about that?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Hiroshi")
                instruction = textbox("Didn’t you mention it earlier?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("No…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                name = namebox("Hiroshi")
                instruction = textbox("I swear I think you did…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 8:
                self.screen.fill((0,0,0))
            if count >= 9:    
                self.scene15d(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene14d2(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Well I was in accident before and my life has changed dramatically since then…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Hiroshi")
                instruction = textbox("Well yea… A lot can change in 10 years…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("Huh? Ten years? What’s with 10 years?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Hiroshi")
                instruction = textbox("Oh ten years at home?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("How do you know that?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Hiroshi")
                instruction = textbox("You mention it earlier...")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("No I did not…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                name = namebox("Hiroshi")
                instruction = textbox("I swear I think you did…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_confused2.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 8:
                self.screen.fill((0,0,0))
            if count >= 9:    
                self.scene15d(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene15d(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("You’re so strange… How do you know about all that? Are you a stalker?!")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Hiroshi")
                instruction = textbox("No!! I’m not… I promise!!")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("Then tell me the truth!")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Hiroshi")
                instruction = textbox("Okay… Are you sure?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("Yes I am sure.")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Hiroshi")
                instruction = textbox("Okay, so your dad makes me watch over his creation so that it will be a safe place…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("By creation, you mean me?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                name = namebox("Hiroshi")
                instruction = textbox("No… This game, Kimiko.")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 8:
                name = namebox("Kimiko")
                instruction = textbox("Huh? What game?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 9:
                name = namebox("Hiroshi")
                instruction = textbox("This whole thing… This is all just a game.")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 10:
                name = namebox("Kimiko")
                instruction = textbox("What do you mean?!")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 11:
                name = namebox("Hiroshi")
                instruction = textbox("I think I understand what is happening now…You haven’t been allowed out of the house for 10 years now right?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 12:
                name = namebox("Kimiko")
                instruction = textbox("Yes.")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 13:
                name = namebox("Hiroshi")
                instruction = textbox("This game is about 10 years old. And 10 years ago, insert name of dad encountered a really bad accident with his family and it was on the news that someone died… Maybe that’s you… He could have possibly uploaded you onto the game and maybe that’s why he didn’t let you leave the house...")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 14:
                name = namebox("Kimiko")
                instruction = textbox("This can’t be happening… What should I do, insert name of moderator.")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 15:
                name = namebox("Hiroshi")
                instruction = textbox("Well you have two options. We can go yo your dad and tell him everything because he might be able to fix this or we can just find some place where we can stay if you’re too overwhelmed with everything I just told you…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 16:    
                decision = decisionbox("What will you choose to do?")
                hiroshi = character_decision("images/characters/Hiroshi (Moderator)/Hiroshi2_shocked5.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("STAY WITH HIROSHI", [35,200], self.scene15d_a, 1, player)
                if player.persuasion == 5 and player.willpower == 5:
                    self.decision_menu("GO TO DAD",[35,240], self.scene15d_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene15d_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene16d(0, player)
            elif count == 2:
                self.scene16d2(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene16d(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I think I’d like to stay with you…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_poker3.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Hiroshi")
                instruction = textbox("You sure?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_poker3.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("Yea, I think you told me more truths in the past hour than my dad has in 10 years…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_poker3.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Hiroshi")
                instruction = textbox("Okay if you say so… We gotta go then, your dad might notice that something is off…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_poker3.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("Yea, okay…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_poker3.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 5:
                self.scene17d(0 ,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene17d(self, count, player):
        bg = None
        pygame.mixer.music.fadeout(1000)
        #count = 1
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                bg = background("images/backgrounds/weird area.png")
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)

            if inspect.isclass(new_player) == True:
                player = new_player
            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Hiroshi")
                instruction = textbox("We’re here in the Middle. This is sort of the safe space of this game. Only the employees know about this place…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_happy8.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Kimiko")
                instruction = textbox("What if the other employees of my dad recognize me?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_happy8.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Hiroshi")
                instruction = textbox("They won’t! Believe me when I say no one knows about you…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_happy8.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Kimiko")
                instruction = textbox("But how about exploring? I wanna get to see what this world is like?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_happy8.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Hiroshi")
                instruction = textbox("You can do more of that here. Promise. I’ll be with you every step of the way")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_happy8.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 5:
                self.credits()
            pygame.display.update()
            self.clock.tick(60)

    def scene16d2(self, count, player): #credit
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count <= 3:
                self.screen.fill((0,0,0))
                bg = background("images/backgrounds/cafe in day.png")
                self.screen.blit(bg.image,bg.rect)
            if count >= 4:
                bg = background("images/backgrounds/stairs day.png")
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I think I’ll just go back to my dad…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_poker3.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Hiroshi")
                instruction = textbox("Okay, if you say so. Do you want me to accompany you back home?")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_poker3.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("No thank you. I’ll manage by myself, as always")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_poker3.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Hiroshi")
                instruction = textbox("Okay, you must get going then…")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi2_poker3.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("Dad, are you back?")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                father = character("images/characters/Tomiichi/Tomiichi3_angry3.png")
                name = namebox("Tomiichi")
                instruction = textbox("Yes, sweetie? What is it?")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("I met Hiroshi, one of your staff…")
                father = character("images/characters/Tomiichi/Tomiichi3_angry3.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                father = character("images/characters/Tomiichi/Tomiichi3_angry3.png")
                name = namebox("Tomiichi")
                instruction = textbox("YOU WENT OUT?!")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 8:
                name = namebox("Kimiko")
                instruction = textbox("Well yea, but I think that’s besides the point right now. I can’t believe you’d do this to me…")
                father = character("images/characters/Tomiichi/Tomiichi3_angry3.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 9:
                father = character("images/characters/Tomiichi/Tomiichi3_angry3.png")
                name = namebox("Tomiichi")
                instruction = textbox("I had to honey, the accident 10 years ago killed you.")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 10:
                name = namebox("Kimiko")
                instruction = textbox("Well that’s what I should be… DEAD. ")
                father = character("images/characters/Tomiichi/Tomiichi3_angry3.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 11:
                father = character("images/characters/Tomiichi/Tomiichi3_angry3.png")
                name = namebox("Tomiichi")
                instruction = textbox("You don’t understand-")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 12:
                name = namebox("Kimiko")
                instruction = textbox("I understand everything pretty clearly! I am living a stolen life! Kill me now! ")
                father = character("images/characters/Tomiichi/Tomiichi3_angry3.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 13:
                father = character("images/characters/Tomiichi/Tomiichi3_angry3.png")
                name = namebox("Tomiichi")
                instruction = textbox("Okay, if that’s what you want…")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 14:
                self.screen.fill((0,0,0)) 
            if count >= 15:
                self.credits()
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()
        quit()
    
    #KATSUO ROUTE KATSUO ROUTE KATSUO ROUTE KATSUO ROUTE KATSUO ROUTE KATSUO ROUTE KATSUO ROUTE KATSUO ROUTE 
    def scene11e(self, count, player):
        bg = background("images/backgrounds/street day.png")#tentative bg
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            self.button_menu("SHOP", [400,600])
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Hmmm… This all seems kinda creepy… There’s something that’s not sitting well with me about this place. How should I even act?")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What will you do?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("WALK SLOW ", [35,200], self.scene11e_a, 1, player)
                self.decision_menu("WALK FAST",[35,240], self.scene11e_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene11e_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene12e(0, player)
            elif count == 2:
                self.scene12f(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene12e(self, count, player):
        bg = background("images/backgrounds/street day.png")#tentative bg
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I guess I should just make the most out of this whole thing.. I’m already outside anyway. Oof! *Bump sounds*")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                self.scene13e(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene13e(self, count, player):
        bg = background("images/backgrounds/street day.png")#tentative bg
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Random Person")
                instruction = textbox("Ouch!! Watch where you’re going.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo1_angry4.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Kimiko")
                instruction = textbox("Oh! I didn’t mean it!")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo1_angry4.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Random Person")
                instruction = textbox("Yea. Whatever")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo1_angry4.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Kimiko")
                instruction = textbox("(to herself) Gosh I feel bad… What should I do?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo1_angry4.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 4:
                decision = decisionbox("What will you do?")
                katsuo = character_decision("images/characters/Katsuo (Glitched NPC)/Katsuo1_angry4.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("APOLOGIZE", [35,200], self.scene13e_a, 1, player)
                self.decision_menu("WALK AWAY",[35,240], self.scene13e_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene13e_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene14e(0, player)
            elif count == 2:
                self.scene12f(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene14e(self, count, player):
        bg = background("images/backgrounds/street day.png")#tentative bg
        pygame.mixer.music.fadeout(1000)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player
            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("My goodness! I’m sorry! I really should be more aware. Are you hurt?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Random Person")
                instruction = textbox("Oh, it’s fine. I should’ve given you a enough space.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("I wanna make it up to you. How about we go get a drink?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Random Person")
                instruction = textbox("It’s fine! It’s no big deal.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("I insist.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Random Person")
                instruction = textbox("Okay. If you say so…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 6:
                self.scene15e(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene15e(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Random Person")
                instruction = textbox("So, what brings you here? I don’t think I’ve ever seen you before…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Kimiko")
                instruction = textbox("Well, I’m not really from around here…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Random Person")
                instruction = textbox("Let’s start with your name.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Kimiko")
                instruction = textbox("Oh, I’m Kimiko. What’s yours?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Katsuo")
                instruction = textbox("The name’s Katsuo. So tell me more about yourself…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Kimiko")
                instruction = textbox("Well yea as I said, I’m not from around here…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Katsuo")
                instruction = textbox("Yea, but I think there’s more about you than that. You seem to be hiding something interesting…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                name = namebox("Kimiko")
                instruction = textbox("Well…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 8:
                decision = decisionbox("What will you talk about?")
                katsuo = character_decision("images/characters/Katsuo (Glitched NPC)/Katsuo6_smirk2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("TALK ABOUT YOUR ACCIDENT", [35,200], self.scene15e_a, 1, player)
                self.decision_menu("SHIFT THE TOPIC OF THE CONVERSATION",[35,240], self.scene15e_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()
        quit()

    def scene16e(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Well if what you mean by interesting is problematic… Than yes! When I was a kid, I got into an accident and after that my dad never let me out of the house…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Katsuo")
                instruction = textbox("Oh my, but… Are you sure that’s it?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("What? What do you mean? That’s already pretty interesting, isn’t it?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Katsuo")
                instruction = textbox("Well, there seems to be something else…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                self.screen.fill((0,0,0))
            if count >= 5:
               self.scene17e(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene16e2(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Really… There’s nothing to know. This whole place seems more interesting than anything else…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo1_upset1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Katsuo")
                instruction = textbox("Uhh… Not really…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo1_upset1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                self.screen.fill((0,0,0))
            if count >= 3:
               self.scene17e(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene17e(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("WHAA?! What happened? What was that?!")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_angry3.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Katsuo")
                instruction = textbox("Nothing…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_angry3.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("Oh come on… I told you about my story. Tell me yours…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_angry3.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Katsuo")
                instruction = textbox("Well you see… I’m a glitch…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_angry3.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("What do you mean by that?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_angry3.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Katsuo")
                instruction = textbox("I’m not supposed to exist anymore…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_angry3.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("That’s insane! Are you going through something?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_angry3.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                name = namebox("Katsuo")
                instruction = textbox("Uh no… I’m a glitch.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_angry3.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 8:
                name = namebox("Kimiko")
                instruction = textbox("Glitch? What’s that?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_angry3.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 9:
                name = namebox("Katsuo")
                instruction = textbox("Huh? Why don’t you know what that is? The glitch is everywhere in this game?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_angry3.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 10:
                name = namebox("Kimiko")
                instruction = textbox("Game? Is that some kind of metaphor?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_angry3.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 11:
                self.screen.fill((0,0,0))
            if count >= 12:
               self.scene18e(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene18e(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("OH NO!?! What is happening to me?!!")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Katsuo")
                instruction = textbox("You got what I got, the glitch.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("I DON’T EVEN KNOW WHAT THAT IS?!")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Katsuo")
                instruction = textbox("Same as what I said earlier. We’re in a game. The game is called Xin. It’s like a virtual reality world where you get to live a life where you can do whatever you want to do and meet other people. The game was created by Tomiichi.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("Huh?! But but that’s my dad?!")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Katsuo")
                instruction = textbox("Have you seen your dad here recently?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("Uh yea, But he left for a business trip recently…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                name = namebox("Katsuo")
                instruction = textbox("Well your dad can fix this… Unless…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 8:
                name = namebox("Kimiko")
                instruction = textbox("Unless what?!?!")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 9:
                name = namebox("Katsuo")
                instruction = textbox("Well, since I have the glitch I have been saving everything in this game that has acquired the glitch and created my own world.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 10:
                name = namebox("Kimiko")
                instruction = textbox("That’s insane… What happens if I go to my dad instead?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 11:
                name = namebox("Katsuo")
                instruction = textbox("Well we don’t know what he might do…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 12:
                decision = decisionbox("What will you do?")
                katsuo = character_decision("images/characters/Katsuo (Glitched NPC)/Katsuo3_poker1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(decision.image, decision.rect)
                if player.courage == 5 and player.optimism == 5:
                    self.decision_menu("GO TO THE GLITCHED WORLD", [35,200], self.scene18e_a, 1, player)
                self.decision_menu("GO TO DAD AND HAVE HIM FIX EVERYTHING",[35,240], self.scene18e_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene18e_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene19e(0,player)
            elif count == 2:
                self.scene19e2(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene19e(self, count, player): #credit
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count <= 4:
                self.screen.blit(bg.image,bg.rect)
            if count >= 5:
                bg = background("images/backgrounds/maxresdefault.png")
                self.screen.blit(bg.image, bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I can’t believe everything is just a game… This is crazy. Take me to the world you built. I’d rather spend my days with you.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_angry2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Katsuo")
                instruction = textbox("But, what if something bad happens to you?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_angry2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("I trust you more than anybody else right now…")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_angry2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Katsuo")
                instruction = textbox(" Are you sure about this?")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_angry2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("As sure as I’ll ever be.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_angry2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Katsuo")
                instruction = textbox("Here we are. It’s not much, but I’m willing to share everything with you.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_angry2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("That’s more than enough.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo6_angry2.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 7:
                self.credits()
            pygame.display.update()
            self.clock.tick(60)

    def scene19e2(self, count, player):
        bg = background("images/backgrounds/cafe in day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count <= 3:
                bg = background("images/backgrounds/cafe in day.png")
                self.screen.blit(bg.image,bg.rect)
            if count >= 4:
                bg = background("images/backgrounds/house out day.png")
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I guess I’m going to go to my dad and have him right all these wrongs.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_tired1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Katsuo")
                instruction = textbox("If you think this is the right choice then go ahead.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_tired1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("Thank you for telling me about your world. I better get going.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_tired1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Katsuo")
                instruction = textbox("Yea okay.")
                katsuo = character("images/characters/Katsuo (Glitched NPC)/Katsuo2_tired1.png")
                self.screen.blit(katsuo.image, katsuo.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("Oh look, perfect, dad is just arriving. I better hurry inside.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 5:
                self.scene20e2(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene20e2(self, count, player):
        bg = background("images/backgrounds/sala day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                bg = background("images/backgrounds/sala day.png")
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Dad! I need your help.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Tomiichi")
                instruction = textbox("What is it? Oh no!")
                father = character("images/characters/Tomiichi/Tomiichi1_upset4.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("What’s wrong?")
                father = character("images/characters/Tomiichi/Tomiichi1_upset4.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Tomiichi")
                instruction = textbox("You’ve got the glitch.")
                father = character("images/characters/Tomiichi/Tomiichi1_upset4.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("Exactly!! Help me get rid of it please.")
                father = character("images/characters/Tomiichi/Tomiichi1_upset4.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Tomiichi")
                instruction = textbox("I told you that you are not allowed to leave this house. Why did you disobey me?")
                father = character("images/characters/Tomiichi/Tomiichi1_upset4.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("I don’t know what got into me. I’m so sorry.")
                father = character("images/characters/Tomiichi/Tomiichi1_upset4.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                name = namebox("Tomiichi")
                instruction = textbox("Well, you’re going to get consequences for this.")
                father = character("images/characters/Tomiichi/Tomiichi1_upset4.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 8:
                self.screen.fill((0,0,0))
            if count >= 9:
                self.scene21e2(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene21e2(self, count, player): #credit
        bg = background("images/backgrounds/bedroom_night.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                bg = background("images/backgrounds/bedroom_night.png")
                self.screen.blit(bg.image,bg.rect)
            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player
            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Uhh... What happened? I feel like I slept for the longest time. My head really hurts…")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Tomiichi")
                instruction = textbox("You got into an accident sweetie. You almost died.")
                father = character("images/characters/Tomiichi/Tomiichi3_upset1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("What?! Where am I?")
                father = character("images/characters/Tomiichi/Tomiichi3_upset1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Tomiichi")
                instruction = textbox("We moved to some place safe. What’s the last thing you remember, sweetie?")
                father = character("images/characters/Tomiichi/Tomiichi3_upset1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("I remember the sound of an ambulance and you telling me that everything’s going to be okay and that you’ll take care of me.")
                father = character("images/characters/Tomiichi/Tomiichi3_upset1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Tomiichi")
                instruction = textbox("Well that was 10 years ago sweetie.")
                father = character("images/characters/Tomiichi/Tomiichi3_upset1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Kimiko")
                instruction = textbox("What happened during all those 10 years?")
                father = character("images/characters/Tomiichi/Tomiichi3_upset1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                name = namebox("Tomiichi")
                instruction = textbox("It doesn’t matter anymore. All that matters is your safe now.")
                father = character("images/characters/Tomiichi/Tomiichi3_upset1.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 8:
                self.screen.fill((0,0,0))
            if count >= 9:
                self.credits()
            pygame.display.update()
            self.clock.tick(60)

    def scene15e_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene16e(0, player)
            elif count == 2:
                self.scene16e2(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene12f(self, count, player):
        bg = background("images/backgrounds/street day.png")#tentative bg
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.fill((0,0,0))
                bg = background("images/backgrounds/outside_day.png")#tentative bg
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Hmmm… I can’t help but think about what dad will think about this whole situation… Even I don’t know what to think.")
                hiroshi = character("images/characters/Hiroshi (Moderator)/Hiroshi1_happy1.png")
                self.screen.blit(hiroshi.image, hiroshi.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What are you feeling right now?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("WORRIED THAT DAD MIGHT GET MAD", [35,200], self.scene12f_a, 1)
                self.decision_menu("RELAX BECAUSE DAD WILL UNDERSTAND",[35,240], self.scene12f_a, 1)
            pygame.display.update()
            self.clock.tick(60)

    def scene12f_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene13f(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene13f(self, count, player):
        bg = background("images/backgrounds/street day.png")#tentative bg
        pygame.mixer.music.fadeout(1000)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count == 0:
                self.screen.fill((0,0,0))
                bg = background("images/backgrounds/outside_day.png")#tentative bg
                self.screen.blit(bg.image,bg.rect)
            if count >= 1:
                bg = background("images/backgrounds/house.png")
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player

            #character, namebox, textbox in order

            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I guess it doesn’t matter. This is all so unbelievable. I don’t know what to do with myself anymore. I guess to find out I should just head home.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Kimiko")
                instruction = textbox("Oh no!! Dad’s home. I don’t know what to do. I don’t want anything bad to happen to me and my relationship with dad. He’s the only one I’ve got left.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 2:
                decision = decisionbox("What are you feeling right now?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("HIDE FIRST AND WAIT TILL THINGS CALM DOWN", [35,200], self.scene13f_a, 1, player)
                self.decision_menu("RUN AND ENTER FROM THE BACK DOOR",[35,240], self.scene13f_a, 1, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene13f_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene15z(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene15z(self, count, player):
        bg = background("images/backgrounds/stairs day.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                bg = background("images/backgrounds/stairs day.png")
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player
            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Tomiichi")
                instruction = textbox("Kimiko, I have to talk to you about something.")
                father = character("images/characters/Tomiichi/Tomiichi2_angry3.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Kimiko")
                instruction = textbox("What is it, dad?")
                father = character("images/characters/Tomiichi/Tomiichi2_angry3.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Tomiichi")
                instruction = textbox("I’m sure you know that you’re not supposed to leave this house.")
                father = character("images/characters/Tomiichi/Tomiichi2_angry3.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Kimiko")
                instruction = textbox("Yeah, dad. It has been like this the past 10 years. How could I forget?")
                father = character("images/characters/Tomiichi/Tomiichi2_angry3.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Tomiichi")
                instruction = textbox("You’re lying to me!! I know what you did. You left while I was on a business trip.")
                father = character("images/characters/Tomiichi/Tomiichi2_angry3.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                name = namebox("Kimiko")
                instruction = textbox("What are you talking about, dad? I’ve been here this whole time.")
                father = character("images/characters/Tomiichi/Tomiichi2_angry3.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 6:
                name = namebox("Tomiichi")
                instruction = textbox("There’s no point in convincing me otherwise. I have all the proof I need. Since you have been misbehaving, you will receive the proper consequences.")
                father = character("images/characters/Tomiichi/Tomiichi2_angry3.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 7:
                self.screen.fill((0,0,0))
            if count >= 8:
                self.scene16z(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene16z(self, count, player):
        bg = background("images/backgrounds/stairs night.png")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count == 0 or count >= 3:
                bg = background("images/backgrounds/stairs night.png")
                self.screen.blit(bg.image,bg.rect)
            if count == 1 or count == 2:
                bg = background("images/backgrounds/sala night_cliff.jpg")
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player
            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Uhh… What happened? I think I passed out. I remember dad getting mad at me though. Wait… The lighting seems different today. Let me take a look.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                name = namebox("Kimiko")
                instruction = textbox("Oh my goodness! I don’t think I’m home anymore. Everything outside looks different. The house is on top of a cliff!")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Tomiichi")
                instruction = textbox("You’re right, Kimiko. We are on top of a cliff. This is what you get for not listening to me.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Tomiichi")
                instruction = textbox("I made it very clear ever since before that you were to not leave the house. This is the consequence for your actions. We now live isolated on a cliff. The reason why I did not allow you to leave the house is because you are dead. Ten years ago, the accident I told you about killed you, so I uploaded you to the company’s game server. All the people you see here are either players from the real world or characters of this world.")
                father = character("images/characters/Tomiichi/Tomiichi3_smirk4.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                name = namebox("Kimiko")
                instruction = textbox("WHAT?!")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 5:
                self.scene17z(0, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene17z(self, count, player):
        bg = background("images/backgrounds/sala night_cliff.jpg")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player
            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("I can’t believe this is happening. Nothing is real. My reality doesn’t seem to exist. I don’t know what to do anymore. I’m going to go mad.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count >= 1:
                decision = decisionbox("What will you do?")
                self.screen.blit(decision.image, decision.rect)
                self.decision_menu("ACCEPT LIFE", [35,200], self.scene17z_a, 1, player)
                if player.courage == 5 and player.endurance == 5:
                    self.decision_menu("ESCAPE THIS LIFE",[35,240], self.scene17z_a, 2, player)
            pygame.display.update()
            self.clock.tick(60)

    def scene17z_a(self, count, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
            if count == 1:
                self.scene20z(0,player)
            elif count == 2:
                self.scene20z2(0,player)
            pygame.display.update()
            self.clock.tick(60)

    def scene20z(self, count, player): #credit
        bg = background("images/backgrounds/sala night_cliff.jpg")
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count >= 0:
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player
            #character, namebox, textbox in order
            if count == 0:
                name = namebox("Kimiko")
                instruction = textbox("Dad, I understand now. You only want what is best for me. And for us--as a family. You can take us back to where we are supposed to be. I’ll behave. I’ll be happy")
                father = character("images/characters/Tomiichi/Tomiichi1_smirk5.png")
                self.screen.blit(father.image, father.rect)
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 1:
                self.screen.fill((0,0,0))
            if count >= 2:
                self.credits()
            pygame.display.update()
            self.clock.tick(60)

    def scene20z2(self, count, player): #credit
        bg = background("images/backgrounds/room night_cliff.jpg") #tentative cliff
        pygame.mixer.music.fadeout(1000)
        #count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        count += 1
            #backgrounds and sounds
            if count == 1:
                
                self.screen.blit(bg.image,bg.rect)
            if count == 2:
                self.screen.fill((0,0,0))
            if count >= 3:
                self.screen.blit(bg.image,bg.rect)

            self.button_menu("SAVE GAME", [50,600], self.save_game, bg, [inspect.getframeinfo(inspect.currentframe()).function, count, player])
            self.button_menu("LOAD GAME", [225,600], self.load_game, bg)
            new_player = self.button_menu("SHOP", [400,600], self.shop, bg, None, player)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)
            self.button_menu("EXIT", [750,600], self.exit_game)
            if inspect.isclass(new_player) == True:
                player = new_player
    
            #character, namebox, textbox in order
            if count == 0:
                self.screen.fill((0,0,0))
            if count == 1:
                name = namebox("Kimiko")
                instruction = textbox(" I can’t do this anymore. I want to be real. If this is unreal I don’t want any part of it, and maybe I shouldn’t be part of it. I’m going to put an end to all of this.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 2:
                name = namebox("Kimiko")
                instruction = textbox("How can I still be alive? Don’t tell me I’m immortal in this world… No! This can’t be. What should I do?! Hmm… Maybe I should go back to my monster excuse for a dad. I need him to take me out of this madness. I’m going to climb back up, no matter what it takes.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 3:
                name = namebox("Kimiko")
                instruction = textbox("I finally made it...  I better hurry in the house… WAIT!! Who is that? There’s someone in the house hugging dad. It’s… It’s… I can’t really see… Okay wait they’re turning around… It’s… Me.")
                self.screen.blit(instruction.image, instruction.rect)
                self.screen.blit(name.image, name.rect)
            if count == 4:
                self.credits()
            pygame.display.update()
            self.clock.tick(60)

    def load_game(self, background):
        load_game = True

        while load_game:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                        
            if background:
                self.screen.blit(background.image,background.rect)
            else:
                self.screen.fill((0,0,0))

            self.load_menu(0, [70,60])
            self.load_menu(1, [508,60])
            self.load_menu(2, [70,124])
            self.load_menu(3, [508,124])
            self.load_menu(4, [70,188])
            self.load_menu(5, [508,188])
            self.load_menu(6, [70,252])
            self.load_menu(7, [508,252])
            self.load_menu(8, [70,316])
            self.load_menu(9, [508,316])
            back = self.button_menu("BACK", [400,500], "back")
            if back == 0:
                load_game = False
            pygame.display.update()
            self.clock.tick(60)

    def save_game(self, background, scene = None, save_game = True):
        new_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        try:
            fh = open("assets/save_files/timestamps.txt", "r")
        except:
            fh = open("assets/save_files/timestamps.txt", "w")
            fh.close()
            fh = open("assets/save_files/timestamps.txt", "r")
        try:
            for i, l in enumerate(fh):
                pass
            i += 1
        except:
            i = 0
        while save_game:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                        
            if background:
                self.screen.blit(background.image,background.rect)
            else:
                self.screen.fill((0,0,0))
            if i <= 9:
                fh = open("assets/save_files/timestamps.txt", "a")
                fh.write(new_timestamp + "\n")
                fh.close()
                data = {"scene" : scene[0], "scene count": scene[1], "player": scene[2]}
                with open(("assets/save_files/save" + str(i) + ".txt"),'wb') as fh:
                    pickle.dump(data,fh)
                save_game = False
            else:
                l1 = self.overwrite_menu(0, [70,60], new_timestamp, scene)
                l2 = self.overwrite_menu(1, [508,60],new_timestamp, scene)
                l3 = self.overwrite_menu(2, [70,124],new_timestamp, scene)
                l4 = self.overwrite_menu(3, [508,124],new_timestamp, scene)
                l5 = self.overwrite_menu(4, [70,188],new_timestamp, scene)
                l6 = self.overwrite_menu(5, [508,188],new_timestamp, scene)
                l7 = self.overwrite_menu(6, [70,252],new_timestamp, scene)
                l8 = self.overwrite_menu(7, [508,252],new_timestamp, scene)
                l9 = self.overwrite_menu(8, [70,316],new_timestamp, scene)
                l10 = self.overwrite_menu(9, [508,316],new_timestamp, scene)
                instructions = textbox("Click on the timestamps above to overwrite.")
                self.screen.blit(instructions.image, instructions.rect)
                if 0 in [l1,l2,l3,l4,l5,l6,l7,l8,l9,l10]:
                    save_game = False
            pygame.display.update()
            self.clock.tick(60)


    def shop(self, background, player, shop = True):
        while shop:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if player.stats > 0:
                        if event.key == pygame.K_w:
                            player.willpower += 1
                            player.stats -= 1
                        if event.key == pygame.K_p:
                            player.persuasion += 1
                            player.stats -= 1
                        if event.key == pygame.K_c:
                            player.courage += 1
                            player.stats -= 1
                        if event.key == pygame.K_e:
                            player.endurance += 1
                            player.stats -= 1
                        if event.key == pygame.K_o:
                            player.optimism += 1
                            player.stats -= 1
                        
            if background:
                self.screen.blit(background.image,background.rect)
            else:
                self.screen.fill((0,0,0))
            shop = shopbox("Increase your skills by spending your stat points. These skills will be valuable to the story. One stat point will be spent for one key press.\n\nW = Willpower\nP = Persuasion\nC = Courage\nE = Endurance\nO = Optimism\n\nCurrent Stat Points:" + str(player.stats))
            willpower = shop_button("assets/images/shop/willpower.png",[50,50])
            persuasion = shop_button("assets/images/shop/persuasion.png",[50,151])
            courage = shop_button("assets/images/shop/courage.png",[50,252])
            endurance = shop_button("assets/images/shop/endurance.png",[50,353])
            optimism = shop_button("assets/images/shop/optimism.png",[50,454])
            w_cap = shop_button_caption("Willpower: " + str(player.willpower), [170,50])
            p_cap = shop_button_caption("Persuasion: " + str(player.persuasion), [170,151])
            c_cap = shop_button_caption("Courage: " + str(player.courage), [170,252])
            e_cap = shop_button_caption("Endurance: " + str(player.endurance), [170,353])
            o_cap = shop_button_caption("Optimism: " + str(player.optimism), [170,454])
            self.screen.blit(willpower.image, willpower.rect)
            self.screen.blit(w_cap.image, w_cap.rect)
            self.screen.blit(persuasion.image, persuasion.rect)
            self.screen.blit(p_cap.image, p_cap.rect)
            self.screen.blit(courage.image, courage.rect)
            self.screen.blit(c_cap.image, c_cap.rect)
            self.screen.blit(endurance.image, endurance.rect)
            self.screen.blit(e_cap.image, e_cap.rect)
            self.screen.blit(optimism.image, optimism.rect)
            self.screen.blit(o_cap.image, o_cap.rect)
            self.screen.blit(shop.image, shop.rect)
            
            back = self.button_menu("BACK", [750,500], "back")
            if back == 0:
                return player
            pygame.display.update()
            self.clock.tick(60)

    def main_screen(self):
        pygame.mixer.music.stop()
        bg_music = music("assets/music/background_music/Dream Culture.mp3", 1)
        bg  = background('assets/images/backgrounds/main.png')
        main_screen = True

        while main_screen:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        
            self.screen.fill((255,255,255))
            self.screen.blit(bg.image, bg.rect)
            self.main_menu("NEW GAME", [750,400], self.scene1, None, player(10,0,0,0,0,0))
            self.main_menu("LOAD GAME", [750,440], self.load_game, background('assets/images/backgrounds/main_notext.png'))
            self.main_menu("EXIT", [750,480], self.exit_game)
            pygame.display.update()
            self.clock.tick(60)

    def credits(self):
        bg = background('assets/images/backgrounds/credits.jpg')
        while True:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.fill((255,255,255))
            self.screen.blit(bg.image, bg.rect)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)

if __name__ == "__main__":
    display = window()
    display.main_screen()

#Desktop/UP_Files/EEE_111/DesignProject
