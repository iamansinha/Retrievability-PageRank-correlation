import sys
import json

# Check if the user has provided a file path argument
if len(sys.argv) < 2:
    print("Usage: python program.py <file_path>")
    sys.exit(1)

# Get the file path argument
file_path = sys.argv[1]

# Wouldn't work for JSON file larger than available RAM space
# # Open the JSON file and load its contents
# with open(file_path, 'r') as f:
#     data = json.load(f)

# Define a generator function to read the file in chunks
def read_json_file(file_path, chunk_size=1024):
    with open(file_path, 'r') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Define a generator function to parse each chunk as JSON
def parse_json_chunks(json_chunks):
    decoder = json.JSONDecoder()
    buffer = ''
    for chunk in json_chunks:
        buffer += chunk
        while True:
            try:
                result, index = decoder.raw_decode(buffer)
                yield result
                buffer = buffer[index:].lstrip()
            except ValueError:
                # Not enough data to decode a JSON object, keep reading
                break


# Define a recursive function to extract the field structure
def get_field_structure(data):
    if isinstance(data, dict):
        return {k: get_field_structure(v) for k, v in data.items()}
    elif isinstance(data, list):
        if len(data) > 0:
            l = [get_field_structure(item) for item in data]
            if all(isinstance(element, str) for element in l):
                return 'list_of_strings'
            return l
        else:
            return []
    else:
        return type(data).__name__

field_structure = []
count = 0
# Process each parsed JSON object
for parsed_object in parse_json_chunks(read_json_file(file_path)):
    count += 1
    if count == 1 or count == 2: # skip first article, because it's result was longer and second's was shorter
        continue
    fields = get_field_structure(parsed_object)
    if fields in field_structure:
        break
    else:
        print(f'Parsed object passed to get_field_structure.')
        field_structure.append(fields)

# Print the resulting field structure
print('\nStructure of the JSON file:\n')
print(json.dumps(field_structure, indent=2))
