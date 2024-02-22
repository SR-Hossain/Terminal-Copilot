import pyperclip
import os

base_directory = str(os.path.expanduser('~/terminal-copilot/'))

with open(f"{base_directory}final_command.txt", "r") as file:
    file_contents = file.read()

pyperclip.copy(file_contents)
