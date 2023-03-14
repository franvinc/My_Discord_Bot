import discord
from discord.ext import commands
import urllib.request
import re
import pafy
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import random
import asyncio
import unidecode
random.seed(None)
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

bot=commands.Bot(command_prefix="/")
queue_index = 0


queue=[]
LOOP=[]
loop_name=[]
titles=[]
song_index=0
@bot.command()
async def join(ctx):
    if (ctx.author.voice and not ctx.voice_client):
        channel=ctx.author.voice.channel
        await channel.connect()
        await ctx.send("Connected")
    elif(ctx.author.voice and ctx.voice_client):
        await ctx.send("Already in the voice channel")
    else:
        await ctx.send("Join the voice channel")

@bot.command()
async def clear(ctx):
    queue.clear()
    loop_name.clear()
    titles.clear()
    global queue_index
    queue_index=0
def my_after(ctx):
    global queue_index
    print("my_after")
    print("queue index is")
    print(queue_index)
    if(queue_index<len(queue)):
        ctx.voice_client.play(queue[queue_index],after=lambda e: my_after(ctx))
        print(titles[queue_index])
        queue_index=queue_index+1
    else:
        queue_index=0

def my_loop_bis(ctx):
    if(len(loop_name)>0):
        html_temp=urllib.request.urlopen("https://www.youtube.com/results?search_query="+loop_name[0])
        video_id_temp=re.findall(r"watch\?v=(\S{11})", html_temp.read().decode())
        song = pafy.new(video_id_temp[0])  # creates new pafy object
        audio = song.getbestaudio()  # gets an audio source
        source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source, after=lambda e: my_loop_bis(ctx))

@bot.command()
async def add(ctx, *msg):
    global queue_index
    print("adding")
    msg_temp=""
    for k in range(len(msg)):
        msg_temp+="+"+str(msg[k])
    msg_temp=unidecode.unidecode(msg_temp)
    titles.append(msg_temp)
    await ctx.send(titles)
    await ctx.send("current index is"+str(queue_index))
    html_temp=urllib.request.urlopen("https://www.youtube.com/results?search_query="+msg_temp)
    video_id_temp=re.findall(r"watch\?v=(\S{11})", html_temp.read().decode())
    song = pafy.new(video_id_temp[0])  # creates a pafy object
    audio = song.getbestaudio()  # gets an audio source
    source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  # converts the youtube audio
    queue.append(source)
@bot.command()
async def play(ctx,*msg):
    if (len(loop_name)>0):
        loop_name.pop()

    msg_temp=""
    for k in range(len(msg)):
        msg_temp+="+"+str(msg[k])
    msg_temp=unidecode.unidecode(msg_temp)
    html_temp=urllib.request.urlopen("https://www.youtube.com/results?search_query="+msg_temp)
    video_id_temp=re.findall(r"watch\?v=(\S{11})", html_temp.read().decode())
    if (ctx.author.voice and not ctx.voice_client):
        channel=ctx.author.voice.channel
        await channel.connect()
        await ctx.send("https://www.youtube.com/watch?v="+video_id_temp[0])
        print("case1")
        song = pafy.new(video_id_temp[0])  # creates a pafy object
        audio = song.getbestaudio()  # gets an audio source
        source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  # converts the youtube audio
        #queue.append(source)
        ctx.voice_client.play(source, after= lambda e: my_after(ctx))


    elif(ctx.author.voice and ctx.voice_client):
        if(ctx.voice_client.is_playing):
            ctx.voice_client.stop()
            print("case2")
            await ctx.send("https://www.youtube.com/watch?v="+video_id_temp[0])
            song = pafy.new(video_id_temp[0])  # creates new pafy object
            audio = song.getbestaudio()  # gets an audio source
            source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  # converts the youtube audio
            #queue.append(source)
            ctx.voice_client.play(source, after=lambda e: my_after(ctx))
        else:
            await ctx.send("https://www.youtube.com/watch?v="+video_id_temp[0])
            print("case3")
            song = pafy.new(video_id_temp[0])  # creates new pafy object
            audio = song.getbestaudio()  # gets an audio source
            source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  # converts the youtube audio
            #queue.append(source)
            ctx.voice_client.play(source,after=lambda e: my_after(ctx))


    else:
        await ctx.send("Join the voice channel")
