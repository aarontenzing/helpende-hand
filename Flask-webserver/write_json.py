import json

def write(data, filename):
    
    with open(filename, 'r') as f:
        try:
            file_data = json.load(f) # file content to python list
            print(file_data)

        except json.decoder.JSONDecodeError:
            file_data = []
            print("file empty")
    
    file_data.append(data) # list van dicts 

    with open(filename, 'w') as f:
        json.dump(file_data, f, indent=4) # dict to array (json)
