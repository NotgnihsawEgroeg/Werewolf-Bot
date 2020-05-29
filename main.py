import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import random

class Player():
    def __init__(self, player_id, role, nickname):
        self.player_id = player_id
        self.role = role
        self.nickname = nickname
    def set_nick(self, new_nick):
        self.nickname = new_nick
    def set_role(self, new_role):
        self.role = new_role

async def dm_input(user_id, prompt):
    #print("starting dm")
    msg = await client.get_user(user_id).send(prompt)
    def check(message):
        return message.author == client.get_user(user_id) and message.channel == msg.channel
    reply = await client.wait_for('message', check=check)
    return reply.content

async def dm_print(user_id, message):
    msg = await client.get_user(user_id).send(message)

async def get_nicks(user_ids):
    nicknames = []
    for i in range(len(user_ids)):
        if user_ids[i] == 100 or user_ids[i] == 101 or user_ids[i] == 102:
            nick = 'Middle Card {}'.format(user_ids[i] - 99)
        else:
            nick = 'Player' + str(user_ids[i])
            #nick = await dm_input(user_ids[i], 'Enter your desired nickname for this game of werewolf. ')
        nicknames.append(nick)

    nick_dict = dict(zip(user_ids, nicknames))
    return nick_dict

def format_player_list(player_list):
    string = ""
    for i in range(len(player_list)):
        string += '{} : {}\n'.format(player_list[i].nickname, player_list[i].role)
    return string

def get_player_from_nick(nickname, player_list):
    for p in player_list:
        if p.nickname == nickname:
            return p.player_id
    return -1


### Night Action class

