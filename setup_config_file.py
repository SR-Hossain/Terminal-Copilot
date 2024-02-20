import json
import os

base_directory = str(os.path.expanduser('~/terminal-copilot/'))
with open(f'{base_directory}config', 'r') as json_file:
    config = json.load(json_file)
    print("just type enter without any input to keep the default values.")
    for key, value in config.items():
        new_value = input(f'{key}(default: {value}): ')
        if new_value:
            config[key] = new_value
            print(f'{key} updated to {new_value}')
with open(f'{base_directory}config', 'w') as json_file:
    json.dump(config, json_file, indent=4)

