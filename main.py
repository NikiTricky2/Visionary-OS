import os
import discord
from discord.ext import commands
import datetime
import random
from urllib import request, parse
import json

import utils as ut

bot = commands.Bot(command_prefix='$', case_insensitive=True)
start_time = datetime.datetime.now()

with open("./assets/languages.json", "r") as f:
    languages = json.loads(f.read())

# Event examples
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')
    game = discord.Game("Open Sourcerers")
    await bot.change_presence(activity = game)

@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return

    # Secret commands here! They will not show in the help command
    
    if message.content.startswith('$ping'):
        await message.channel.send('Pong and Hello!')
    
    if message.content.startswith('$i-read-source-code ' + str(message.author.id)):
        await message.channel.send(message.author.mention + " reads source code!")

@bot.listen('on_command_error')
async def on_command_error(ctx, error):    
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        err = str(error)
    if isinstance(error, commands.MissingPermissions):
        err = "You do not have the appropriate permissions to run this command."
    if isinstance(error, commands.BotMissingPermissions):
        err = "I don't have sufficient permissions!"
    else:
        # print("error not caught")
        # print(error) 
        raise error
        # return
    
    embed = ut.embeds.ErrorEmbed(ctx, err)
    await ctx.send(embed=embed)

# Example of a command
@bot.command(name='command_name', description="Description for help command")
async def command(ctx, other_arguments_here):
    pass # Do stuff here

@bot.command(name='uptime', description="Get the time the bot has been online")
async def uptime(ctx):
    t = datetime.datetime.now() - start_time
    embed = ut.embeds.SendEmbed(ctx, "Uptime", str(t))
    await ctx.send(embed=embed)

@bot.command(name='8ball', description="Answers a yes/no question")
async def ball(ctx, *, question):
    answers = ["Yes", "No", "I don't know", "Maybe", "Yep", "Nope", "Absolutley yes", "Absolutley no"]
    embed = ut.embeds.SendEmbed(ctx, question, random.choice(answers))
    await ctx.send(embed=embed)

@bot.command(name='translate', description="Translate some text to another language")
async def translate(ctx, language_from, language_to, *, text):
    if language_from not in languages.keys():
        await ctx.send(f"Language {language_from} not found")
    elif language_to not in languages.keys():
        await ctx.send(f"Language {language_to} not found")
    
    language_from = languages[language_from]
    language_to = languages[language_to]

    try:
        resp = request.urlopen(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={language_from}&tl={language_to}&dt=t&q={parse.quote_plus(text)}").read().decode("utf8")
    except:
        await ctx.send("An error occurred", "An error occurred. Please try again later.")
    
    translated_text = ""
    
    for sentence in json.loads(resp)[0]:
        translated_text += sentence[0]
    
    embed = ut.embeds.SendEmbed(ctx, "Translated text", translated_text)
    await ctx.send(embed=embed)

@bot.command(name="latex", description="Render some LaTeX")
async def latex(ctx, *, latex):
    url = "https://latex.codecogs.com/gif.latex?\\bg_white&space;" + parse.quote(latex.replace("(", "\(").replace(")", "\)"))
    embed = ut.embeds.SendEmbed(ctx, "Rendered LaTeX", latex, image=url)
    await ctx.send(embed=embed)

bot.run(os.environ['BOT_TOKEN'])