class Action():
    async def __init__(self, player, player_list):
        self.player = player

        ### Constructs nick list for swaps
        self.nick_list = []
        for player_element in player_list:
            self.nick_list.append(player_element.nickname)

        ### troublemaker action input
        if player.role == 'troublemaker':
            self.type = 'troublemaker_swap'
            prompt = "Which two players would you like to swap? (comma separated)"

            async def get_troublemaker_input(prompt, nick_list, player_id):
                temp_input = await dm_input(player_id, prompt)
                input_list = temp_input.split(",")

                if input_list.length() == 2:
                    input_list[0] = input_list[0].strip()
                    input_list[1] = input_list[1].strip()
                    if (input_list[0] in nick_list) and (input_list[1] in nick_list):
                        return input_list
                    else:
                        prompt = "Player not found. Please try again."
                        return get_troublemaker_input(prompt, nick_list, player_id)
                else:
                    prompt = "Please input two players and try again."
                    return get_troublemaker_input(prompt, nick_list)
                ### Nice recursion

            self.player_swap_list = get_troublemaker_input(prompt, self.nick_list, self.player_id)

        elif player.role == 'robber':
            self.type = 'robber_swap'
            self.player_swap_list = []
            self.player_swap_list.append(player.nickname)
            prompt = "Enter a player to steal their role."

            async def get_robber_input(prompt, nick_list, player_id):
                temp_input = await dm_input(player_id, prompt)
                if temp_input in nick_list:
                    return temp_input
                else:
                    prompt = "Player not found. Please try again."
                    return get_robber_input(prompt, nick_list, player_id)

            self.player_swap_list.append(get_robber_input(prompt, self.nick_list, self.player_id))

        elif player.role == 'insomniac':
            self.type = 'inform_insom'

        elif player.role == 'mason':
            self.type = 'inform_mason'
            self.check = False

        elif player.role == 'werewolf':
            self.type = 'inform_were'
            self.were_check = False
            self.min_check = False

        elif player.role == 'minion':
            self.type = 'inform_minion'


        elif player.role == 'drunk':
            self.type = 'prompt_drunk'
            prompt = "Pick a number, 1 through 3."

            async def get_drunk_card_id(prompt, player_id):
                temp_input = await dm_input(player_id, prompt)
                try:
                    temp_input = int(temp_input)
                except ValueError:
                    prompt = "A NUMBER, in base 10, 1 through 3, dummy. Try again."
                    return get_drunk_card_id(player_id, prompt)
                except:
                    print("Unexpected error picking drunk card.")
                    raise

                ### return id of center card (100-102)
                if temp_input < 4 and temp_input > 0:
                    return (temp_input + 99)
                else:
                    prompt = "The card number must be between 1 and 3. Try again."
                    return get_drunk_card_id(prompt, player_id)

            self.picked_card_id = get_drunk_card_id(prompt, player.player_id)

        elif player.role == 'seer':
            prompt = "Would you like to see two cards (type 'cards') or a player (type 'player')?"
            async def get_seer_input(prompt,  player_list, player_id):
                input = await dm_input(player_id, prompt)
                seer_action_dict = {'type' : None, 'player' : None}
                if input == 'player':
                    prompt = "Which player?"
                    input = await dm_input(player_id, prompt)
                    if input in player_list:
                        seer_action_dict['type'] = 'see_player'
                        seer_action_dict['player'] = input
                        return seer_action_dict
                    else:
                        prompt = "Player not found, please try again. (type 'cards' or 'player')"
                        return get_seer_input(prompt, player_list, player_id)
                elif input == 'cards':
                    message = 'Input accepted!'
                    await dm_print(player_id, message)
                    seer_action_dict['type'] = 'see_cards'
                    return seer_action_dict
                else:
                    prompt = "Not a valid option. Please try again."
                    return get_seer_input(prompt)

            seer_dict = get_seer_input(prompt, self.nick_list, player.player_id)
            self.type = seer_dict['type']
            self.seen_player = seer_dict['player']

    async def execute(self, player_list):
        if self.type == 'troublemaker_swap':
            for player1 in player_list:
                if player1.nick == self.player_swap_list[0]:
                    for player2 in player_list:
                        if player2.nick == self.player_swap_list[1]:
                            temp = player2.role
                            player2.role = player1.role
                            player1.role = temp
                            return player_list

            ###td: inform tm and gm
            return

        elif self.type == 'robber_swap':
            for player1 in player_list:
                if player1.nick == self.player_swap_list[0]:
                    for player2 in player_list:
                        if player2.nick == self.player_swap_list[1]:
                            temp = player2.role
                            player2.role = player1.role
                            player1.role = temp
                            return player_list
            ###td: inform robber and gm
            return

        elif self.type == 'inform_insom':
            message = 'Your current role is {}'.format(player.role)
            await dm_print(player.player_id, message)
            return player_list

        elif self.type == 'inform_were':
            for player1 in player_list:
                if player1.role == 'werewolf' and player1.were_check == False:
                    player1.werecheck = True
                    for player2 in player_list:
                        if player2.role == 'werewolf' and player2.were_check == False:
                            if player1.player_id in [100, 101, 102] and player2.player_id in [100, 101, 102]:
                                pass
                            elif player2.player_id in [100, 101, 102]:
                                await dm_print(player1.player_id, "You are the only werewolf.")
                            elif player1.player_id in [100, 101, 102]:
                                await dm_print(player2.player_id, "You are the only werewolf.")
                            else:
                                await dm_print(player1.player_id, "The other werewolf is {}".format(player2.nickname))
                                await dm_print(player2.player_id, "The other werewolf is {}".format(player1.nickname))
            return player_list

        elif self.type == 'inform_minion':
            return
        elif self.type == 'inform_mason':
            for player1 in player_list:
                if player1.role == 'mason' and player1.check == False:
                    player1.check = True
                    for player2 in player_list:
                        if player2.role == 'mason' and player2.check == False:
                            if player1.player_id in [100, 101, 102] and player2.player_id in [100, 101, 102]:
                                pass
                            elif player2.player_id in [100, 101, 102]:
                                await dm_print(player1.player_id, "You are the only mason.")
                            elif player1.player_id in [100, 101, 102]:
                                await dm_print(player2.player_id, "You are the only mason.")
                            else:
                                await dm_print(player1.player_id, "The other mason is {}".format(player2.nickname))
                                await dm_print(player2.player_id, "The other mason is {}".format(player1.nickname))
            return player_list
        elif self.type == 'prompt_drunk':
            for card in player_list:
                if card.player_id == self.picked_card_id:
                    temp = player.role
                    player.role = self.player.role
                    self.player.role = temp
            ### td: inform drunk of successful operation
            return player_list

        elif self.type == 'see_player':
            for player in player_list:
                if self.seen_player == player.nick:
                    await dm_print(self.player.player_id, "Your chosen player is a {}".format(player.role))
            return player_list

        elif self.type == 'see_cards':
            for card in player_list:
                if card.player_id in [100, 101]:
                    await dm_print(self.player.player_id, "One card is a {}".format(card.role))
            return player_list

        else:
            raise("Action not found '{}'.".format(self.type))

