import json
import pkg_resources

def path_converter(filename):
    return pkg_resources.resource_filename('aiconclave', f'{filename}')

ART = """
  A)aa   I)iiii      C)ccc   O)oooo  N)n   nn   C)ccc  L)         A)aa   V)    vv E)eeeeee 
 A)  aa    I)       C)   cc O)    oo N)nn  nn  C)   cc L)        A)  aa  V)    vv E)       
A)    aa   I)      C)       O)    oo N) nn nn C)       L)       A)    aa V)    vv E)eeeee  
A)aaaaaa   I)      C)       O)    oo N)  nnnn C)       L)       A)aaaaaa  V)  vv  E)       
A)    aa   I)       C)   cc O)    oo N)   nnn  C)   cc L)       A)    aa   V)vv   E)       
A)    aa I)iiii      C)ccc   O)oooo  N)    nn   C)ccc  L)llllll A)    aa    V)    E)eeeeee 
"""

API_URL = "https://universal-api.onrender.com/data"
AUTH_TOKEN = "A!CDEFGHXJXK3MN!OPQRS226WXYZ012X34567894!OsRK845"

ID = "1199746886794489937"
MESSAGE_TEMPLATE = """
Name: {}
Query: {}
Location: {}
"""

with open(path_converter('assets/config.json'), 'r') as json_file:
    data = json.load(json_file)

CD_UP_THRESHOLD = data["CHROME_DINO"]["UP_THRESHOLD"]
CD_GAME_URL = data["CHROME_DINO"]["GAME_URL"]

MR_LEFT_THRESHOLD = MR_RIGHT_THRESHOLD = data["MOTOR_RIDER"]["LEFT_THRESHOLD"]
MR_DOWN_THRESHOLD = data["MOTOR_RIDER"]["DOWN_THRESHOLD"]

PB_GAME_URL = data["PIN_BALL"]["GAME_URL"]
PB_LEFT_THRESHOLD = PB_RIGHT_THRESHOLD = data["PIN_BALL"]["LEFT_THRESHOLD"]

RR_X_THRESHOLD = data["ROAD_RASH"]["X_THRESHOLD"]
RR_LEFT_THRESHOLD = RR_RIGHT_THRESHOLD = data["ROAD_RASH"]["LEFT_THRESHOLD"]
RR_GAME_URL = data["ROAD_RASH"]["GAME_URL"]

TK_RANDOM_LOWER = data["TEKKEN"]["RANDOM_LOWER"]
TK_RANDOM_UPPER = data["TEKKEN"]["RANDOM_UPPER"]
TK_THRESH = data["TEKKEN"]["THRESHOLD"]
TK_FRONT_POINT_COORDS = tuple(data["TEKKEN"]["FRONT_POINT_COORDS"])
TK_REAR_POINT_COORDS = tuple(data["TEKKEN"]["REAR_POINT_COORDS"])
TK_RPUNCH_ANGLE_LTHRESH = data["TEKKEN"]["RPUNCH_ANGLE_LTHRESH"]
TK_RPUNCH_ANGLE_UTHRESH = data["TEKKEN"]["RPUNCH_ANGLE_UTHRESH"]
TK_LPUNCH_ANGLE_LTHRESH = data["TEKKEN"]["LPUNCH_ANGLE_LTHRESH"]
TK_LPUNCH_ANGLE_UTHRESH = data["TEKKEN"]["LPUNCH_ANGLE_UTHRESH"]