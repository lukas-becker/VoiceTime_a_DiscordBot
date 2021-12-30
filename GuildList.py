from Guild import Guild


class GuildList:

    def __init__(self):
        self.guilds = []

    def add(self, new_guild):
        for guild in self.guilds:
            if new_guild.id == guild.id:
                return

        self.guilds.append(new_guild)

    def remove(self, guild_to_remove):
        for guild in self.guilds:
            if guild_to_remove.id == guild.g_id:
                self.guilds.remove(guild)
                return

    def check_guild(self, guild_id):
        for guild in self.guilds:
            if guild.id == guild_id:
                return True
        return False

    def get_by_id(self, guild_id):
        for guild in self.guilds:
            if guild.id == guild_id:
                return guild

    def to_json(self):
        tmp_guild_list = []
        for guild in self.guilds:
            tmp_guild_list.append(guild.to_json())
        return tmp_guild_list

    @staticmethod
    def from_json(json):
        tmp_guild_list = GuildList()
        for guild in json:
            tmp_guild_list.add(Guild.from_json(guild))

        return tmp_guild_list
