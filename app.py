# encoding: utf-8
"""
Created on Jul 09, 2015

@author: dimitris.theodorou
"""
import os
from traceback import format_exc
from pprint import pprint
from cStringIO import StringIO

from flask import Flask, jsonify
from flask.json import JSONEncoder
from sqlalchemy import create_engine
from sqlalchemy.engine import RowProxy
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy_session import flask_scoped_session

def ppr(obj):
    s = StringIO()
    pprint(obj, stream=s)
    return s.getvalue()

class JsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, RowProxy):
            return dict(o.items())
        return JSONEncoder.default(self, o)

app = Flask(__name__)
app.json_encoder = JsonEncoder

@app.route("/")
def index():
    return "Hello! v2"

@app.route("/environ")
def environ():
    return ppr(os.environ)

DB_URL = os.environ["DB_URL"]#, "postgres://docker@db:5432/docker")
engine = create_engine(DB_URL)
session = flask_scoped_session(sessionmaker(engine), app)

@app.route("/sql/<query>")
def sql(query):
    response = {"query": query}
    try:
        query_result = session.execute(query)
        session.commit()
        response["message"] = "Executed successfully."
        if query_result.rowcount is not None:
            response["rows_affected"] = query_result.rowcount
        if query_result.returns_rows:
            response["returned_rows"] = query_result.fetchall()
    except Exception as ex:
        response["error"] = str(ex)
        response["traceback"] = format_exc()
    return jsonify(**response)

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False)
