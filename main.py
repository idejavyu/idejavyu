import pygame as pg
import sys
import random


#Клас у якому знаходиться інформація про розміри екрану, функції зміни чи отримання інформації
class ScreenInfo:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_size(self):
        return self.width, self.height

    def set_size(self, width, height):
        self.width = width
        self.height = height

class global_var():
    def __init__(self,d1,d2,prison=0, move_again=0):
        self.d1=d1
        self.d2=d2
        self.prison=prison
        self.move_again=move_again

class Label_info:
    def __init__(self,text=""):
        self.text = text

class System_info:
    def __init__(self,turn,stage,mode, players_c=4,current_place=0, systemcall="", action=0):
        self.TURN = turn
        self.STAGE = stage
        self.mode = mode
        self.PLAYERS = players_c
        self.systemcall = systemcall
        self.action = action
        self.current_place=current_place

    def inc_stage(self):
        self.STAGE +=1

    def null_stage(self):
        self.STAGE = 0

    def inc_mode(self):
        self.mode+=1

class States:
    def __init__(self,state=0):
        self.state=state

    def set_state(self, id):
        self.state=id

class PullC:
    def __init__(self, global_pull, local_pull):
        self.global_pull=global_pull
        self.local_pull=local_pull

    def refile_deck(self):
        self.local_pull= self.global_pull



class Players:
    def __init__(self, id, x, y, pos, prisoned=False, prison_stage=0,money=500,free=0,owned=0):
        self.id = id
        self.x = x
        self.y = y
        self.pos = pos
        self.prisoned = prisoned
        self.prison_stage = prison_stage
        self.money = money
        self.free = free
        self.owned=owned

    def move(self, new_x, new_y, new_pos):
        self.x = new_x
        self.y = new_y
        self.pos = new_pos

    def prison(self):
        if self.prisoned:
            if self.prison_stage==3:
                self.money -= 50
            else:
                self.prison_stage+=1
            return True
        else:
            return False

    def to_prison(self):
        self.prisoned = True

class Field:
    def __init__(self,idv, name, price, start_rent, rent,house_price,id,zone,zone_active=0, owned=0, house=0,mult=0):
        self.name = name
        self.price = price
        self.start_rent = start_rent
        self.owned = owned
        self.house = house
        self.rent = rent
        self.mult = mult
        self.house_price = house_price
        self.id=id
        self.idv = idv
        self.zone=zone
        self.zone_active=zone_active

    def new_rent(self):
        self.new_mult()
        self.rent=self.start_rent * self.mult
        return self.rent

    def new_mult(self):
        if self.house == 0:
            self.mult = 0
        if self.house == 1:
            self.mult = 5
        if self.house == 2:
            self.mult = 12
        if self.house == 3:
            self.mult = 45
        if self.house == 4:
            self.mult = 80
        return self.mult

    def sell(self):
        self.owned=0

    def sell_house(self):
        if self.house>0:
            self.house-=1
        self.new_mult()

    def buy_house(self):
        if self.house < 5:
            self.house += 1
        self.new_mult()

    def buy(self, id):
        self.owned = id





