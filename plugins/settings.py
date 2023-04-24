from typing import Any
import novus
from novus.ext import client, database as db


class Settings(client.Plugin):

    @staticmethod
    async def set_guild_item(column: str, guild_id: int, value: Any) -> None:
        """
        Set an item in the database.

        Parameters
        ----------
        column : str
            The name of the column that you want to set the given value to.
        guild_id : int
            The ID of the guild that you want to set the data for.
        value : Any
            The value that you want to set.
        """

        async with db.Database.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO
                    guild_settings
                    (
                        guild_id,
                        {0}
                    )
                VALUES
                    (
                        $1,
                        $2
                    )
                ON CONFLICT (guild_id)
                DO UPDATE
                SET
                    {0} = excluded.{0}
                """.format(column),
                guild_id,
                value,
            )

    @client.command(
        name="settings channel report",
        options=[
            novus.ApplicationCommandOption(
                name="channel",
                type=novus.ApplicationOptionType.channel,
                description="The channel where you want reports to funnel to.",
                channel_types=[novus.ChannelType.guild_text],
            ),
        ],
        default_member_permissions=novus.Permissions(manage_guild=True),
    )
    async def report_channel_settings(
            self,
            interaction: novus.types.CommandI,
            channel: novus.GuildTextChannel) -> None:
        """
        Set the report channel.
        """

        await interaction.defer(ephemeral=True)
        assert interaction.guild
        await self.set_guild_item(
            "report_channel_id",
            interaction.guild.id,
            channel.id,
        )
        await interaction.send(
            f"The report channel has been set to **{channel.mention}**.",
            ephemeral=True,
        )

    @client.command(
        name="settings channel message_logs",
        options=[
            novus.ApplicationCommandOption(
                name="channel",
                type=novus.ApplicationOptionType.channel,
                description="The channel where you want message logs to funnel to.",
                channel_types=[novus.ChannelType.guild_text],
            ),
        ],
        default_member_permissions=novus.Permissions(manage_guild=True),
    )
    async def message_logs_channel_settings(
            self,
            interaction: novus.types.CommandI,
            channel: novus.GuildTextChannel) -> None:
        """
        Set the message logs channel.
        """

        await interaction.defer(ephemeral=True)
        assert interaction.guild
        await self.set_guild_item(
            "message_channel_id",
            interaction.guild.id,
            channel.id,
        )
        await interaction.send(
            f"The message logs channel has been set to **{channel.mention}**.",
            ephemeral=True,
        )

    @client.command(
        name="settings role staff",
        options=[
            novus.ApplicationCommandOption(
                name="role",
                type=novus.ApplicationOptionType.role,
                description="The role that all of staff members have.",
            ),
        ],
        default_member_permissions=novus.Permissions(manage_guild=True),
    )
    async def staff_role_settings(
            self,
            interaction: novus.types.CommandI,
            role: novus.Role) -> None:
        """
        Set the staff role.
        """

        await interaction.defer(ephemeral=True)
        assert interaction.guild
        await self.set_guild_item(
            "staff_role_id",
            interaction.guild.id,
            role.id,
        )
        await interaction.send(
            f"The report channel has been set to **{role.mention}**.",
            allowed_mentions=novus.AllowedMentions.none(),
            ephemeral=True,
        )
