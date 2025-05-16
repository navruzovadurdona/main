import tkinter as tk
import random

# Цвета граней
COLORS = {
    'U': 'white',
    'D': 'yellow',
    'F': 'green',
    'B': 'blue',
    'L': 'orange',
    'R': 'red'
}

# Начальное состояние кубика
def create_solved_cube():
    return {face: [face]*9 for face in COLORS}

# Поворот списка 3x3 по часовой стрелке
def rotate_face_cw(face):
    return [
        face[6], face[3], face[0],
        face[7], face[4], face[1],
        face[8], face[5], face[2]
    ]


class RubikGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Симулятор Кубика Рубика")
        self.cube = create_solved_cube()
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.buttons()
        self.draw_cube()

    def draw_cube(self):
        self.canvas.delete("all")
        size = 30
        face_positions = {
            'U': (3, 0),
            'L': (0, 3),
            'F': (3, 3),
            'R': (6, 3),
            'B': (9, 3),
            'D': (3, 6),
        }
        for face, (x0, y0) in face_positions.items():
            for i in range(3):
                for j in range(3):
                    color = COLORS[self.cube[face][i*3 + j]]
                    self.canvas.create_rectangle(
                        (x0 + j) * size, (y0 + i) * size,
                        (x0 + j + 1) * size, (y0 + i + 1) * size,
                        fill=color, outline='black'
                    )

    def buttons(self):
        moves = ['U', 'D', 'F', 'B', 'L', 'R']
        for i, move in enumerate(moves):
            tk.Button(self.root, text=move, command=lambda m=move: self.make_move(m)).pack(side=tk.LEFT)
        tk.Button(self.root, text="Перемешать", command=self.shuffle).pack(side=tk.LEFT)
        tk.Button(self.root, text="Сброс", command=self.reset).pack(side=tk.LEFT)

    def make_move(self, move):
        print(f"Повернули грань: {move} (движения пока не реализованы)")
        # Пока просто перерисовываем, не поворачивая
        self.draw_cube()

    def shuffle(self):
        print("Кубик перемешан (визуально пока нет)")
        self.draw_cube()

    def reset(self):
        self.cube = create_solved_cube()
        self.draw_cube()
        
    
    def make_move(self, move):
        # Реализуем повороты граней по базовым правилам кубика
        if move == 'U':
            self.cube['U'] = rotate_face_cw(self.cube['U'])
            # Соседи U: F, R, B, L (верхние ряды)
            temp = self.cube['F'][:3]
            self.cube['F'][:3] = self.cube['R'][:3]
            self.cube['R'][:3] = self.cube['B'][:3]
            self.cube['B'][:3] = self.cube['L'][:3]
            self.cube['L'][:3] = temp
        elif move == 'D':
            self.cube['D'] = rotate_face_cw(self.cube['D'])
            # Соседи D: F, L, B, R (нижние ряды)
            temp = self.cube['F'][6:]
            self.cube['F'][6:] = self.cube['L'][6:]
            self.cube['L'][6:] = self.cube['B'][6:]
            self.cube['B'][6:] = self.cube['R'][6:]
            self.cube['R'][6:] = temp
        elif move == 'F':
            self.cube['F'] = rotate_face_cw(self.cube['F'])
            # Соседи F: U, R, D, L (зависит от элементов)
            temp = [self.cube['U'][6], self.cube['U'][7], self.cube['U'][8]]
            self.cube['U'][6], self.cube['U'][7], self.cube['U'][8] = \
                self.cube['L'][8], self.cube['L'][5], self.cube['L'][2]
            self.cube['L'][2], self.cube['L'][5], self.cube['L'][8] = \
                self.cube['D'][2], self.cube['D'][1], self.cube['D'][0]
            self.cube['D'][0], self.cube['D'][1], self.cube['D'][2] = \
                self.cube['R'][6], self.cube['R'][3], self.cube['R'][0]
            self.cube['R'][0], self.cube['R'][3], self.cube['R'][6] = temp
        elif move == 'B':
            self.cube['B'] = rotate_face_cw(self.cube['B'])
            temp = [self.cube['U'][0], self.cube['U'][1], self.cube['U'][2]]
            self.cube['U'][0], self.cube['U'][1], self.cube['U'][2] = \
                self.cube['R'][2], self.cube['R'][5], self.cube['R'][8]
            self.cube['R'][2], self.cube['R'][5], self.cube['R'][8] = \
                self.cube['D'][8], self.cube['D'][7], self.cube['D'][6]
            self.cube['D'][6], self.cube['D'][7], self.cube['D'][8] = \
                self.cube['L'][0], self.cube['L'][3], self.cube['L'][6]
            self.cube['L'][0], self.cube['L'][3], self.cube['L'][6] = temp
        elif move == 'L':
            self.cube['L'] = rotate_face_cw(self.cube['L'])
            temp = [self.cube['U'][0], self.cube['U'][3], self.cube['U'][6]]
            self.cube['U'][0], self.cube['U'][3], self.cube['U'][6] = \
                self.cube['B'][8], self.cube['B'][5], self.cube['B'][2]
            self.cube['B'][2], self.cube['B'][5], self.cube['B'][8] = \
                self.cube['D'][0], self.cube['D'][3], self.cube['D'][6]
            self.cube['D'][0], self.cube['D'][3], self.cube['D'][6] = \
                self.cube['F'][0], self.cube['F'][3], self.cube['F'][6]
            self.cube['F'][0], self.cube['F'][3], self.cube['F'][6] = temp
        elif move == 'R':
            self.cube['R'] = rotate_face_cw(self.cube['R'])
            temp = [self.cube['U'][8], self.cube['U'][5], self.cube['U'][2]]
            self.cube['U'][8], self.cube['U'][5], self.cube['U'][2] = \
                self.cube['F'][8], self.cube['F'][5], self.cube['F'][2]
            self.cube['F'][2], self.cube['F'][5], self.cube['F'][8] = \
                self.cube['D'][8], self.cube['D'][5], self.cube['D'][2]
            self.cube['D'][2], self.cube['D'][5], self.cube['D'][8] = \
                self.cube['B'][6], self.cube['B'][3], self.cube['B'][0]
            self.cube['B'][0], self.cube['B'][3], self.cube['B'][6] = temp

        self.draw_cube()


if __name__ == "__main__":
    root = tk.Tk()
    app = RubikGUI(root)
    root.mainloop()
