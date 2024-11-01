import json
import btree
import io

# Load the JSON file

with io.open('schedule_0.json', 'r') as file:
    data = json.load(file)

# Create a B-tree
bt = btree.BTree()

# Insert items into the B-tree
for event in data['scheduledEvent']:
    key = (event['hour'], event['minute'], event['second'])
    bt[key] = event

# Function to get an item based on hour, minute, and second
def get_event(hour, minute, second):
    key = (hour, minute, second)
    return bt.get(key, None)

# Example usage
event = get_event(-1, 13, 15)
print(event)