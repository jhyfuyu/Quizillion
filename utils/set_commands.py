from aiogram import Bot, types
from myconfig.config import DEFAULT_COMMANDS

def set_default_commands(bot: Bot):
    for command in DEFAULT_COMMANDS:
        # bot.register_command(command[0], command[1])
        pass
    