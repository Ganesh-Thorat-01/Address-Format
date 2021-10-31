
![Logo](https://i.pinimg.com/originals/aa/34/53/aa34538b884a1103e9cf82bbd52cfad7.jpg)


# Address Update-Address Formatting Issue


## Problem Statement
- **UIDAI Address Object Consists of Common Fields Like**
    - **House/Building/Apartment,**
    - **Street/Road/Lane,**
    - **Area/Locality/Sector,**
    - **Landmark,** 
    - **Village/Town/City,** 
    - **Pincode,** 
    - **Sub District,** 
    - **District,**
    - **State**

- **Often  Address  in  Urban  Area  Contains  Repetition  of Texts**
    - Example : “Mumbai”
- **De-Clutter the Address**
    - Identify Repetitive Constituents
    - Merge and Format the Address
- **Optionally Solve for Local Language Address**

## Objective
- **To develop  the  API  which  will  undertake  Address Formatting**
    - Accepts  the  Address  in  Raw  Form  (English  and Local Language Address)
    - Formats the Address and Presents as an Output
- **Must be a Scalable Design**

### **_You can reach the API here_**:- https://addressformat.herokuapp.com/


## Tech Stack

- **FastAPI**
- **Python**
- **Deep Translator**
- **Uvicorn**
## Deployment 
<br>
<p align="left"> <a href="https://heroku.com" target="_blank"> <img src="https://www.vectorlogo.zone/logos/heroku/heroku-icon.svg" alt="heroku" width="40" height="40"/> </a> </p>

- **Setting up Your Heroku Account**
    ```bash
    heroku login
    heroku create
    ```
- **Create requirements.txt file**
    ```bash
    pip freeze > requirements.txt
    ```
- **Create Procfile**
    ```
    web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
    ```
- **Upload to Heroku**
    ```bash
    git push heroku main
    heroku open
    ```

## Demo
https://youtu.be/uuOBTh0Zfhs

## Screenshots
**API home page**
![img](https://i.imgur.com/IcJUAj0.png)
**Working Examples**
![img](https://i.imgur.com/xAAJH1z.png)
![img](https://i.imgur.com/GJEsyEH.png)



## Usage/Examples
-**Test on CSV File**
-Sample input data:-https://github.com/Ganesh-Thorat-01/Address-Format/tree/main/Data
```python
import requests
import json as js
import pandas as pd

sample_address=pd.read_csv("Address_data.csv")
new_df=pd.DataFrame(columns=["Building","Street","Locality","Landmark","VTC","Sub-District","District","State","Pincode","Mobile"])
for ind in sample_address.index:
    building=sample_address["building"][ind]
    street=sample_address["street"][ind]
    landmark=sample_address["landmark"][ind]
    locality=sample_address["locality"][ind]
    vtc=sample_address["vtc"][ind]
    district=sample_address["district"][ind]
    state=sample_address["state"][ind]

    BASE_URL = 'https://addressformat.herokuapp.com/api'
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywidXNlcm5hbWUiOiJ0ZXN0dXNlciIsInBhc3N3b3JkX2hhc2giOiIkMmIkMTIkSURCVEo5S3FQd3JCaUxlQWJqMDMyZW5WSko2Q1NUeDV3OWRuUEIuaUd0RGp0SzNRZnhvQTYifQ.WNZwRK4CQBmasD6eUzY1PrPoQWnyP3pb5CE12593LAE"
    data=js.dumps({"building": building,
        "street": street,
        "locality": locality,
        "landmark": landmark,
        "vtc": vtc,
        "pincode": None,
        "sub_district": None,
        "district": district,
        "state": state,
        "mobile":None})

    headers = {'Authorization': "Bearer {}".format(token)}
    auth_response = requests.get(BASE_URL, headers=headers,data=data)
    
    response=auth_response.json()
    print(ind,response)
    df=response["Address"]
    new_df= new_df.append(df, ignore_index = True)
    
new_df.to_csv('Data/Testing_output.csv', index=False)

```

- **Input in Local language**

```python
import requests
import json as js

BASE_URL = 'https://addressformat.herokuapp.com/api'
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywidXNlcm5hbWUiOiJ0ZXN0dXNlciIsInBhc3N3b3JkX2hhc2giOiIkMmIkMTIkSURCVEo5S3FQd3JCaUxlQWJqMDMyZW5WSko2Q1NUeDV3OWRuUEIuaUd0RGp0SzNRZnhvQTYifQ.WNZwRK4CQBmasD6eUzY1PrPoQWnyP3pb5CE12593LAE"
data=js.dumps({"building": "No. 2",
    "street": None,
    "locality": "प्रभाग क्र. 3",
    "landmark": "रामचंद्र महाराज मंदिर",
    "vtc": "शिरसोंडी",
    "pincode": 423208,
    "sub_district": "मालेगाव",
    "district": "नाशिक",
    "state": "महाराष्ट्र",
    "mobile":None})

headers = {'Authorization': "Bearer {}".format(token)}
auth_response = requests.get(BASE_URL, headers=headers,data=data)

print(auth_response.json())
```
- **Output**
```json
{'Address in Local Language': {'इमारत': 'क्रमांक 2', 'रस्ता': None, 'परिसर': 'प्रभाग क्रमांक 3', 'लँडमार्क': 'रामचंद्र महाराज मंदिर', 'शहर': 'शिरसोंडी', 'उप जिल्हा': 'मालेगाव', 'जिल्हा': 'नाशिक', 'राज्य': 'महाराष्ट्र', 'पिन कोड': '423208 ', 'मोबाईल': None}, 'Address in English': {'Building': 'No. 2', 'Street': None, 'Locality': 'Division No. 3', 'Landmark': 'Ramchandra Maharaj Temple', 'VTC': 'Shirsondi', 'Sub-District': 'Malegaon', 'District': 'Nashik', 'State': 'Maharashtra', 'Pincode': '423208 ', 'Mobile': None}}

```
- **Input in English language**
```python
import requests
import json as js

BASE_URL = 'https://addressformat.herokuapp.com/api'
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywidXNlcm5hbWUiOiJ0ZXN0dXNlciIsInBhc3N3b3JkX2hhc2giOiIkMmIkMTIkSURCVEo5S3FQd3JCaUxlQWJqMDMyZW5WSko2Q1NUeDV3OWRuUEIuaUd0RGp0SzNRZnhvQTYifQ.WNZwRK4CQBmasD6eUzY1PrPoQWnyP3pb5CE12593LAE"
data=js.dumps({"building": "No. 2",
    "street": "Cubbon pet main road",
    "locality": None,
    "landmark": "",
    "vtc": "Bangalore North",
    "pincode": 560002,
    "sub_district": "Bangalore",
    "district": "Bangalore",
    "state": "Karnataka",
    "mobile":None})

headers = {'Authorization': "Bearer {}".format(token)}
auth_response = requests.get(BASE_URL, headers=headers,data=data)

print(auth_response.json())
```
- **Output**
```json
{'Address': {'Building': 'No. 2', 'Street': 'Cubbon Pet Main Road', 'Locality': None, 'Landmark': None, 'VTC': 'Bengaluru North', 'Sub-District': 'Bengaluru', 'District': None, 'State': 'Karnataka', 'Pincode': '560002 ', 'Mobile': None}}
```
**Its correcting _names of city_ as well as _state_ with present name**<br>
**_Note_**:- Token is given only for testing purpose and will be removed in future.
## Run Locally

**Clone the project**

```bash
  git clone https://github.com/Ganesh-Thorat-01/Address-Format
```

**Go to the project directory**

```bash
  cd Address-Format
```

**Install dependencies**

```bash
    pip install -r requirements.txt
```

**Start the server**

```bash
  uvicorn main:app --reload
```


## Authors
**Innovation Geeks**
- [@Ganesh-Thorat-01](https://github.com/Ganesh-Thorat-01)
- [@Pranav2001VS](https://github.com/Pranav2001VS)
- [@RohanPawar1911](https://github.com/RohanPawar1911)

## Feedback

If you have any feedback, please reach out to us at thorat.ganeshscoe@gmail.com

