# StockDashboardPy
StockDashboard.py is a web-based database application for accessing data fom the iShares Russell 2000 ETF index which tracks the investment results of a collection of small-capitalization U.S. equities. ![1](https://www.ishares.com/us/products/239710/ishares-russell-2000-etf#:~:text=The%20iShares%20Russell%202000%20ETF,of%20small%2Dcapitalization%20U.S.%20equities.) The current state of the project is a MVP, and is currently not hosted because the database is so large that it would incur a monthly fee. The application consists of a search interface allowing a user to search for a company name, stock ticker, or industry and return a candle stick diagram and basic facts about the stock from Ishares.

This application was build with Flask, and utilitizes a SQLite3 database to store all stock information. The search bar features autocomplete which makes finding a stock's ticker much easier and it is implemented in the backend using javascript. The following images were captured of the application running locally.

<h1>The Home Page</h1>

![alt text](demo_img/homePage.png?raw=true)


