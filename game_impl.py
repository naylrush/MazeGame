
from cell import *
from game_map import GameMap


class GameImpl:
    def successful(self, game):
        print('You passed')

    def unsuccessful(self, game):
        print('You bumped into a wall')

    def update_bullets(self, game):
        game.current_player.inventory.update_bullets()
        print('Your bullets were updated. Now you have: ' + str(game.current_player.inventory.bullets))

    def kill_player(self, game, killed_player):
        print('Player ' + str(game.current_player.id) + ' kills Player ' + str(killed_player.id) + '!')

    def stun_for(self, game, duration):
        game.current_player.stun = duration
        print('You are stunned by ' + str(game.current_player.stun) + ' steps')

    def player_is_stunned(self, game):
        if game.current_player.stun == 0:
            return False
        stun = game.current_player.stun
        print('Player ' + str(game.current_player.id) + ' is still stunned by ', end='')
        print('1 step' if stun == 1 else (str(stun) + ' steps'))
        return True

    def teleport_to(self, game, destination):
        print('You have been teleported')
        game.game_map.player_move_to(destination)

    def gave_over(self, game):
        game.game_is_over = True
        print('Game is over! Player ' + str(game.current_player.id) + ' wins!')

    def inventory(self, game):
        print('Inventory:')
        print('\tBullets: ' + str(game.current_player.inventory.bullets))

    def shoot(self, game, direction: Direction):
        if game.current_player.inventory.bullets == 0:
            print('You are out of bullets')
            return False
        print('Not implemented')
        return True

    def help(self, game):
        print('''Walk keys:
    W — Up
    A — Left
    S — Down
    D — Right
    
Actions:
    X <W, A, S, D> - Shoot (type Q to break shooting) 

Other:
    I - Inventory
    ? - Help

After any action except 'Other' you make a step.

For more information read this —— https://github.com/NaylRush/MazeGame
@NaylRush''')

    def move_to(self, game, direction: Direction):
        current_cell = game.game_map.player_cell(game.current_player)
        # before step
        if isinstance(current_cell, RubberRoom) and direction != current_cell.direction:
            self.successful(game)
            return
        elif isinstance(current_cell, Exit) and direction == current_cell.direction:
            self.gave_over(game)
            return
        # step
        if not game.game_map.player_try_go_to(game.current_player, direction):
            self.unsuccessful(game)
        else:
            self.successful(game)
            current_cell = game.game_map.player_cell(game.current_player)
            if isinstance(current_cell, Armory):
                self.update_bullets(game)
                return
            elif isinstance(current_cell, Stun):
                self.stun_for(game, current_cell.duration)
                return
            elif isinstance(current_cell, Teleport):
                self.teleport_to(game, current_cell.destination)
                return
