import tkinter as tk
import random

WIDTH, HEIGHT = 400, 600
PIPE_GAP = 150
PIPE_WIDTH = 60
GRAVITY = 1.5
FLAP_STRENGTH = -12
BIRD_SIZE = 30
PIPE_SPEED = 4

class FlappyBirdGame:
    def __init__(self, root):  
        self.root = root
        self.root.title("Flappy Bird with Tkinter")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()

        self.bird = self.canvas.create_oval(
            WIDTH // 4 - BIRD_SIZE // 2, HEIGHT // 2 - BIRD_SIZE // 2,
            WIDTH // 4 + BIRD_SIZE // 2, HEIGHT // 2 + BIRD_SIZE // 2,
            fill="yellow"
        )

        self.bird_y_velocity = 0


        self.pipes = []
        self.add_pipe()


        self.score = 0
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", font=("Arial", 16), fill="black", text=f"Score: {self.score}")

        self.root.bind("<space>", self.flap)


        self.running = True
        self.game_loop()

    def add_pipe(self):
        y_position = random.randint(200, HEIGHT - 200)
        top_pipe = self.canvas.create_rectangle(WIDTH, 0, WIDTH + PIPE_WIDTH, y_position - PIPE_GAP, fill="green")
        bottom_pipe = self.canvas.create_rectangle(WIDTH, y_position, WIDTH + PIPE_WIDTH, HEIGHT, fill="green")
        self.pipes.append((top_pipe, bottom_pipe))

    def move_pipes(self):
        for top_pipe, bottom_pipe in self.pipes:
            self.canvas.move(top_pipe, -PIPE_SPEED, 0)
            self.canvas.move(bottom_pipe, -PIPE_SPEED, 0)

        
        self.pipes = [
            (top_pipe, bottom_pipe) for top_pipe, bottom_pipe in self.pipes
            if self.canvas.coords(top_pipe)[2] > 0
        ]

    
        if len(self.pipes) == 0 or self.canvas.coords(self.pipes[-1][0])[0] < WIDTH // 2:
            self.add_pipe()

    def check_collision(self):
        bird_coords = self.canvas.coords(self.bird)
        
        
        if bird_coords[1] <= 0 or bird_coords[3] >= HEIGHT:
            return True

        
        for top_pipe, bottom_pipe in self.pipes:
            if self.overlap(self.bird, top_pipe) or self.overlap(self.bird, bottom_pipe):
                return True

        return False

    def overlap(self, item1, item2):
        coords1 = self.canvas.coords(item1)
        coords2 = self.canvas.coords(item2)
        return not (
            coords1[2] < coords2[0] or
            coords1[0] > coords2[2] or
            coords1[3] < coords2[1] or
            coords1[1] > coords2[3]
        )

    def update_score(self):
        for top_pipe, _ in self.pipes:
            pipe_coords = self.canvas.coords(top_pipe)
            if pipe_coords[2] < WIDTH // 4 and pipe_coords[2] + PIPE_SPEED >= WIDTH // 4:
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def flap(self, event):
        self.bird_y_velocity = FLAP_STRENGTH

    def game_loop(self):
        if not self.running:
            return

        
        self.bird_y_velocity += GRAVITY
        self.canvas.move(self.bird, 0, self.bird_y_velocity)


        self.move_pipes()

        
        if self.check_collision():
            self.running = False
            self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2, text="Game Over", font=("Arial", 32), fill="red"
            )
            return

       
        self.update_score()

        
        self.root.after(20, self.game_loop)

if __name__ == "__main__": 
    root = tk.Tk()
    game = FlappyBirdGame(root)
    root.mainloop()