### Takes a list of actions then executes the ones of the given type
async def execute_actions(action_type, action_list, player_list):
    for action in action_list:
        if action_type == action.type:
            player_list = await action.execute(player_list)
    return player_list

### Executes all actions in order
async def execute_all(action_list, player_list):
    player_list = await execute_actions('inform_were', action_list, player_list)
    player_list = await execute_actions('inform_minion', action_list, player_list)
    player_list = await execute_actions('inform_mason', action_list, player_list)
    player_list = await execute_actions('see_player', action_list, player_list)
    player_list = await execute_actions('see_cards', action_list, player_list)
    player_list = await execute_actions('robber_swap', action_list, player_list)
    player_list = await execute_actions('troublemaker_swap', action_list, player_list)
    player_list = await execute_actions('prompt_drunk', action_list, player_list)
    player_list = await execute_actions('inform_insom', action_list, player_list)


gm_id = 268834601466593280
global_roles = ['villager', 'werewolf', 'mason', 'troublemaker', 'insomniac', 'robber', 'seer', 'drunk', 'hunter', 'minion']
werewolf_textchannel = 711232285994909749
player_list = []

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PREFIX = str(os.getenv('PREFIX'))

def validate_roles(role_list, global_roles):
    #global_roles = ['villager', 'werewolf', 'mason', 'troublemaker', 'insomniac', 'robber', 'seer', 'drunk', 'hunter', 'minion'] 
    validity = 0
    print(global_roles)
    for i in range(len(role_list)):
        for j in range(len(global_roles)):
            print('checking {} and {}'.format(role_list[i], global_roles[j]))
            if role_list[i] == global_roles[j]:
                validity += 1
            else:
                #print(role_list[i])
    
    print(validity)
    if validity == len(role_list):
        return True
    else: 
        return False


client = discord.Client()

@client.event
async def on_ready():
    print("running client")

