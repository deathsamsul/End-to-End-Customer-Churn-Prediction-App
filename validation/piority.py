from typing import Any

sorting_field = [
    "customerID","gender","SeniorCitizen","Partner","Dependents",
    "tenure","PhoneService","MultipleLines","InternetService",
    "OnlineSecurity","OnlineBackup","DeviceProtection","TechSupport",
    "StreamingTV","StreamingMovies","Contract","PaperlessBilling",
    "PaymentMethod","MonthlyCharges","TotalCharges","Churn","avg_spend"
]


sorting_map = {i.lower(): i for i in sorting_field}

def priority(item: dict, field: str) -> tuple:
    value: Any = item.get(field,None)

    if value is None:
        return (2, None)

    if isinstance(value, str):
        value = value.lower()

    if isinstance(value, int) and value == -1:
        return (1, value)

    return (0, value)
