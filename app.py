from flask import Flask,request,render_template,session
import requests
import re

class String(str):
      def Clean(self):
            self = self.replace('\n',',')
            self = re.sub(r'[\"\'\s]','',self)
            return self

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def home():
        validatedData = {}
        if "verify" in request.form:
                data = String(request.form['sno']).Clean().split(',')
                for sno in data:
                        validatedData[sno] = ValidateDCR(sno)
                return render_template("home.html",validatedData = validatedData)
        return render_template("home.html")

def ValidateDCR(modSrNum):
    url = f'https://solardcrportal.nise.res.in/VerifyDCR/PnlNumberO?PnlNumber={modSrNum}'
    try:
        response = requests.get(url).text
    except Exception as e:
        print(e.__str__)
    if "ItemTransId" in response: result = True
    else: result = False
    return result

"""
Test data:

"WS05249034697231, WS05249034697220"
'RSL144CM2403300063,RSL144CM2403300028'

"""

if __name__ == "__main__":
        app.run(debug=True)