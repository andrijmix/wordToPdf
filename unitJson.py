import json
import os

#extract the array from the json file
def extract_array_from_json(json_file_path, array_name):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    if array_name in data:
        return data[array_name]
    else:
        raise KeyError(f"Array '{array_name}' not found in the JSON file.")






if __name__ == "__main__":
    json_folder = "jsons"
    arrays=[]
    numberArrays = 0
    # return the number of file in the folder
    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
    print(f"Number of JSON files in folder: {len(json_files)}")
    #in the loop extract the array from the json file
    for i in range(1, len(json_files) + 1):
        json_file_path = f"{json_folder}/response_page_{i}.json"
        try:
            array_data = extract_array_from_json(json_file_path, "data")
            #unit the array
            arrays.extend(array_data)
            numberArrays+= len(array_data)
            print(f"Size of arrays : {len(arrays)}")
        except KeyError as e:
            print(e)
        except FileNotFoundError:
            print(f"File {json_file_path} not found.")
    #save the arrays as a     json file
    #the name of array is data
    with open('arrays.json', 'w') as outfile:
        json.dump({"data": arrays}, outfile, indent=4)

    print(f"numberArrays {numberArrays}")
    print(f"Total number of arrays: {len(arrays)}")