@client.event
async def on_message(message):
    global global_roles
    if message.author == client.user:
        return

    if message.content == 'werewolf.help':
        pass

    if message.content == 'werewolf.setplayers':
        await message.channel.send('Consulting the Game Master ... ')
        ### GM decides who's playing.
        player_ids_str = await dm_input(gm_id, "Enter comma separated player ids. ")
        player_ids_str = player_ids_str.replace(' ', '')
        player_ids = player_ids_str.split(',')
        #player_ids = list(range(len(global_roles)))
        ### 100, 101, and 102 are the middle cards.
        player_ids.extend([100, 101, 102])

        ### Manual role prompt
        manual_roles = False
        manual_role_ask = await dm_input(gm_id, 'Would you like to assign roles manually? (Y/N) ')
        if manual_role_ask == 'Y':
            manual_roles = True
        else:
            manual_roles = False

        if manual_roles == False:
            decided = False
            while(decided == False):
                ### Role Loop: GM decides which roles are included.
                roles_str = await dm_input(gm_id, "Role options include: {}. Enter comma separated roles you would like to include. Must include {} roles. ".format(global_roles, len(player_ids)))
                roles_str.replace(' ', '')
                roles = roles_str.split(',')
                #global_roles = ['villager', 'werewolf', 'mason', 'troublemaker', 'robber', 'seer', 'drunk', 'hunter', 'minion']
                decided_str = await dm_input(gm_id, "Your roles are: {}. Is this ok? (Y/N) ".format(roles))
                if decided_str == 'Y' and len(roles) == len(player_ids) and validate_roles(roles, global_roles):
                    decided = True
                elif len(roles) != len(player_ids):
                    await dm_print(gm_id, 'Length of roles given ({}) does not match number of players ({}).'.format(len(roles), len(player_ids)))
                elif validate_roles(roles, global_roles) == False:
                    await dm_print(gm_id, 'Invalid roles.')

            random.shuffle(roles)
        #player_dict = dict(zip(player_ids, roles))
        nickname_dict = await get_nicks(player_ids)
        if manual_roles == True:
            nicknames = list(nickname_dict.values())
            decided = False
            while(decided == False):
                ### Role Loop: GM decides which roles are included.
                roles_str = await dm_input(gm_id, "Role options include: villager, werewolf, mason, troublemaker, robber, seer, drunk, hunter, tanner, minion. Enter comma separated roles you would like to include. Must include {} roles. Roles will be assigned directly to players. Here are the players: {}".format(len(player_ids), nicknames))
                roles_str.replace(' ', '')
                roles = roles_str.split(',')
                role_dict = dict(zip(nicknames, roles))
                #global_roles = ['villager', 'werewolf', 'mason', 'troublemaker', 'robber', 'seer', 'drunk', 'hunter', 'minion']
                decided_str = await dm_input(gm_id, "Your player:roles are: {}. Is this ok? (Y/N) ".format(role_dict))
                if decided_str == 'Y' and len(roles) == len(player_ids) and validate_roles(roles, global_roles):
                    decided = True
                elif len(roles) != len(player_ids):
                    await dm_print(gm_id, 'Length of roles given ({}) does not match number of players ({}).'.format(len(roles), len(player_ids)))
                elif validate_roles(roles, global_roles) == False:
                    await dm_print(gm_id, 'Invalid roles.')

        global player_list

        ### Contruct array of Player objects.
        for i in range(len(player_ids)):
            p = Player(player_ids[i], roles[i], nickname_dict[player_ids[i]])
            player_list.append(p)

        role_message = await client.get_user(gm_id).send(format_player_list(player_list))

    if message.content == 'werewolf.startgame':
        await message.channel.send('Game is starting, everyone close your eyes!')

        for i in range(len(player_list)):
            if player_list[i].player_id == 100 or player_list[i].player_id == 101 or player_list[i].player_id == 102:
                pass
            else:
                print(player_list[i])
                await dm_print(player_list[i].player_id, 'Your starting role is {}. Good Luck!'.format(player_list[i].role))
                pass

        ### Night Actions Here
        action_list = []
        for p in player_list:
            action_list.append(Action(p, player_list))

        execute_all(action_list, player_list)

        ### After Night Actions, have a 10 minute wait period with warnings.
        await message.channel.send('Everybody wake up and begin discussion. You have 10 minutes.')
        '''
        await asyncio.sleep(300)
        await message.channel.send('5 Minutes left.')

        await asyncio.sleep(120)
        await message.channel.send('2 Minutes left.')

        await asyncio.sleep(60)
        await message.channel.send('1 Minute left')

        await asyncio.sleep(30)
        await message.channel.send('30 Seconds left')
        '''
        #await asyncio.sleep(30)
        await message.channel.send('TIME\'S UP!!! YOU MUST VOTE NOW!')

        ### Voting
        deaths = []

        player_nicks_vote = [0] * len(player_list)
        for i in range(len(player_list)):
            player_nicks_vote[i] = player_list[i].nickname

        vote_dict = dict(zip(player_nicks_vote, [0 for j in range(len(player_nicks_vote))]))
        for i in range(len(player_list)):
            vote = await dm_input(player_list[i].player_id, 'Who do you want to kill? Options are: {}.'.format(player_nicks_vote))
            if player_list[i].role == 'hunter':
                deaths.append(vote)
            else:
                vote_dict[vote] += 1

        await dm_print(gm_id, 'Here are the votes: {}'.format(str(vote_dict)))
        vote_list = list(vote_dict.values())
        death = player_nicks_vote[vote_list.index(max(vote_list))]
        deaths.append(death)

        if len(deaths) == 1:
            await message.channel.send('{} was killed by the village.'.format(death))
        else:
            await message.channel.send('{} and {} were killed by the village.'.format(deaths[0], deaths[1]))

        for p in player_list:
            if p.nickname in death:
                if p.role == 'werewolf':
                    await message.channel.send('{} was a werewolf. The villagers win!'.format(p.nickname))
                elif p.role == 'tanner':
                    await message.channel.send('{} was a tanner. They win!'.format(p.nickname))
                else:
                    await message.channel.send('{} was a {}. The werewolves win!'.format(p.nickname, p.role))



client.run(TOKEN)
