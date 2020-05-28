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

class Action():
    def __init__(self, player, player_list):
        self.player = player
        self.nick_list = []
        for player_element in player_list:
            self.nick_list.append(player_element.nickname)

        if player.role == 'troublemaker':
            self.type = 'swap'
            prompt = "Which two players would you like to swap? (comma separated)"
            def get_troublemaker_input(prompt):
                temp_input = dm_input(player.player_id, prompt)
                input_list = input.split(",")
                if input_list.length() == 2:
                    input_list[0] = input_list[0].strip()
                    input_list[1] = input_list[1].strip()
                    if (input_list[0] in self.nick_list) and (input_list[1] in self.nick_list):

                if
        elif player.role == 'robber':
            self.type = 'swap'
        elif player.role == 'insomniac':
            self.type = 'inform_insom'
        elif player.role == 'mason':
            self.type = 'inform_mason'
        elif player.role == 'werewolf':
            self.type = 'inform_were'
        elif player.role == 'minion':
            self.type = 'inform_minion'
        elif player.role == 'drunk':
            self.type = 'prompt_drunk'
        elif player.role == 'seer':
            prompt = "Would you like to see cards (type 'cards') or player (type 'player')?"
            def get_seer_input(prompt):
                input = dm_input(player.player_id, prompt)
                if input == 'player':
                    message = 'Input accepted!'
                    dm_print(player.player_id, message)
                    return 'see_player'
                elif input == 'cards':
                    message = 'Input accepted!'
                    dm_print(player.player_id, message)
                    return 'see_cards'
                else:
                    prompt = "Not a valid option. Please try again."
                    return get_seer_input(prompt)
            self.type = get_seer_input(prompt)



    def execute(self, player_list)


gm_id = 268834601466593280
global_roles = ['villager', 'werewolf', 'mason', 'troublemaker', 'robber', 'seer', 'drunk', 'hunter', 'minion']
werewolf_textchannel = 711232285994909749

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PREFIX = str(os.getenv('PREFIX'))


client = discord.Client()

@client.event
async def on_ready():
    print("running client")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'werewolf.help':
        pass

    if message.content == 'werewolf.setplayers':
        await message.channel.send('Consulting the Game Master ... ')
        ### GM decides who's playing.
        player_ids_str = await dm_input(gm_id, "Enter comma separated player ids. ")
        player_ids_str = player_ids_str.replace(' ', '')
        #player_ids = split(',', player_ids_str)
        player_ids = list(range(len(global_roles)))
        ### 100, 101, and 102 are the middle cards.
        player_ids.extend([100, 101, 102])

        decided = False
        while(decided == False):
            ### Role Loop: GM decides which roles are included.
            roles_str = await dm_input(gm_id, "Role options include: villager, werewolf, mason, troublemaker, robber, seer, drunk, hunter, tanner, minion. Enter comma separated roles you would like to include. Must include {} roles. ".format(len(player_ids)))
            roles = roles_str.split(',')
            #global_roles = ['villager', 'werewolf', 'mason', 'troublemaker', 'robber', 'seer', 'drunk', 'hunter', 'minion']
            decided_str = await dm_input(gm_id, "Your roles are: {}. Is this ok? (Y/N) ".format(roles))
            if decided_str == 'Y' and len(roles) == len(player_ids):
                decided = True
            elif len(roles) != len(player_ids):
                await dm_print(gm_id, 'Length of roles given ({}) does not match number of players ({}).'.format(len(roles), len(player_ids)))

        random.shuffle(roles)
        #player_dict = dict(zip(player_ids, roles))
        nickname_dict = await get_nicks(player_ids)
        global player_list = []

        ### Contruct array of Player objects.
        for i in range(len(player_ids)):
            p = Player(player_ids[i], roles[i], nickname_dict[player_ids[i]])
            player_list.append(p)

        role_message = await client.get_user(gm_id).send(format_player_list(player_list))

    if message.content == 'werewolf.startgame':





client.run(TOKEN)
