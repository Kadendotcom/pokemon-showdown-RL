
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
        # if the bot is forced to switch, check for the best possible switch (offensively). then make that switch. If there is no best typing switch, just make the first available swap.
        minimal_multi=1
        best_atk=-1
        #Force swap case 
        if battle.force_switch:
            bestMon=battle.available_switches[0]
            for mon  in battle.available_switches:
                best_offense = max(mon.stats.get("atk"), mon.stats.get("spa"))
                if (battle.opponent_active_pokemon.damage_multiplier(mon.type_1) > minimal_multi or (mon.type_2 and battle.opponent_active_pokemon.damage_multiplier(mon.type_2) > minimal_multi)) and best_offense > best_atk:
                    bestMon = mon
                    best_atk = best_offense
            return self.create_order(bestMon)
        #Constantly checks if the current mon matchup is good for the bot.
        #This will catch if the opponent made a swap that will be defensively strong against the bots mon
        
        opp_mon_type=battle.opponent_active_pokemon.type_1
        opp_mon_type2=battle.opponent_active_pokemon.type_2
        if battle.active_pokemon.damage_multiplier(opp_mon_type) >= 4 or (opp_mon_type2 and battle.active_pokemon.damage_multiplier(opp_mon_type2) >= 4) :
            bestMon=battle.active_pokemon
            for mon in battle.available_switches:
                if (mon.damage_multiplier(opp_mon_type) <2 or (opp_mon_type2 and mon.damage_multiplier(opp_mon_type2) <2)) and (mon.stats.get("atk") > bestMon.stats.get("atk") or mon.stats.get("spa") > bestMon.stats.get("spa")):
                    bestMon=mon
            if bestMon!=battle.active_pokemon:
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
        




