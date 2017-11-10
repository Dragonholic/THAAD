
def model1():
    gamepad.blit(img, (x,y))


class Player:
    init_weapon = 1
    def __init__(self,model, weapon):
        self.x = 100
        self.y = 334

        if model == 1:


    def move(self, x, y):
        self.x = self.x + x
        self.y = self.y + y



player1 = Player(1,1)

while True:
    background = (0, 0, 0)




