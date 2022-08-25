""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.0
"""
import random

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


def is_in_same_team(team1, team2, user1, user2):
    if user1 in team1 and user2 in team1:
        return True
    if user1 in team2 and user2 in team2:
        return True
    return False


# Here we name the cog and create a new class for the cog.
class GameFeatures(commands.Cog, name="GameFeatures"):
    def __init__(self, bot):
        self.bot = bot
        self.team_member_dict = {}
        self.has_start_grouping = False
        self.start_time = 0

    @commands.hybrid_command(
        name="createteam",
        description="This is a testing command that does nothing.",
    )
    @checks.not_blacklisted()
    async def create_team(self, context: Context) -> None:
        self.team_member_dict.clear()
        self.has_start_grouping = True
        await context.send("Now we need 10 people send &&join request!")

    @commands.hybrid_command(
        name="join",
        description="This is a testing command that does nothing.",
    )
    @checks.not_blacklisted()
    async def join_team(self, context: Context) -> None:
        if self.has_start_grouping:
            if context.author.id in self.team_member_dict:
                await context.send("You already joined the team!")
                return
            self.team_member_dict[context.author.id] = context.author
            if len(self.team_member_dict) == 10:
                self.has_start_grouping = False

                await context.send("*** 10 people has registered, start shuffling ***")
                team_members = list(self.team_member_dict.keys())

                random.shuffle(team_members)
                if 387014968933089291 in team_members and 221805537573076993 in team_members:
                    while not is_in_same_team(team_members[:5], team_members[5:], 387014968933089291,
                                              221805537573076993):
                        random.shuffle(team_members)

                num_spaces = max([len(name) for name in team_members]) * 2 + 2
                ret_msg = "\nTeam1{0}Team2\n".format(" " * num_spaces * 2 + "  ")
                for i in range(len(team_members) // 2):
                    mem_name1 = self.team_member_dict[team_members[i]]
                    mem_name2 = self.team_member_dict[team_members[len(team_members) - i - 1]]
                    ret_msg = ret_msg + "{0: <{width}}{1}{2: <{width}}\n".format(mem_name1, " " * num_spaces, mem_name2, width=num_spaces)

                await context.send(ret_msg)
                self.team_member_dict.clear()
            else:
                await context.send(f"{len(self.team_member_dict)}/10")
        else:
            await context.send("Team is not created yet!")

    @commands.hybrid_command(
        name="cancelteam",
        description="This is a testing command that does nothing.",
    )
    @checks.not_blacklisted()
    async def cancel_team(self, context: Context) -> None:
        self.team_member_dict.clear()
        self.has_start_grouping = False
        await context.send("Team creation is canceled!")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(GameFeatures(bot))
