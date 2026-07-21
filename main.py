import tkinter as tk
import random

class Gamblinginator3000(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("gamblinginator3000")
        self.geometry("800x600")
        self.configure(bg="#000")
        self.resizable(False, False)

        #  b&w color pallette blehh
        self.BG = "#000000"
        self.FG = "#FFFFFF"
        self.GRAY = "#888888"
        self.FONT_BIG = ("Courier New", 32, "bold")
        self.FONT_MED = ("Courier New", 18, "bold")
        self.FONT_SML = ("Courier New", 14)
        self.FONT_BTN = ("Courier New", 16, "bold")
        self.FONT_ICON = ("Courier New", 48, "bold")

        # Single Canvas
        self.c = tk.Canvas(self, bg=self.BG, highlightthickness=0)
        self.c.pack(fill="both", expand=True)

        # State n Hitbox tracking
        self.buttons = []
        self.animating = False
        
        self.c.bind("<Button-1>", self.on_click)
        self.reset_game()
        self.render()

    def reset_game(self):
        self.gold = 100
        self.hp = 3
        self.floor = 1
        self.max_floor = 5
        self.luck = 0
        self.bet = 10
        self.slots = ["cherry", "cherry", "cherry"]
        self.state = "hub"
        
        # Result tracking
        self.last_game = None
        self.last_won = False
        self.last_amount = 0
        self.last_msg = ""

    def clear(self):
        # Wipe EVERYTHING to prevent overlay bugs cuz ts pmo wayyyy too much
        self.c.delete("all")
        self.buttons = []

    def add_btn(self, x, y, w, h, text, action):

        self.c.create_rectangle(x, y, x+w, y+h, outline=self.FG, width=2)
        self.c.create_text(x+w/2, y+h/2, text=text, font=self.FONT_BTN, fill=self.FG)
        self.buttons.append({'x1': x, 'y1': y, 'x2': x+w, 'y2': y+h, 'action': action})

    def draw_hud(self):
        self.c.create_rectangle(0, 0, 800, 60, fill="#111", outline=self.FG, width=2)
        self.c.create_text(120, 30, text=f"GOLD: {self.gold}", font=self.FONT_MED, fill=self.FG)
        hp_str = "O" * self.hp + "." * (3 - self.hp)
        self.c.create_text(320, 30, text=f"HP: {hp_str}", font=self.FONT_MED, fill=self.FG)
        self.c.create_text(520, 30, text=f"LUCK: +{self.luck}%", font=self.FONT_MED, fill=self.FG)
        self.c.create_text(700, 30, text=f"FLR: {self.floor}/{self.max_floor}", font=self.FONT_MED, fill=self.FG)

# this segment gave me schizophrenia
    def draw_icon(self, cx, cy, size, name):
        s = size
        if name == 'heads':
            self.c.create_oval(cx-s, cy-s, cx+s, cy+s, outline=self.FG, width=4)
            self.c.create_text(cx, cy, text="H", font=self.FONT_ICON, fill=self.FG)
        elif name == 'tails':
            self.c.create_oval(cx-s, cy-s, cx+s, cy+s, outline=self.FG, width=4)
            self.c.create_text(cx, cy, text="T", font=self.FONT_ICON, fill=self.FG)
        elif name == 'seven':
            self.c.create_polygon(cx-s, cy-s, cx+s, cy-s, cx+s, cy-s+s//3, cx-s//3, cy+s, cx-s//2, cy+s, cx+s//2, cy-s+s//3, cx-s, cy-s+s//3, fill=self.FG, outline=self.FG)
        elif name == 'cherry':
            r = s // 2
            self.c.create_oval(cx-s, cy-r, cx-s+2*r, cy+r, outline=self.FG, width=3)
            self.c.create_oval(cx, cy-r, cx+2*r, cy+r, outline=self.FG, width=3)
            self.c.create_line(cx-s+r, cy-r, cx, cy-s, cx+r, cy-r, fill=self.FG, width=3, smooth=True)
        elif name == 'bell':
            self.c.create_polygon(cx-s, cy+s//2, cx-s//2, cy-s, cx+s//2, cy-s, cx+s, cy+s//2, outline=self.FG, width=3)
            self.c.create_oval(cx-s//4, cy+s//2, cx+s//4, cy+s, outline=self.FG, width=3)
        elif name == 'diamond':
            self.c.create_polygon(cx, cy-s, cx+s, cy, cx, cy+s, cx-s, cy, outline=self.FG, width=3)
        elif name == 'lemon':
            self.c.create_oval(cx-s, cy-s//2, cx+s, cy+s//2, outline=self.FG, width=3)
            self.c.create_polygon(cx-s, cy, cx-s-s//3, cy-s//4, cx-s-s//3, cy+s//4, fill=self.FG)
            self.c.create_polygon(cx+s, cy, cx+s+s//3, cy-s//4, cx+s+s//3, cy+s//4, fill=self.FG)

    # ==========================================
    # RENDERING (State Machine)
    # ==========================================
    def render(self):
        self.clear()
        if self.state == "hub": self.render_hub()
        elif self.state == "coin": self.render_coin()
        elif self.state == "slots": self.render_slots()
        elif self.state == "result": self.render_result()
        elif self.state == "gameover": self.render_gameover()
        elif self.state == "win": self.render_win()

    def render_hub(self):
        self.draw_hud()
        self.c.create_text(400, 140, text="gamblinginator3000", font=self.FONT_BIG, fill=self.FG)
        self.c.create_text(400, 190, text="The House always wins. Eventually :p", font=self.FONT_SML, fill=self.GRAY)
        
        self.add_btn(250, 260, 300, 60, "[ COIN FLIP ]", lambda: self.set_state("coin"))
        self.add_btn(250, 340, 300, 60, "[ SLOTS ]", lambda: self.set_state("slots"))
        self.add_btn(250, 480, 300, 40, "[ QUIT ]", self.destroy)

    def render_coin(self):
        self.draw_hud()
        self.c.create_text(400, 120, text="COIN FLIP :3", font=self.FONT_BIG, fill=self.FG)
        self.draw_icon(400, 240, 60, "heads")
        
        self.c.create_text(400, 340, text=f"BET: {self.bet}", font=self.FONT_MED, fill=self.FG)
        self.add_btn(280, 370, 80, 40, "- 10", lambda: self.adjust_bet(-10))
        self.add_btn(440, 370, 80, 40, "+ 10", lambda: self.adjust_bet(10))
        
        self.add_btn(300, 440, 200, 60, "[ FLIP ]", self.flip_coin)
        self.add_btn(300, 520, 200, 40, "[ BACK ]", lambda: self.set_state("hub"))

    def render_slots(self):
        self.draw_hud()
        self.c.create_text(400, 120, text="SLOT MACHINE :3", font=self.FONT_BIG, fill=self.FG)
        
        for i in range(3):
            x = 250 + i * 120
            self.c.create_rectangle(x, 160, x+100, 280, outline=self.FG, width=3)
            self.draw_icon(x+50, 220, 35, self.slots[i])
            
        self.c.create_text(400, 340, text=f"BET: {self.bet}", font=self.FONT_MED, fill=self.FG)
        self.add_btn(280, 370, 80, 40, "- 10", lambda: self.adjust_bet(-10))
        self.add_btn(440, 370, 80, 40, "+ 10", lambda: self.adjust_bet(10))
        
        self.add_btn(300, 440, 200, 60, "[ PULL ]", self.spin_slots)
        self.add_btn(300, 520, 200, 40, "[ BACK ]", lambda: self.set_state("hub"))

    def render_result(self):
        self.draw_hud()
        self.c.create_text(400, 120, text="RESULT", font=self.FONT_BIG, fill=self.FG)
        
        if self.last_game == "coin":
            self.draw_icon(400, 240, 60, "heads" if self.last_won else "tails")
        else:
            for i in range(3):
                x = 250 + i * 120
                self.c.create_rectangle(x, 160, x+100, 280, outline=self.FG, width=3)
                self.draw_icon(x+50, 220, 35, self.slots[i])

        color = self.FG if self.last_won else self.GRAY
        self.c.create_text(400, 340, text=f"{self.last_msg} {self.last_amount} Gold", font=self.FONT_MED, fill=color)
        self.add_btn(300, 440, 200, 60, "[ CONTINUE ]", self.next_floor)

    def render_gameover(self):
        self.c.create_text(400, 200, text="BANKRUPT", font=self.FONT_BIG, fill=self.FG)
        self.c.create_text(400, 260, text="The House claims your soul.", font=self.FONT_MED, fill=self.GRAY)
        self.c.create_text(400, 300, text=f"Reached Floor {self.floor}", font=self.FONT_SML, fill=self.FG)
        self.add_btn(300, 400, 200, 60, "[ TRY AGAIN ]", self.restart)

    def render_win(self):
        self.c.create_text(400, 200, text="HIGH ROLLER", font=self.FONT_BIG, fill=self.FG)
        self.c.create_text(400, 260, text="You beat the Casino!", font=self.FONT_MED, fill=self.FG)
        self.c.create_text(400, 300, text=f"Final Gold: {self.gold}", font=self.FONT_SML, fill=self.FG)
        self.add_btn(300, 400, 200, 60, "[ PLAY AGAIN ]", self.restart)

#interaction logic
    def on_click(self, event):
        if self.animating: return
        for btn in reversed(self.buttons):
            if btn['x1'] <= event.x <= btn['x2'] and btn['y1'] <= event.y <= btn['y2']:
                btn['action']()
                return

    def set_state(self, state):
        self.state = state
        self.render()

    def adjust_bet(self, amt):
        self.bet = max(10, min(self.gold, self.bet + amt))
        self.render()

    def restart(self):
        self.reset_game()
        self.render()

    def take_damage(self):
        self.hp -= 1
        if self.hp <= 0 or self.gold <= 0:
            self.state = "gameover"
            self.render()
            return True
        return False

    def next_floor(self):
        self.floor += 1
        if self.floor > self.max_floor:
            self.state = "win"
            self.render()
        else:
            self.state = "hub"
            self.render()

    def flip_coin(self):
        if self.bet > self.gold: return
        self.gold -= self.bet
        self.animating = True
        
        def animate(step):
            self.clear()
            self.draw_hud()
            self.c.create_text(400, 120, text="COIN FLIP", font=self.FONT_BIG, fill=self.FG)
            name = "heads" if step % 2 == 0 else "tails"
            self.draw_icon(400, 240, 60, name)
            if step < 6:
                self.after(100, lambda: animate(step + 1))
            else:
                self.resolve_coin()
                
        animate(0)

    def resolve_coin(self):
        win_chance = 0.45 + (self.luck / 100.0)
        won = random.random() < win_chance
        
        if won:
            amt = int(self.bet * 1.8)
            self.gold += amt
            self.luck += 2
            msg = "WIN!"
        else:
            amt = self.bet
            self.luck = max(0, self.luck - 1)
            msg = "LOSE!"

        self.last_game = "coin"
        self.last_won = won
        self.last_amount = amt
        self.last_msg = msg
        
        if not won:
            if self.take_damage(): 
                self.animating = False
                return

        self.state = "result"
        self.render()
        self.animating = False

    def spin_slots(self):
        if self.bet > self.gold: return
        self.gold -= self.bet
        self.animating = True
        
        symbols = ["seven", "cherry", "bell", "diamond", "lemon"]
        
        def animate_reel(reel_idx, steps):
            if steps > 0:
                self.clear()
                self.draw_hud()
                self.c.create_text(400, 120, text="SLOT MACHINE", font=self.FONT_BIG, fill=self.FG)
                
                for i in range(3):
                    x = 250 + i * 120
                    self.c.create_rectangle(x, 160, x+100, 280, outline=self.FG, width=3)
                    if i == reel_idx:
                        self.draw_icon(x+50, 220, 35, random.choice(symbols))
                    else:
                        self.draw_icon(x+50, 220, 35, self.slots[i])
                        
                self.c.create_text(400, 340, text=f"BET: {self.bet}", font=self.FONT_MED, fill=self.FG)
                
                self.after(80 + reel_idx * 40, lambda: animate_reel(reel_idx, steps - 1))
            else:
                if random.random() < (self.luck / 100.0):
                    self.slots[reel_idx] = "seven"
                else:
                    self.slots[reel_idx] = random.choice(symbols)
                
                if reel_idx < 2:
                    self.after(200, lambda: animate_reel(reel_idx + 1, 8))
                else:
                    self.resolve_slots()

        animate_reel(0, 8)

    def resolve_slots(self):
        s1, s2, s3 = self.slots
        amt = 0
        msg = ""
        
        if s1 == s2 == s3:
            if s1 == "seven":
                amt = self.bet * 10
                msg = "JACKPOT!"
                self.luck += 5
            else:
                amt = self.bet * 5
                msg = f"THREE {s1.upper()}S!"
                self.luck += 2
        elif s1 == s2 or s2 == s3 or s1 == s3:
            amt = int(self.bet * 1.5)
            msg = "TWO MATCH!"
            self.luck += 1
        else:
            msg = "NO MATCH."
            self.luck = max(0, self.luck - 1)

        won = amt > 0
        
        self.last_game = "slots"
        self.last_won = won
        self.last_amount = amt
        self.last_msg = msg

        if won:
            self.gold += amt
        else:
            amt = self.bet
            if self.take_damage(): 
                self.animating = False
                return

        self.state = "result"
        self.render()
        self.animating = False

if __name__ == "__main__":
    app = Gamblinginator3000()
    app.mainloop()
