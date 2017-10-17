import discord
import asyncio
import re
from Plugins import roleAuth
from Plugins import botConf
from Plugins import fccid

client = discord.Client()

def serverRole(author_id):
    roles = client.get_server("281017054549508098").get_member(author_id).roles
    return roles


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='FCC Lookup / !help'))

help_msg = '!id fccid_here'

@client.event
async def on_message(message):
    ##!private creates a new private message and then sends some text over.
    if message.content.startswith('?private'):
        privateMessage = await client.start_private_message(message.author)
        await client.send_message(privateMessage, 'test')

    if message.content.startswith('?help'):
        #await client.purge_from(message.channel, limit=1, check=message.author)
        privateMessage = await client.start_private_message(message.author)
        await client.send_message(privateMessage, help_msg)


    if message.content.startswith('!id'):
        if roleAuth.checkRole(serverRole(message.author.id)):
            await client.send_typing(message.channel)
            try:
                msg = message.content
                split = msg.split(' ')
                id = split[1]
                url1 = ('https://fccid.io/%s\\' % id)
                url2 = ('https://gov.fccid.io/%s\\' % id)
                title = fccid.manu(id)
                freq = fccid.freq(id)
                photos = fccid.internal(id)
                power = fccid.power(id)
                diagram = fccid.diagram(id)
                schematics = fccid.schematics(id)
                part = fccid.part(id)
                assembled = "```" + title + "\r\n" + freq + "\r\n" + power + "  " + part + "```" + "\r\n" + 'Details: ' + url1 + ' or ' + url2 + '\r\n' + photos + '\r\n' + diagram + '\r\n' + schematics
                await client.send_message(message.channel, assembled)
            except:
                await client.send_message(message.channel,
                                          'Something went wrong, here is the url. Take it or leave it ya prick!\r\n\r\n' + 'FCC.Gov: ' + url1 + '\r\n' + 'FCCID: ' + url2)

    if message.content.startswith('!debug'):
        if roleAuth.checkRole(serverRole(message.author.id)):
            await client.send_typing(message.channel)
            msg = message.content
            split = msg.split(' ')
            id = split[1].upper()
            url1 = ('https://fccid.io/%s\\' % id)
            url2 = ('https://gov.fccid.io/%s\\' % id)
            title = fccid.manu(id)
            freq = fccid.freq(id)
            photos = fccid.internal(id)
            power = fccid.power(id)
            diagram = fccid.diagram(id)
            schematics = fccid.schematics(id)
            part = fccid.part(id)
            assembled = "```" + title + "\r\n" + freq + "\r\n" + power + "  " + part + "```" + "\r\n" + 'Details: ' + url1 + ' or ' + url2 + '\r\n' + photos + '\r\n' + diagram + '\r\n' + schematics
            await client.send_message(message.channel, assembled)


    if message.content.startswith('?test'):
        if roleAuth.checkRole(serverRole(message.author.id)):
            await client.send_message(message.channel, 'Authorized')


    if message.content.startswith('?getroles'):
        if roleAuth.checkRole(serverRole(message.author.id)):
            privateMessage = await client.start_private_message(message.author)
            await client.send_message(privateMessage, botConf.grabAuthroles())

    if message.content.startswith('?updateroles'):
        if roleAuth.checkRole(serverRole(message.author.id)):
            privateMessage = await client.start_private_message(message.author)
            msg = message.content
            split = msg.split(' ', 4)
            try:
                role1 = split[1]
            except:
                role1 = 'None'
            try:
                role2 = split[2]
            except:
                role2 = 'None'
            try:
                role3 = split[3]
            except:
                role3 = 'None'
            try:
                role4 = split[4]
            except:
                role4 = 'None'
            await client.send_typing(message.channel)
            await client.send_message(privateMessage, 'Below are the new roles, to save these roles now type: confirmed')
            await client.send_message(privateMessage, 'Role1: ' + role1 + '\r\nRole2: ' + role2 + '\r\nRole3: ' + role3 + '\r\nRole4: ' + role4)
            if await client.wait_for_message(author=message.author, content='confirmed'):
                botConf.updateAuthroles(role1, role2, role3, role4)
                await client.send_message(privateMessage, 'Authorized roles have been succesfully saved.')
            else:
                await client.send_message(privateMessage, 'Authorized roles have NOT been saved.')




client.run(botConf.grabKey())