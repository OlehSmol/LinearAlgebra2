from flask import Flask, jsonify, request, Response
# from matrix import Matrix

from src.hamming import Hamming

app = Flask(__name__)


@app.errorhandler(415)
def unsupported_media_type(error=None):
    message = {
        'status': 415,
        'message': 'Unsupported Media Type: ' + request.url,
    }
    response = jsonify(message)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.status_code = 415

    return response

# @app.route('/linearalgebra/api/v1.0/consistent', methods=['POST', 'OPTIONS'])
# def get_tasks():
#     if request.method == 'OPTIONS':
#         response = Response('', status=200, mimetype='application/json')
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#         response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#         return response
#
#     else:
#         if request.headers['Content-Type'] == 'application/json':
#             json = request.json
#             print(json)
#             matrix = json['matrix']
#             new = Matrix(matrix)
#             result = {
#                 'consistency': new.is_consistent(),
#                 'steps': new.get_steps()
#             }
#             response = jsonify(result)
#             response.headers.add('Access-Control-Allow-Origin', '*')
#             # response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#             # response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#             return response
#         else:
#             return unsupported_media_type()

@app.route('/linearalgebra/api/v1.0/error-correction', methods=['POST', 'OPTIONS'])
def get_tasks():
    if request.method == 'OPTIONS':
        response = Response('', status=200, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    else:
        if request.headers['Content-Type'] == 'application/json':
            json = request.json
            print(json)

            #---------------------------------------
            phrase = json['phrase']
            resend = json['resend']
            #---------------------------------------

            code = Hamming(json.phrase, json.resend)


            result = {
                'result': code.get_all(),
                'statistic': code.get_statistic()
            }
            response = jsonify(result)
            response.headers.add('Access-Control-Allow-Origin', '*')

            return response
        else:
            return unsupported_media_type()

if __name__ == "__main__":
    app.run()
