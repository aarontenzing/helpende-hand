import json

<<<<<<< HEAD
def write(data):
    with open('data_list.json', 'r+') as f:
        file_data = json.load(f)    
        print(file_data)    
        file_data["log"].append(json.load(data))
        json.dump(file_data, f) # converts python dict to json
=======
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
>>>>>>> f3fdd4032ebd9f3e692863af78a5bb44b6c43c0d
