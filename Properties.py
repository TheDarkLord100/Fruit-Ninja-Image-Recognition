import json

props = {}
DiscardedPoints = {}
Video = None

def loadProperties(): 
    with open("props.json", 'r') as f:
        global props
        props = json.load(f)
        
    
