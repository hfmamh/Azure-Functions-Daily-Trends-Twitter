import azure.functions as func
import logging

import requests
from requests_html import HTMLSession
from datetime import datetime
import pandas as pd


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="HttpExample")
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        #return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
        resp=get_trends(name)
        return func.HttpResponse(resp)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    

def get_trends(country):
    #country='peru'
    session = HTMLSession()
    country_f=country.lower().replace(' ','-')
    r=session.get(f'https://getdaytrends.com/{country_f}/')
    d=[]
    now = datetime.today()
    for i in range(1,16):
        trend=r.html.xpath(f'//*[@id="trends"]/table[1]/tbody/tr[{i}]/td[1]/a')[0].text
        count=float(r.html.xpath(f'//*[@id="trends"]/table[1]/tbody/tr[{i}]/td[1]/div/span')[0].text.strip('K tweets|| Under ||M tweets'))
        d.append({
            'trend':trend,
            'rank':i,
            'country':country,
            'tweets':count,
            'datetime': now
        }
        )
    df=pd.DataFrame(d)
    #logging.info(df.to_string())

    return df.to_string()