def main():
    pg.init()
    clock = pg.time.Clock()
    # Створення екрану з заданими розмірами
    screen_info = ScreenInfo(1920, 1080)
    screen_width, screen_height = screen_info.get_size()
    screen = pg.display.set_mode((screen_width, screen_height))

    f = (Field(0,"Adidas", 60, 2, 2, 50,1,0),
         Field(1,"Chanel", 60, 2, 2, 50,3,0),
         Field(2,"TNF", 80, 4, 4, 50,4,0),
         Field(3, "Rail station North", 100, 25, 25, -1, 5, 1),
         Field(4,"Mirinda", 100, 6, 6, 100,6,2),
         Field(5,"Fanta", 120, 8, 8, 100,7,2),
         Field(6,"Pepsi", 140, 10, 10, 100,9,2),
         Field(7,"Facebook", 160, 12, 12, 100,10,3),
         Field(8,"Instagram", 160, 12, 12, 100,12,3),
         Field(9,"Twitter", 180, 14, 14, 100,13,3),
         Field(10,"Youtube", 200, 16, 16, 100,15,4),
         Field(11, "Rail station East", 100, 25, 25, -1, 16, 1,1),
         Field(12,"Twitch", 200, 16, 16, 100,17,4),
         Field(13,"Kick", 220, 18, 18, 100,19,4),
         Field(14,"Burger King", 240, 20, 20, 150,21,5),
         Field(15,"KFC", 240, 20, 20, 150,22,5),
         Field(16,"McDonald`s", 260, 22, 22, 150,24,5),
         Field(17, "Rail station South", 100, 25, 25, -1, 25, 1,1),
         Field(18,"Honor", 280, 24, 24, 150,26,6),
         Field(19,"Samsung", 300, 26, 26, 150,27,6),
         Field(20,"Mi", 320, 28, 28, 150,29,6),
         Field(21,"Windows", 340, 30, 30, 200,30,7),
         Field(22,"Linux", 360, 32, 32, 200,32,7),
         Field(23,"Mac", 380, 34, 34, 200,33,7),
         Field(24, "Rail station West", 100, 25, 25, -1, 35, 1,1),
         Field(25,"NASA", 400, 40, 40, 200,34,37,8),
         Field(26,"Space X", 400, 50, 50, 200,39,8))



    dice_pos1 = pg.Rect(1267,650,128,128)
    dice_pos2 = pg.Rect(1411, 650, 128, 128)

    p=(Players(0, 622, 67, 0),
       Players(1, 654, 99, 0), 
       Players(2, 686, 131, 0),
       Players(3, 718, 163, 0))

    s=System_info(1,1,1)

    d=global_var(0,0)


    Iboard = pg.image.load('images/board.png')


    players = [pg.image.load('images/P1.png'),
            pg.image.load('images/P2.png'),
            pg.image.load('images/P3.png'),
            pg.image.load('images/P4.png'),
               ]

    dice = [pg.image.load('images/d1.png'),
            pg.image.load('images/d2.png'),
            pg.image.load('images/d3.png'),
            pg.image.load('images/d4.png'),
            pg.image.load('images/d5.png'),
            pg.image.load('images/d6.png'),
            ]

    players_card = [pg.image.load('images/Card1.png'),
            pg.image.load('images/Card2.png'),
            pg.image.load('images/Card3.png'),
            pg.image.load('images/Card4.png'),
               ]


    button_sound = pg.mixer.Sound("sfx/click.mp3")
    button_sound.set_volume(0.1)
    bg_music = pg.mixer.Sound("sfx/bg.mp3")
    bg_music.set_volume(0.04)
    bg_music.play(-1)

    # Заголовок
    pg.display.set_caption("Monopoly")

    # Шрифт
    font = pg.font.SysFont("font/AktivGroteskCorp-Medium.ttf", 30)

    try:
        custom_font1 = pg.font.Font("font/AktivGroteskCorp-Medium.ttf", 24)
    except FileNotFoundError:
        custom_font1 = font

    try:
        custom_font2 = pg.font.Font("font/AktivGroteskCorp-Medium.ttf", 28)
    except FileNotFoundError:
        custom_font2 = font



    lb = [Label_info(),Label_info(),Label_info(),Label_info(),Label_info(),Label_info()]


    # Кольори
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (180, 180, 180)
    DGREY = (100, 100, 100)
    GREEN = (61, 163, 59)
    BLUE = (59, 163, 157)
    MAGENTA = (163, 59, 159)
    RED = (163, 59, 59)

    PLAYER_COLOR=[GREEN, BLUE, MAGENTA, RED]



    def draw_main_menu():
        screen.fill(BLACK)
        text_surface = custom_font2.render("Головне меню", True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 60))
        screen.blit(text_surface, text_rect)

        onclickbutton()



    def draw_single_player():
        screen.fill(BLACK)
        text_surface = custom_font2.render("Одиночна гра", True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 60))
        screen.blit(text_surface, text_rect)

        onclickbutton()


    def draw_multiplayer():
        screen.fill(BLACK)
        text_surface = custom_font2.render("Мультиплеер", True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 60))
        screen.blit(text_surface, text_rect)
        onclickbutton()

    def draw_settings():
        screen.fill(BLACK)
        text_surface = custom_font2.render("Налаштування", True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 60))
        screen.blit(text_surface, text_rect)
        onclickbutton()

    def draw_stats():
        screen.fill(BLACK)
        text_surface = custom_font2.render("Статистика", True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 60))
        screen.blit(text_surface, text_rect)
        onclickbutton()

    def draw_newgame():
        screen.fill(BLACK)
        text_surface = custom_font2.render("Нова гра", True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 60))
        screen.blit(text_surface, text_rect)
        onclickbutton()
        filename="save1.txt"
        with open(filename, "w") as file:
            pass


    def draw_download():
        screen.fill(BLACK)
        text_surface = custom_font2.render("Продовжити гру", True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 60))
        screen.blit(text_surface, text_rect)
        onclickbutton()

    def onclickbutton():
        for button in buttons:
            if button.active:
                button.current_color=button.color
                button.draw()
            if button.is_clicked(pg.mouse.get_pos()) and button.active:
                button.current_color = GREY
                button.draw()
                button.current_color = button.color
            elif not button.active:
                button.current_color = DGREY
                button.draw()
            else:
                button.draw()




    # Клас властивостей кнопки
    class Button:
        def __init__(self, x, y, width, height, text, color=WHITE, action=None, active=True):
            self.width = width
            self.height = height
            self.rect = pg.Rect(x, y, width, height)
            self.color = color
            self.text = text
            self.action = action
            self.active = active
            self.set_state = current_state.set_state
            self.current_color = WHITE

        def draw(self):
            self.current_color = DGREY if not self.active else self.current_color
            pg.draw.rect(screen, self.current_color, self.rect)
            text_surface = custom_font1.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

        def draw_custom(self):
            self.current_color = DGREY if not self.active else self.current_color
            pg.draw.rect(screen, self.current_color, self.rect)
            text_surface = font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)


        def is_clicked(self, pos):
            return self.active and self.rect.collidepoint(pos)

    def handle_button_click(button):
        if button.action:
            button.action()
        elif button.set_state:
            button.set_state(button.action)

    def create_buttons_main_menu():
        button_width = 200
        button_height = 50
        button_x = (screen_width - button_width) // 2
        spacing = 60
        buttons = [
            Button(button_x, 100 + spacing * i, button_width, button_height, text, action=action)
            for i, (text, action) in enumerate([
                ("Single player", lambda: current_state.set_state(STATE_SINGLE_PLAYER)),
                ("Multiplayer", lambda: current_state.set_state(STATE_MULTIPLAYER)),
                ("Settings", lambda: current_state.set_state(STATE_SETTINGS)),
                ("Stats", lambda: current_state.set_state(STATE_STATS)),
                ("debug", lambda: current_state.set_state(STATE_ONGAME)),
                ("Exit", sys.exit)
            ])
        ]
        return buttons

    def create_buttons_single_player():
        button_width = 200
        button_height = 50
        button_x = (screen_width - button_width) // 2
        spacing = 60
        buttons = [
            Button(button_x, 100 + spacing * i, button_width, button_height, text, action=action)
            for i, (text, action) in enumerate([
                ("New game", lambda: current_state.set_state(STATE_NEWGAME)),
                ("Continue", lambda: current_state.set_state(STATE_DOWNLOAD)),
                ("Back", lambda: current_state.set_state(STATE_MAIN_MENU)),
            ])
        ]
        return buttons

    def create_buttons_stats():
        button_width = 200
        button_height = 50
        button_x = (screen_width - button_width) // 2
        spacing = 60
        buttons = [
            Button(button_x, 100 + spacing * i, button_width, button_height, text, action=action)
            for i, (text, action) in enumerate([
                ("Go back", lambda: current_state.set_state(STATE_MAIN_MENU)),
            ])
        ]
        return buttons

    def create_buttons_settings():
        button_width = 200
        button_height = 50
        button_x = (screen_width - button_width) // 2
        spacing = 60
        buttons = [
            Button(button_x, 100 + spacing * i, button_width, button_height, text, action=action)
            for i, (text, action) in enumerate([
                ("Go back", lambda: current_state.set_state(STATE_MAIN_MENU)),
            ])
        ]
        return buttons

    def create_buttons_multiplayer():
        button_width = 200
        button_height = 50
        button_x = (screen_width - button_width) // 2
        spacing = 60
        buttons = [
            Button(button_x, 100 + spacing * i, button_width, button_height, text, action=action)
            for i, (text, action) in enumerate([
                ("Go back", lambda: current_state.set_state(STATE_MAIN_MENU)),
            ])
        ]
        return buttons

    def animate_dice():
        for j in range(2):
            for i in range(6):
                screen.fill((217, 217, 217), dice_pos1)
                screen.fill((217, 217, 217), dice_pos2)
                screen.blit(dice[i], dice_pos1)
                screen.blit(dice[i], dice_pos2)
                pg.time.delay(100)
                pg.display.update(dice_pos1)
                pg.display.update(dice_pos2)

    def move_op(id,counter):
        while counter!=0:
            if p[id]==0:
                p[id].money+=200
            if id == 0:
                if p[id].pos == 0 or p[id].pos == 10:
                    p[id].move(p[id].x + 176, p[id].y, p[id].pos + 1)
                elif p[id].pos == 11 or p[id].pos == 19:
                    p[id].move(p[id].x, p[id].y + 176, p[id].pos + 1)
                elif p[id].pos == 20 or p[id].pos == 30:
                    p[id].move(p[id].x - 176, p[id].y, p[id].pos + 1)
                elif p[id].pos == 31:
                    p[id].move(p[id].x, p[id].y - 176, p[id].pos + 1)
                elif p[id].pos == 39:
                    p[id].move(p[id].x, p[id].y - 176, 0)
                elif p[id].pos < 10 and p[id].pos > 0:
                    p[id].move(p[id].x + 80, p[id].y, p[id].pos + 1)
                elif p[id].pos > 11 and p[id].pos < 19:
                    p[id].move(p[id].x, p[id].y + 80, p[id].pos + 1)
                elif p[id].pos > 20 and p[id].pos < 30:
                    p[id].move(p[id].x - 80, p[id].y, p[id].pos + 1)
                elif p[id].pos > 31 or p[id].pos < 39:
                    p[id].move(p[id].x, p[id].y - 80, p[id].pos + 1)
            if id == 1:
                if p[id].pos == 0 or p[id].pos == 10:
                    p[id].move(p[id].x + 144, p[id].y, p[id].pos + 1)
                elif p[id].pos == 11 or p[id].pos == 19:
                    p[id].move(p[id].x, p[id].y + 144, p[id].pos + 1)
                elif p[id].pos == 20 or p[id].pos == 30:
                    p[id].move(p[id].x - 144, p[id].y, p[id].pos + 1)
                elif p[id].pos == 31:
                    p[id].move(p[id].x, p[id].y - 144, p[id].pos + 1)
                elif p[id].pos == 39:
                    p[id].move(p[id].x, p[id].y - 144, 0)
                elif p[id].pos < 10 and p[id].pos > 0:
                    p[id].move(p[id].x + 80, p[id].y, p[id].pos + 1)
                elif p[id].pos > 11 and p[id].pos < 19:
                    p[id].move(p[id].x, p[id].y + 80, p[id].pos + 1)
                elif p[id].pos > 20 and p[id].pos < 30:
                    p[id].move(p[id].x - 80, p[id].y, p[id].pos + 1)
                elif p[id].pos > 31 or p[id].pos < 39:
                    p[id].move(p[id].x, p[id].y - 80, p[id].pos + 1)
            if id == 2:
                if p[id].pos == 0 or p[id].pos == 10:
                    p[id].move(p[id].x + 112, p[id].y, p[id].pos + 1)
                elif p[id].pos == 11 or p[id].pos == 19:
                    p[id].move(p[id].x, p[id].y + 112, p[id].pos + 1)
                elif p[id].pos == 20 or p[id].pos == 30:
                    p[id].move(p[id].x - 112, p[id].y, p[id].pos + 1)
                elif p[id].pos == 31:
                    p[id].move(p[id].x, p[id].y - 112, p[id].pos + 1)
                elif p[id].pos == 39:
                    p[id].move(p[id].x, p[id].y - 112, 0)
                elif p[id].pos < 10 and p[id].pos > 0:
                    p[id].move(p[id].x + 80, p[id].y, p[id].pos + 1)
                elif p[id].pos > 11 and p[id].pos < 19:
                    p[id].move(p[id].x, p[id].y + 80, p[id].pos + 1)
                elif p[id].pos > 20 and p[id].pos < 30:
                    p[id].move(p[id].x - 80, p[id].y, p[id].pos + 1)
                elif p[id].pos > 31 or p[id].pos < 39:
                    p[id].move(p[id].x, p[id].y - 80, p[id].pos + 1)
            if id == 3:
                if p[id].pos == 0 or p[id].pos == 10:
                    p[id].move(p[id].x + 80, p[id].y, p[id].pos + 1)
                elif p[id].pos == 11 or p[id].pos == 19:
                    p[id].move(p[id].x, p[id].y + 80, p[id].pos + 1)
                elif p[id].pos == 20 or p[id].pos == 30:
                    p[id].move(p[id].x - 80, p[id].y, p[id].pos + 1)
                elif p[id].pos == 31:
                    p[id].move(p[id].x, p[id].y - 80, p[id].pos + 1)
                elif p[id].pos == 39:
                    p[id].move(p[id].x, p[id].y - 80, 0)
                elif p[id].pos < 10 and p[id].pos > 0:
                    p[id].move(p[id].x + 80, p[id].y, p[id].pos + 1)
                elif p[id].pos > 11 and p[id].pos < 19:
                    p[id].move(p[id].x, p[id].y + 80, p[id].pos + 1)
                elif p[id].pos > 20 and p[id].pos < 30:
                    p[id].move(p[id].x - 80, p[id].y, p[id].pos + 1)
                elif p[id].pos > 31 or p[id].pos < 39:
                    p[id].move(p[id].x, p[id].y - 80, p[id].pos + 1)
            counter -= 1
            pg.time.delay(1000)
            create_main_game()
            pg.display.flip()


    def check_field(zone):
        temp_mas = []
        temp_num = []
        tp=0
        if f[s.current_place].house_price==-1:
            temp_mas = (f[3].owned, f[11].owned, f[17].owned, f[24].owned)
            for j in range(4):
                j+=1
                for i in range(4):
                    if temp_mas[i]==j:
                        tp+=1
                if tp>1:
                    for i in range(4):
                        if f[i].owned == j:
                            f[i].mult= tp
                tp=0


        else:
            for i in range(27):
                if f[i].house_price!=-1 and f[i].zone==zone:
                    temp_mas.append(f[i])
                    if len(temp_mas)==3:
                        for j in range(3):
                            temp_num.append(temp_mas[j].owned)
                        if temp_num[0]==temp_num[1]==temp_num[2]:
                            for t in range(3):
                                f[temp_mas[t].idv].zone_active=1
                            return True
                        return False





    def uprgade_field(id):
        f[s.current_place].house+=1
        p[id].money-=f[s.current_place].house_price
        f[s.current_place].new_rent()
        buttons[s.current_place + 6].text += "*"
        s.STAGE = 5

    def move(id):
        create_buttons_main_game(s.mode, buttons)
        counter=d.d1+d.d2+2
        if d.d1 == d.d2:
            d.prison +=1
            if d.prison == 3:
                if p[id].free > 0:
                    p[id].free -= 1
                    return
                go_to_prison(s.TURN)
                p[id].prisoned = True
                return
            d.move_again=1
        move_op(id,counter)
        create_main_game()
        pg.display.flip()

    def go_to_prison(id):
        id = 11-id
        if id==0:
            return
        elif id<0:
            id += 40

        move_op(s.TURN-1,id)

    def sell_something(id):
        if f[s.current_place].house==0:
            f[s.current_place].sell()
            p[id].owned-=1
            p[id].money += f[s.current_place].price / 2
            s.STAGE=5
        else:
            f[s.current_place].sell_house()
            p[id].money+=f[s.current_place].house_price / 2
        s.STAGE = 5


    def on_prison(id):
        if p[id].prison():
            if p[id].free>0:
                p[id].free-=1
                p[id].prisoned= False
                p[id].prison_stage=0
                return False
            if d.d1==d.d2:
                p[id].prisoned = False
                p[id].prison_stage=0
            return True
        return False


    def rent(id):
        if p[id].prisoned:
            p[id].money -= 50
            p[id].prisoned = False
            s.STAGE = 5
            return
        p[id].money-=f[s.current_place].new_rent
        p[f[s.current_place].owned-1].money+=f[s.current_place].new_rent
        s.STAGE = 5

    def buy(id):
        f[s.current_place].owned=id+1
        p[id].owned+=1
        p[id].money-=f[s.current_place].price
        buttons[s.current_place+6].color=PLAYER_COLOR[id]
        s.STAGE = 5



    def roll_dice(buttons):
        create_buttons_main_game(s.mode, buttons)
        onclickbutton()
        pg.display.flip()
        animate_dice()
        d.d1 = random.randint(0, 5)
        d.d2 = random.randint(0, 5)
        screen.fill((217, 217, 217), dice_pos1)
        screen.fill((217, 217, 217), dice_pos2)
        screen.blit(dice[d.d1], dice_pos1)
        screen.blit(dice[d.d2], dice_pos2)
        pg.display.update(dice_pos1)
        pg.display.update(dice_pos2)


    def roll(id, buttons):
        if s.action == 6:
            roll_dice(buttons)
            if d.d1==d.d2:
                p[id].money += 50
            else:
                p[id].money -= 50
            s.STAGE=4
            return
        s.inc_stage()
        roll_dice(buttons)
        if on_prison(id):
            s.STAGE=4
        else:
            move(id)
            s.inc_stage()
            create_buttons_main_game(s.mode, buttons)


    def create_side_buttons():
        btns = [
                Button(775+i*160, 35, 77, 24, text, action=action)
                for i, (text, action) in enumerate([
                    ("", lambda: get_info(0)),
                    ("", lambda: get_info(1)),
                ])]
        btns += [
            Button(1015+i*80, 35, 77, 24, text, action=action)
            for i, (text, action) in enumerate([
                ("", lambda: get_info(2)),
                ("", lambda: get_info(23)),
                ("", lambda: get_info(3)),
                ("", lambda: get_info(4)),
            ])]
        btns += [
            Button(1414 + i * 80, 35, 77, 24, text, action=action)
            for i, (text, action) in enumerate([
                ("", lambda: get_info(5)),
                ("", lambda: get_info(6)),
            ])]
        btns += [
            Button(1734, 222+i*80, 24, 77, text, action=action)
            for i, (text, action) in enumerate([
                ("", lambda: get_info(7)),
                ("", lambda: get_info(8)),
            ])]
        btns += [
            Button(1734, 462 + i * 80, 24, 77, text, action=action)
            for i, (text, action) in enumerate([
                ("", lambda: get_info(9)),
                ("", lambda: get_info(24)),
                ("", lambda: get_info(10)),
            ])]
        btns += [
            Button(1734, 782, 24, 77, text, action=action)
            for i, (text, action) in enumerate([
                ("", lambda: get_info(11)),
            ])]

        btns += [
            Button(1494-i*80, 1021, 77, 24, text, action=action)
            for i, (text, action) in enumerate([
                ("", lambda: get_info(12)),
                ("", lambda: get_info(13)),
            ])]

        btns += [
            Button(1255 - i * 80, 1021, 77, 24, text, action=action)
            for i, (text, action) in enumerate([
                ("", lambda: get_info(14)),
                ("", lambda: get_info(25)),
                ("", lambda: get_info(15)),
                ("", lambda: get_info(16)),
            ])]

        btns += [
            Button(855 - i * 80, 1021, 77, 24, text, action=action)
            for i, (text, action) in enumerate([
                ("", lambda: get_info(17)),
                ("", lambda: get_info(18)),
            ])]

        btns += [
            Button(588, 781 - i * 80, 24, 77, text, action=action)
            for i, (text, action) in enumerate([
                ("", lambda: get_info(19)),
                ("", lambda: get_info(20)),
            ])]

        btns += [
            Button(588, 541 - i * 160, 24, 77, text, action=action)
            for i, (text, action) in enumerate([
                ("", lambda: get_info(26)),
                ("", lambda: get_info(21)),
                ("", lambda: get_info(22)),
            ])]

        return btns

    def chance_action(id_player,id_action):
        if id_action == 0:
            p[id_player].money +=100
            s.systemcall = "You win 100$!"
            s.STAGE = 4
        if id_action == 1:
            p[id_player].money += 10
            s.systemcall = "You win 10$!"
            s.STAGE = 4
        if id_action == 2:
            p[id_player].money -= 40
            s.systemcall = "You lost 40$!"
            s.STAGE=4
        if id_action == 3:
            s.systemcall = "Move 3 points!"
            move_op(id_player, 3)
            choose_action(s.TURN - 1, p[s.TURN - 1].pos)
        if id_action == 4:
            s.systemcall = "Move 5 points!"
            move_op(id_player, 5)
            choose_action(s.TURN-1, p[s.TURN-1].pos)
        if id_action == 5:
            s.systemcall = "You win ticket from jail!"
            p[id_player].free += 1
            s.STAGE = 4
        if id_action==6:
            s.systemcall = "You go to prison!"
            go_to_prison(id_player)
            p[id_player].prisoned = True
            s.STAGE = 4

    chance_p = PullC([0,0,1,1,2,2,3,3,4,4,5,5,6,6], [])

    def chance(id):
        if len(chance_p.local_pull) == 0:
            chance_p.refile_deck()
        rand_num = random.randint(0, len(chance_p.local_pull)-1)
        chance_p.local_pull.remove(chance_p.local_pull[rand_num])
        chance_action(id, rand_num)

    def generate_buttons_main_game():
        buttons = [
            Button(826 + i * 147, 650, 131, 60, text, action=action)
            for i, (text, action) in enumerate([
                ("Buy", lambda: buy(s.TURN-1)),
                ("Upgrade", lambda: uprgade_field(s.TURN-1)),
                ("Rent", lambda: get_info(rent(s.TURN-1))),
            ])
        ]
        buttons += [
            Button(826 + i * 147, 718, 131, 60, text, action=action)
            for i, (text, action) in enumerate([
                ("Sell", lambda: sell_something(s.TURN-1)),
                ("Skip", lambda: skip()),
                ("Roll", lambda: roll(s.TURN - 1, buttons)),
            ])
        ]
        buttons += create_side_buttons()
        return buttons

    def create_buttons_main_game(md,buttons):
        if md==1:
            buttons = generate_buttons_main_game()
            s.inc_mode()
        elif md==2:
            #Roll
            if s.STAGE == 1:
                buttons[0].active = False
                buttons[1].active = False
                buttons[2].active = False
                buttons[3].active = False
                buttons[4].active = False
                buttons[5].active = True
                s.systemcall = "Roll dice!"

            #Disabling
            elif s.STAGE == 2:
                buttons[0].active = False
                buttons[1].active = False
                buttons[2].active = False
                buttons[3].active = False
                buttons[4].active = False
                buttons[5].active = False
                s.systemcall = "Moving!"
            #Actions

            elif s.STAGE == 3:
                choose_action(s.TURN-1, p[s.TURN-1].pos)
                ##Ready to buy
                if s.action==1:
                    buttons[0].active = True if p[s.TURN-1].money >= f[s.current_place].price and f[s.current_place].owned==0 else False
                    buttons[1].active = False
                    buttons[2].active = False
                    buttons[3].active = False
                    buttons[4].active = True
                    buttons[5].active = False
                    s.systemcall = "You can buy this place!"
                ##Ready to rent
                elif s.action==2:
                    buttons[0].active = False
                    buttons[1].active = False
                    buttons[2].active = True
                    buttons[3].active = False
                    buttons[4].active = True
                    buttons[5].active = False
                    s.systemcall = "Pay rent!"
                elif s.action==3:

                ##My location
                    buttons[0].active = False
                    buttons[1].active = True if check_field(f[s.current_place].zone) and f[s.current_place].house<5 and p[s.TURN-1].money > f[s.current_place].house_price else False
                    buttons[2].active = False
                    buttons[3].active = True
                    buttons[4].active = True
                    buttons[5].active = False
                    s.systemcall = "You can buy or sell houses!" if check_field(f[s.current_place].zone) and f[s.current_place].house<5 and p[s.TURN-1].money > f[s.current_place].house_price else "You can sell houses!"
                ##Nothing to do
                elif s.action==4:
                    buttons[0].active = False
                    buttons[1].active = False
                    buttons[2].active = False
                    buttons[3].active = False
                    buttons[4].active = True
                    buttons[5].active = False
                    s.systemcall = "Skip!"
                elif s.action == 6:
                    buttons[0].active = False
                    buttons[1].active = False
                    buttons[2].active = False
                    buttons[3].active = False
                    buttons[4].active = True
                    buttons[5].active = True if p[s.TURN-1].money >= 50 else False
                    s.systemcall = "You can pay 50$ and win 100$!" if p[s.TURN-1].money >= 50 else "Skip!"
            #Prison
            elif s.STAGE == 4:
                buttons[0].active = False
                buttons[1].active = False
                buttons[2].active = True
                buttons[3].active = False
                buttons[4].active = True
                buttons[5].active = False
                s.systemcall = "Try your luck or pay 50$!"

            elif s.STAGE == 5:
                buttons[0].active = False
                buttons[1].active = False
                buttons[2].active = False
                buttons[3].active = False
                buttons[4].active = True
                buttons[5].active = False
        return buttons




    def choose_action(id,pos):
        if pos in (0, 2, 8, 14, 18, 20, 23, 28, 31, 34, 36, 38,11):
            if pos == 11:
                s.action=4
                return

            #Take money
            if pos in (2,34):
                p[id].money +=100
                s.action = 4
                return
            #Loose money
            if pos in (18,38):
                p[id].money -=100
                s.action = 4
                return
            #Chance
            if pos in (8,14,23,28,36):
                chance(id)
                return
            #Big Active
            else:
                if pos ==0:
                    p[id].money+=250
                    s.action=4
                    return
                if pos == 31:
                    if p[id].free > 0:
                        p[id].free -= 1
                    else:
                        go_to_prison(id)
                        p[id].prisoned=True
                    s.action = 4
                    return
                if pos == 20:
                    s.action=6
                    return
        else:
            for location in f:
                if location.id == pos:
                    s.current_place=location.idv
                    break
            if f[s.current_place].owned==0:
                s.action=1
            elif f[s.current_place].owned == id+1:
                s.action=3
            else:
                s.action=2




    def update_information(id):
        for i in range(id):
            lb[i+2].text = "Name: Player " + str(p[i].id+1) + "\n" + "Money: " + str(p[i].money) + "$\n" + "Jail escape: " + str(p[i].free) + "\n" + "Owned: " + str(p[i].owned) + "\n" + "Jailed? "
            lb[i+2].text += str(p[i].prisoned) if p[i].prisoned else "False"

    def update_system_information():
        lb[1].text = "Turn: " + str(s.TURN) + "\n" + s.systemcall

    def get_info(id):
        lb[0].text = "Name: " + f[id].name + "\n" + "Price: " + str(f[id].price) + "$\n" + "Rent: " + str(
            f[id].new_rent()) + "$\n" + "Multiplier: " + str(f[id].new_mult()) + "x\n"

    def print_split(id,x_offset,y_offset):
        line_spacing=35
        text_lines = lb[id].text.split("\n")
        for line in text_lines:
            if id==1:
                text_surface = custom_font2.render(line, True, BLACK)
            else:
                text_surface = custom_font1.render(line, True, BLACK)
            screen.blit(text_surface, (x_offset,y_offset))
            y_offset += line_spacing

    def skip():
        if d.move_again == 1:
            d.move_again = 0
        elif s.TURN != s.PLAYERS:
            s.TURN += 1
        else:
            s.TURN = 1
        s.STAGE = 1
        d.prison = 0
        check=0
        check1=0
        for i in range(s.PLAYERS):
            if p[i].money<0:
                check+=1
            else:
                check1 = i
        check1+=1
        if check==s.PLAYERS-1:
            s.STAGE = 2;
            s.systemcall = "Player " + check1 + " WIN!"
            return

        if p[s.TURN].money<0:
            skip()

    def create_main_game():
        screen.fill(BLACK)
        screen.blit(Iboard, (612, 59))
        screen.fill((217, 217, 217), dice_pos1)
        screen.fill((217, 217, 217), dice_pos2)
        screen.blit(dice[d.d1], dice_pos1)
        screen.blit(dice[d.d2], dice_pos2)
        update_information(s.PLAYERS)
        update_system_information()
        print_split(0,800,240)
        print_split(1,1180,240)
        for i in range(s.PLAYERS):
            screen.blit(players[i], (p[i].x, p[i].y))
            screen.blit(players_card[i], (49,62+i*253))
            print_split(i+2,51,64+i*253)


        onclickbutton()



    # Константи для роботи меню
    STATE_MAIN_MENU = 0
    STATE_SINGLE_PLAYER = 1
    STATE_MULTIPLAYER = 2
    STATE_SETTINGS = 3
    STATE_STATS = 4
    STATE_DOWNLOAD = 5
    STATE_NEWGAME = 6
    STATE_ONGAME = 7

    current_state=States()
    current_state.set_state(STATE_MAIN_MENU)

    # Цикл роботи програми
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        button_sound.play()
                        print(f"Button clicked: {button.text}")
                        handle_button_click(button)

        if current_state.state == STATE_MAIN_MENU:
            buttons = create_buttons_main_menu()
            draw_main_menu()
        elif current_state.state == STATE_SINGLE_PLAYER:
            buttons = create_buttons_single_player()
            draw_single_player()
        elif current_state.state == STATE_MULTIPLAYER:
            buttons = create_buttons_multiplayer()
            draw_multiplayer()
        elif current_state.state == STATE_SETTINGS:
            buttons = create_buttons_settings()
            draw_settings()
        elif current_state.state == STATE_STATS:
            buttons = create_buttons_stats()
            draw_stats()
        elif current_state.state == STATE_NEWGAME:
            draw_newgame()
            current_state.set_state(STATE_ONGAME)
        elif current_state.state == STATE_DOWNLOAD:
            draw_download()
        elif current_state.state == STATE_ONGAME:
            buttons = create_buttons_main_game(s.mode, buttons)
            create_main_game()
            pg.display.flip()
            onclickbutton()

        # Оновлення екрану
        pg.display.flip()
        clock.tick(30)

    # Вихід
    pg.quit()




if __name__ == '__main__':
    main()


