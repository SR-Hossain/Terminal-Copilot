import json
import os
import textwrap

import google.generativeai as genai
from IPython.display import Markdown


class Gemini:
    def __init__(self):
        self.base_directory = str(os.path.expanduser('~/terminal-copilot/'))
        with open(f'{self.base_directory}config', 'r') as json_file:
            config = json.load(json_file)
            self.GOOGLE_API_KEY = config['AI_API_KEY']
            self.MODEL = config['MODEL']
            self.DISTRO = config['DISTRO']
        genai.configure(api_key=self.GOOGLE_API_KEY)
        self.geminiModel = genai.GenerativeModel(self.MODEL)
        self.prompt = [
            f"""
I am using you in terminal mode in {self.DISTRO}.
Give me only commands.
give me commands in json format, for example:
[
    {{"command": "sudo apt update\\nsudo apt upgrade -y"}},
    {{"command": "ls -l"}},
    {{"command": "echo 'Hello World' > hello.txt"}},
    {{"command": "cat hello.txt"}}
]
I will extract your commands and select only one command, that will run in bash terminal.
Don't provide me with markdown format. 
"""
        ]
        self.previous_history = []
        self.load_history()

    def load_history(self):
        with open(f'{self.base_directory}history.json', 'r') as json_file:
            self.previous_history = json.load(json_file)

    def to_markdown(self, text):
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

    def generateResponse(self):
        new_history = {
            "prompt": input('prompt: ')
        }
        new_history['response'] = self.geminiModel.generate_content(
            self.prompt + [f"Previous history: {self.previous_history}"] + [f"new prompt that you have to response to: {new_history}"]).text
        self.previous_history.append(new_history)
        self.save_history(new_history)
        print(new_history['response'])
        index = 1
        response = json.loads(new_history['response'])
        for command in response:
            print(f"Command {index}: {command['command']}")
            index += 1
        try:
            with open(f'{self.base_directory}final_command.txt', 'w') as file:
                file.write(response[int(input('Select one: '))-1]['command'])
        except:
            with open(f'{self.base_directory}final_command.txt', 'w') as file:
                file.write(response['command'])
        return new_history['response']

    def generateChat(self):
        self.prompt = []
        while True:
            print(self.generateResponse())

    def save_history(self, new_history):
        with open(f'{self.base_directory}history.json', 'w') as json_file:
            json.dump(self.previous_history[max(0, len(self.previous_history)-100):], json_file)

    def showModels(self):
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models.append(m.name)
        return models



