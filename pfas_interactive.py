import pandas as pd
import numpy as np

groundWater = pd.read_excel('concatenated_grd_wtr.xlsx')

surfaceWater = pd.read_excel('surface_wtr.xlsx')

groundWater = groundWater[['Ionic PFAS','Concentration with unit','year','Location']]

surfaceWater = surfaceWater[['Ionic PFAS','Concentration with unit','year','Location']]

drinkingWater = pd.read_excel('Drinking_Water.xlsx')

drinkingWater = drinkingWater[['Ionic PFAS','Concentration with unit','year','Location']]

drinkingWater

drinkingWater['Data Available'] = 1

def clean_measurements(value):
    if '<MRL' in value.lower(): # convert value to lowercase to handle variations like 'ND', 'Nd', etc.
        return 0
    elif 'nd' in value.lower(): # convert value to lowercase to handle variations like 'ND', 'Nd', etc.
        return 0
    elif '-' in value.lower(): # convert value to lowercase to handle variations like 'ND', 'Nd', etc.
        return (float(value.split('-')[0]) + float((value.split('-')[1].split(' '))[0]))/2
    elif 'ppb' in value.lower(): # convert value to lowercase to handle variations like 'PPB', 'Ppb', etc.
        return float(value.lower().replace(' ppb', '').replace(',', '')) * 1000 # convert value to lowercase to handle variations like 'PPB', 'Ppb', etc.
    elif 'ppt' in value.lower(): # convert value to lowercase to handle variations like 'PPT', 'Ppt', etc.
        return float(value.lower().replace(' ppt', '').replace(',', '')) # convert value to lowercase to handle variations like 'PPT', 'Ppt', etc.
    else:
        return value

drinkingWater['Concentration with unit'] = drinkingWater['Concentration with unit'].apply(lambda x: clean_measurements(x))

drinkingWater['Concentration with unit'] = drinkingWater['Concentration with unit'].apply(lambda x: 0 if x=='< MRL' else x)

drinkingWater['year'] = drinkingWater['year'].apply(lambda x: str(x).split('-'))

def yearsBetween(x):

  years = x.copy()

  if (int(x[-1:][0]) - int(x[0])) == 1:

    return x

  else:

    for i in range(int(x[0]),int(x[-1:][0])-1):

      years.append(i+1)

  return [int(year) for year in years]

drinkingWater['year'] = drinkingWater['year'].apply(lambda x: x if len(x) == 1 else yearsBetween(x))

drinkingWater = drinkingWater.explode('year')

drinkingWater.dropna(inplace= True)

drinkingWater['Location'] = drinkingWater['Location'].astype(int)

drinkingWater['Type'] = 'Drinking Water'

drinkingWater['year'] = drinkingWater['year'].astype(int)

drinkingWater

drinkingWater.dtypes

"""#Prepare Ground Water DF"""

groundWater['Concentration with unit'].replace(0, np.nan, inplace=True)

groundWater

def ppbORppt(x):
    if x == 0:  # Handle case where x is 0
        return '0 ppt'
    if isinstance(x, str):
        if 'ppb' in x:
            return f"{float(x.replace('ppb', '')) * 1000} ppt"
        elif 'ppt' in x:
            return f"{float(x.replace('ppt', ''))} ppt"
    return np.nan  # Handle any other cases, if needed

# Apply lambda function to convert units
groundWater['Concentration with unit'] = groundWater['Concentration with unit'].apply(lambda x: ppbORppt(x))

groundWater

groundWater.dtypes

groundWater['Concentration with unit'] = groundWater['Concentration with unit'].astype(str)

groundWater['Concentration with unit'] = groundWater['Concentration with unit'].fillna(0)

#Make column 'data available' that will = 1 if the concentration is '<mrl' or *** ppt/ppb, and 0 if concentration is 'nan' or 'nd.'
groundWater['Data Available'] = 1

