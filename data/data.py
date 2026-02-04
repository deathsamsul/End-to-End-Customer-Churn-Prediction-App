import json,os



db_file = "customer.json"


#load data
def data_load():
    if not os.path.exists(db_file):
        return[]
    with open(db_file,'r')as f:
        return json.load(f)
    
# save data
def save_data(data):
    with open(db_file, "w") as f:
        json.dump(data, f, indent=4)
