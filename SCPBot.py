# Title: SCPBot     Author: TDXPQ (Aditya Jindal)
# Description:  Discord both that allows users to get SCP descriptsions based off either name or number.

# Import custom functions.
from WebParsing import scp_info, scp_rand, scp_name

#Import external libraries.
import discord
from discord.ext import commands
import random

# Define hardcoded variables.
TOKEN = open('TOKEN.txt', 'r')
client = commands.Bot(command_prefix = '-')


# Define project code.
@client.event
async def on_ready():
    print('Bot is ready.')

@client.command(aliases=['SCP', 'Scp'])
async def scp(ctx, num, para_length='1'):   #Num is used to the the SCP number and par_length is used to know how many paragraphs from the description the user wants.
    if num.casefold() == 'random':  #Allows user to get a random SCP entry.
        scp_entry = scp_rand()
    else:
        try:    #Handle the error if user inputs a string that is not a number.
           user_input = int(num.strip())
           scp_entry = scp_info(user_input)
        except:
            await ctx.send(f"{num} is not a valid SCP entry")
            return
    try:    #Handles the error if user inserts a paragraph length that is not a number, it will defualt to 1.
        length = int(para_length.strip())
    except:
        length = 1

    if scp_entry.valid:
        await ctx.send(f"SCP:{scp_entry.str_num}\nSeries:{scp_entry.series}")
        await ctx.send(f"Name:{scp_entry.name}")

        if length < 0:  #If the user inputs a negative number the program will take that to mean a 1.
            length = 1
        elif length > len(scp_entry.desc):  #If user puts a number greater than the number of paragraphs then program takes that to mean all of the paragraphs or 0.
            length = 0

        if length == 0: #Important to note that the program takes 0 to mean output the entire description.
            for paragraph in range(0, len(scp_entry.desc)):
                await ctx.send(scp_entry.desc[paragraph])
        else:
            for paragraph in range(0, length):
                await ctx.send(scp_entry.desc[paragraph])
    else:
         await ctx.send(f"{scp_entry.num} is an invalid SCP Number")
    return


@client.command()
async def scpname(ctx, para_length, *, entry_name):
    try:    #This block tries the scp_name function for any reason if it errors out the output will just be void.
        scp_num = scp_name(entry_name.strip())
    except:
        return
    if scp_num == 0:    #This conditional is if the name is not found.
        await ctx.send(f"{entry_name.strip()} is not a valid SCP name")
        return
    
    try:    #Handles the error if user inserts a paragraph length that is not a number, it will defualt to 1.
        length = int(para_length.strip())
    except:
        await ctx.send(f"{para_length.strip()} is not a valid number of paragraph")
        return
    
    scp_entry = scp_info(scp_num)

    if scp_entry.valid: #Following code is to print out the results like int the scp command.
        await ctx.send(f"SCP:{scp_entry.str_num}\nSeries:{scp_entry.series}")
        await ctx.send(f"Name:{scp_entry.name}")

        if length < 0:  #If the user inputs a negative number the program will take that to mean a 1.
            length = 1
        elif length > len(scp_entry.desc):  #If user puts a number greater than the number of paragraphs then program takes that to mean all of the paragraphs or 0.
            length = 0

        if length == 0: #Important to note that the program takes 0 to mean output the entire description.
            for paragraph in range(0, len(scp_entry.desc)):
                await ctx.send(scp_entry.desc[paragraph])
        else:
            for paragraph in range(0, length):
                await ctx.send(scp_entry.desc[paragraph])
    return

client.run(TOKEN)