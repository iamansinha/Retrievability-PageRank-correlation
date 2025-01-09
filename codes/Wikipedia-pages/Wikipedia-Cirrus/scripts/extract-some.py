import json
import gzip

input_filename = './enwiki-20230220-cirrussearch-content.json.gz'
output_filename = './10lines.json'

with gzip.open(input_filename, 'rt') as input_file, open(output_filename, 'w') as output_file:
    # Loop over the first 10 lines
    for i in range(10):
        # Read one line from the input file
        line = input_file.readline()
        # Parse the JSON data in the line
        data = json.loads(line)
        # Write the data to the output file
        json.dump(data, output_file)
        output_file.write('\n')
