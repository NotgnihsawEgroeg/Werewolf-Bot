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

class Action():
    def __init__(player):
        pass
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

async def get_action(player):
    if player.role == 'seer':
        pass
        

gm_id = 268834601466593280
global_roles = ['villager', 'werewolf', 'mason', 'troublemaker', 'robber', 'seer', 'drunk', 'hunter', 'minion']
werewolf_textchannel = 711232285994909749
player_list = []

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
    global player_list
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
        player_list = []

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
                #await dm_print(player_list[i].player_id, 'Your starting role is {}. Good Luck!'.format(player_list[i].role))
                pass

        ### Night Actions Here
        





client.run(TOKEN)
