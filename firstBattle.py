
import asyncio
import os
from dotenv import load_dotenv
from poke_env import AccountConfiguration
from poke_env.player import RandomPlayer
from poke_env.battle import battle
from poke_env import battle
from poke_env.player import battle_order
from poke_env import Player
from poke_env.battle import move
from poke_env import calc
from poke_env.calc import calculate_damage

from poke_env.battle import pokemon

#Learning how to make own player class. Customizing move choice logic, return values etc.
class QartiPlayer(Player):
    async def choose_move(self,battle):
        minimal_multi=1
        if battle.force_switch:
            bestMon = battle.available_switches[0]
            for mon in battle.available_switches:
                if battle.opponent_active_pokemon.damage_multiplier(mon.type_1) > minimal_multi or (mon.type_2 and battle.opponent_active_pokemon.damage_multiplier(mon.type_2) > minimal_multi):
                    bestMon = mon
            return self.create_order(bestMon)

        # list of moves active pokemon can make this turn
        moves=battle.available_moves
        damageCalculator= calculate_damage
        #start max damage at -1 to satisfy base power of 0 for stat moves. Could change later, when I want the bot to swap instead of using stat moves when it cant attack.
        maxDamage=-1
        # loop through all moves
        for i in moves:
            # check all stats in opponent stat dict are valid, otherwise just use max base power in available moves
            if all(battle.opponent_active_pokemon.stats.values()):
                #calc max damage and the move that produced max damage
                currentDamage=(damageCalculator(attacker_identifier = battle.active_pokemon.identifier(battle.player_role),defender_identifier = battle.opponent_active_pokemon.identifier(battle.opponent_role),move = i,battle = battle))[0]
                #track max damage across all moves in possible moves list.
                if currentDamage>maxDamage:
                    maxDamage=currentDamage
                    maxMove=i
            elif i.base_power>maxDamage:
                maxDamage=i.base_power
                maxMove=i
        return self.create_order(maxMove)
class QartiPlayerNoSwap(Player):
    async def choose_move(self,battle):
        if battle.force_switch:
            return self.choose_random_move(battle=battle)

        # list of moves active pokemon can make this turn
        moves=battle.available_moves
        damageCalculator= calculate_damage
        #start max damage at -1 to satisfy base power of 0 for stat moves. Could change later, when I want the bot to swap instead of using stat moves when it cant attack.
        maxDamage=-1
        # loop through all moves
        for i in moves:
            # check all stats in opponent stat dict are valid, otherwise just use max base power in available moves
            if all(battle.opponent_active_pokemon.stats.values()):
                #calc max damage and the move that produced max damage
                currentDamage=(damageCalculator(attacker_identifier = battle.active_pokemon.identifier(battle.player_role),defender_identifier = battle.opponent_active_pokemon.identifier(battle.opponent_role),move = i,battle = battle))[0]
                #track max damage across all moves in possible moves list.
                if currentDamage>maxDamage:
                    maxDamage=currentDamage
                    maxMove=i
            elif i.base_power>maxDamage:
                maxDamage=i.base_power
                maxMove=i
        return self.create_order(maxMove)
        #modifying choose_move can allow you to change the logic behind making a move choice. therefore allowing you to make optimal move choices
        # choose move is called each time the QartiPlayer has to make a move
    def optimal_swap(self,battle):
        pass
    def is_super_effective(self,battle):
        pass

async def main():

    load_dotenv()
    myAccountConfig=AccountConfiguration(os.getenv("SHOWDOWN_USERNAME"), os.getenv("SHOWDOWN_PASSWORD"))
    player_1= QartiPlayer(myAccountConfig)

    player_2= RandomPlayer(AccountConfiguration.generate("Bot"),max_concurrent_battles=2)

    player_3 = RandomPlayer(AccountConfiguration.generate("Bot"),max_concurrent_battles=1)
    
    player_4= QartiPlayerNoSwap()

    await player_3.battle_against(player_2, n_battles=300)

    await player_1.battle_against(player_2, n_battles=300)
    
    await player_4.battle_against(player_1, n_battles=300)

    if player_1.win_rate>player_3.win_rate:
        print(f"Qarti Bot won:{player_1.n_won_battles} and Random Bot won: {player_3.n_won_battles} ")
    else:
        print("Qarit Bot sucks. ")
    
    if player_4.win_rate<player_1.win_rate:
        print(f"Custom swapping wins. Qarti Bot with swapping logic beat Qarit Bot without swapping logic. Swapping Logic:{player_1.n_won_battles} vs. No Swapping Logic:{player_4.n_won_battles} ")
    else:
        print(f"Random swapping wins. Qarti Bot with no swapping logic beat Qarit Bot with swapping logic. Swapping Logic:{player_1.n_won_battles} vs. No Swapping Logic:{player_4.n_won_battles} ")

    # print(f"Finished Battles: {player_1.n_finished_battles}")
    # print(f"Player 1 wins: {player_1.n_won_battles}")

if __name__ == "__main__":
    asyncio.run(main())


