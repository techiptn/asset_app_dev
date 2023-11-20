import datetime
import pandas as pd

def validate_date(date_input):
    # using try-except blocks for handling the exceptions
    try:
        # formatting the date using strptime() function
        dateObject = datetime.datetime.strptime(date_input, '%Y-%m-%d')
        # print(dateObject)
        return True
    # If the date validation goes wrong
    except ValueError:
        # printing the appropriate text if ValueError occurs
        # print("Incorrect data format, should be YYYY-MM-DD")
        return False

def validate_float(value):
    # using try-except blocks for handling the exceptions
    try:
        float(value)
        return True
    # If the value validation goes wrong
    except ValueError:
        return False

def validate_userid(value, userdata):
    # using try-except blocks for handling the exceptions
    try:
        username(value, userdata)
        return True
    # If the data validation goes wrong
    except:
        return False

def val_datapath(datapath):
    try:
        with open(datapath, 'r') as t:
            t.close()
        return True
    except FileNotFoundError:
        return False

# function to return key for any value
def get_key(d_name, val):
    for key, value in d_name.items():
        if val == value:
            return key
    return "key doesn't exist"


# count Itemcode
def nextcode(digit7, data_path):
    df = pd.read_csv(data_path)
    filt = (df['AssetCode'].str[0:7] == digit7)
    nx = df['AssetCode'][filt].count() + 1
    strnx = ("{0:0=3d}".format(nx))
    return strnx

# UserID and Name
def username(userid, userinfo_csv):
    df = pd.read_csv(userinfo_csv)
    filt = (df['UserID'] == userid)
    name = df.loc[filt, 'UserName'].to_list()[0]
    return name

# UserID and Name
def savebkfile(targetcsv):
    tstamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(targetcsv)
    df.to_csv(targetcsv+tstamp)

    

def code_data_dic(code, assetdata):
    df= pd.read_csv(assetdata)
    filt = (df['AssetCode'] == code )
    ab = df.loc[filt].to_dict('records')[0]
    values = [x for x in ab.values()]
    date_str = ab['Date']
    date_format = '%Y-%m-%d'
    date_obj = datetime.datetime.strptime(date_str, date_format)
    values[1] = date_obj
    return values
    

# Display only latest updated info
# def latestonly(targetcsv):
#     df = pd.read_csv(targetcsv)
#     filt = (df['AssetCode', 'Updated'] == )
#     return name
