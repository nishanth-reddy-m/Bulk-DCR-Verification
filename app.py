from flask import Flask,request,render_template,session
from time import perf_counter
import re
import aiohttp
import asyncio

class String(str):
      def Clean(self):
            self = self.replace('\n',',')
            self = re.sub(r'[\"\'\s]','',self)
            return self

app = Flask(__name__)

def format_data(data):
        cleaned_data = String(data).Clean().split(',')
        formated_data = []
        for item in cleaned_data:
            if item and item not in formated_data and item.strip():
                  formated_data.append(item)
        return formated_data

@app.route("/",methods=["GET","POST"])
def home():
        if "verify" in request.form:
                process = {}
                start = perf_counter()
                data = request.form['sno']
                formated_data = format_data(data)
                process['no_of_inputs'] = len(formated_data)
                validatedData = asyncio.run(ValidateAllDCRs(formated_data))
                end = perf_counter()
                process['execution_time'] = f'{end-start:.3f}'
                return render_template("home.html",validatedData = validatedData, process = process)
        return render_template("home.html")

async def ValidateDCR(session,serialno):
       url = f'https://solardcrportal.nise.res.in/VerifyDCR/PnlNumberO?PnlNumber={serialno}'
       try:
             async with session.get(url, timeout=10) as response:
                    text = await response.text()
                    return serialno, ("ItemTransId" in text)
       except Exception as e:
        print(e.__str__)

async def ValidateAllDCRs(serialnos):
       async with aiohttp.ClientSession() as session:
        tasks = [ValidateDCR(session, sno) for sno in serialnos]
        results = await asyncio.gather(*tasks)
        return dict(results)

"""
Test data:

"WS05249034697231, WS05249034697220"
'RSL144CM2403300063,RSL144CM2403300028'

"""

if __name__ == "__main__":
        app.run(debug=True)