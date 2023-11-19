fields = [
            'AssetCode',
            'Date',
            'AcquisitionType',
            'DeviceType',
            'AcquisitionLocation',
            'Manufacturer',
            'SN',
            'PurchasePrice(+Tx)',
            'AcquisitionValue(CAD)',
            'Tax',
            'UserID',
            'UserName',
            'CurrentLocation',
            'Com1',
            'Com2',
            'Status',
            'Updated'
    ]

skip_fields = [
            'AssetCode',
            'PurchasePrice(+Tx)',
            'UserName',
            'Updated'
        ]

# Required fields
required_input = [
            'Date',
            'AcquisitionType',
            'DeviceType',
            'AcquisitionLocation',
            'Manufacturer',
            'SN',
            'UserID',
            'AcquisitionValue(CAD)',
            'Tax',
            'CurrentLocation'
]

# Available options
# Acquisition Type
a_choices = {'P': 'Purchase', 'L': 'Lease'}

# Device Type
d_choices = {
    'D': 'Desktop', 'N': 'Laptop',
    'M': 'Monitor', 'S': 'Smartphone',
    'P': 'Printer', 'W': 'NW Device',
    'T': 'Tablet', 'R': 'Server',
    'C': 'Camera', 'E': 'ETCs'
    }

# AcquisitionLocation
a_loca = {
    'M': 'Montréal',
    'B': 'Bécancour',
    'T': 'Trois-Rivières'
    }

# CurrentLocation
c_loca = {
    'M': 'Montréal',
    'B': 'Bécancour',
    'T': 'Trois-Rivières'
    }

# Manufacturer  
m_choices = {
        'D': 'Dell', 'L': 'Lenovo', 'S': 'Samsung',
        'G': 'LG', 'U': 'ASUS', 'F': 'FortiGate',
        'Q': 'Qnap', 'A': 'APPLE', 'T': 'TP-Link',
        'C': 'Canon', 'H': 'HP', 'E': 'ETCs'
    }

# option fields
option_dict = {
            'AcquisitionType': a_choices,
            'DeviceType': d_choices,
            'AcquisitionLocation': a_loca,
            'Manufacturer': m_choices,
            'CurrentLocation': c_loca
            }

# Declaration for initial setup
valuedict = {}
for i in fields:
    valuedict[i] = ''

inputkeys = []

option_dict_list = [
                    a_choices, d_choices,
                    a_loca, m_choices
                    ]

option_list = [
                'AcquisitionType',
                'DeviceType',
                'AcquisitionLocation',
                'Manufacturer'
            ]
