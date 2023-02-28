import pygame as py

py.init()

WIDTH = 800
HEIGHT = 800 

WINDOW = py.display.set_mode((WIDTH,HEIGHT))

CLOCK = py.time.Clock()

gui_font = py.font.Font(None,30)

class Button :
    def __init__(self,text,width,height,position,elevation) :
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y = position[1]

        # top rectangle
        self.top_rect = py.Rect((position),(width,height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = py.Rect((position),(width,height))
        self.bottom_color = '#354B5E'

        #text
        self.text_surf = gui_font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    def draw(self) :
        # elevation logic
        self.top_rect.y = self.original_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        py.draw.rect(WINDOW,self.bottom_color,self.bottom_rect,border_radius = 20)

        py.draw.rect(WINDOW,self.top_color,self.top_rect,border_radius = 20)
        WINDOW.blit(self.text_surf,self.text_rect)
        self.check_click()
    
    def check_click(self) :
        mouse_pos = py.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos) :

            self.top_color = '#D74B4B'

            if py.mouse.get_pressed()[0] :
                self.dynamic_elevation = 0
                self.pressed = True
            else : 
                self.dynamic_elevation = self.elevation
                if self.pressed == True :
                    print('click')
                    self.pressed = False 
        else : 
            self.dynamic_elevation = self.elevation 
            self.top_color = '#475F77'
            if self.pressed == True :
                print('click')
                self.pressed = False 
            

button1 = Button('Test',200,40,(WIDTH/2,HEIGHT/2),6)

running = True
while running :

    for event in py.event.get() :
        if event.type == py.QUIT :
            py.quit()
    

    # update
    py.display.update()
    CLOCK.tick(60)

    # render
    WINDOW.fill('#DCDDD8')
    button1.draw()

