import pygame 
import random

pygame.init()

gdisplay = pygame.display.set_mode((400,400))

clock = pygame.time.Clock()


class Game(object):
    def __init__(self):
        self.game_space = self.create_game_space()
        self.width = 33
        self.height = 33
        self.w_max = 13
        self.h_max = 13
        self.timer = 0
        self.piece_dict = self.create_pieces()
        self.focus_piece = {'x': 0, 'y': 0, 'type': self.piece_dict['T'], 'rotation': 0, 'shape': 'T'} #rotation: 0 90 180
        self.current_pieces =   [] #[{'x': 3, 'y': 4, 'type': self.piece_dict['T']},
                                #{'x': 7, 'y': 9, 'type': self.piece_dict['s_l']}]

    def create_game_space(self):
        game_array = [[0 for i in range(12)] for j in range(12)]
        return game_array

    def rotate_focus(self):
        x = self.focus_piece['x']
        y = self.focus_piece['y']
        shape = self.focus_piece['shape']
        current_rotation = self.focus_piece['rotation']

        if current_rotation == 270:
            self.focus_piece = {'x': x, 'y': y, 'type': self.piece_dict[shape], 'rotation': 0, 'shape': shape}
        elif current_rotation == 0:
            rot = self.create_rotation_dict()
            self.focus_piece = {'x': x, 'y': y, 'type': rot[shape][90], 'rotation': 90, 'shape': shape}
        elif current_rotation == 90:
            rot = self.create_rotation_dict()
            self.focus_piece = {'x': x, 'y': y, 'type': rot[shape][180], 'rotation': 180, 'shape': shape}
        elif current_rotation == 180:
            rot = self.create_rotation_dict()
            self.focus_piece = {'x': x, 'y': y, 'type': rot[shape][270], 'rotation': 270, 'shape': shape}

    def create_rotation_dict(self):
        piece_dict = {'T': {}, 'L_l': {}, 'L_r': {}, 's_l': {}, 's_r': {}, 'sq': {}}

        piece_dict['T'][0]   = [[0, 1, 0], 
                                [1, 1, 1]]

        piece_dict['L_l'][0] = [[1, 0, 0], 
                                [1, 1, 1]]

        piece_dict['L_r'][0] = [[0, 0, 1], 
                                [1, 1, 1]]

        piece_dict['s_l'][0] = [[1, 1, 0], 
                                [0, 1, 1]]

        piece_dict['s_r'][0] = [[0, 1, 1], 
                                [1, 1, 0]]

        piece_dict['sq'][0]  = [[1, 1], 
                                [1, 1]]

        piece_dict['T'][90]   = [[1, 0], 
                                 [1, 1],
                                 [1, 0]]
                                
        piece_dict['L_l'][90] = [[1, 1], 
                                 [1, 0],
                                 [1, 0]]

        piece_dict['L_r'][90] = [[1, 0], 
                                 [1, 0],
                                 [1, 1]]

        piece_dict['s_l'][90] = [[0, 1], 
                                 [1, 1],
                                 [1, 0]]

        piece_dict['s_r'][90] = [[1, 0], 
                                 [1, 1],
                                 [0, 1]]

        piece_dict['sq'][90]  = [[1, 1], 
                                 [1, 1]]

        piece_dict['T'][180]   = [[1, 1, 1], 
                                  [0, 1, 0]]

        piece_dict['L_l'][180] = [[1, 1, 1], 
                                  [0, 0, 1]]

        piece_dict['L_r'][180] = [[1, 1, 1], 
                                  [1, 0, 0]]

        piece_dict['s_l'][180] = [[1, 1, 0], 
                                  [0, 1, 1]]

        piece_dict['s_r'][180] = [[0, 1, 1], 
                                  [1, 1, 0]]

        piece_dict['sq'][180]  = [[1, 1], 
                                  [1, 1]]

        piece_dict['T'][270]   = [[0, 1], 
                                  [1, 1],
                                  [0, 1]]
                                
        piece_dict['L_l'][270] = [[0, 1], 
                                  [0, 1],
                                  [1, 1]]

        piece_dict['L_r'][270] = [[1, 1], 
                                  [0, 1],
                                  [0, 1]]

        piece_dict['s_l'][270] = [[0, 1], 
                                  [1, 1],
                                  [1, 0]]

        piece_dict['s_r'][270] = [[1, 0], 
                                  [1, 1],
                                  [0, 1]]

        piece_dict['sq'][270]  = [[1, 1], 
                                  [1, 1]]

        return piece_dict

    def create_pieces(self):
        piece_dict = {}

        piece_dict['T']   = [[0, 1, 0], 
                             [1, 1, 1]]

        piece_dict['L_l'] = [[1, 0, 0], 
                             [1, 1, 1]]

        piece_dict['L_r'] = [[0, 0, 1], 
                             [1, 1, 1]]

        piece_dict['s_l'] = [[1, 1, 0], 
                             [0, 1, 1]]

        piece_dict['s_r'] = [[0, 1, 1], 
                             [1, 1, 0]]

        piece_dict['sq']  = [[1, 1], 
                             [1, 1]]

        return piece_dict

    def reset_space(self):
        self.game_space = self.create_game_space()

    def include_pieces(self):
        '''Places current pieces on the board'''

        for piece in self.current_pieces:
            x = piece['x']
            y = piece['y']
            figure = piece['type']
            for i in range(len(figure)):
                for j in range(len(figure[0])):
                    if figure[i][j] == 1:
                        self.game_space[i + y][j + x] = figure[i][j]

    def include_focus_piece(self):
        x = self.focus_piece['x']
        y = self.focus_piece['y']
        figure = self.focus_piece['type']
        for i in range(len(figure)):
            for j in range(len(figure[0])):
                if figure[i][j] == 1:
                    self.game_space[i + y][j + x] = figure[i][j]

    def _attempt_draw(self, piece, x_move=0, y_move=0):
        self.reset_space()
        self.include_pieces()

        x = piece['x'] + x_move
        y = piece['y'] + y_move
        figure = piece['type']
        for i in range(len(figure)):
            for j in range(len(figure[0])):
                if figure[i][j] == 1 and self.game_space[i + y][j + x] == 1:
                    return False
        return True

    def _check_move_down(self, piece):
            x = piece['x']
            y = piece['y']
            figure = piece['type']

            x_len = len(figure[0])
            y_len = len(figure)

            result = False
            if y + y_len + 1 < self.h_max:
                result = self._attempt_draw(piece, y_move = 1)
            if result == False:
                self.solidify_focus_piece()
                return result
            return result

    def _check_move_left(self, piece):
            x = piece['x']
            y = piece['y']
            figure = piece['type']

            x_len = len(figure[0])
            y_len = len(figure)

            if x - 1 >= 0:
                return self._attempt_draw(piece, x_move = -1)
            return False

    def _check_move_right(self, piece):
            x = piece['x']
            y = piece['y']
            figure = piece['type']

            x_len = len(figure[0])
            y_len = len(figure)

            if x + x_len + 1 < self.w_max:
                return self._attempt_draw(piece, x_move = 1)
            return False

    def move_down(self, piece):
        if self._check_move_down(piece):
            piece['y'] += 1
        else:
            print('cant move down')

    def move_left(self, piece):
        if self._check_move_left(piece):
            piece['x'] -= 1
        else:
            print('cant move down')

    def move_right(self, piece):
        if self._check_move_right(piece):
            piece['x'] += 1
        else:
            print('cant move down')

    def draw_space(self, display):
        for r_index, row in enumerate(self.game_space):
            for e_index, elm in enumerate(row):
                if elm == 1:
                    pygame.draw.rect(display, (0, 255, 0), [e_index * self.width, r_index * self.height, self.width, self.height])
                    pygame.draw.rect(display, (255, 255, 255), [e_index * self.width, r_index * self.height, self.width, self.height], 1)

    def solidify_focus_piece(self):
        self.current_pieces.append(self.focus_piece)
        self.create_new_focus()

    def create_new_focus(self):
        ran = random.choice(['T', 'L_l', 'L_r', 's_l', 's_r', 'sq'])
        self.focus_piece = {'x': 0, 'y': 0, 'type': self.piece_dict[ran], 'shape': ran, 'rotation': 0}

    def run(self, display):
        self.reset_space()
        self.include_pieces()
        self.include_focus_piece()
        self.draw_space(display)



def events(state):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            state.timer = 0
            if event.key == pygame.K_DOWN:
                state.move_down(state.focus_piece)
            if event.key == pygame.K_LEFT:
                state.move_left(state.focus_piece)
            if event.key == pygame.K_RIGHT:
                state.move_right(state.focus_piece)
            if event.key == pygame.K_r:
                state.rotate_focus()
        if event.type == pygame.KEYUP:
            pass
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


def main():
    count = 0
    new_game = Game()
    timer = 0
    while True:

        events(new_game)
        gdisplay.fill((0, 0, 0))
        new_game.run(gdisplay)

        print(new_game.timer)
        if new_game.timer % 100 == 0 and new_game.timer != 0:
            new_game.move_down(new_game.focus_piece)
            new_game.timer = 0
        pygame.display.update()
        clock.tick(40)
        new_game.timer += 1

main()