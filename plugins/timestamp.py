from datetime import datetime as dt, timedelta, timezone
import re

import novus
from novus.ext import client
import pytz


class Timestamp(client.Plugin):

    @staticmethod
    def get_timezone_from_string(timezone_name: str) -> timezone | None:
        """
        Try and work out a timezone from an input string, in given priority
        order:

        * See if the string is a TZ name
        * See if the string is in form UTC+XX:YY
        * See if the string is one of our common locations
            * US states
            * European countries
        * See if the string is one of our common acronyms
        * Fallback to null
        """

        # TZ names
        if timezone_name in pytz.common_timezones:
            if timezone_name.casefold() == "GMT":
                pass
            else:
                return pytz.timezone(timezone_name)

        # UTC offsets
        match = re.search(
            r"^utc(?P<direction>[+-])(?P<hour>\d{1,2}(?::(?P<minute>\d{2}))?)$",
            timezone_name,
            re.IGNORECASE,
        )
        if match is not None:
            delta = timedelta(
                hours=int(match.group("hour")),
                minutes=int(match.group("minute") or 0)
            )
            if match.group("direction") == "-":
                delta = -delta
            return timezone(delta)

        # Common countries
        # TODO

        # Common acronyms
        acronyms = {
            "UTC": pytz.utc,

            # Australia
            "ACST": pytz.timezone("Australia/Adelaide"),
            "ACST": pytz.timezone("Australia/Adelaide"),
            "ACT": pytz.timezone("Australia/Adelaide"),
            "AEST": pytz.timezone("Australia/Melbourne"),
            "AEDT": pytz.timezone("Australia/Melbourne"),
            "AET": pytz.timezone("Australia/Melbourne"),
            "AWST": pytz.timezone("Australia/Perth"),
            "AWDT": pytz.timezone("Australia/Perth"),

            # America
            "ET": pytz.timezone("America/New_York"),
            "EST": pytz.timezone("America/New_York"),
            "EDT": pytz.timezone("America/New_York"),
            "CT": pytz.timezone("America/Chicago"),
            "CST": pytz.timezone("America/Chicago"),
            "CDT": pytz.timezone("America/Chicago"),
            "MT": pytz.timezone("America/Phoenix"),
            "MST": pytz.timezone("America/Phoenix"),
            "MDT": pytz.timezone("America/Phoenix"),
            "PT": pytz.timezone("America/Los_Angeles"),
            "PST": pytz.timezone("America/Los_Angeles"),
            "PDT": pytz.timezone("America/Los_Angeles"),

            # Europe
            "GMT": pytz.timezone("Europe/London"),
            "BST": pytz.timezone("Europe/London"),
            "CET": pytz.timezone("Europe/Brussels"),
            "CEST": pytz.timezone("Europe/Brussels"),

            # Africa
            # Asia
        }
        if timezone_name.upper() in acronyms:
            return acronyms[timezone_name.upper()]

        # Fallback
        return None

    @client.command(
        name="timestamp",
        options=[
            novus.ApplicationCommandOption(
                name="year",
                type=novus.ApplicationOptionType.integer,
                description="The year of the given datetime.",
                min_value=2_000,
                max_value=3_000,
                required=False,
            ),
            novus.ApplicationCommandOption(
                name="month",
                type=novus.ApplicationOptionType.integer,
                description="The month of the given datetime.",
                choices=[
                    novus.ApplicationCommandChoice("January", 1),
                    novus.ApplicationCommandChoice("February", 2),
                    novus.ApplicationCommandChoice("March", 3),
                    novus.ApplicationCommandChoice("April", 4),
                    novus.ApplicationCommandChoice("May", 5),
                    novus.ApplicationCommandChoice("June", 6),
                    novus.ApplicationCommandChoice("July", 7),
                    novus.ApplicationCommandChoice("August", 8),
                    novus.ApplicationCommandChoice("September", 9),
                    novus.ApplicationCommandChoice("October", 10),
                    novus.ApplicationCommandChoice("November", 11),
                    novus.ApplicationCommandChoice("December", 12),
                ],
                required=False,
            ),
            novus.ApplicationCommandOption(
                name="day",
                type=novus.ApplicationOptionType.integer,
                description="The day of the given datetime.",
                min_value=1,
                max_value=31,
                required=False,
            ),
            novus.ApplicationCommandOption(
                name="hour",
                type=novus.ApplicationOptionType.integer,
                description="The hour of the given datetime, in 24 hour (military) time.",
                min_value=0,
                max_value=23,
                required=False,
            ),
            novus.ApplicationCommandOption(
                name="minute",
                type=novus.ApplicationOptionType.integer,
                description="The minute of the given datetime.",
                min_value=0,
                max_value=59,
                required=False,
            ),
            novus.ApplicationCommandOption(
                name="timezone",
                type=novus.ApplicationOptionType.string,
                description="The timezone of the provided timestamp",
                required=False,
            ),
        ],
    )
    async def timestamp(
            self,
            ctx: novus.types.CommandI,
            *,
            year: int | None = None,
            month: int | None = None,
            day: int | None = None,
            hour: int | None = None,
            minute: int | None = None,
            timezone: str = "UTC") -> None:
        """
        Sends a well-formatted Discord timestamp message.
        """

        # Get timezone so we can say if the timezone is valid
        if (tz_object := self.get_timezone_from_string(timezone)) is None:
            return await ctx.send(
                f"The timezone `{timezone}` is not valid.",
                ephemeral=True,
            )

        # The default values for each datetime attribute is the current time
        now = dt.utcnow()
        default = lambda a, b: a if a is not None else b
        created_time = dt(
            year=default(year, now.year),
            month=default(month, now.month),
            day=default(day, now.day),
            hour=default(hour, now.hour),
            minute=(
                minute if minute is not None
                else 0 if hour is not None
                else now.minute
            ),
            second=0,
            microsecond=0,
            tzinfo=tz_object,
        )
        timestamp: str = format(created_time.timestamp(), ".0f")
        await ctx.send(f"<t:{timestamp}> (`<t:{timestamp}>`)")
