import datetime, os, shutil
import pandas as pd
from module import *
from glob import glob
from io import BytesIO
from zipfile import ZipFile

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
def nextcode(digit7, assetdata):
    df = pd.read_csv(assetdata)
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

#edit page default autofill
def code_data_dic(code, assetdata):
    df = pd.read_csv(assetdata, index_col=0)
    filt2 = (df.index == code)
    ab = df.loc[filt2].to_dict('records')[0]
    values = [x for x in ab.values()]
    date_str = ab['Date'][:10]
    date_format = '%Y-%m-%d'
    date_obj = datetime.datetime.strptime(date_str, date_format)
    values[1] = date_obj.date()
    return values

#Delete values
def data_delete(code, data, ack):
    df = pd.read_csv(data, index_col=0)
    df3 = df.drop(code)
    newsavebkfile(data, ack)
    # if ack == 'asset':
    #     savebkfile(data)
    # elif ack == 'user':
    #     user_bkfile(data)
    df3.to_csv(data)


#Add user info
def adduser(id, name, dep, emno, userdata):
    df = pd.read_csv(userdata, index_col=0)
    new = {'UserID':[id],
        'UserName':[name],
        'Dep.':[dep],
        'EmNo':[emno]
        }
    new['email'] = [new['UserID'][0]+'@ultiumcam.net']
    df2 = pd.DataFrame.from_dict(new)
    df3 = pd.concat([df, df2], ignore_index=True)
    newsavebkfile(userdata, 'user')
    # user_bkfile(userdata)
    df3.to_csv(userdata)


#edit user default autofill
def code_user(code, userdata):
    df = pd.read_csv(userdata, index_col=0)
    filt2 = (df.index == code)
    ab = df.loc[filt2].to_dict('records')[0]
    values = [x for x in ab.values()]
    return values


#Trim and arrage index
def indextrim(assetdata):
    df = pd.read_csv(assetdata)
    df2 = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df2.to_csv(assetdata)

# Display only latest updated info
def filter_list(assetdata):
    df = pd.read_csv(assetdata, index_col=0)
    df["Updated"] = df["Updated"].astype('datetime64[ns]')
    maxval = df.groupby('AssetCode')['Updated'].max()
    # filter with multiple conditions
    filt = df['Updated'].isin(maxval) & df['Status'] == 1
    df_latest = df[filt]
    return df_latest

def dp_convert(df):
    df.reset_index(inplace=True)
    dt_col = df.columns.tolist()
    dt_col[0] = ''
    dt_values = df.values.tolist()
    return [dt_col, dt_values]


def label_list(assetdata, selected):
    df = pd.read_csv(assetdata, index_col=0)
    # filter with multiple conditions
    filt = df.index.isin(selected)
    df_label = df[filt]
    l_table = df_label[["AssetCode","Date","SN","UserName"]]
    l2 = l_table.values.tolist()
    return l2


def qr_sv_img(assetdata, list):        
    qrlist2 = [int(x) for x in list]
    qrlist3 = label_list(assetdata, qrlist2)
    imgdict = {}
    for i in qrlist3:
        imgdict[i[0]] = qr_gen(i[0], i[1], i[2], i[3])
    return imgdict


def zipfiles(target):
    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        for file in glob(os.path.join(target, '*.png')):
            zf.write(file, os.path.basename(file))
    stream.seek(0)
    return stream

# delete specific folder's all files (before downloading a label)
def cleanupfolder(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# delete file if bk files over than certain amount
def cleanupfolder2(path, index:int):
    files = os.listdir(path)
    numlen = len(files)
    while numlen >= index:
        del_file = os.path.join(path, files[0])
        os.unlink(del_file)
        files = os.listdir(path)
        numlen = len(files)

# Old version autobackup
'''
def savebkfile(data):
    tstamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(data, index_col=0)
    file_path = 'data/bk/items/as'
    df.to_csv(file_path+tstamp+'.bk')

def user_bkfile(data):
    tstamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(data, index_col=0)
    file_path = 'data/bk/user/ud'
    df.to_csv(file_path+tstamp+'.bk')
'''

#Data auto backup new
def newsavebkfile(data, ack):
    tstamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(data, index_col=0)
    if ack == 'asset':
        file_path = 'data/bk/items/'
        prefix = 'as'
    elif ack == 'user':
        file_path = 'data/bk/user/'
        prefix = 'ud'
    cleanupfolder2(file_path, 100)
    df.to_csv(file_path+prefix+tstamp+'.bk')
