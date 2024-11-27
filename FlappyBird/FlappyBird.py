import tkinter as tk
import random

# Constantes
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 600
BIRD_COLOR = "yellow"
PIPE_COLOR = "green"
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_GAP = 150  # Distância entre o topo e o fundo dos pipes
PIPE_FREQUENCY = 90  # Menor valor cria mais pipes, ajustando para 90 vai gerar menos pipes
PIPE_SPEED = -5
PIPE_MIN_HEIGHT = 100  # Altura mínima para o pipe
PIPE_MAX_HEIGHT = 400  # Altura máxima para o pipe

class FlappyBird:
    def _init_(self, master):
        self.master = master
        self.master.title("Flappy Bird Clone")
        self.reset_game()

    def reset_game(self):
        # Inicializa o canvas e elementos do jogo
        self.canvas = tk.Canvas(self.master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="skyblue")
        self.canvas.pack()

        self.bird = self.canvas.create_oval(50, 300, 100, 350, fill=BIRD_COLOR)  # Posição inicial do pássaro
        self.bird_y_velocity = 0
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.pipe_counter = 0  # Para controlar a geração de pipes

        self.score_text = self.canvas.create_text(50, 20, text="Score: 0", font=("Arial", 16), fill="black")
        self.master.bind("<space>", self.jump)
        self.master.bind("<r>", self.restart_game)  # Reiniciar o jogo
        self.update()

    def jump(self, event):
        if not self.game_over:
            self.bird_y_velocity = JUMP_STRENGTH

    def restart_game(self, event):
        if self.game_over:
            self.canvas.delete("all")  # Apaga tudo da tela
            self.reset_game()  # Reinicia o jogo chamando reset_game

    def update(self):
        if not self.game_over:
            # Atualiza a velocidade vertical do pássaro e a posição
            self.bird_y_velocity += GRAVITY
            self.canvas.move(self.bird, 0, self.bird_y_velocity)

            # Verifica colisões
            self.check_collision()

            # Move os pipes
            self.move_pipes()

            # Atualiza a pontuação
            self.update_score()

            # Chama a função de update a cada 20 milissegundos
            self.master.after(20, self.update)

    def check_collision(self):
        bird_coords = self.canvas.coords(self.bird)

        # Verifica se o pássaro bateu no teto ou no chão
        if bird_coords[1] < 0 or bird_coords[3] > CANVAS_HEIGHT:
            self.game_over = True
            self.display_game_over()

        # Verifica colisão com os pipes
        for pipe in self.pipes:
            if self.check_pipe_collision(pipe, bird_coords):
                self.game_over = True
                self.display_game_over()

        # Verifica se o pássaro passou de um pipe (incrementa pontuação)
        for pipe in self.pipes:
            if self.canvas.coords(pipe['top'])[2] < bird_coords[0] and not pipe['scored']:
                self.score += 1
                pipe['scored'] = True  # Marca o pipe como já "passado" para não contar mais pontos

    def check_pipe_collision(self, pipe, bird_coords):
        pipe_coords_top = self.canvas.coords(pipe['top'])
        pipe_coords_bottom = self.canvas.coords(pipe['bottom'])

        # Verifica colisão do pássaro com os pipes
        return (pipe_coords_top[0] < bird_coords[2] and pipe_coords_top[2] > bird_coords[0] and
                (bird_coords[1] < pipe_coords_top[3] or bird_coords[3] > pipe_coords_bottom[1]))

    def display_game_over(self):
        # Exibe a mensagem de fim de jogo
        self.canvas.create_text(200, 300, text="Game Over", font=("Arial", 24), fill="red")
        self.canvas.create_text(200, 350, text=f"Score: {self.score}", font=("Arial", 16), fill="black")
        self.canvas.create_text(200, 400, text="Press 'R' to Restart", font=("Arial", 16), fill="black")

    def move_pipes(self):
        pipes_to_remove = []

        # Controla a frequência de criação de pipes
        self.pipe_counter += 1
        if self.pipe_counter % PIPE_FREQUENCY == 0:
            self.create_pipe()

        # Move os pipes para a esquerda e remove os que saem da tela
        for pipe in self.pipes:
            self.canvas.move(pipe['top'], PIPE_SPEED, 0)
            self.canvas.move(pipe['bottom'], PIPE_SPEED, 0)
            if self.canvas.coords(pipe['top'])[2] < 0:  # Se o pipe sair da tela
                pipes_to_remove.append(pipe)

        for pipe in pipes_to_remove:
            self.canvas.delete(pipe['top'])
            self.canvas.delete(pipe['bottom'])
            self.pipes.remove(pipe)

    def create_pipe(self):
        # Altura do pipe varia entre PIPE_MIN_HEIGHT e PIPE_MAX_HEIGHT
        pipe_height = random.randint(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT)
        top_pipe = self.canvas.create_rectangle(400, 0, 450, pipe_height, fill=PIPE_COLOR)
        bottom_pipe = self.canvas.create_rectangle(400, pipe_height + PIPE_GAP, 450, CANVAS_HEIGHT, fill=PIPE_COLOR)

        # Armazena informações sobre os pipes (incluindo se já foram passados para pontuação)
        self.pipes.append({'top': top_pipe, 'bottom': bottom_pipe, 'scored': False})

    def update_score(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")


if _name_ == "_main_":
    root = tk.Tk()
    game = FlappyBird(root)
    root.mainloop()
