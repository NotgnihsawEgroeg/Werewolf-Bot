
class Get:
    def list_of_names():
        name_list = ["Josh", "Joey", "John", "Rebecca", "Peter", "Calvin", "Biff", "Joseph", "Benjamin", "Laura"]
        return name_list
        #a list of all the player's names. I recommend keeping this in the bot's code
        #in order to cross reference it with player answers, so you can tell players
        #that a desired name is not in the list when they vote, steal, etc.

    def troublemaker_choices(tm_name):
        swap_list = ["Josh", "Biff"]
        return swap_list
        #query the bot to ask [player_name] (troublemaker) for swap info, in the form of
        #[player 1, player 2]

    def robber_choice(robber_name):
        steal = "Rebecca"
        return steal
        #query the bot to ask [player_name] (robber) for steal info (which player to steal from)

    def seer_choice(seer_name):
        player = "Laura"
        if 1 == 1:
            return player
        else:
            return "card_choice"
        #query the bot for the seer's desired player or return a specific string if the seer
        #would rather see cards from the middle

    def drunk_card_choice(drunk_name):
        num = 2
        return num - 1
        #any number 1 through 3

    def votes():
        vote_dict = ["Calvin" : 5, "Peter" : 6]
        return vote_dict
        #query all players for their votes and tally up;
        #the dict is in the format [player name1] : [# of votes], [player name2] : [# of votes], etc
class Send:

    def roles(player_dict):
        return 0
        #send everyone their roles, with an explanation on what the role does
        #dict format ex. ["John" : "robber", "Joey" : "seer"]

    def confirm(player_name):
        return 0
        #send a message of confirmation to a player that they
        #have successfully performed an action (useful for troublemaker and drunk)

    def robber_role(robber_name, new_role):
        return 0
        #send a message with the robber's new role

    def minion_info(minion_name, werewolf_name1, werewolf_name2):
        return 0
        #tell the minion who the werewolves are (player 1 and player 2)

    def seer_player_info(seer_name, player, role):
        return 0
        #tell the seer what the role of the requested player is

    def seer_card_info(seer_name, card_role1, card_role2):
        return 0
        #tell the seer two cards out of the middle if they chose that option

    def other_werewolf(werewolf_name1, werewolf_name2):
        return 0
        #tell the werewolves who the other werewolf is
        #if there isn't another werewolf, werewolf2 == None

    def other_mason(mason_name1, mason_name2):
        return 0
        #tell the mason who the other mason is
        #if there isn't another mason, mason2 == None

    def confirm_insomniac(insomniac_name):
        return 0
        #tell the insomniac that they are the insomniac

    def game_summary(log):
        return 0

        #log will be a string that tells the "story" of the game
        #there should be an option to send the game summary to general chat
