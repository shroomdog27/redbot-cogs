# Modified MIT License (MIT)
#
# Copyright (c) 2020 shroomdog27
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, and sublicense
# the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import discord
import datetime
from redbot.core import commands as Commands
from redbot.core import Config
from redbot.core.utils.chat_formatting import humanize_list, inline, escape


class VCLoggerCog(Commands.Cog):
    """My custom cog"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=777761593677316458)

    async def get_channel(self, guild: discord.Guild) -> discord.TextChannel:
        txt_id = await self.config.guild(guild).channel()
        text_channel = guild.get_channel(txt_id)
        return text_channel

    async def set_channel(self, guild: discord.Guild, text_channel_id: int):
        await self.config.guild(guild).channel.set(text_channel_id)

    @Commands.group()
    @Commands.guild_only()
    async def vclog(self, ctx):
        """Root command for Voice Chat Logger Commands"""
        pass

    @vclog.command(name="channel")
    async def vclog_channel(self, ctx, txt_channel: discord.TextChannel):
        """Sets the text channel to send messages to"""
        vc_id = txt_channel.id
        await self.set_channel(ctx.guild, vc_id)
        await ctx.tick()
        return

    @Commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before_state: discord.VoiceState,
        after_state: discord.VoiceState,
    ) -> None:
        before = before_state.channel
        after = after_state.channel
        channel_to_send = None
        msg = "{emoji} `{time}`".format(emoji=":microphone:", time=datetime.datetime.now().strftime("%H:%M:%S"))
        if before is None:
            channel_msg = str(member) + " has joined " + inline(after.name)
            msg += channel_msg + "\n"
            channel_to_send = await self.get_channel(after.guild)
        elif after is None:
            channel_msg = str(member) + " has left " + inline(before.name)
            msg += channel_msg + "\n"
            channel_to_send = await self.get_channel(before.guild)
        elif before == after:
            return
        else:
            channel_msg = str(member) + " has moved from " + inline(before.name) + " to " + inline(after.name)
            channel_to_send = await self.get_channel(after.guild)
            msg += channel_msg
        if channel_to_send is None:
            return
        await channel_to_send.send(msg)
        return
