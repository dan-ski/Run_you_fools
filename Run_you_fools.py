# Run you fools
# Player has to run from falling comets

from livewires import games, color
import random

games.init(screen_width=1280, screen_height=720, fps=50)

class Hero(games.Sprite):
    hero_image = games.load_image("hero_2.jpg")

    def __init__(self):
        super(Hero,self).__init__(image=Hero.hero_image,
                                 x=games.mouse.x,
                                 bottom=games.screen.height)
        self.score=games.Text(value=0, size=100, color=color.black,
                              top=5, right=games.screen.width-10)
        games.screen.add(self.score)
        self.time_til_drop = 0
        self.count=0

    def update(self):
        self.x=games.mouse.x

        if self.left<0:
            self.left=0

        if self.right>games.screen.width:
            self.right=games.screen.width

        self.check_pass()
        self.check_drop()

    def check_pass(self):
        if not self.overlapping_sprites:
            self.count+=1
            if self.count % 50 == 0:
                self.score.value+=1
            self.score.right = games.screen.width - 10

        else:
            self.end_game()

    def check_drop(self):
        """Decrease the counter measuring the time or drop the comet and reset countdown"""
        comet_x = random.randrange(games.screen.width)
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_comet = Comet(x=comet_x)
            games.screen.add(new_comet)

            # Set the margin more less 30 % of comet's height, no matter what the speed of comet is 
            self.time_til_drop = int(new_comet.height * 1.3 / Comet.speed) + 1

    def end_game(self):
        """End the game"""
        end_message=games.Message(value="Koniec gry!",
                                  size=90,
                                  color=color.black,
                                  x=games.screen.width/2,
                                  y=games.screen.height/2,
                                  lifetime=5*games.screen.fps,
                                  after_death=games.screen.quit)
        games.screen.add(end_message)

class Comet (games.Sprite):
    """A comet falling down on Earth"""
    comet_image=games.load_image("rock.jpg")
    speed=1

    def __init__(self,x=games.screen.width/2,y=90):
        super(Comet,self).__init__(image=Comet.comet_image,
                                   x=x,
                                   y=y,
                                   dy=Comet.speed
                                   )
    def update(self):
        """Check if the bottom of the comet touched the bottom of screen"""
        if self.bottom>games.screen.width:
            self.destroy()

def main():
    sky_image=games.load_image("night_sky.jpg", transparent=False)
    games.screen.background=sky_image

    the_hero = Hero()
    games.screen.add(the_hero)

    games.mouse.is_visible=False
    games.screen.event_grab=True

    games.screen.mainloop()

main()

