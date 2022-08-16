import os
import random
from datetime import datetime
import discord
from discord.ext import commands
from discord import utils, ui, interactions
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class TaskModal(ui.Modal, title="New Task"):
    title = ui.TextInput(label="title")
    description = ui.TextInput(label="description")
    role = ui.TextInput(label="role")
    difficulty = ui.TextInput(label="difficulty")

    async def on_submit(self, interaction: interactions.Interaction) -> None:
        embed = discord.Embed(title=self.title,
                              description=f"{self.description}\n\n{self.role}\n\n{self.difficulty}",
                              timestamp=datetime.now(),
                              colour=discord.Colour.blurple())
        embed.set_author(name=interaction.user,
                         icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)


bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f"Welcome to the server {member.mention}!")
    return


# @bot.listen('on_message')
# async def on_message(message) -> bool:
#     if message.content.startswith('$hello'):
#         member = message.author
#         await message.channel.send(f'Hello {member.mention}!')
#         return True
#
#     if message.content.startswith('$role'):
#         msg = message.content.split()
#         role = msg[-1]
#         guild = message.guild
#         member = message.author
#         match len(msg):
#             case 3:
#                 if not utils.get(guild.roles, name=role) and\
#                         member.guild_permissions.manage_roles:
#                     # color = "%06x" % random.randint(0, 0xFFFFFF)
#                     await guild.create_role(name=role)
#             case 2:
#                 if utils.get(guild.roles, name=role):
#                     await member.add_roles(role)
#                 else:
#                     await message.channel.send(f"Role doesn't exists")
#             case _:
#                 await message.channel.send(f'Role invalid.')
#                 return False
#         return True
#
#     if message.content.startswith('$task'):
#         TaskModal()
#         return True


@bot.command(name='role')
async def role(ctx, *, arg):
    msg = arg.split()
    role_name = msg[-1]
    guild = ctx.guild
    member = ctx.author
    match len(msg):
        case 2:
            if not utils.get(guild.roles, name=role_name) and \
                    member.guild_permissions.manage_roles:
                # color = "%06x" % random.randint(0, 0xFFFFFF)
                await bot.create_role(guild,
                                      name=role_name,
                                      colour=discord.Colour(0xffffff))
                await ctx.send(f"Role {role_name} created!")
            else:
                await ctx.send(f"You don't have permissions!")
        case 1:
            role_obj = utils.get(guild.roles, name=role_name)
            if role_obj:
                await member.add_roles(role_obj)
                await ctx.send(f"Role {role_name} added!")
            else:
                await ctx.send(f"Role doesn't exists")
        case _:
            await ctx.send(f'Role invalid.')
            return False
    return True


bot.run(TOKEN)
