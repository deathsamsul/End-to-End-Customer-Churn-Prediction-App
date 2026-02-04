from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated


class customer_input(BaseModel):
    gender:Annotated[Literal['Male','Female','Other'],Field(...,description='chose your gender')]
    SeniorCitizen:Annotated[Literal[0,1],Field(...,description='if you are seniorcirizen then enter 1 else 0')]
    Partner:Annotated[Literal['Yes','No'] ,Field(default='No',title='prtner')]
    Dependents:Annotated[Literal['Yes','No'] ,Field(default='No',title='dependents')]
    tenure:Annotated[int,Field(default=0,title='tenure',description='your tenure')]
    PhoneService:Annotated[Literal['Yes','No'] ,Field(default='No',title='phoneservice')]
    MultipleLines:Annotated[Literal['Yes','No','No phone service'] ,Field(default='No',title='MultipleLines')]
    InternetService:Annotated[Literal['DSL', 'Fiber optic', 'No'] ,Field(default='No',title='InternetService',description='what type of service')]
    OnlineSecurity:Annotated[Literal['Yes','No'] ,Field(default='No',title='OnlineSecurity')]
    OnlineBackup:Annotated[Literal['Yes','No'] ,Field(default='No',title='OnlineBackup')]
    DeviceProtection:Annotated[Literal['Yes','No'] ,Field(default='No',title='DeviceProtection')]
    TechSupport:Annotated[Literal['Yes','No'] ,Field(default='No',title='TechSupport')]
    StreamingTV:Annotated[Literal['Yes','No'] ,Field(default='No',title='StreamingTV')]
    StreamingMovies:Annotated[Literal['Yes','No'] ,Field(default='No',title='StreamingMovies')]
    Contract:Annotated[Literal['Month-to-month', 'One year', 'Two year'] ,Field(...,description='duration of contract',title='Contract')]
    PaperlessBilling:Annotated[Literal['Yes','No'] ,Field(default='Yes',title='PaperlessBilling')]
    PaymentMethod:Annotated[Literal['Electronic check','Mailed check','Bank transfer (automatic)','Credit card (automatic)'] ,
                            Field(description='type of your payment',title='PaymentMethod')]
    MonthlyCharges:Annotated[float ,Field(...,title='monthlychages',description='your monthlycharges')]
    TotalCharges:Annotated[float ,Field(...,title='totalchages',description='your totalcharges')]



class update_customer(BaseModel):
    gender:Literal['Male',"Female","Other"] | None =None
    SeniorCitizen:Literal[0,1] | None =None
    Partner:Literal['Yes','No'] | None =None
    Dependents:Literal['Yes','No'] | None =None
    tenure:int | None =None
    PhoneService:Literal['Yes','No'] | None =None
    MultipleLines:Literal['Yes','No','No phone service'] | None =None
    InternetService:str | None =None
    OnlineSecurity:Literal['Yes','No'] | None =None
    OnlineBackup:Literal['Yes','No'] | None =None
    DeviceProtection:Literal['Yes','No'] | None =None 
    TechSupport:Literal['Yes','No'] | None =None
    StreamingTV:Literal['Yes','No'] | None =None
    StreamingMovies:Literal['Yes','No'] | None =None
    Contract:str | None =None
    PaperlessBilling:Literal['Yes','No'] | None =None
    PaymentMethod:str | None =None
    MonthlyCharges:float | None =None
    TotalCharges:float | None =None
    Churn:str|None=None