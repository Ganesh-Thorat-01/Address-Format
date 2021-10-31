from fastapi.openapi.models import Schema
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, oauth2
from passlib.hash import bcrypt
from tortoise import fields 
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model 
from pydantic import BaseModel,PositiveInt,validator
import pandas as pd
from langdetect import detect
from deep_translator import GoogleTranslator
import uvicorn
import Data.dictionary as dictionary
import re

app = FastAPI(openapi_url=None)

JWT_SECRET = '73d9cb0dc74dda7cb79f00a6d3fc8159a8e8a3b0793567ef343900c6ddbe5413'

class Address(BaseModel):
    building: str =None
    street: str =None
    locality: str =None
    landmark: str =None
    vtc: str =None
    pincode: PositiveInt =None
    sub_district: str =None
    district: str =None
    state: str =None
    mobile: PositiveInt =None

    @validator("pincode")
    def pincode_length(cls, v):
        if len(str(v)) != 6 and v is not None:
            raise ValueError("Pincode must be of six digits")
        return v

    @validator("mobile")
    def mobile_length(cls, v):
        if len(str(v)) != 10 and v is not None:
            raise ValueError("Mobile no. must be of 10 digits")
        return v
    

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False 
    if not user.verify_password(password):
        return False
    return user 

@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    user_obj = await User_Pydantic.from_tortoise_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    
    return {'access_token' : token, 'token_type' : 'bearer'}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    return await User_Pydantic.from_tortoise_orm(user)

