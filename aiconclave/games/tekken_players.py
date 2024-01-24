import time
import random
import pydirectinput as pg
import pyautogui as pag

class Tekken:
    def __init__(self):
        self.left = "left"
        self.right = "right"
        self.keys = {
            "green": "a", 
            "red": "s",
            "blue": "z", 
            "pink": "x"
        }

    def press_key(self, delay=0.2, *args):
        for key in args:
            if isinstance(key, list) and len(key) == 2:
                pg.keyDown(self.keys[key[0]])
                pg.keyDown(self.keys[key[1]])
                time.sleep(delay)
                pg.keyUp(self.keys[key[1]])
                pg.keyUp(self.keys[key[0]])  
            else:
                pg.keyDown(self.keys[key])
                time.sleep(0.1)
                pg.keyUp(self.keys[key])
    
    def perform_combo_hit(self):
        combo_hits = [
            ["pink", "green", "blue", "green", "pink"],
            ["pink", "green", "blue", "pink", "red"],
            ["pink", "green", "blue", "pink", "green"],
            ["blue", "green", "red", "blue", ["pink", "red"], "green", "green", "pink", "green"],
        ]
        random_combo = random.choice(combo_hits)
        self.press_key(0, *random_combo)
        
    def r_kick(self):
        self.press_key(0.0, "red")
    
    def r_punch(self):
        self.press_key(0.0, "green")
    
    def l_kick(self):
        self.press_key(0.0, "blue")
    
    def l_punch(self):
        self.press_key(0.0, "pink")
    
class PaulPhoenix(Tekken):
    def burning_fist(self):
        pg.keyDown(self.left)
        time.sleep(0.55)
        for _ in range(2):
            self.press_key(0.5, ["pink", "green"])
        pg.keyUp(self.left)
        
    def hammer_of_god(self):
        pg.keyDown(self.right)
        time.sleep(0.25)
        self.press_key(0.5, ["pink", "green"])
        pg.keyUp(self.right)

    
    def foot_launch(self):
        pg.keyDown(self.left)
        for _ in range(1):
            self.press_key(0.7, ["green", "blue"])
        pg.keyUp(self.left)
        
    def gut_buster(self, other=False):
        pg.keyDown("down")
        pg.keyDown(self.right)
        for _ in range(3):
            self.press_key(0.6, ["pink", "green"] if other else ["green", "pink"])
        pg.keyUp(self.right)
        pg.keyUp("down")
    

def main():
    time.sleep(2)
    
    paul = PaulPhoenix()

    paul.burning_fist()
    paul.hammer_of_god()
    paul.gut_buster(other=True)
    paul.perform_combo_hit()
    paul.foot_launch()
    
if __name__ == "__main__":
    main()