Personal repository for joint project
Note: requires ofboard scraper (in development). The .txt file also requires population and starter data (huge apologies but the line numbers matter). Not all data points added, what we add depends on scraper cabilities
dependencies aside from scrapers: Conda (For venv, unless you're crazy like that), Optuna, Numpy 

Description: A semi-AI driven (Semi as in single layer neural) driving weights behind 3rd-order linearization of a moving set of data that takes in the last 20 pieces of data and makes a decision on whether to buy a stock. 
The sucess of the model is based entirely on its simple reward system: if it buys a stock, that stock has to create a profit over a single day hold. (Treating every iteration as a day-long step)
