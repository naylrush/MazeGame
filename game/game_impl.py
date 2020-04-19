
from copy import deepcopy
from models.cell import *


class GameImpl:
    def successful(self, game):
        print('You passed')

    def unsuccessful(self, game):
        print('You bumped into a wall')

    def update_bullets(self, game):
        game.current_player.inventory.update_bullets()
        print('Your bullets were updated. Now you have: ' + str(game.current_player.inventory.bullets))

    def kill_player(self, game, killed_player):
        killed_player.stun = 1
        killed_player.inventory.reset()
        game.game_map.player_move_to(killed_player, killed_player.start_position)
        print('Player ' + str(game.current_player.id) + ' kills Player ' + str(killed_player.id) + '!')
        print('Player ' + str(killed_player.id) + ' has been teleported to his start position')

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
        game.game_map.player_move_to(game.current_player, destination)

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
        current_position = deepcopy(game.game_map.player_position(game.current_player))
        current_position.shift_to(direction)
        while not game.game_map.map.is_out_of_map(current_position):
            players = game.game_map.players_at(current_position)
            if len(players) != 0:
                killed_player = players.pop()
                players.add(killed_player)
                self.kill_player(game, killed_player)
                return True
            current_position.shift_to(direction)
        print('Your shot did not hit anyone')
        return False

    def help(self, game):
        print('''Walk keys:
    W — Up
    A — Left
    S — Down
    D — Right
    
Actions:
    X <W, A, S, D> - Shoot (type Q to break shooting) 

Other:
    E - Inventory
    ? - Help

After any action except 'Other' you make a step.

For more information read this —— https://github.com/NaylRush/MazeGame
@NaylRush''')

    def move_to(self, game, direction: Direction):
        current_cell = game.game_map.player_cell(game.current_player)
        # before step
        if type(current_cell) is RubberRoom and direction != current_cell.direction:
            self.successful(game)
            return
        elif type(current_cell) is Exit and direction == current_cell.direction:
            self.gave_over(game)
            return
        # step
        if not game.game_map.player_try_go_to(game.current_player, direction):
            self.unsuccessful(game)
        else:
            self.successful(game)
            current_cell = game.game_map.player_cell(game.current_player)
            if type(current_cell) is Armory:
                self.update_bullets(game)
                return
            elif type(current_cell) is Stun:
                self.stun_for(game, current_cell.duration)
                return
            elif type(current_cell) is Teleport:
                while type(game.game_map.player_cell(game.current_player)) is Teleport:
                    self.teleport_to(game, current_cell.destination)
                return
