import discord
from discord.ext import commands
import asyncio
import role_ids

def in_list(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        text = '{0.title} '
        duration = self.player.duration
        if duration:
            text = text + ' [{0[0]}m{0[1]}s]'.format(divmod(duration, 60))
        return text.format(self.player)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.queue = []
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    @asyncio.coroutine
    def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = yield from self.songs.get()
            self.queue.remove(self.current)
            yield from self.bot.send_message(self.current.channel, 'Now playing```' + str(self.current) + '```') 
            self.current.player.start()
            yield from self.play_next_song.wait()

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state
        return state

    @asyncio.coroutine
    def create_voice_client(self, channel):
        voice = yield from self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()            
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    @asyncio.coroutine
    def summon(self, ctx):
        if not in_list(ctx.message.author.roles, lambda x: x.name in ['Master Control', 'Nixie', 'Slackerzz', 'Patreons']):
            yield from self.bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
            return False
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            yield from self.bot.say('You are not in a voice channel.')
            return False
        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = yield from self.bot.join_voice_channel(summoned_channel)
        else:
            yield from state.voice.move_to(summoned_channel)
        return True

    @commands.command(pass_context=True, no_pm=True, description='Add a youtube url to the music queue and start streaming music.')
    @asyncio.coroutine
    def play(self, ctx, *, song : str):
        if not in_list(ctx.message.author.roles, lambda x: x.name in ['Master Control', 'Nixie', 'Slackerzz', 'Patreons']):
            yield from self.bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
            return False
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'aac',
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'logtostderr': False,
            'no_warnings': True
        }
        if state.voice is None:
            success = yield from ctx.invoke(self.summon)
            if not success:
                return
        try:
            player = yield from state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            text = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            yield from self.bot.send_message(ctx.message.channel, text.format(type(e).__name__, e))
        else:
            entry = VoiceEntry(ctx.message, player)
            yield from self.bot.say('Queued up by **' + ctx.message.author.display_name + '**```' + str(entry) + '```')
            yield from state.songs.put(entry)
            state.queue.append(entry)

    @commands.command(pass_context=True, no_pm=True, description='Pause the current playing song')
    @asyncio.coroutine
    def pause(self, ctx):
        if not in_list(ctx.message.author.roles, lambda x: x.name in ['Master Control', 'Nixie', 'Slackerzz', 'Patreons']):
            yield from self.bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
            return False
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True, description='Resume the current playing song')
    @asyncio.coroutine
    def resume(self, ctx):
        if not in_list(ctx.message.author.roles, lambda x: x.name in ['Master Control', 'Nixie', 'Slackerzz', 'Patreons']):
            yield from self.bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
            return False
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True, description='Stop the music and make Nya leave')
    @asyncio.coroutine
    def stop(self, ctx):
        if not in_list(ctx.message.author.roles, lambda x: x.name in ['Master Control', 'Nixie', 'Slackerzz', 'Patreons']):
            yield from self.bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
            return False
        server = ctx.message.server
        state = self.get_voice_state(server)
        if state.is_playing():
            player = state.player
            player.stop()
        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            yield from state.voice.disconnect()
        except:
            pass

    @commands.command(pass_context=True, no_pm=True, description='Skip the current playing song')
    @asyncio.coroutine
    def skip(self, ctx):
        if not in_list(ctx.message.author.roles, lambda x: x.name in ['Master Control', 'Nixie', 'Slackerzz', 'Patreons']):
            yield from self.bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
            return False
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            yield from self.bot.say('Not playing any music right now...')
            return
        yield from self.bot.say('Skipping song...')
        state.skip()

    @commands.command(pass_context=True, no_pm=True, description='Display the current playing song')
    @asyncio.coroutine
    def playing(self, ctx):
        if not in_list(ctx.message.author.roles, lambda x: x.name in ['Master Control', 'Nixie', 'Slackerzz', 'Patreons']):
            yield from self.bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
            return False
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            yield from self.bot.say('Not playing anything.')
        else:
            yield from self.bot.say('Now playing```{}'.format(state.current) + '```')

    @commands.command(pass_context=True, description='Display the music queue')
    @asyncio.coroutine
    def queue(self, ctx):
        if not in_list(ctx.message.author.roles, lambda x: x.name in ['Master Control', 'Nixie', 'Slackerzz', 'Patreons']):
            yield from self.bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
            return False
        state = self.get_voice_state(ctx.message.server)
        songs = state.queue
        if len(songs) == 0 and not state.current:
            yield from self.bot.say("Nothing is in the queue!")
        else:
            current_song = "Now playing: {}".format(state.current)
            if len(songs) != 0:
                songs = "{}\n\n{}".format(current_song, "\n".join([str(song) for song in songs]))
            else:
                songs = "{}".format(current_song)
            yield from self.bot.say('Queue :```' + songs + '```')

def setup(bot):
    bot.add_cog(Music(bot))