#Make sure all years are single year not range.
groundWater['year'].unique()

groundWater['Type'] = 'Ground Water'

# Remove ' ppt' and convert to float
groundWater['Concentration with unit'] = groundWater['Concentration with unit'].str.replace(' ppt', '').astype(object)

# Replace NaN values with 0 after the initial cleaning
groundWater['Concentration with unit'].fillna(0, inplace=True)

groundWater

groundWater.dtypes

"""#Prepare Surface Water DF"""

surfaceWater

surfaceWater

surfaceWater['Concentration with unit'] = surfaceWater['Concentration with unit'].astype(str)

surfaceWater['Concentration with unit'] = surfaceWater['Concentration with unit'].fillna(0)

#Make column 'data available' that will = 1 if the concentration is '<mrl' or *** ppt/ppb, and 0 if concentration is 'nan' or 'nd.'
surfaceWater['Data Available'] = 1

surfaceWater

surfaceWater['Type'] = 'Surface Water'

# Remove ' ppt' and convert to float
surfaceWater['Concentration with unit'] = surfaceWater['Concentration with unit'].str.replace(' ppt', '').astype(object)

surfaceWater['Concentration with unit'].fillna(0, inplace=True)

surfaceWater

surfaceWater.dtypes

"""#Merge All Dataframes"""

drinkingWater['Concentration with unit'] = drinkingWater['Concentration with unit'].apply(lambda x: 0 if x=='< MRL ' else x)

drinkingWater['year'] = drinkingWater['year'].astype(int)

mergedData = pd.concat([drinkingWater, groundWater, surfaceWater], ignore_index=True)

mergedData['Concentration with unit'] = mergedData['Concentration with unit'].str.replace(' ppt', '').astype(float)

mergedData['Concentration with unit'].fillna(0, inplace=True)

mergedData.to_excel('mergedData.xlsx', index=False)

mergedData.columns

"""#Pull in Shape File"""

from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ny_new_york_zip_codes_geo.min.json') as response:
  zipcodes = json.load(response)

#Make list to define radio item choices...
PFASoptions = list(mergedData['Ionic PFAS'].unique())

  #Make list to define range slider choices...
Years = list(mergedData['year'].unique())

