
from copy import deepcopy
from game_field.game_field import random_position_on_field
from models.direction import Direction
from models.player import Player


class GameImpl:
    def __init__(self):
        self.general_field_id = 0
        self.current_player_index = 0

    def calc_next_player(self, game):
        self.current_player_index = (self.current_player_index + 1) % len(game.players)
        return game.players[self.current_player_index]

    def place_players(self, game, players_count, players_positions):
        players = []
        general_game_field = game.game_fields[self.general_field_id]
        for i in range(players_count):
            players.append(Player())
            if players_positions is not None and i < len(players_positions):
                players[-1].start_position = players_positions[i]
                general_game_field.add_player_at(players[-1], players_positions[i])
            else:
                random_position = random_position_on_field(general_game_field)
                players[-1].start_position = random_position
                general_game_field.add_player_at(players[-1], random_position)
        return players

    def can_player_go(self, game):
        self.try_wake_up_player(game)
        if game.current_player.stun == 0:
            return True
        stun = game.current_player.stun
        print('Player {} is still stunned by {}'.format(game.current_player.id,
              '1 step' if stun == 1 else (str(stun) + ' steps')))
        game.current_player.stun -= 1
        return False

    def wake_up_player(self, game, player):
        player.wake_up()
        game.game_fields[player.field_id[-1]].remove_player(player)
        player.field_id.pop()

    def try_wake_up_player(self, game):
        if not game.current_player.sleep_times:
            return
        if game.current_player.sleep_times[-1] == 0:
            self.wake_up_player(game, game.current_player)
            self.you_waked_up()
            print(game.current_player.inventory)
        else:
            game.current_player.sleep_times[-1] -= 1

    def successful(self):
        print('You passed')

    def unsuccessful(self):
        print('You bumped into a wall')

    def you_waked_up(self):
        print('You waked up')

    def kill_player(self, game, killed_player):
        if killed_player.is_sleeping():
            self.wake_up_player(game, killed_player)
            print('Player {} kills sleep Player {} and wakes him up!'.format(game.current_player.id, killed_player.id))
        else:
            print('Player {} kills Player {}!'.format(game.current_player.id, killed_player.id))
        killed_player.stun = 1
        killed_player_field = game.game_fields[killed_player.field_id]
        killed_player_field.player_position(killed_player).inventory = deepcopy(killed_player.inventory)
        killed_player.inventory.reset()
        killed_player_field.player_go_to(killed_player, killed_player.start_position)
        print('Player {} has been teleported to his start position'.format(killed_player.id))

    def shoot(self, game, direction: Direction):
        if game.current_player.inventory.bullets == 0:
            print('You are out of bullets')
            return False
        game.current_player.inventory.bullets -= 1
        current_field = game.game_fields[game.current_player.field_id[-1]]
        current_position = deepcopy(current_field.player_position(game.current_player))
        while not current_field.field.is_out_of_field(current_position):
            players = current_field.players_at(current_position)
            if players and not (len(players) == 1 and game.current_player in players):
                if len(players) == 1 and game.current_player in players:
                    current_position += direction
                    break
                killed_player = players.pop()
                if killed_player == game.current_player:
                    killed_player = players.pop()
                    players.add(game.current_player)
                players.add(killed_player)
                if game.current_player.is_sleeping():
                    print('You killed Player {} when was sleeping and waked up with him'.format(killed_player.id))
                    self.wake_up_player(game, game.current_player)
                    self.wake_up_player(game, killed_player)
                    self.you_waked_up()
                    return True
                self.kill_player(game, killed_player)
                return True
            current_position += direction
        print('Your shot did not hit anyone')
        return True

    def help(self, game):
        print('''Walk keys:
    W — Up
    A — Left
    S — Down
    D — Right

Actions:
    X <W, A, S, D> - Shoot

Other:
    E - Inventory
    ? - Help

After any action except 'Other' you make a step.

For more information read this —— https://github.com/NaylRush/MazeGame
@NaylRush''')

    def go_to(self, game, direction: Direction):
        # before step
        current_field = game.game_fields[game.current_player.field_id[-1]]
        current_cell = current_field.player_cell(game.current_player)
        result = current_cell.can_go_this_direction(game, self, direction)
        if result is None:
            return
        if not result:
            self.unsuccessful()
            return
        # step
        if not current_field.player_can_go_to(game.current_player, direction):
            self.unsuccessful()
            return
        current_field.player_go_to(game.current_player, direction)
        current_cell = current_field.player_cell(game.current_player)
        current_cell.take_inventory(game)
        current_cell.arrive(game, self)
        self.successful()
