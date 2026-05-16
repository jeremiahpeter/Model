from doctest import master

import optuna
import Algo_library as Alg
import copy


#initiates the model
#hold space to stop the program
while True :
    go_next = input("train or predict? (T/P)", end="  ")
    if  go_next != "T" and go_next != "P" :
        print("invalid input, try again.")
    elif go_next == "T" :
        limit = input("number of iterations? (N) to run until stopped.", end="   ")
        if limit == "N" :
            print("training will run until stopped.")
            break
        else:
            limit = int(limit)
            break

with open('info.txt', 'r') as file:
    ticker = file.readline(0)
    last_buy = int(file.readline(1))
    avg_profit = int(file.readline(2))
    google_trends_data = file.readline(3).split(" ")
    price_data = file.readline(4).split(" ")
    sales_data = file.readline(5).split(" ")
    buys_data = file.readline(6).split(" ")
    sentiment_data = file.readline(7).split(" ")
    



#data constructs for risk,.
Sentiment_data = Alg.avg(sentiment_data)
Google_data = Alg.avg(google_trends_data)

risk_data = [sentiment_data, 
             Google_data]
risk_names = ["sentiment", "google_trends"]


#data constructs for movement
Sales_data = Alg.avg(sales_data)
Buys_data = Alg.avg(buys_data)

movement_data = [sales_data, 
                 buys_data]
movement_names = ["sales", "buys"]


#data constructs for price
Price_data = Alg.avg(price_data)

curr_data = [price_data]
curr_names = ["price"]


def objective(trial):

    global  ticker
    ticker += 1

    master_threshold = [trial.suggest_float("master_index", -3.0, 3.0)]

    
    google_weights = [trial.suggest_float(f'w_{i}', -1.0, 1.0) for i in range(20)]
    price_weights = [trial.suggest_float(f'w_{i}', -1.0, 1.0) for i in range(20)]
    sales_weights = [trial.suggest_float(f'w_{i}', -1.0, 1.0) for i in range(20)]
    buys_weights = [trial.suggest_float(f'w_{i}', -1.0, 1.0) for i in range(20)]
    sentiment_weights = [trial.suggest_float(f'w_{i}', -1.0, 1.0) for i in range(20)]


    risk_data_weights = [sentiment_weights, google_weights] 

    movment_data_weights = [sales_weights, buys_weights]

    price_data_weights  = [price_weights]


    curr_threshold = [trial.suggest_float("current_threshold", 0, 5)]
    movement_threshold = [trial.suggest_float("movement_threshold", 0, 5)]
    risk_threshold = [trial.suggest_float('risk_threshold', 0, 5)]
    


    global new_risk_data
    new_risk_data = []
    risk_index = 0
    for I in range(len(risk_data)) :
        ranged_data = copy.deepcopy(risk_data[I])
        ranged_data.sort(reverse=True) 
        regressed_components = Alg.regress(ranged_data, risk_data_weights[I], 3)
        next_point = get_data(risk_names[I])
        new_risk_data += [next_point]
        risk = regressed_components[0] * ( next_point **3 ) + regressed_components[1] * (next_point ** 2 )+ regressed_components[2] * next_point + regressed_components[3]
        risk_index += risk


    global new_movement_data
    new_movement_data = []
    movement_index = 0
    for I in range(len(movement_data)) :
        ranged_data = copy.deepcopy(movement_data[I])
        ranged_data.sort(reverse=True) 
        regressed_components = Alg.regress(ranged_data, movment_data_weights[I], 3)
        next_point = get_data(movement_names[I])
        new_movement_data += [next_point]
        movement = regressed_components[0] * ( next_point **3 ) + regressed_components[1] * (next_point ** 2 )+ regressed_components[2] * next_point + regressed_components[3]
        movement_index += movement 
        

    global new_curr_data
    new_curr_data = []
    curr_index = 0
    for I in range(len(curr_data)) :
        ranged_data = copy.deepcopy(curr_data[I])
        ranged_data.sort(reverse=True) 
        regressed_components = Alg.regress(ranged_data, price_data_weights[I], 3)
        next_point = get_data(curr_names[I])
        new_curr_data += [next_point]
        curr = regressed_components[0] * ( next_point **3 ) + regressed_components[1] * (next_point ** 2 )+ regressed_components[2] * next_point + regressed_components[3]
        curr_index += curr

    

    total_index = risk_index - risk_threshold + movement_index - movement_threshold + curr_index - curr_threshold
    Buy = False


    global new_avg_profit
    if total_index > master_threshold :
        Buy = True
        price_baught_at = new_curr_data[-1]
        profit  = price_baught_at - last_buy
        new_avg_profit = (avg_profit * 4 + profit) / 5
        last_buy = price_baught_at
    else:
        new_avg_profit = avg_profit 



    global risk_data, movement_data, curr_data

    for I in range(len(risk_data)) :
        risk_data[I] = [Alg.cycle_data(risk_data[I], new_risk_data[I])]

    for I in range(len(movement_data)) :
        movement_data[I] = [Alg.cycle_data(movement_data[I], new_movement_data[I])]
        

    for I in range(len(curr_data)) :
        curr_data[I] = [Alg.cycle_data(curr_data[I], new_curr_data[I])]
    

    return new_avg_profit

study = optuna.create_study(study_name="trading_algo",storage="sqlite:///trading_study.db", direction='maximize',load_if_exists=True)
study.optimize(objective, n_trials=limit)

with open("info.txt", "w") as file:
    file.write(f"{ticker}\n")
    file.write(f"{last_buy}\n")
    file.write(f"{new_avg_profit}\n")
    file.write(" ".join(google_trends_data) + "\n")
    file.write(" ".join(price_data) + "\n")
    file.write(" ".join(sales_data) + "\n")
    file.write(" ".join(buys_data) + "\n")
    file.write(" ".join(sentiment_data) + "\n")

best_weights = study.best_params