all_locations = list(set([
    # Manhattan
'10001', '10002', '10003', '10004', '10005', '10006', '10007', '10009',
    '10010', '10011', '10012', '10013', '10014', '10016', '10017', '10018',
    '10019', '10021', '10022', '10023', '10024', '10025', '10026', '10027',
    '10028', '10029', '10030', '10031', '10032', '10033', '10034', '10035',
    '10036', '10037', '10038', '10039', '10040', '10044', '10069', '10103',
    '10119', '10128', '10162', '10165', '10170', '10173', '10199', '10279',
    '10280', '10282', '10065', '10075', '10124', '10128',

    # Bronx
    '10451', '10452', '10453', '10454', '10455', '10456', '10457', '10458',
    '10459', '10460', '10461', '10462', '10463', '10464', '10465', '10466',
    '10467', '10468', '10469', '10470', '10471', '10472', '10473', '10474',
    '10475',

    # Brooklyn
    '11201', '11203', '11204', '11205', '11206', '11207', '11208', '11209',
    '11210', '11211', '11212', '11213', '11214', '11215', '11216', '11217',
    '11218', '11219', '11220', '11221', '11222', '11223', '11224', '11225',
    '11226', '11228', '11229', '11230', '11231', '11232', '11233', '11234',
    '11235', '11236', '11237', '11238', '11239', '11241', '11243', '11249',

    # Queens
    '11004', '11101', '11102', '11103', '11104', '11105', '11106', '11109',
    '11351', '11354', '11355', '11356', '11357', '11358', '11359', '11360',
    '11361', '11362', '11363', '11364', '11365', '11366', '11367', '11368',
    '11369', '11370', '11372', '11373', '11374', '11375', '11377', '11378',
    '11379', '11385', '11411', '11412', '11413', '11414', '11415', '11416',
    '11417', '11418', '11419', '11420', '11421', '11422', '11423', '11426',
    '11427', '11428', '11429', '11432', '11433', '11434', '11435', '11436',
    '11691', '11692', '11693', '11694', '11697',

    # Staten Island
    '10304', '10305', '10306', '10307', '10301', '10302', '10303', '10308', '10309', '10310', '10311', '10312', '10313', '10314',

    # Long Island
    '11507', '11003', '11021', '11003', '11509', '11510', '11510', '11762', '11558', '11050',
    '11709', '11001', '11001', '11710', '11001', '11714', '11793', '11545', '11548', '11514', '11516',
    '11771', '11771', '11561', '11735', '11576', '11577', '11548', '11758', '11554', '11732', '11518', '11596',
    '11003', '11096', '11736', '11737', '11735', '11774', '11001', '11002', '11003', '11010', '11520', '11530',
    '11531', '11535', '11536', '11599', '11040', '11530', '11542', '11545', '11547', '11020', '11021', '11022', '11023',
    '11024', '11025', '11026', '11027', '11021', '11548', '11050', '11023', '11558', '11558', '11551', '11549', '11550',
    '11040', '11557', '11557', '11557', '11557', '11598', '11801', '11802', '11803', '11804', '11815', '11819', '11854',
    '11855', '11096', '11558', '11756', '11853', '11753', '11024', '11021', '11030', '11020', '11042', '11552', '11040',
    '11560', '11771', '11791', '11559', '11756', '11561', '11560', '11003', '11561', '11563', '11564', '11565', '11030',
    '11040', '11758', '11762', '11560', '11003', '11559', '11566', '11765', '11501', '11530', '11553', '11753', '11732',
    '11545', '11791', '11771', '11590', '11099', '11040', '11041', '11042', '11043', '11044', '11510', '11710', '11040',
    '11758', '11566', '11040', '11580', '11793', '11581', '11572', '11804', '11545', '11548', '11568', '11771', '11771',
    '11791', '11756', '11803', '11030', '11569', '11050', '11050', '11051', '11052', '11053', '11054', '11055', '11571',
    '11572', '11592', '11570', '11571', '11570', '11572', '11592', '11575', '11530', '11531', '11576', '11576', '11576',
    '11545', '11548', '11577', '11021', '11023', '11021', '11050', '11579', '11783', '11735', '11001', '11550', '11559',
    '11793', '11030', '11771', '11580', '11581', '11582', '11583', '11793', '11552', '11590', '11593', '11594', '11595',
    '11597', '11568', '11596', '11797', '11598', '11598',
    '11930', '11701', '11701', '11708', '11931', '11768', '11707', '11703', '11702', '11704', '11933', '11743', '11963',
    '11705', '11706', '11751', '11743', '11705', '11706', '11930', '11743', '11777', '11713', '11715', '11716', '11780',
    '11717', '11932', '11932', '11718', '11719', '11933', '11772', '11702', '11980', '11934', '11721', '11720', '11721',
    '11722', '11749', '11760', '11782', '11724', '11743', '11725', '11726', '11727', '11770', '11768', '11935', '11772',
    '11729', '11780', '11729', '11746', '11937', '11730', '11939', '11940', '11731', '11772', '11942', '11733', '11967',
    '11941', '11768', '11717', '11731', '11706', '11738', '11770', '11782', '06390', '11901', '11780', '11768', '11702',
    '11763', '11739', '11740', '11944', '11743', '11946', '11743', '11760', '11788', '11780', '11757', '11954', '11741',
    '00501', '00544', '11742', '11743', '11743', '11750', '11746', '11747', '11760', '11749', '11751', '11751', '11752',
    '11947', '11754', '11706', '11743', '11743', '11950', '11949', '11726', '11950', '11951', '11952', '11763', '11747',
    '11750', '11775', '11805', '11953', '11764', '11954', '11955', '11766', '11935', '11767', '11956', '11780', '11701',
    '11703', '11706', '11713', '11963', '11757', '11772', '11968', '11901', '11768', '11702', '11702', '11769', '11770',
    '11770', '11733', '11951', '11784', '11957', '11957', '11961', '11772', '11958', '11717', '11963', '11706', '11733',
    '11777', '11776', '11930', '11978', '11959', '11960', '11961', '11901', '11778', '11779', '11763', '11962', '11780',
    '11706', '11754', '11782', '11789', '11770', '11784', '11733', '11964', '11965', '11967', '11786', '11787', '11788',
    '11745', '11789', '11968', '11969', '11722', '11719', '11746', '11970', '11720', '11969', '11968', '11971', '11972',
    '11790', '11794', '11790', '11794', '11733', '11768', '11776', '11973', '11792', '11975', '11976', '11976', '11707',
    '11704', '11717', '11702', '11977', '11743', '11795', '11796', '11977', '11978', '11978', '11798', '11792', '11792',
    '11743', '11798', '11980', '10008', '10041', '10045', '10055', '10090', '10101', '10102', '10104', '10105', '10106',
    '10107', '10108', '10109', '10113', '10114', '10116', '10118', '10120', '10121', '10122', '10123', '10124',
    '10125', '10126', '10129', '10130', '10131', '10132', '10133', '10138', '10150', '10151', '10155',
    '10156', '10157', '10158', '10159', '10160', '10161', '10163', '10164', '10166', '10167', '10168',
    '10169', '10171', '10172', '10175', '10176', '10178', '10179', '10185', '10196', '10197', '10198',
    '10203', '10211', '10212', '10213', '10242', '10249', '10256', '10258', '10259', '10260', '10261',
    '10265', '10268', '10269', '10270', '10271', '10272', '10273', '10274', '10275', '10276', '10277',
    '10278', '10281', '10285', '10286', '11240', '11242', '11244', '11247', '11251', '11255', '11386','11755',
    '11405', '11424', '11425', '11439', '11451', '11005'
] + list(set(mergedData['Location'].unique()))))

