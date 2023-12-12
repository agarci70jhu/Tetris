# -*- coding: utf-8 -*-

"""
EN.640.635 Software Carpentry.
Final Project (Tetris)

Author:
    Angel Garcia

This code attempts its best to recreate the famous game known as tetris. It is
a very basic rendition of the game since it misses complex moves such as
T-spins and other features found in modern tetris games. The menu provided on
the game is more a proof of concept and only functionally works to pause, exit,
and turn off the music. The game can be paused using SPACE or ESC
 
"""

from sys import exit
import pygame
from pygame.image import load

from random import choice

class Main:
    """
    A class to run the entire game.

    ...

    Attributes
    ----------
    display_surface : pygame display object
        surface on which game is displayed
    clock : pygame clock object
        clock used for internal timer
    paused : bool
        variable to check if game is paused
    menu_state : str
        varible to check menu state
    clicked : bool
        checks if mouse is currently pressed down
    next_shapes : list
        list of upcoming shapes
    game : Game class object
        initializes the Game class
    score : Score class object
        initializes the Score class
    preview : Preview class object
        initializes the Preview class
    menu : Menu class object
        initializes the Menu class
    music : pygame Sound object
        stores file for music played
    music_on : bool
        stores state of music on or off

    Methods
    -------
    def update_score(lines, score, level):
        updates user score
        
    def get_next_shape():
        obtains the next shape

    def run():
        runs the game
    """
    def __init__(self):
        """
        Constructs all necessary objects to run the game

        Parameters
        ----------
        display_surface : pygame display object
            surface on which game is displayed
        clock : pygame clock object
            clock used for internal timer
        paused : bool
            variable to check if game is paused
        menu_state : str
            varible to check menu state
        clicked : bool
            checks if mouse is currently pressed down
        next_shapes : list
            list of upcoming shapes
        game : Game class object
            initializes the Game class
        score : Score class object
            initializes the Score class
        preview : Preview class object
            initializes the Preview class
        menu : Menu class object
            initializes the Menu class
        music : pygame Sound object
            stores file for music played
        music_on : bool
            stores state of music on or off
        """
        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        self.paused = True
        self.menu_state = "main"
        self.clicked = False
        pygame.display.set_caption("Tetris")
        
        # shapes
        self.next_shapes = [choice(list(tetromino_dict.keys())) for shape in range(3)]
        
        # components
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()
        self.menu = Menu()
        
        # music
        self.music = pygame.mixer.Sound("music/barge.wav")
        self.music.set_volume(0.1)
        self.music.play()
        self.music_on = True
        
    def update_score(self, lines, score, level):
        """
        Updates the user score

        Parameters
        ----------
        lines : int
            Number of lines cleared
        score : int
            User score
        level : int
            Current level of game
        
        Returns
        -------
        None
        """
        self.score.lines = lines
        self.score.score = score
        self.score.level = level
        
    def get_next_shape(self):
        """
        Obtains the next shape

        Parameters
        ----------
        None
        
        Returns
        -------
        next_shape : str
            The next shape to be placed
        """
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(tetromino_dict.keys())))
        return next_shape
        
    def run(self):
        """
        Runs the game

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        while True:                
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        self.paused = True
                        
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    self.clicked = False
            
            # display
            self.display_surface.fill(DARK_PURPLE)
            

            
            # check if game paused
            if self.paused == True:
                #check menu state
                if self.menu_state == "main":
                    if self.menu.resume_button.draw(self.display_surface):
                        self.paused = False
                    
                    if self.menu.options_button.draw(self.display_surface) and not self.clicked:
                        self.menu_state = "options"
                        self.clicked = True
                    
                    if self.menu.quit_button.draw(self.display_surface):
                        pygame.quit()
                        exit()
                
                if self.menu_state == "options":
                    if self.menu.video_button.draw(self.display_surface):
                        pass
                    
                    if self.menu.audio_button.draw(self.display_surface) and not self.clicked:
                        if self.music_on:
                            self.music.stop()
                            self.music_on = False
                            
                        else:
                            self.music.play()
                            self.music_on = True
                        
                    if self.menu.keys_button.draw(self.display_surface):
                        pass
                    
                    if self.menu.back_button.draw(self.display_surface):
                        self.menu_state = "main"
                
            else:
                # components
                self.game.run()
                self.score.run()
                self.preview.run(self.next_shapes)
                
            # updating the game
            pygame.display.update()
            self.clock.tick(120)

class Game:
    """
    A class to represent the Game.

    ...

    Attributes
    ----------
    surface : pygame surface object
        surface on which main game is displayed
    display_surface : pygame surface object
        current surface of display
    rect : bool
        variable to check if game is paused
    sprites : pygame group object
        container to hold multiple sprites
    get_next_shape : str
        next shape to be placed
    update_score : int, int, int
        represents lines, level, and score
    line_surface : pygame surface object
        copy of the surface variable
    field_data : list
        numerical representation of game grid
    tetromino : Tetromino class object
        a random shape
    down_speed : int
        speed at which blocks fall
    press_speed : int
        speed at which blocks fall when user speeds it up
    down_pressed : bool
        down key pressed bool state
    timers : dict
        different timers to represent actions completed
    current_level : int
        the current level
    current_score : int
        the current score
    current_lines : int
        the current lines cleared
    
    Methods
    -------
    def calculate_score(num_lines):
        calcualtes the current user score and updates attributes
        
    def check_game_over():
        checks if the user has lost
    
    def create_new_tetromino:
        creates new tetromino object
        
    def timer_update():
        updates the timer
    
    def move_down():
        moves pieces down
        
    def draw_grid():
        draws grid of game onto surface
        
    def input():
        checks for user input and creates action
    
    def check_row():
        checks if line in row is full
        
    def run():
        runs the Game class
    """
    def __init__(self, get_next_shape, update_score):
        """
        Constructs all necessary attributes for the Game object

        Parameters
        ----------
        surface : pygame surface object
            surface on which main game is displayed
        display_surface : pygame surface object
            current surface of display
        rect : bool
            variable to check if game is paused
        sprites : pygame group object
            container to hold multiple sprites
        get_next_shape : str
            next shape to be placed
        update_score : int, int, int
            represents lines, level, and score
        line_surface : pygame surface object
            copy of the surface variable
        field_data : list
            numerical representation of game grid
        tetromino : Tetromino class object
            a random shape
        down_speed : int
            speed at which blocks fall
        press_speed : int
            speed at which blocks fall when user speeds it up
        down_pressed : bool
            down key pressed bool state
        timers : dict
            different timers to represent actions completed
        current_level : int
            the current level
        current_score : int
            the current score
        current_lines : int
            the current lines cleared
        """
        # general
        self.surface = pygame.Surface ((game_width, game_height))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (padding, padding))
        self.sprites = pygame.sprite.Group()
        
        # game connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score
        
        # lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)
        
        # tetromino
        self.field_data = [[0 for x in range(columns)] for y in range(rows)]
        self.tetromino = Tetromino(
            choice(list(tetromino_dict.keys())), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)
        
        # timer
        self.down_speed = start_speed
        self.press_speed = self.down_speed * 0.3
        self.down_pressed = False
        
        self.timers = {
            'vertical move': Timer(self.down_speed, True, self.move_down),
            'horizontal move': Timer(move_speed),
            'rotate': Timer(rotate_speed)
        }
        self.timers['vertical move'].activate()
        
        # score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0
        
    def calculate_score(self, num_lines):
        """
        Updates the user score, lines, and level

        Parameters
        ----------
        num_lines : int
            Number of lines cleared
            
        Returns
        -------
        None
        """
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_level
        
        # increase level every 10 lines
        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.75
            self.press_speed = self.down_speed * 0.3
            self.timers["vertical move"].duration = self.down_speed
        
        self.update_score(self.current_lines, self.current_score, self.current_level)
    
    def check_game_over(self):
        """
        Checks if user loses and quits if lost

        Parameters
        ----------
        None
            
        Returns
        -------
        None
        """
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                pygame.quit()
                exit()
    
    def create_new_tetromino(self):
        """
        Creates new Tetromino object

        Parameters
        ----------
        None
        
        -------
        None
        """
        self.check_row()
        self.check_game_over()
        self.tetromino = Tetromino(
            self.get_next_shape(), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)
    
    def timer_update(self):
        """
        Updates the timer

        Parameters
        ----------
        None
            
        Returns
        -------
        None
        """
        for timer in self.timers.values():
            timer.update()
    
    def move_down(self):
        """
        Moves the shape down

        Parameters
        ----------
        None
            
        Returns
        -------
        None
        """
        self.tetromino.move_down()
    
    def draw_grid(self):
        """
        Creates data representation of the game grid

        Parameters
        ----------
        None
            
        Returns
        -------
        None
        """
        for col in range(1, columns):
            x = col * cell_size
            pygame.draw.line(self.line_surface, LINE_COLOR, (x,0), (x,self.surface.get_height()), 1)
            
        for row in range(1, rows):
            y = row * cell_size
            pygame.draw.line(self.line_surface, LINE_COLOR, (0,y), (self.surface.get_width(),y))
            
        self.surface.blit(self.line_surface, (0,0))
        
    def input(self):
        """
        Checks for user input and applies move onto shape

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        keys = pygame.key.get_pressed()
        
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
                
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()
                
        # check for rotation
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()
                
        # down speedup
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers['vertical move'].duration = self.press_speed
            
        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers['vertical move'].duration = self.down_speed

    def check_row(self):
        """
        Checks if row needs to cleared and gets rid of it

        Parameters
        ----------
        None
            
        Returns
        -------
        None
        """
        # get the full row indexes
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)
                
        if delete_rows:
            for delete_row in delete_rows:
                # delete full rows
                for block in self.field_data[delete_row]:
                    block.kill()
                    
                # move blocks down
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1
                            
            # rebuild field data
            self.field_data = [[0 for x in range(columns)] for y in range(rows)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
                
            # update score
            self.calculate_score(len(delete_rows))

    def run(self):
        """
        Runs the Game class

        Parameters
        ----------
        None
            
        Returns
        -------
        None
        """
        # update
        self.input()
        self.timer_update()
        self.sprites.update()
        
        # drawing
        self.surface.fill(DARK_PURPLE)
        self.sprites.draw(self.surface)
        
        self.draw_grid()
        self.display_surface.blit(self.surface, (padding,padding))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
        
class Tetromino:
    """
    A class to represent a Tetromino.

    ...

    Attributes
    ----------
    shape : str
        the shape to be turned into a tetromino object
    block_positions : tuple
        positions on which graphic should be placed
    color : str
        color of the tetromino
    create_new_tetromino : method
        creates new tetromino
    field_data : list
        data representation of current grid
    blocks : list
        list of blocks to create a tetromino

    Methods
    -------
    def check_horz_collision(lines, score, level):
        updates user score
        
    def check_vert_collision():
        obtains the next shape

    def move_horizontal():
        runs the game
    
    def move_down():
        moves the piece down
        
    def rotate():
        rotates the current piece
    """
    def __init__(self, shape, group, create_new_tetromino, field_data):
        """
        Constructs all necessary attributes for the tetromino class

        Parameters
        ----------
        shape : str
            the shape to be turned into a tetromino object
        block_positions : tuple
            positions on which graphic should be placed
        color : str
            color of the tetromino
        create_new_tetromino : method
            creates new tetromino
        field_data : list
            data representation of current grid
        blocks : list
            list of blocks to create a tetromino
        """
        # setup
        self.shape = shape
        self.block_positions = tetromino_dict[shape]['shape']
        self.color = tetromino_dict[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data
        
        # create blocks
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]
    
    def check_horz_collision(self, blocks, amount):
        """
        Checks if piece is colliding horizontally

        Parameters
        ----------
        blocks : list
            List of blocks in a tetromino object
        amount : int
            how far to check collision
            
        Returns
        -------
        bool
        """
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False
    
    def check_vert_collision(self, blocks, amount):
        """
        Checks if piece is colliding vertically

        Parameters
        ----------
        blocks : list
            List of blocks in a tetromino object
        amount : int
            how far to check collision
            
        Returns
        -------
        bool
        """
        collision_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False
        
    def move_horizontal(self, amount):
        """
        Moves piece horizontally if valid position

        Parameters
        ----------
        amount : int
            how far to move object
            
        Returns
        -------
        None
        """
        if not self.check_horz_collision(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount
    
    def move_down(self):
        """
        Moves piece down if valid position

        Parameters
        ----------
        None
            
        Returns
        -------
        None
        """
        if not self.check_vert_collision(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1
                
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
                
            self.create_new_tetromino()
    
    def rotate(self):
        """
        Rotates current piece

        Parameters
        ----------
        None
            
        Returns
        -------
        None
        """
        if self.shape != 'O':
            # pivot point
            rotate_point = self.blocks[0].pos
            
            # new block positions
            new_block_positions = [block.rotate(rotate_point) for block in self.blocks]
            
            # collision check
            for pos in new_block_positions:
                # horizontal
                if pos.x < 0 or pos.x >= columns:
                    return
                
                # field check
                if self.field_data[int(pos.y)][int(pos.x)]:
                    return
                
                # vertical / floor check
                if pos.y > rows:
                    return
            
            # implement new positions
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]
        
class Block(pygame.sprite.Sprite):
    """
    A class to represent a Block.

    ...

    Attributes
    ----------
    group : pygame Group object
        container to hold sprite objects
    pos : tuple
        current block position
    color : str
        color of block
    image : pygame Surface object
        gets current surface for block
    rect : tuple
        topleft position of block

    Methods
    -------
    def rotate(rotate_point):
        rotates the current block
        
    def horizontal_collide(x, field_data):
        checks if block is colliding horizontally

    def vertical_collide(y, field_data):
        checks if block is colliding vertically
    
    def update():
        updates the current block
    """
    def __init__(self, group, pos, color):
        """
        Constructs all necessary attributes for the tetromino class

        Parameters
        ----------
        group : pygame Group object
            container to hold sprite objects
        pos : tuple
            current block position
        color : str
            color of block
        image : pygame Surface object
            gets current surface for block
        rect : tuple
            topleft position of block
        """
        super().__init__(group)
        self.image = pygame.Surface((cell_size, cell_size))
        self.image.fill(color)
        
        # position
        self.pos = pygame.Vector2(pos) + block_offset
        self.rect = self.image.get_rect(topleft = self.pos * cell_size)
        
    def rotate(self, rotate_point):
        """
        Rotates current piece

        Parameters
        ----------
        rotate_point : tuple
            point to rotate around
            
        Returns
        -------
        new_pos : tuple
            position of block after rotation
        """
        distance = self.pos - rotate_point
        rotated = distance.rotate(90)
        new_pos = rotate_point + rotated
        return new_pos
    
    def horizontal_collide(self, x, field_data):
        """
        Checks if current block is colliding horizontally

        Parameters
        ----------
        x : int
            x position of block
        field_data : list
            numerical representation of current game grid
        
        Returns
        -------
        bool
        """
        if not 0 <= x < columns:
            return True
        
        if field_data[int(self.pos.y)][x]:
            return True
            
        
    def vertical_collide(self, y, field_data):
        """
        Checks if current block is colliding vertically

        Parameters
        ----------
        y : int
            y position of block
        field_data : list
            numerical representation of current game grid
            
        Returns
        -------
        bool
        """
        if y >= rows:
            return True
        
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True
    
    def update(self):
        """
        Updates the current block

        Parameters
        ----------
        None
        
        Returns
        -------
        bool
        """
        self.rect.topleft = self.pos * cell_size

class Menu():
    """
    A class to represent a Menu.

    ...

    Attributes
    ----------
    display_surface : pygame Surface object
        current surface that is displayed
    resume_button : Button object
        button with resume function
    quit_button : Button object
        button with quit function
    options_button : Button object
        button with options function
    video_button : Button object
        button with video function
    audio_button : Button object
        button with audio function
    keys_button : Button object
        button with key function
    back_button : Button object
        button with back function

    Methods
    -------
    None
    """
    def __init__(self):
        """
        Constructs all necessary attributes for the Menu class

        Parameters
        ----------
        display_surface : pygame Surface object
            current surface that is displayed
        resume_button : Button object
            button with resume function
        quit_button : Button object
            button with quit function
        options_button : Button object
            button with options function
        video_button : Button object
            button with video function
        audio_button : Button object
            button with audio function
        keys_button : Button object
            button with key function
        back_button : Button object
            button with back function
        """
        self.display_surface = pygame.display.get_surface()
        
        # load button images
        resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
        options_img = pygame.image.load("images/button_options.png").convert_alpha()
        quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
        video_img = pygame.image.load('images/button_video.png').convert_alpha()
        audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
        keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
        back_img = pygame.image.load('images/button_back.png').convert_alpha()

        # Create button instances for main menu
        self.resume_button = Button(game_width / 1.6, game_height / 5, resume_img, 1)
        self.quit_button = Button(game_width / 1.5, game_height / 5 * 3, quit_img, 1)
        self.options_button = Button(game_width / 1.6, game_height / 5 * 2, options_img, 1)
        
        # Button instances for options
        self.video_button = Button(game_width / 2, game_height / 5, video_img, 1)
        self.audio_button = Button(game_width / 2, game_height / 5 * 2, audio_img, 1)
        self.keys_button = Button(game_width / 2, game_height / 5 * 3, keys_img, 1)
        self.back_button = Button(game_width / 1.4, game_height / 5 * 4, back_img, 1)
        
class Button():
    """
    A class to represent a Button.

    ...

    Attributes
    ----------
    image : pygame surface object
        image transformed into scaled surface
    rect : tuple
        center position of image
    clicked : bool
        state of wether mouse is clicked or not

    Methods
    -------
    def draw(surface):
        draws image/text onto surface
    """
    def __init__(self, x, y, image, scale):
        """
        Constructs all necessary attributes for the Button class

        Parameters
        ----------
        image : pygame surface object
            image transformed into scaled surface
        rect : tuple
            center position of image
        clicked : bool
            state of wether mouse is clicked or not
        x : int
            x position
        y : int
            y position
        scale : int
            scale set for image
        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), 
                                                 int(height * scale)))
        self.rect = self.image.get_rect(center = (x,y))
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self, surface):
        """
        Draws image/text onto surface
        
        Parameters
        ----------
        surface : pygame Surface object
            the surface to be drawn
        
        Returns
        -------
        action : bool
            representation of completed click
        """
        action = False
  		#get mouse position
        pos = pygame.mouse.get_pos()
  
  		#check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
  
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
  
  		#draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        return action

class Timer:
    """
    A class to represent a Timer.

    ...

    Attributes
    ----------
    duration : int
        time passed
    repeated : bool
        time repeated
    func : function
        function representing timer
    start_time : int
        time of start
    active : bool
        bool for timer activation

    Methods
    -------
    def activate():
        activates timer
    
    def deactivate():
        deactivates timer
    
    def update():
        updates timer
    """
    def __init__(self, duration, repeated = False, func = None):
        """
        Constructs all necessary attributes for the Timer class

        Parameters
        ----------
        duration : int
            time passed
        repeated : bool
            time repeated
        func : function
            function representing timer
        start_time : int
            time of start
        active : bool
            bool for timer activation
        """
        self.repeated = repeated
        self.func = func
        self.duration = duration
        
        self.start_time = 0
        self.active = False
        
    def activate(self):
        """
        Activates timer
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.active = True
        self.start_time = pygame.time.get_ticks()
        
    def deactivate(self):
        """
        Deactivates timer
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.active = False
        self.start_time = 0
        
    def update(self):
        """
        Updates timer
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration and self.active:
            # call a function
            if self.func and self.start_time != 0:
                self.func()
            
            # reset timer
            self.deactivate()
            
            # repeat the timer
            if self.repeated:
                self.activate()

class Preview:
    """
    A class to represent a Preview.

    ...

    Attributes
    ----------
    surface : pygame surface object
        surface representing where the preview goes
    rect : tuple
        topright of the surface
    display_surface : pygame surface object
        current surface of display
    shape_surfaces: dict
        loads images for upcoming shapes
    increment_height : int
        height position for placing preview shapes

    Methods
    -------
    def display_pieces(shapes):
        displays pieces onto surface
    
    def run(next_shapes):
        runs the Preview class
    """
    def __init__(self):
        """
        Constructs all necessary attributes for the Button class

        Parameters
        ----------
        surface : pygame surface object
            surface representing where the preview goes
        rect : tuple
            topright of the surface
        display_surface : pygame surface object
            current surface of display
        shape_surfaces: dict
            loads images for upcoming shapes
        increment_height : int
            height position for placing preview shapes
        """
        # general
        self.surface =pygame.Surface((sidebar_width,game_height * preview_height_frac))
        self.rect = self.surface.get_rect(topright = (window_width - padding,padding))
        self.display_surface = pygame.display.get_surface()
        
        # shapes
        self.shape_surfaces = {shape: load("graphics/{}.png".format(shape)).convert_alpha() for shape in tetromino_dict.keys()}
        
        # image position data
        self.increment_height = self.surface.get_height() / 3
        
    def display_pieces(self, shapes):
        """
        Displays pieces onto surface
        
        Parameters
        ----------
        shapes : list
            upcoming shapes to be displayed
        
        Returns
        -------
        None
        """
        for i, shape in enumerate(shapes):
            shape_surface = self.shape_surfaces[shape]
            
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + i * self.increment_height
            
            rect = shape_surface.get_rect(center = (x,y))
            self.surface.blit(shape_surface, rect)
        
    def run(self, next_shapes):
        """
        Runs the Preview class
        
        Parameters
        ----------
        next_shapes : list
            upcoming shapes to be displayed
        
        Returns
        -------
        None
        """
        self.surface.fill(DARK_PURPLE)
        self.display_pieces(next_shapes)
        self.display_surface.blit(self.surface,self.rect)
        
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

class Score:
    """
    A class to represent a Score.

    ...

    Attributes
    ----------
    surface : pygame surface object
        surface representing where the score goes
    rect : tuple
        topright of the surface
    display_surface : pygame surface object
        current surface of display
    font : Font object
        loads font to be used
    increment_height : int
        height position for placing user attributes
    score : int
        user score
    level : int
        user level
    lines : int
        number of lines cleared

    Methods
    -------
    def display_text(pos, text):
        displays text onto surface
    
    def run(next_shapes):
        runs the Score class
    """
    def __init__(self):
        """
        Constructs all necessary attributes for the Timer class

        Parameters
        ----------
        surface : pygame surface object
            surface representing where the score goes
        rect : tuple
            topright of the surface
        display_surface : pygame surface object
            current surface of display
        font : Font object
            loads font to be used
        increment_height : int
            height position for placing user attributes
        score : int
            user score
        level : int
            user level
        lines : int
            number of lines cleared
        """
        self.surface =pygame.Surface((sidebar_width,game_height * 
                                      score_height_frac - padding))
        self.rect = self.surface.get_rect(bottomright = (window_width - 
                                            padding,window_height - padding))
        self.display_surface = pygame.display.get_surface()
        
        # font
        self.font = pygame.font.Font("graphics/Russo_One.ttf", 30)
        
        # increment
        self.increment_height = self.surface.get_height() / 3
        
        # data
        self.score = 0
        self.level = 1
        self.lines = 0
        
    def display_text(self, pos, text):
        """
        Displays text inputted onto surface
        
        Parameters
        ----------
        pos : tuple
            position to draw text
        
        text : str
            text to be drawn
        
        Returns
        -------
        None
        """
        text_surface = self.font.render(f'{text[0]}: {text[1]}', True, 'white')
        text_rect = text_surface.get_rect(center = pos)
        self.surface.blit(text_surface, text_rect)
        
    def run(self):
        """
        Runs the Score class
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.surface.fill(DARK_PURPLE)
        for i, text in enumerate([('Score', self.score), ('Level', self.level),
                                  ('Lines', self.lines)]):
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + i * self.increment_height
            
            self.display_text((x,y), text)
        
        self.display_surface.blit(self.surface,self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

if __name__ == '__main__':
    # Size of game
    columns = 10
    rows = 20
    cell_size = 40
    game_width, game_height = columns * cell_size, rows * cell_size

    # Size of side bar
    sidebar_width = 200
    preview_height_frac = 0.7
    score_height_frac = 1 -  preview_height_frac

    # Window
    padding = 20
    window_width = game_width + sidebar_width + padding * 3
    window_height = game_height + padding * 2

    # game behaviour 
    start_speed = 300 # lower number means faster
    move_speed = 75
    rotate_speed = 150
    block_offset = pygame.Vector2(columns // 2, -1)

    # Colors
    YELLOW = '#f1e60d'
    RED = '#e51b20'
    BLUE = '#204b9b'
    GREEN = '#65b32e'
    PURPLE = '#7b217f'
    CYAN = '#6cc6d9'
    ORANGE = '#f07e13'
    GRAY = '#1C1C1C'
    DARK_PURPLE = '#301934'

    LINE_COLOR = '#FFFFFF'

    # shapes
    tetromino_dict = {
    	'T': {'shape': [(0,0), (-1,0), (1,0), (0,-1)], 'color': PURPLE},
    	'O': {'shape': [(0,0), (0,-1), (1,0), (1,-1)], 'color': YELLOW},
    	'J': {'shape': [(0,0), (0,-1), (0,1), (-1,1)], 'color': BLUE},
    	'L': {'shape': [(0,0), (0,-1), (0,1), (1,1)], 'color': ORANGE},
    	'I': {'shape': [(0,0), (0,-1), (0,-2), (0,1)], 'color': CYAN},
    	'S': {'shape': [(0,0), (-1,0), (0,-1), (1,-1)], 'color': GREEN},
    	'Z': {'shape': [(0,0), (1,0), (0,-1), (-1,-1)], 'color': RED}
    }

    SCORE_DATA = {1: 40, 2: 100, 3: 300, 4: 1200}
    
    main = Main()
    main.run()