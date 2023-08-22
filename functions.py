from __future__ import annotations


# seems completed..
class Function:
    def __init__(self, name, commands: list = []):
        self.commands = commands

    def addCommand(self, commands: list):
        self.commands.extend(commands)

    def addCommand(self, command: str):
        self.commands.append(command)