borough_mapping = {
    # Manhattan
    **dict.fromkeys([
        '10001', '10002', '10003', '10004', '10005', '10006', '10007', '10009',
        '10010', '10011', '10012', '10013', '10014', '10016', '10017', '10018',
        '10019', '10021', '10022', '10023', '10024', '10025', '10026', '10027',
        '10028', '10029', '10030', '10031', '10032', '10033', '10034', '10035',
        '10036', '10037', '10038', '10039', '10040', '10044', '10069', '10103',
        '10119', '10128', '10162', '10165', '10170', '10173', '10199', '10279',
        '10280', '10282', '10065', '10075', '10124', '10128', '10008', '10041', '10045',
        '10055', '10090', '10101', '10102', '10104', '10105', '10106', '10107', '10108',
        '10109', '10113', '10114', '10116', '10118', '10120', '10121', '10122', '10123',
        '10124', '10125', '10126', '10129', '10130', '10131', '10132', '10133', '10138',
        '10150', '10151', '10155', '10156', '10157', '10158', '10159', '10160', '10161',
        '10163', '10164', '10166', '10167', '10168', '10169', '10171', '10172', '10175',
        '10176', '10178', '10179', '10185', '10196', '10197', '10198', '10203', '10211',
        '10212', '10213', '10242', '10249', '10256', '10258', '10259', '10260', '10261',
        '10265', '10268', '10269', '10270', '10271', '10272', '10273', '10274', '10275',
        '10276', '10277', '10278', '10281', '10285', '10286'
    ], 'New York (Manhattan)'),

    # Bronx
    **dict.fromkeys([
        '10451', '10452', '10453', '10454', '10455', '10456', '10457', '10458',
        '10459', '10460', '10461', '10462', '10463', '10464', '10465', '10466',
        '10467', '10468', '10469', '10470', '10471', '10472', '10473', '10474',
        '10475',
    ], 'Bronx (The Bronx)'),

    # Brooklyn
    **dict.fromkeys([
        '11201', '11203', '11204', '11205', '11206', '11207', '11208', '11209',
        '11210', '11211', '11212', '11213', '11214', '11215', '11216', '11217',
        '11218', '11219', '11220', '11221', '11222', '11223', '11224', '11225',
        '11226', '11228', '11229', '11230', '11231', '11232', '11233', '11234',
        '11235', '11236', '11237', '11238', '11239', '11241', '11243', '11249',
        '11240', '11242', '11244', '11247', '11251', '11255', '11386', '11755',
        '11405', '11424', '11425', '11439', '11451'
    ], 'Kings (Brooklyn)'),

    # Queens
    **dict.fromkeys([
       '11004', '11101', '11102', '11103', '11104', '11105', '11106', '11109',
       '11351', '11354', '11355', '11356', '11357', '11358', '11359', '11360',
       '11361', '11362', '11363', '11364', '11365', '11366', '11367', '11368',
       '11369', '11370', '11372', '11373', '11374', '11375', '11377', '11378',
       '11379', '11385', '11411', '11412', '11413', '11414', '11415', '11416',
       '11417', '11418', '11419', '11420', '11421', '11422', '11423', '11426',
       '11427', '11428', '11429', '11432', '11433', '11434', '11435', '11436',
       '11691', '11692', '11693', '11694', '11697', '11001', '11002', '11003',
       '11004', '11005', '11010', '11040', '11042', '11096', '11405',
    ], 'Queens (Queens)'),

    # Staten Island
    **dict.fromkeys([
        '10304', '10305', '10306', '10307', '10301', '10302', '10303', '10308', '10309', '10310', '10311', '10312', '10313', '10314'
    ], 'Richmond (Staten Island)'),

    # Nassau County
    **dict.fromkeys([
        '11507', '11509', '11510', '11558', '11545', '11548',
        '11514', '11516', '11561', '11535', '11536', '11599',
        '11520', '11530', '11531', '11532', '11533', '11534',
        '11553', '11560', '11572', '11576', '11577', '11579',
        '11580', '11581', '11582', '11583', '11590', '11592',
        '11595', '11596', '11598', '11501', '11542', '11549',
        '11551', '11552', '11554', '11555', '11556', '11557',
        '11568', '11569', '11571', '11575', '11578', '11584',
        '11586', '11589', '10090', '10101', '10102', '10104',
        '10105', '10106', '10107', '10108', '10109', '10113',
        '10114', '10116', '10118', '10120', '10121', '10122',
        '10123', '10124', '10125', '10126', '10129', '10130',
        '10131', '10132', '10133', '10138', '10150', '10151',
        '10155', '10156', '10157', '10158', '10159', '10160',
        '10161', '10163', '10164', '10166', '10167', '10168',
        '10169', '10171', '10172', '10175', '10176', '10178',
        '10179', '10185', '10196', '10197', '10198', '10203',
        '10211', '10212', '10213', '10242', '10249', '10256',
        '10258', '10259', '10260', '10261', '10265', '10268',
        '10269', '10270', '10271', '10272', '10273', '10274',
        '10275', '10276', '10277', '10278', '10281', '10285',
        '10286', '11001', '11002', '11003', '11010', '11020',
        '11021', '11022', '11023', '11024', '11030', '11040',
        '11042', '11050', '11051', '11052', '11053', '11054',
        '11055', '11518', '11520', '11530', '11531', '11535',
        '11536', '11542', '11545', '11547', '11548', '11549',
        '11550', '11552', '11553', '11554', '11555', '11556',
        '11557', '11558', '11559', '11560', '11561', '11563',
        '11565', '11566', '11568', '11570', '11571', '11572',
        '11575', '11576', '11577', '11579', '11580', '11581',
        '11582', '11590', '11596', '11597', '11598', '11599',
        '11709', '11710', '11714', '11732', '11735', '11736',
        '11737', '11753', '11756', '11758', '11762', '11765',
        '11783', '11791', '11793', '11797', '11774', '11025',
        '11026', '11027', '11096', '11802', '11853', '11564',
        '11099', '11041', '11043', '11044', '11045', '11046',
        '11047', '11048', '11049', '11593', '11594', '11774',
        '11853', '11564', '11099', '11041', '11043', '11044',
        '11594', '11025', '11026', '11027', '11802', '11564',
        '11099', '11041', '11043', '11044', '11594', '11774',
        '11026', '11027', '11802', '11853', '11564', '11041',
        '11043', '11044', '11593', '11771'

    ], 'Nassau (Long Island)'),

    # Suffolk County
    **dict.fromkeys([
        '00501', '00544', '06390', '11701', '11702', '11703',
        '11704', '11705', '11706', '11707', '11708', '11709',
        '11710', '11713', '11714', '11715', '11716', '11717',
        '11718', '11719', '11720', '11721', '11722', '11724',
        '11725', '11726', '11727', '11729', '11730', '11731',
        '11732', '11733', '11735', '11738', '11739', '11740',
        '11741', '11742', '11743', '11745', '11746', '11747',
        '11749', '11750', '11751', '11752', '11754', '11755',
        '11756', '11757', '11758', '11760', '11761', '11762',
        '11763', '11764', '11766', '11767', '11768', '11769',
        '11770', '11772', '11775', '11776', '11777', '11778',
        '11779', '11780', '11782', '11784', '11786', '11787',
        '11788', '11789', '11790', '11792', '11794', '11795',
        '11796', '11797', '11798', '11801', '11803', '11804',
        '11805', '11815', '11819', '11854', '11855', '11901',
        '11902', '11903', '11904', '11930', '11931', '11932',
        '11933', '11934', '11935', '11937', '11939', '11940',
        '11941', '11942', '11944', '11946', '11947', '11949',
        '11950', '11951', '11952', '11953', '11954', '11955',
        '11956', '11957', '11958', '11959', '11960', '11961',
        '11962', '11963', '11964', '11965', '11967', '11968',
        '11969', '11970', '11971', '11972', '11973', '11975',
        '11976', '11977', '11978', '11980'


    ], 'Suffolk (Long Island)')
}