@app.post('/users', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@app.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user  

#Home Page  
@app.get("/")
def Home():
    return {'Message':'Hello Strangers',
            "Languages Supported":"English,Hindi,Bengali,Gujarati,Kannada,Malayalam,Marathi,Nepali,Punjabi,Sindhi,Tamil,Telugu,Urdu",
            "Return language":"Response returns in both English as well as Input Language | If Input is in English language return only in English",
            "Paramters ":{
                "building": "str | Building/House/Apartment | if not available write '' or None",
                "street": "str | Street/Lane/Road | if not available write '' or None",
                "locality": "str | Locality/Area/Sector | if not available write '' or None",
                "landmark": "str | Landmark/Nearby landmark | if not available write '' or None",
                "vtc": "str | Village/Town/City | if not available write '' or None",
                "pincode": "int | Pincode | if not available write None",
                "sub_district": "str | Sub-District | if not available write '' or None",
                "district": "str | District | if not available write '' or None",
                "state": "str | State | if not available write '' or None",
                "mobile": "int | Mobile No. | if not available write None"
                        },
            "Example":{
                "building": "No. 141",
                "street": "Cubbon pet main road",
                "locality": None,
                "landmark": "",
                "vtc": "Bangalore North",
                "pincode": 560002,
                "sub_district": "Bangalore",
                "district": "Bangalore",
                "state": "Karnataka",
                "mobile": None
            },
            "API call Method":"GET",
            "API call URL":"https://addressformat.herokuapp.com/api",
            "API call Headers":"Authorization: Bearer <token>",
            "Documentation":"https://github.com/Ganesh-Thorat-01/Address-Format",
            "©Copyright":"Innovation Geeks",
            
            }





#API Page
@app.get("/api")
async def api(user_input: Address,user: User_Pydantic = Depends(get_current_user),User: User_Pydantic= Depends(oauth2_scheme)):
    if User:
       pass
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid token')


    city_df=pd.read_csv("Data/city.csv")
    state_df=pd.read_csv("Data/state.csv")

    data=user_input.dict()
    building=data['building']
    street=data['street']
    locality=data['locality']
    landmark=data['landmark']
    vtc=data['vtc']
    pincode=data['pincode']
    sub_district=data['sub_district']
    district=data['district']
    state=data['state']
    mobile=data['mobile']

    if building is None or len(building)==0:
        building=''
    else:
        building=building+" "
    if street is None or len(street)==0:
        street=''
    else:
        street=street+" "
    if locality is None or len(locality)==0:
        locality=''
    else:
        locality=locality+" "
    if landmark is None or len(landmark)==0:
        landmark=''
    else:
        landmark=landmark+" "
    if vtc is None or len(vtc)==0:
        vtc=''
    else:  
        vtc=vtc+" "
    if pincode is None or len(str(pincode))==0:
        pincode=str(pincode)
        pincode=''
    else:
        pincode=str(pincode)
        pincode=pincode+" "
    if sub_district is None or len(sub_district)==0:
        sub_district=''
    else:
        sub_district=sub_district+" "
    if district is None or len(district)==0:
        district=''
    else:
        district=district+" "
    if state is None or len(state)==0:
        state=''
    else:
        state=state+" "
    if mobile is None or len(str(mobile))==0:
        mobile=str(mobile)
        mobile=''
    else:
        mobile=str(mobile)
        mobile=mobile+" "

    address=building+street+locality+landmark+vtc+sub_district+district+state+pincode+mobile
    detected_language=detect(address)

    
    if building is None or len(building)==0:
        building=None
    else: 
        building=GoogleTranslator().translate(building)
        if "#" in building:
            building=building.replace('#','no. ')
        building=building.title()
        building=building.strip()

    if street is None or len(street)==0:
        street=None
    else:
        street=GoogleTranslator().translate(street)
        if "#" in street:
            street=street.replace("#","No. ")
        street = re.sub('[^a-zA-Z.\d\s]', '', street)
        street=street.title()
        street=street.strip()
    if locality is None or len(locality)==0:
        locality=None
    else:
        locality=GoogleTranslator().translate(locality)
        if "#" in locality:
            locality=locality.replace("#","No. ")
        locality = re.sub('[^a-zA-Z.\d\s]', '', locality)
        locality=locality.title()
        locality=" ".join(pd.Series(locality.split()).drop_duplicates().tolist())
        locality=locality.strip()
    
    if landmark is None or len(landmark)==0:
        landmark=None
    else:
        landmark=GoogleTranslator().translate(landmark)
        if "#" in landmark:
            landmark=landmark.replace("#","No. ")
        landmark = re.sub('[^a-zA-Z.\d\s]', '', landmark)
        landmark=landmark.title()
        landmark=" ".join(pd.Series(landmark.split()).drop_duplicates().tolist())
        landmark=landmark.strip()
        
    if vtc is None or len(vtc)==0:
        vtc=None
    else:
        vtc=GoogleTranslator().translate(vtc)
        vtc=vtc.title()
        vtc=re.sub('[^a-zA-Z.\d\s]', '', vtc)
        for i in dictionary.post_office:
            if i in vtc:
                vtc=vtc.replace(i,"")
        
        vtc=" ".join(pd.Series(vtc.split()).drop_duplicates().tolist())
        vtc=vtc.strip()
    if pincode is None or len(str(pincode))==0:
        pincode=None
    else:
        pincode=str(pincode)
        pincode=re.sub('[^a-zA-Z.\d\s]', '', pincode)

    if sub_district is None or len(sub_district)==0:
        sub_district=None
    else:
        sub_district=GoogleTranslator().translate(sub_district)
        sub_district=sub_district.title()
        sub_district=re.sub('[^a-zA-Z.\d\s]', '', sub_district)
        sub_district=" ".join(pd.Series(sub_district.split()).drop_duplicates().tolist())
        sub_district=sub_district.strip()
        
    if district is None or len(district)==0:
        district=None
    else:
        district=GoogleTranslator().translate(district)
        district=district.title()
        district=re.sub('[^a-zA-Z.\d\s]', '', district)
        district=" ".join(pd.Series(district.split()).drop_duplicates().tolist())
        district=district.strip()

    if state is None or len(state)==0:
        state=None
    else:
        state=GoogleTranslator().translate(state)
        state=state.title()
        state=re.sub('[^a-zA-Z.\d\s]', '', state)
        state=" ".join(pd.Series(state.split()).drop_duplicates().tolist())
        state=state.strip()
    if mobile is None or len(str(mobile))==0:
        mobile=None
    else:
        mobile=str(mobile)
        mobile=re.sub('[^a-zA-Z.\d\s]', '', mobile)


    
    # Avoid Duplicates entity   
    if sub_district==district or district==vtc:
        district=None
    if vtc==sub_district:
        sub_district=None

    if building==street:
        building=None
    if building==vtc:
        building=None
    if building==landmark:
        building==None
    if building==locality:
        building=None
        
    if street == locality:
        street=None
    if street==landmark:
        street=None
    if street==vtc:
        street=None
    
    if locality == landmark:
        locality=None
    if locality==vtc:
        locality=None

    if landmark == vtc:
        landmark = None
    

    #Update names to present name of entity
    #building
    if building is not None:
        for i in building.split():
            if (city_df["Past1"]==i).any() | (city_df["Past2"]==i).any() | (city_df["Past3"]==i).any():
                building=building.replace(i,city_df[(city_df["Past1"]==i) | (city_df["Past2"]==i) | (city_df["Past3"]==i)].iloc[0]["Present"])
    #street
    if street is not None:
        for i in street.split():
            if (city_df["Past1"]==i).any() | (city_df["Past2"]==i).any() | (city_df["Past3"]==i).any():
                street=street.replace(i,city_df[(city_df["Past1"]==i) | (city_df["Past2"]==i) | (city_df["Past3"]==i)].iloc[0]["Present"])
    #locality
    if locality is not None:
        for i in locality.split():
            if (city_df["Past1"]==i).any() | (city_df["Past2"]==i).any() | (city_df["Past3"]==i).any():
                locality=locality.replace(i,city_df[(city_df["Past1"]==i) | (city_df["Past2"]==i) | (city_df["Past3"]==i)].iloc[0]["Present"])
    
    #landmark
    if landmark is not None:
        for i in landmark.split():
            if (city_df["Past1"]==i).any() | (city_df["Past2"]==i).any() | (city_df["Past3"]==i).any():
                landmark=landmark.replace(i,city_df[(city_df["Past1"]==i) | (city_df["Past2"]==i) | (city_df["Past3"]==i)].iloc[0]["Present"])
    
    #VTC
    if vtc is not None:
        for i in vtc.split():
            if (city_df["Past1"]==i).any() | (city_df["Past2"]==i).any() | (city_df["Past3"]==i).any():
                vtc=vtc.replace(i,city_df[(city_df["Past1"]==i) | (city_df["Past2"]==i) | (city_df["Past3"]==i)].iloc[0]["Present"])
    #Sub District
    if sub_district is not None:
        for i in sub_district.split():
            if (city_df["Past1"]==i).any() | (city_df["Past2"]==i).any() | (city_df["Past3"]==i).any():
                sub_district=sub_district.replace(i,city_df[(city_df["Past1"]==i) | (city_df["Past2"]==i) | (city_df["Past3"]==i)].iloc[0]["Present"])
    #District
    if district is not None:
        for i in district.split():
            if (city_df["Past1"]==i).any() | (city_df["Past2"]==i).any() | (city_df["Past3"]==i).any():
                district=district.replace(i,city_df[(city_df["Past1"]==i) | (city_df["Past2"]==i) | (city_df["Past3"]==i)].iloc[0]["Present"])

    #State
    if state is not None:
        if (state_df["Past"]==state).any() :
            state=state_df[(state_df["Past"]==state)].iloc[0]["Present"]

    if building=="In":
        building=None
    if street=="In":
        street=None
    if locality=="In":
        locality=None
    if landmark=="In":
        landmark=None
    if vtc=="In":
        vtc=None
    if sub_district=="In":
        sub_district=None
    if district=="In":
        district=None
    if state=="In":
        state=None
    



    #Translate the address
    if building is None or len(building)==0:
        local_building=None
    elif building.isdigit():
        local_building=building
    else:
        local_building=GoogleTranslator(target=detected_language).translate(building)

    if street is None or len(street)==0:
        local_street=None
    else:
        local_street=GoogleTranslator(target=detected_language).translate(street)

    if locality is None or len(locality)==0:
        local_locality=None
    else:
        local_locality=GoogleTranslator(target=detected_language).translate(locality)

    if landmark is None or len(landmark)==0:
        local_landmark=None
    else:    
        local_landmark=GoogleTranslator(target=detected_language).translate(landmark)

    if vtc is None or len(vtc)==0:
        local_vtc=None
    else:
        local_vtc=GoogleTranslator(target=detected_language).translate(vtc)

    local_pincode=pincode

    if sub_district is None or len(sub_district)==0:
        local_sub_district=None
    else:
        local_sub_district=GoogleTranslator(target=detected_language).translate(sub_district)

    if district is None or len(district)==0:
        local_district=None
    else:
        local_district=GoogleTranslator(target=detected_language).translate(district)

    if state is None or len(state)==0:
        local_state=None
    else:
        local_state=GoogleTranslator(target=detected_language).translate(state)

    local_mobile=mobile
    


    word_building=GoogleTranslator(target=detected_language).translate("Building")
    word_street=GoogleTranslator(target=detected_language).translate("Street")
    word_locality=GoogleTranslator(target=detected_language).translate("Locality")
    word_landmark=GoogleTranslator(target=detected_language).translate("Landmark")
    word_vtc=GoogleTranslator(target=detected_language).translate("City")
    word_pincode=GoogleTranslator(target=detected_language).translate("Pincode")
    word_sub_district=GoogleTranslator(target=detected_language).translate("Sub District")
    word_district=GoogleTranslator(target=detected_language).translate("District")
    word_state=GoogleTranslator(target=detected_language).translate("State")
    word_mobile=GoogleTranslator(target=detected_language).translate("Mobile")

    try:
        if detected_language in dictionary.unsupported_languages:
            return {"Address":{"Building":building,"Street":street,"Locality":locality,"Landmark":landmark,"VTC":vtc,"Sub-District":sub_district,"District":district,"State":state,"Pincode":pincode,"Mobile":mobile}}
        else:
            return {"Address in Local Language":{word_building:local_building,word_street:local_street,word_locality:local_locality,word_landmark:local_landmark,word_vtc:local_vtc,word_sub_district:local_sub_district,word_district:local_district,word_state:local_state,word_pincode:local_pincode,word_mobile:local_mobile},'Address in English':{"Building":building,"Street":street,"Locality":locality,"Landmark":landmark,"VTC":vtc,"Sub-District":sub_district,"District":district,"State":state,"Pincode":pincode,"Mobile":mobile}}
    except:
        return {"Error": "Unauthorized user"}




register_tortoise(
    app, 
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)

if __name__=='__main__':
    uvicorn.run(app)
