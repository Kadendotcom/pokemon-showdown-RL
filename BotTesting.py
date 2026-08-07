import asyncio
import os
from dotenv import load_dotenv
from poke_env import AccountConfiguration
from playerClasses import QartiPlayer,QartiPlayerNoSwap



async def main():
    
    #in order to create a bot battle test, you must create at least 2 player objects. 
    #for example player_1 = QartiPlayer()
    #This will create a player object
    #You can pass multiple arguments when creating a player object, such as account config, max conc battles etc. 
    #These are more precisely defined in the poke_env documentation.
    #After you have at least 2 valid player objects, you must make them battle
    #For example await player_1.battle_against(player_2, n_battles=5)
    #The above line will create a sequence of 5 battles between player 1 and player 2.
    #You can see the basic print statements to view the stats of the battle sequence below.
    
    load_dotenv()
    myAccountConfig=AccountConfiguration(os.getenv("SHOWDOWN_USERNAME"), os.getenv("SHOWDOWN_PASSWORD"))
    player_1= QartiPlayer(myAccountConfig)
    player_4= QartiPlayerNoSwap()
    await player_4.battle_against(player_1, n_battles=10000)

    
    if player_4.win_rate<player_1.win_rate:
        print(f"Custom swapping wins. Qarti Bot with swapping logic beat Qarit Bot without swapping logic. Swapping Logic:{player_1.n_won_battles} vs. No Swapping Logic:{player_4.n_won_battles} ")
    else:
        print(f"Random swapping wins. Qarti Bot with no swapping logic beat Qarit Bot with swapping logic. Swapping Logic:{player_1.n_won_battles} vs. No Swapping Logic:{player_4.n_won_battles} ")



if __name__ == "__main__":
    asyncio.run(main())