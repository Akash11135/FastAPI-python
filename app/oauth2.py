from jose import JWTError , jwt
from datetime import datetime , timedelta
#secret key
#Algo hs256
#expiration time/date

SECRET_KEY = "09293487283756734659287356987sghkebfeskhjf908679834grhfvdkbvhddfg8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=200

def create_access_token(data:dict):
    to_encode = data.copy() #create copy of data to encode in the jwt token
    expire_time = datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire_time})

    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credential_exception):
    payload = jwt.decode(token,SECRET_KEY ,algorithms=ALGORITHM)
    id:str = payload.get("users_id")

    if id is None:
        raise credential_exception

    token_data