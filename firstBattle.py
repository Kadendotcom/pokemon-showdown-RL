import asyncio
from poke_env import AccountConfiguration
from poke_env.player import RandomPlayer
from poke_env.battle import battle
from poke_env import battle
from poke_env.player import battle_order 
from poke_env import Player
from poke_env.battle import move

#Learning how to make own player class. Customizing move choice logic, return values etc.
class QartiPlayer(Player):
    async def choose_move(self,battle):
        moves=battle.available_moves
        largestDamage=max(moves)
        moveType=moves[0].PokemonType
        opponentType=battle.opponent_active_pokemon
        #modifying choose_move can allow you to change the logic behind making a move choice. therefore allowing you to make optimal move choices 
        # choose move is called each time the QartiPlayer has to make a move.
        print(f"{battle.active_pokemon.current_hp}")
        # choose_move must return a battleorder.
        return self.choose_random_move(battle=battle)
        
async def main():
    
    myAccountConfig=AccountConfiguration("Qarti","***REMOVED***")
    player_1= QartiPlayer()
    
    player_2= RandomPlayer(max_concurrent_battles=1)
    
    
    await player_1.battle_against(player_2, n_battles=1)

    print(f"Finished Battles: {player_1.n_finished_battles}")
    print(f"Player 1 wins: {player_1.n_won_battles}")
    
if __name__ == "__main__":
    asyncio.run(main())
    
    