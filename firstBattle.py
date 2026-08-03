
import asyncio
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
        # if the bot must switch to a pokemon, choose a random pokemon (for now)
        if battle.force_switch:
            return self.choose_random_move(battle=battle)
        # list of moves active pokemon can make this turn 
        moves=battle.available_moves
        damageCalculator= calculate_damage
        maxDamage=-1
        # loop through all moves
        for i in moves:
            # check all stats in opponent stat dict are valid, otherwise just use max base power in available moves
            if all(battle.opponent_active_pokemon.stats.values()):
                #calc max damage and the move that produced max damage
                currentDamage=(damageCalculator(attacker_identifier = battle.active_pokemon.identifier(battle.player_role),defender_identifier = battle.opponent_active_pokemon.identifier(battle.opponent_role),move = i,battle = battle))[0]
                if currentDamage>maxDamage:
                    maxDamage=currentDamage
                    maxMove=i               
            elif i.base_power>maxDamage:
                maxDamage=i.base_power
                maxMove=i
        
        return self.create_order(maxMove)

        #modifying choose_move can allow you to change the logic behind making a move choice. therefore allowing you to make optimal move choices 
        # choose move is called each time the QartiPlayer has to make a move.
        print(f"{battle.active_pokemon.current_hp}")
        # choose_move must return a battleorder.
        return self.choose_random_move(battle=battle)
        
async def main():
    
    myAccountConfig=AccountConfiguration("Qarti","***REMOVED***")
    player_1= QartiPlayer()
    
    player_2= RandomPlayer(max_concurrent_battles=2)
    
    player_3 = RandomPlayer(max_concurrent_battles=1)
    
    await player_3.battle_against(player_2, n_battles=100)
    
    await player_1.battle_against(player_2, n_battles=100)
    
    if player_1.win_rate>player_3.win_rate:
        print(f"Qarti Bot won:{player_1.n_won_battles} and Random Bot won: {player_3.n_won_battles} ")
    else:
        print("Qarit Bot sucks. ")

    # print(f"Finished Battles: {player_1.n_finished_battles}")
    # print(f"Player 1 wins: {player_1.n_won_battles}")
    
if __name__ == "__main__":
    asyncio.run(main())
    
    