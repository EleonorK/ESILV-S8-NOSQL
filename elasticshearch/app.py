import json
from datetime import datetime

input_file = "companies2.json"
output_file = "output.json"

def convert_to_iso8601_fromstr(date_str):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, '%a %b %d %H:%M:%S %Z %Y')
    # Convert the datetime object to a string in ISO 8601 format
    return date_obj.isoformat()

def convert_to_iso8601_fromobj(date_obj):
    # Extract the date and time string from the input string
    date_time_str = date_obj["$date"].split(".")[0] + "Z"
    # Convert the date and time string to a datetime object
    date_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%SZ')
    return date_obj.isoformat()

with open(input_file, "r") as f_input, open(output_file, "w") as f_output:
    for i, line in enumerate(f_input):
        # Parse the JSON object
        obj = json.loads(line)
        # Convert the date format
        # It may be an object or a string
        if isinstance(obj["created_at"], str):
            obj["created_at"] = convert_to_iso8601_fromstr(obj["created_at"])
        else:
            obj["created_at"] = convert_to_iso8601_fromobj(obj["created_at"])
        if isinstance(obj["updated_at"], str):
            obj["updated_at"] = convert_to_iso8601_fromstr(obj["updated_at"])
        else:
            obj["updated_at"] = convert_to_iso8601_fromobj(obj["updated_at"])
        # Remove the id from the document
        _id = obj.pop("_id", None) 
        # Write the index line
        f_output.write('{"index":{"_index":"companies","_id":%d}}\n' % i)
        # Write the data line
        f_output.write(json.dumps(obj) + "\n")
