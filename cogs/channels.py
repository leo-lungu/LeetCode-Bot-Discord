import discord
from discord.ext import commands

from bot_globals import logger
from embeds.channels_embeds import (
    channel_receiving_all_notification_types_embed,
    channel_receiving_no_notification_types_embed,
    set_channels_instructions_embed)
from models.server_model import Server
from utils.middleware import admins_only, ensure_server_document
from utils.views import ChannelsSelectView


class Channels(commands.GroupCog, name="notifychannel"):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.app_commands.command(name="enable", description="Admins only: Set which channels should receive notifications")
    @ensure_server_document
    @admins_only
    async def enable(self, interaction: discord.Interaction, channel: discord.TextChannel | None = None) -> None:
        logger.info("file: cogs/channels.py ~ notify enable ~ run")

        if not interaction.guild or not isinstance(interaction.channel, discord.TextChannel) or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(contents="An error has occured! Please try again.", ephemeral=True)
            return

        if channel is None:
            channel = interaction.channel

        logger.info(
            "file: cogs/channels.py ~ notify enable ~ channel id: %s", channel.id)

        server_id = interaction.guild.id

        # TODO: add projection
        server = await Server.find_one(Server.id == server_id)

        if all(channel.id in notification_type[1] for notification_type in server.channels):
            embed = channel_receiving_all_notification_types_embed()
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        available_types = [
            notification_type[0] for notification_type in server.channels if channel.id not in notification_type[1]]

        embed = set_channels_instructions_embed(channel.name, adding=True)
        await interaction.response.send_message(embed=embed, view=ChannelsSelectView(server_id, channel.id, channel.name, available_types, adding=True), ephemeral=True)

    @discord.app_commands.command(name="disable", description="Admins only: Stop channel from receiving selected notification types")
    @ensure_server_document
    @admins_only
    async def disable(self, interaction: discord.Interaction, channel: discord.TextChannel | None = None) -> None:
        logger.info("file: cogs/channels.py ~ notify disable ~ run")

        if not interaction.guild or not isinstance(interaction.channel, discord.TextChannel) or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(contents="An error has occured! Please try again.", ephemeral=True)
            return

        if channel is None:
            channel = interaction.channel

        logger.info(
            "file: cogs/channels.py ~ notify disable ~ channel id: %s", channel.id)

        server_id = interaction.guild.id

        # TODO: add projection
        server = await Server.find_one(Server.id == server_id)

        if all(channel.id not in notification_type[1] for notification_type in server.channels):
            embed = channel_receiving_no_notification_types_embed()
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        available_types = [
            notification_type[0] for notification_type in server.channels if channel.id in notification_type[1]]

        embed = set_channels_instructions_embed(channel.name, adding=False)
        await interaction.response.send_message(embed=embed, view=ChannelsSelectView(server_id, channel.id, channel.name, available_types, adding=False), ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(Channels(client))
