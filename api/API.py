from flask import Flask
from flask import request,jsonify
from dgkeyphrase_final import keyphrase_text

app = Flask(__name__)


@app.route("/analyze/phrases",methods=["POST"])
def requestHandler():
    req=request.get_json()
    print(req['data'][0])
    results = {} 
    results = {"output":[]}   
    for textString in req['data']: 
        data= keyphrase_text(textString)
        results["output"].append(data) 

    response = results
    return response

@app.route("/health", methods=["GET"])
def healthResponse():
    print("health api hit from " + request.remote_addr);
    return jsonify({"status": 200, "server": "up"})

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')    

