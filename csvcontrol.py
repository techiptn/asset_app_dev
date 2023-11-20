import csv
from datafield import *
from datahandle import *

def data_read(datalist):
    with open(datalist, 'r') as a_list:
        reader = csv.DictReader(a_list)
        data = list(reader)
        a_list.close()
    return data


def data_update(datalist, update_dict):
    savebkfile(datalist)
    dl = data_read(datalist)
    fieldnames = list(dl[0].keys())

    with open(datalist, 'a') as a_list:
        writer = csv.DictWriter(a_list, fieldnames=fieldnames)
        # writer.writeheader()
        writer.writerow(update_dict)
        a_list.close()


def addasset(userdata):
    for i in fields:
        if i in skip_fields:
            pass
        elif i in required_input:
            if i in option_dict:
                if i in [x for x in option_dict.keys()]:
                    a_list = [
                        f'[{x}]{option_dict[i][x]}'
                        for x in option_dict[i].keys()
                        ]
                    v1 = input(f'{i}:{a_list}?: ').upper()
                    while v1 not in [y for y in option_dict[i].keys()]:
                        v1 = input(f'{i}:{a_list}?: ').upper()
                    v2 = option_dict[i][v1]
                    confirm = input(f'Is the Value "{v2}"? [Y][N]')
                    while confirm.lower() != 'y':
                        v1 = input(f'{i}:{a_list}?: ').upper()
                        while v1 not in [y for y in option_dict[i].keys()]:
                            v1 = input(f'{i}:{a_list}?: ').upper()
                        v2 = option_dict[i][v1]
                        confirm = input(f'Is the Value "{v2}"? [Y][N]')
                    inputkeys.append(v1)
                    valuedict[i] = v2
                else:
                    v4 = input(f'{i}: ')
                    confirm = input(f'Is {i} "{v4}"? [Y][N]?')
                    while confirm.lower() != 'y':
                        v4 = input(f'{i}: ')
                        confirm = input(f'Is {i} "{v4}"? [Y][N]?')
                    valuedict[i] = v4

            elif i in ['AcquisitionValue(CAD)','Tax']:
                v5 = input(f'{i}?:')
                while not validate_float(v5):
                    v5 = input(f'No valid input, number only, {i}?:')
                confirm = input(f'${v5}? [Y][N]?')
                while confirm.lower() != 'y':
                    v5 = input(f'{i}?:')
                    while not validate_float(v5):
                        v5 = input(f'No valid input, number only, {i}?:')
                    confirm = input(f'${v5}? [Y][N]?')
                valuedict[i] = v5
            
            elif i == 'Date':
                v3 = input(f'{i}(YYYY-MM-DD):')
                while not (validate_date(v3) and len(v3) == 10):
                    v3 = input(f'No valid input, {i}(YYYY-MM-DD)?:')
                confirm = input(f'Is Date "{v3}"? [Y][N]?')
                while confirm.lower() != 'y':
                    v3 = input(f'{i}(YYYY-MM-DD):')
                    while not (validate_date(v3) and len(v3) == 10):
                        v3 = input(f'No valid input, {i}(YYYY-MM-DD)?:')
                    confirm = input(f'Is Date "{v3}"? [Y][N]?')
                valuedict[i] = v3

            elif i == 'UserID':
                v6 = input(f'{i}?:')
                while not validate_userid(v6, userdata):
                    v6 = input(f'UserID does not exist, {i}?:')
                name = username(v6, userdata)
                confirm = input(f'{v6},{name}? [Y][N]?')
                while confirm.lower() != 'y':
                    v6 = input(f'{i}?:')
                    while not validate_userid(v6, userdata):
                        v6 = input(f'UserID does not exist,{i}?:')
                    name = username(v6, userdata)
                    confirm = input(f'{v6},{name}? [Y][N]?')
                valuedict[i] = v6
                valuedict['UserName'] = name

            else:
                v4 = input(f'{i}?: ')
                while v4 == '':
                    v4 = input(f'This cannot be empty, {i}?: ')
                confirm = input(f'Is {i} "{v4}"? [Y][N]?')
                while confirm.lower() != 'y':
                    v4 = input(f'{i}?: ')
                    while v4 == '':
                        v4 = input(f'This cannot be empty, {i}?: ')
                    confirm = input(f'Is {i} "{v4}"? [Y][N]?')
                valuedict[i] = v4
        else:
            v4 = input(f'{i}?: ')
            confirm = input(f'Is {i} "{v4}"? [Y][N]?')
            while confirm.lower() != 'y':
                v4 = input(f'{i}?: ')
                confirm = input(f'Is {i} "{v4}"? [Y][N]?')
            valuedict[i] = v4


# Input missing fields
def code_gen(rawdata):
    value = ''
    for i in range(len(option_list)):
        value = value + get_key(
                option_dict_list[i], valuedict[option_list[i]]
                )
    strdate = valuedict['Date'].strftime("%Y-%m-%d")
    yy = strdate[2:4]
    mm = int(strdate[5:7])
    m_hex = [x for x in hex(mm)][-1].upper()
    tempsum = value+yy+m_hex
    nxnum = nextcode(tempsum, rawdata)
    return tempsum + str(nxnum)


def data_fillup(assetdata, userdata):
    valuedict['AssetCode'] = code_gen(assetdata)
    valuedict['AcquisitionValue(CAD)'] = round(float(valuedict['AcquisitionValue(CAD)']), 2)
    valuedict['Tax'] = round(float(valuedict['Tax']), 2)
    valuedict['PurchasePrice(+Tx)'] = (
        valuedict['AcquisitionValue(CAD)'] + valuedict['Tax']
        )
    valuedict['PurchasePrice(+Tx)'] = round(float(valuedict['PurchasePrice(+Tx)']), 2)
    valuedict['Updated'] = datetime.datetime.now()
    valuedict['UserName'] = username(valuedict['UserID'], userdata)


def data_edit(userdata):
    valuedict['Updated'] = datetime.datetime.now()
    valuedict['UserName'] = username(valuedict['UserID'], userdata)



