# -- Load library --
from __init__ import app
import sys, os
import distutils.util
from flask import Flask, jsonify, request
import json
from bson import json_util
from sklearn.datasets import fetch_20newsgroups
import time

# -- Load custome modules --



####################################################
# For test.                                   #
####################################################
@app.route('/test/<id>/<step>', methods=['GET'])
def test(id, step):
    try:
        try:
            test_module_name = app.config['GAINER_PARAMS'][id]['test_module_name']
            test_module = __import__(test_module_name)

        except Exception:
            # -- Create response --
            returned_json = {'message': 'Invalid test id: ' + str(sys.exc_info())}
            resp = jsonify(returned_json)
            resp.status_code = 200
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
            # -- Create response --

        # Get all data
        test_module.test(step)

        # -- Create response --
        returned_json = {'message': 'success'}
        resp = jsonify(returned_json)
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
        # -- Create response --

    except Exception:
        print(sys.exc_info())
        shutdown_server()
        print('######## Server shutdown #########')
        return show_error_page(500, "Unexpected Error")





####################################################
# Functions for web app.                           #
####################################################

# -- Not Found Error Message --
@app.errorhandler(404)
def not_found(e):
    return e
# -- Not Found Error Message --


# -- Error Message --
def show_error_page(code=None, error=None):
    if code:
        message = {
            'status': code,
            'message': error
        }
    else:
        code = 500
        message = {
            'status': 500,
            'message': 'Unexpected Error'
        }
    resp = jsonify(message)
    resp.status_code = code
    return resp
# -- Error Message --

# -- Shutdown server --
@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
# -- Shutdown server --