@bot.command()
async def loop(ctx,*msg):
    if(len(loop_name)>0):
        loop_name.pop()
    msg_temp=""

    for k in range(len(msg)):
        msg_temp+="+"+str(msg[k])
    msg_temp=unidecode.unidecode(msg_temp)
    loop_name.append(msg_temp)
    html_temp=urllib.request.urlopen("https://www.youtube.com/results?search_query="+msg_temp)
    video_id_temp=re.findall(r"watch\?v=(\S{11})", html_temp.read().decode())

    if (ctx.author.voice and not ctx.voice_client):
        channel=ctx.author.voice.channel
        await channel.connect()
        await ctx.send("https://www.youtube.com/watch?v="+video_id_temp[0])
        print("case1")
        song = pafy.new(video_id_temp[0])  # creates a pafy object
        audio = song.getbestaudio()  # gets an audio source
        source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  # converts the youtube audio
        #queue.append(source)
        #LOOP.append(source)

        #print(LOOP[0])
        #print(LOOP)
        ctx.voice_client.play(source, after= lambda b: my_loop_bis(ctx))


    elif(ctx.author.voice and ctx.voice_client):
        if(ctx.voice_client.is_playing):
            ctx.voice_client.stop()
            print("case2")
            await ctx.send("https://www.youtube.com/watch?v="+video_id_temp[0])
                       song = pafy.new(video_id_temp[0])  # creates new pafy object
            audio = song.getbestaudio()  # gets an audio source
            source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  # converts the youtube audio
            #queue.append(source)
            #LOOP.append(source)

            ctx.voice_client.play(source, after=lambda b: my_loop_bis(ctx))

        else:
            await ctx.send("https://www.youtube.com/watch?v="+video_id_temp[0])
            print("case3")
            song = pafy.new(video_id_temp[0])  # creates new pafy object
            audio = song.getbestaudio()  # gets an audio source
            source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  # converts the youtube audio
            #queue.append(source)
            #LOOP.append(source)
            #print(LOOP[0])
            #print(LOOP)
            ctx.voice_client.play(source,after=lambda b: my_loop_bis(ctx))


    else:
        await ctx.send("Join the voice channel")
@bot.command()
async def pause(ctx):
    if(ctx.voice_client.is_playing):
        ctx.voice_client.pause()
        await ctx.send("Paused")
    else:
        await ctx.send("Nothing to pause")

@bot.command()
async def resume(ctx):
    if(ctx.voice_client.is_paused):
        ctx.voice_client.resume()
        await ctx.send("Resuming")
    else:
        await ctx.send("Bot is not paused")


@bot.command()
async def skip(ctx):
    if(ctx.voice_client.is_paused or ctx.voice_client.is_playing):
        ctx.voice_client.stop()
        await ctx.send("Skipping")
    else:
        await ctx.send("No audio files to stop")
@bot.command()
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.voice_client.disconnect()
        await ctx.send("Leaving")

    else:
        await ctx.send("No channel to leave")

@bot.command()
async def roll(ctx,input : str):
    str_res="["
    counter=0
    somme=0
    dice=input
    dice=dice.split("d")
    if(dice[0]==''):
        dice_number=1
        dice_range=int(dice[1])
    else:
        dice_number=int(dice[0])
        dice_range=int(dice[1])

    while(counter<dice_number):
        counter+=1
        res=random.randrange(dice_range)+1
        somme+=res
        str_res+=str(res)+" "
    str_res+="]"

    await ctx.send((str(ctx.author)).split("#")[0]+ " Roll : "+str(somme))
    await ctx.send(str_res)

bot.run("INSERT YOUR DISCORD TOKEN HERE")
