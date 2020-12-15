#Naive Stock Trading Optimization

# Part 1 Objectives
# given a dictionary of stock data in the form:
# stock_prices = { date : [open, high, low, close] }
# determine
#  1) the % of times that the stock price moved up  x% from the day's open within Y trading days
#  2) the % of time it closed up X% within Y trading days
#  3) the % of time it ended the period down X% without hitting the target

# Part 2 Objectives:
# Evaluate profits/losses based on the following criteria:
#    1) The stock is bought each day and sold if the target high is reached
#    2) At the end of the time period, the stock is sold at close of final day(if it s still owned)

import csv
import pprint
import random


stock_prices = {}
date_list = []
with open('data2.csv') as file:
    reader = csv.reader(file, delimiter=",")
    line_count = 0
    for row in reader:
        if line_count == 0:
            line_count += 1
        else:
            date_list.append(row[0])
            stock_prices[row[0]] = [row[1],row[2], row[3], row[4]]
            line_count += 1
        #if line_count > 50:
        #    break


def get_subset(start_date, num_days): #returns an array with consecutive dates as string 'yyyy-mm-dd'
    dates = []
    starting_index = date_list.index(start_date)
    for i in range(starting_index, starting_index + num_days):
        dates.append(date_list[i])
    return dates


def increased_by_target(percentage, start_date, num_days):
    dates = get_subset(start_date, num_days)
    target = float(stock_prices[dates[0]][0]) * (1 + percentage/100)
    for date in dates:
        if float(stock_prices[date][1]) >= target : return True
    return False


def frequency_hits_target(percentage, date_list, num_days):
    count = 0
    for date in date_list:
        if date_list.index(date) < (len(date_list) - num_days):
            if increased_by_target(percentage, date, num_days) : count += 1
    print("The stock price hit the target", int(count/len(date_list)*100), "% of time.")

def closes_above_target(percentage, start_date, num_days):
    dates = get_subset(start_date, num_days)
    target = float(stock_prices[dates[0]][0]) * (1 + percentage/100)
    for date in dates:
        if float(stock_prices[date][3]) >= target : return True
    return False


def frequency_closes_above_target(percentage, date_list, num_days):
    count = 0
    for date in date_list:
        if date_list.index(date) < (len(date_list) - num_days):
            if closes_above_target(percentage, date, num_days) : count += 1
    print("The stock price closed above the target", int(count/len(date_list)*100), "% of time.")


def ended_below_x(percentage, start_date, num_days):
    dates = get_subset(start_date, num_days)
    target = float(stock_prices[dates[0]][0]) * (1 - percentage/100)
    for date in dates:
        if float(stock_prices[date][1]) <= target : return True
    return False

def frequency_ended_below_x(percentage, date_list, num_days):
    count = 0
    for date in date_list:
        if date_list.index(date) < (len(date_list) - num_days):
            if ended_below_x(percentage, date, num_days) : count += 1
    print("The stock price closed down {x}%".format(x=percentage), int(count/len(date_list)*100), "% of time.")


#manual tests:
#frequency_hits_target(1, date_list, 5)
#frequency_closes_above_target(1, date_list, 5)
#frequency_ended_below_x(1, date_list, 5)



#Part 2

def find_returns(percentage, date_list, num_days, starting_capital):
    principal = starting_capital
    percentage = percentage/100
    commission_fee = 1
    for date in date_list:
        if date_list.index(date) < (len(date_list) - num_days):
            daily_investment = starting_capital/10 - commission_fee
            principal -= daily_investment
            buy_price = float(stock_prices[date][0])
            if increased_by_target(percentage, date, num_days):
                sell_price = float(buy_price * (1 + percentage))
            else:
                sell_price = float(stock_prices[date_list[date_list.index(date) + num_days]][3])
            p_l = (sell_price - buy_price) / buy_price
            daily_investment = daily_investment * (1 + p_l) - commission_fee
            principal += daily_investment
            print("Ending Trade Value: ", daily_investment)
            print("New Principal: ", principal)
    print(principal)



#manual test examples
#find_returns(1, date_list, 5,10000)
#print(increased_by_target(2, '2019-12-10', 8))
#pprint.PrettyPrinter().pprint(stock_prices)