"""#Plotly App"""

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

app.layout = html.Div([
    html.H4('View Compound Prevalence by Zipcode'),
    dcc.Dropdown(
        ['Drinking Water', 'Ground Water', 'Surface Water'],
        'Ground Water',
        clearable=False, id="Type"
    ),
    html.P("Select a compound:"),
    dcc.RadioItems(
        id='Compound',
        options=[{'label': comp, 'value': comp} for comp in PFASoptions],
        value='PFOS',
        inline=True
    ),
    dcc.RangeSlider(
        min=min(Years), max=max(Years), step=1, value=[min(Years), max(Years)],
        marks={i: '{}'.format(i) for i in range(min(Years), max(Years)+1)}, id='RangeChosen'
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"),
    [Input("Type", "value"),
     Input("Compound", "value"),
     Input("RangeChosen", "value")]
)
def display_choropleth(con_type, compound, years):

    df = mergedData[(mergedData['Ionic PFAS'] == compound) &
                    (mergedData['year'] >= years[0]) &
                    (mergedData['year'] <= years[1]) &
                    (mergedData['Type'] == con_type)]

    grouped = df.groupby(['Ionic PFAS', 'Location', 'year']).agg(
        mean_concentration=('Concentration with unit', 'mean'),
        std_concentration=('Concentration with unit', 'std'),
        sample_count=('Data Available', 'sum')
    ).reset_index()

    grouped['std_concentration'].fillna(0, inplace=True)
    grouped['color'] = grouped['mean_concentration'].apply(lambda x: 0 if x == 0 else x)

    grouped_tuples = [tuple(x) for x in grouped[['Ionic PFAS', 'year', 'Location']].values]
    allPossibleFields = [(compound, year, zip) for zip in all_locations for year in range(years[0], years[1] + 1)]
    dataWeNeed = list(set(allPossibleFields) - set(grouped_tuples))

    rowsToAddToDF = []
    for pair in dataWeNeed:
        rowsToAddToDF.append([pair[0], pair[1], pair[2]])

    dataWeNeeded = pd.DataFrame(columns=['Ionic PFAS', 'year', 'Location'], data=rowsToAddToDF)
    dataWeNeeded['Location'] = dataWeNeeded['Location'].apply(lambda x: str(x).zfill(5))

    dataAvailable = grouped[['Ionic PFAS', 'year', 'Location']]
    dataAvailable['Location'] = dataAvailable['Location'].apply(lambda x: str(x).zfill(5))

    filtered = pd.merge(
        dataWeNeeded,
        dataAvailable,
        on=['Ionic PFAS', 'year', 'Location'],
        how='left',
        indicator=True
    )

    dataWeNeeded = filtered[filtered['_merge'] == 'left_only']
    dataWeNeeded = dataWeNeeded.drop(columns=['_merge'])

    dataWeNeeded['mean_concentration'] = 0
    dataWeNeeded['std_concentration'] = 0
    dataWeNeeded['color'] = -55

    complete_df = pd.concat([grouped, dataWeNeeded], ignore_index=True)
    complete_df['Location'] = complete_df['Location'].apply(lambda x: str(x).zfill(5))
    complete_df['Borough'] = complete_df['Location'].map(borough_mapping)

    complete_df['sample_count'] = complete_df['sample_count'].fillna(0)


    year_range_text = f"{years[0]}" if years[0] == years[1] else f"{years[0]} - {years[1]}"
    complete_df['hover_text'] = complete_df.apply(
        lambda row: (
            f"Zipcode: {row['Location']}<br>" +
            f"County: {row['Borough']}<br>" +
            f"PFAS Compound: {row['Ionic PFAS']}<br>" +
            f"Year: {year_range_text}<br>" +
            (
                (
                    f"Mean: {row['mean_concentration']} ppt<br>" +
                    f"Standard Deviation: {row['std_concentration']} ppt<br>"
                ) if row['color'] != 0 and row['color'] != -55 else ""
            ) +
            (
                (
                    "<br>Note - Individual concentrations for this zipcode are all Not Detected"
                    if row['color'] == 0 else
                    "<br>Note - Data Not Available for individual concentrations of PFAS"
                ) if row['color'] == 0 or row['color'] == -55 else ""
            )
        ),
        axis=1
    )

    # Define custom color scale
    custom_color_scale = [
        [0, "Blue"],  # Color for values far below 0
        [0.5, "White"],  # Midpoint color (white) representing 0
        [1, "Red"]  # Color for values above 0
    ]

    fig = px.choropleth(
        complete_df,
        geojson=zipcodes,
        locations='Location',
        color='color',
        hover_name='hover_text',
        hover_data={'year': False, 'Ionic PFAS': False, 'mean_concentration': False, 'std_concentration': False, 'Location': False, 'color': False, 'sample_count': True},
        color_continuous_scale=custom_color_scale,
        color_continuous_midpoint=0,
        range_color=(-55, 55),
        featureidkey="properties.ZCTA5CE10",
        scope="usa"
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_showscale=False  # Hide the color scale
    )

    fig.update_geos(fitbounds="locations", visible=True)

    return fig

app.run_server(host='0.0.0.0', port=10000)


