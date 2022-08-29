import os
from flask import Flask, render_template,request,redirect,flash, session, url_for
from flask_security import Security, current_user, auth_required, hash_password, SQLAlchemySessionUserDatastore
from database import db_session, init_db
from flask_login import login_required, logout_user, LoginManager
from models import User, Role
import json
import sqlite3 as sq
import pandas as pd
import plotly
import helpers.plotly_layouts as plt
import helpers.stocks as stocks


# Create app
app = Flask(__name__)
app.config['DEBUG'] = True

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Generate a secret key
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pddfgfhghgf--ghb3Ag-ghgjwwss1234')
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '182837584038784930239485749030293857390')

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

## Load the stock database from stock.py
conn = sq.connect('{}.sqlite'.format("database"),check_same_thread=False)
df = pd.read_sql('select * from {}'.format("stock_database"), conn)
stock_infos = pd.read_sql("select * from {}".format("stock_infos"), conn)

# Views
@app.route("/",  methods=['GET', 'POST'])
def index():
    return render_template("home.html")

# Dynamic endpoint for stock data per ticker. Requires filtering data by ticker
@app.route("/stocks/<ticker>", methods=['POST','GET'])
# @auth_required()
def stocks(ticker):

    df_tickers = df["Ticker"].unique()

    if ticker is None or ticker not in df_tickers:
        ticker = "AAN"

    data = df[df["Ticker"]==ticker]
    plot = plt.create_plotly(data)

    ## Stock info
    ticker_info = stock_infos[stock_infos["Ticker"]==ticker]
    ticker_info = ticker_info.transpose()
    ticker_info.columns = ["Ticker Information"]
    df1 = ticker_info.iloc[:round(len(ticker_info)/2)-1, :]
    df2 = ticker_info.iloc[(round(len(ticker_info)/2)):, :]

    df1 = df1.to_html()
    df2 = df2.to_html()

    plotly_plot = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("stocks.html", plotly_plot= plotly_plot, ticker = ticker,
                          df_tickers = df_tickers, ticker_info = [df1,df2])

# Simple landing page to choose a stock
@app.route("/stocks")
# @auth_required()
def stocks_redirect():
    df_tickers = df["Ticker"].unique()
    return render_template("stocks.html", df_tickers= df_tickers, ticker_info=None)

# An error handler for 404 errors that renders a a template if stock ticker is not found
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.directory='./'
    app.run(host='127.0.0.1', port=5000)
