# StockDashboardPy
StockDashboard.py is a web-based database application for accessing data from the iShares Russell 2000 ETF index which tracks the investment results of a collection of small-capitalization U.S. equities. The current state of the project is a MVP, and is currently not hosted because the database is so large that it would incur a monthly fee. The application consists of a search interface allowing a user to search for a company name, stock ticker, or industry and return a candle stick diagram and basic facts about the stock from Ishares.

This application was build with Flask, and utilitizes a SQLite3 database to store all stock information. The search bar features autocomplete which makes finding a stock's ticker much easier and it is implemented in the backend using javascript. The following images were captured of the application running locally.

## Demo
https://user-images.githubusercontent.com/72423203/189508884-b49022e8-dd22-4146-9a77-199ee2d93f1f.mp4


<h3>The Home Page</h3>

![alt text](demo_img/homePage.png?raw=true)

<h3>Stocks Page: Autocomplete</h3>

![alt text](demo_img/stocks1.png?raw=true)

<h3>Stocks Page: Search Autocomplete: APPLIED INDUSTRIAL TECHNOLOGIES IN</h3>

![alt text](demo_img/stocks2.png?raw=true)

<h3>Stocks Page: Search Output + Candle stick diagram: APPLIED INDUSTRIAL TECHNOLOGIES IN</h3>

![alt text](demo_img/stocks3.png?raw=true)

<h3>Stocks Page: Search Interactive Candle stick diagram: APPLIED INDUSTRIAL TECHNOLOGIES IN</h3>

![alt text](demo_img/stocks4.png?raw=true)


<h4>Running StockDashboardPy Locally</h4>

<p>Clone my repository</p>

```python
$ git clone https://github.com/peter-w-bryant/StockDashboardPy.git
```
<p>Create + activate virtual environment</p>

```python
$ python -m venv ./env
$ env/Scripts/activate
```
<p>Install all dependencies</p>

```python
$ pip install -r requirements.txt
```
<p>Create database (named database.sqlite)</p>

```python
$ python helpers/stocks.py
```

<p>Run the app and start your local server</p>

```python
$ python app.py
```

