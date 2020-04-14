
from cell import *


class GameImpl:
    def successful(self, game):
        print('You passed')

    def unsuccessful(self, game):
        print('You bumped into a wall')

    def update_bullets(self, game):
        game.current_player.inventory.update_bullets()
        print('Your bullets were updated. Now you have: ' + str(game.current_player.inventory.bullets))

    def kill_player(self, game, id):
        print('Player ' + str(game.current_player_id) + ' kills Player ' + str(id) + '!')

    def stun_for(self, game, duration):
        game.current_player.stun = duration
        print('You are stunned for ' + str(game.current_player.stun) + ' steps')

    def teleport_to(self, game, destination):
        print('You have been teleported')
        game.current_player.move_to(destination)

    def gave_over(self, game):
        game.game_is_over = True
        print('Game is over! Player ' + str(game.current_player_id) + ' wins!')

    def move_to(self, game, direction: Direction):
        # before step
        current_cell = game.map.get(game.current_player.position)
        if isinstance(current_cell, RubberRoom) and direction != current_cell.direction:
            self.successful(game)
            return
        elif isinstance(current_cell, Exit) and direction == current_cell.direction:
            self.gave_over(game)
            return
        # step
        if not game.current_player.try_go_to(direction):
            self.unsuccessful(game)
        else:
            self.successful(game)
            current_cell = game.map.get(game.current_player.position)
            if isinstance(current_cell, Armory):
                self.update_bullets(game)
                return
            elif isinstance(current_cell, Stun):
                self.stun_for(game, current_cell.duration)
                return
            elif isinstance(current_cell, Teleport):
                self.teleport_to(game, current_cell.destination)
                return

    def inventory(self, game):
        print('Inventory:')
        print('\tBullets: ' + str(game.current_player.inventory.bullets))

    def shot_a_bullet(self, game):
        if game.current_player.inventory.bullets == 0:
            print('You run out of bullets')
            return False
        print('Not implemented')
        return True

    def help(self, game):
        print('''
Walk keys:
    W — Up
    A — Left
    S — Down
    D — Right
    
Actions:
    X - Shot a bullet

Other:
    I - Inventory
    ? - Help

After any action except 'Other' you make a step.

For more information read this —— https://github.com/NaylRush/MazeGame
@NaylRush
        ''')
