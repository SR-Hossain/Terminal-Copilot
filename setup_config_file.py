import json

with open('config', 'r') as json_file:
    config = json.load(json_file)
    print("just type enter without any input to keep the default values.")
    for key, value in config.items():
        new_value = input(f'{key}(default: {value}): ')
        if new_value:
            config[key] = new_value
with open('config', 'w') as json_file:
    json.dump(config, json_file, indent=4)

