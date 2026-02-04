from fastapi import FastAPI,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import Field,computed_field
from typing import Literal,Annotated
from ml_model.predictor import churn_predictor,ram_use
from validation.schema import customer_input,update_customer
from data.data import data_load,save_data
from validation.piority import sorting_map,priority






# fastapi object instance
app=FastAPI(title='customer data management api and churn prediction',version='1.0.0')




#health check endpoint for cloude platform
@app.get('/health')
def health():
    return{
        'message':'ok',
        'model_version':'1.0.0',
        'model_load':True
    }

# first endpoint for home page
@app.get('/')
def home():
    return {'message':'hi iam samsul i build this customer churn prediction'}

# 2nd endpoint for about
@app.get('/about')
def about():
    return {'message':'this is customer churn prediction fastapi webappliction for data manage and prediction'}





# 4rd endpoint for retreving data
@app.get('/customers')
def view():
    data=data_load()
    return data

# filtering with sorting data 
@app.get('/customers/sort')
def customer_sort(
    sort_by:str=Query(default='tenure',description='sort base for sorting'),
    order:Literal['asc','desc']=Query(default='desc',description='sorting order : "asc","desc"',example='asc'),

    customerID:int | None =None,
    gender:str | None =None,
    SeniorCitizen:int | None =None,
    Partner:str | None =None,
    Dependents:str | None =None, 
    tenure:int | None =None,
    PhoneService:str | None =None,
    MultipleLines:str | None =None,
    InternetService:str | None =None,
    OnlineSecurity:str | None =None,
    OnlineBackup:str | None =None,
    DeviceProtection:str | None =None ,
    TechSupport:str | None =None,
    StreamingTV:str | None =None,
    StreamingMovies:str | None =None,
    Contract:str | None =None,
    PaperlessBilling:str | None =None,
    PaymentMethod:str | None =None,
    MonthlyCharges:float | None =None,
    TotalCharges:float | None =None,
    #avg_spend:float | None =None,
    Churn:str|None=None
):
    


    key = sort_by.lower()

    if key not in sorting_map:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by only Allowed values"
        )
    sort_by = sorting_map[key]

    data=data_load()
    fillterd=[i for i in data
        if (customerID is None or i.get('customerID')==customerID) and
        (gender is None or i.get('gender',"").lower()==gender.lower()) and
        (SeniorCitizen is None or i.get('SeniorCitizen')==SeniorCitizen)
        and (Partner is None or i.get('Partner',"").lower()==Partner.lower())and 
        (Dependents is None or i.get('Dependents','').lower()==Dependents.lower())and
        (tenure is None or i.get('tenure')==tenure) and 
        (PhoneService is None or i.get('PhoneService','').lower()==PhoneService.lower())and
        (MultipleLines is None or i.get('MultipleLines','').lower()==MultipleLines.lower())and
        (InternetService is None or i.get('InternetService','').lower()==InternetService.lower())and
        (OnlineSecurity is None or i.get('OnlineSecurity','').lower()==OnlineSecurity.lower()) and
        (OnlineBackup is None or i.get('OnlineBackup','').lower()==OnlineBackup.lower())and
        ( DeviceProtection is None or i.get('DeviceProtection','').lower()==DeviceProtection.lower())and
        (TechSupport is None or i.get('TechSupport','').lower()==TechSupport.lower())and
        (StreamingTV is None or i.get('StreamingTV','').lower()==StreamingTV.lower())and
        (StreamingMovies is None or i.get('StreamingMovies','').lower()==StreamingMovies.lower())and 
        (Contract is None or i.get('Contract','').lower()==Contract.lower()) and
        (PaperlessBilling is None or i.get('PaperlessBilling','').lower()==PaperlessBilling.lower())and
        (PaymentMethod is None or i.get('PaymentMethod','').lower()==PaymentMethod.lower())and
        (MonthlyCharges is None or i.get('MonthlyCharges')==MonthlyCharges)and
        (TotalCharges is None or i.get('TotalCharges')==TotalCharges)
        #(avg_spend is None or ((i.get('MonthlyCharges')!=0) and (i.get('TotalCharges')/i.get('MonthlyCharges'))==avg_spend))
        ]
    
    ord=order=='desc'
    return sorted(fillterd,key=lambda x:priority(x,sort_by),reverse=ord)





#id wise customer fetch
@app.get('/customers/{customer_id}')
def fetch_customer(customer_id:Annotated[int,Field(...,description='customer unique id',examples=0,)]):
    data=data_load()
    for x in data:
        if x.get('customerID')==customer_id:
            return x
    raise HTTPException(status_code=404,detail='customer not found')


class new_customer(customer_input):

    @computed_field
    @property
    def avg_spend(self)->float:
        if self.tenure==0:
            return 0
        avg_spend=self.TotalCharges/self.tenure
        return avg_spend


# add new customer 
@app.post('/post',status_code=201)
def add_customers(customer:Annotated[new_customer,Field(description='adding customer data')]):
    data=data_load()
    # new id generate
    new_id=max([i['customerID'] for i in data],default=0)+1

    new={
        'customerID':new_id,
        **customer.model_dump(),
        'avg_spend':customer.avg_spend
    }
    data.append(new)
    save_data(data)
    return {'message':'customer add successfully','customer':new}

# delet customer data
@app.delete('/delet/{customer_id}')
def delet_customer(customer_id:Annotated[int,Field(...,description='customer_id for delet customer')]):
    data=data_load()

    for index,customer in enumerate(data):
        if customer.get('customerID')==customer_id:
            deletd=data.pop(index)
            save_data(data)
            return {'message':'customer deleted','customer':deletd}
    raise HTTPException(status_code=404,detail='customer not found')



@app.patch('/patch/{customer_id}')
def update_customer(customer_id:Annotated[int,Field(...,description='give unique customer id')],customer:update_customer):
    data=data_load()
    for index,cus in enumerate(data):
        if cus.get('customerID')==customer_id:
            update=customer.model_dump(exclude_unset=True)
            cus.update(update)
            data[index]=cus
            save_data(data)
            return {'message':'customer updated successfully',
                                                         'customer':cus}
    raise HTTPException (status_code=404,detail='customer not found')


# churn prediction function
@app.post('/predict',response_model=dict)
def customer_churn_predict(customer:customer_input):
    try:
        return JSONResponse(status_code=200,content={'churn prediction : churn_predictor(customer.model_dump())'})
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))

#for ram uses
@app.get("/ram")
def ram():
    try :
        return JSONResponse(status_code=200,content={'ram_use':ram_use()})
    except Exception as e:
        return JSONResponse(status_code=200,content=str(e))
