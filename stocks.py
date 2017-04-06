#!/usr/bin/py
import math

#stocks.py -- an attempt to solve hackerrank problem ``stock predictions''
#reads in file stdin.txt which contains:
#amount of money to spend   number of stocks   days left to trade
#stock name shares owned prices for last five days
#(and a row for each stock)
#output is to print number of transactions, and then on each following line
#the stock name, BUY/SELL, and the number of shares

#calculate score for stock prices using all prices
#this should be a measure of odds of stock going up based on past performance
def calc_G(myprices):
    G = 0
    norm = 0
    N = len(myprices)
    a = 8.0/N
    b = 0.5*N

    for i in range(N):
        weight = 1.0/(1.0 + math.exp(a*(N-1-i-b)))  #weight more recent data heavier than older data
        G += (myprices[i] - myprices[N-1]) * weight
        norm += weight

    return G/norm

#like calc_G, but calculates score for stock prices using only increases
#the idea is that we can choose when to sell, so if we have enough time to wait out
#low prices, we can ignore them
def calc_Gplus(myprices):
    Gplus = 0
    norm = 0
    N = len(myprices)
    a = 8.0/N
    b = 0.5*N

    for i in range(N):
        weight = 1.0/(1+math.exp(a*(N-1-i-b)))
        if (myprices[i] > myprices[N-1]):
            Gplus += (myprices[i] - myprices[N-1]) * weight
        norm += weight

    return Gplus/norm

#takes m, available money, k, number of stocks, d, days left, and arrays of stock names, number owned, and prices
#prints to screen the number of transactions being made, and on each of the following lines
#stock name BUY or SELL and the number of shares to buy or sell
def printTransactions(m, k, d, name, owned, prices):

    cents = int(100*m)

    #open existing data file if present so we can look at a longer history than the stocks given to us
    data = []
    file_length = 0

    try:
        myfile = open("efl_stocks.txt", 'r') 
        for line in myfile:
            data.append(str(line))

            file_length = len(data)
        myfile.close()
    except IOError as e:
        file_length = 0

    score = []

    for i in range(len(name)):
        #see if name already in data  won't worry about sorting list for now since number of stocks capped at 10.
        data_index = -1
        for j in range(file_length):
            if data[j].split()[0] == name[i]:
                data[j] = data[j].rstrip()  #remove newline
                data[j] += " " + str(prices[i][len(prices[i])-1])  #append current price
                data_index = j
                
        if data_index == -1: #no previous record
            data_index = file_length;
            append_string = str(name[i])
            for word in prices[i]:
                append_string += " " + str(word)
            data.append(append_string)
            file_length += 1

        #analyze data[data_index]
        single_prices = []
        for word in data[data_index].split()[1:]:
            single_prices.append(int(100*float(word)))

        G = calc_G(single_prices)
        G_plus = calc_Gplus(single_prices)

        Nturns = len(single_prices) + d
        #using crude linear weighting.  The more time we have left to trade, the more G+ should be favored since we can wait out low prices
        #the less time we have, the more important G is, since it includes losses and gains
        score.append([name[i],(len(single_prices)*G + d*G_plus)/(len(single_prices)+d)/single_prices[len(single_prices)-1], single_prices[len(single_prices)-1], owned[i]])
        #added /current price so that stocks we can buy more of are more highly favored

        #print "G: ", G, ", G+: ", G_plus, ", score: ", score[len(score)-1][1]  #debugging

    #rewrite updated price lists to file
    with open("efl_stocks.txt", 'w') as myfile:
        for line in data:
            line = line.rstrip()
            myfile.write(line)
            myfile.write('\n')

    #decide what to buy and sell based on scores  Buy positive scores, and sell negative
    score.sort(key = lambda score: score[1], reverse=True)  #sort by score, highest to lowest
    score_tot = 0;
    target_number = []
    for i in range(len(score)):
        if score[i][1] > 0:
            score_tot += score[i][1]
    for i in range(len(score)):
        target_number.append(math.floor((score[i][1]*cents)/(score[i][2]*score_tot)))

    trades = []

    for i in range(len(target_number)):
        if target_number[i] < 0:
            trades.append(["SELL", int(score[i][3])])
        else:
            trades.append(["BUY", target_number[i]])
            cents -= target_number[i]*score[i][2]

    #spend any left-over money
    for i in range(len(score)):
        if cents > score[i][2]:
            cents -= cents/int(score[i][2])*score[i][2]
            trades[i][1] += int(cents/int(score[i][2]))

    #count number of transactions
    num_trans = 0
    for i in range(len(trades)):
        if trades[i][1] != 0:
            num_trans += 1

    #print results
    print num_trans
    for i in range(len(trades)):
        if trades[i][1] != 0:
            print score[i][0], ' ', trades[i][0], ' ', int(trades[i][1])

    return

if __name__ == '__main__':
    #comment out reading from stdin used by Hackerrank
    #m, k, d = [float(i) for i in raw_input().strip().split()]
    #k = int(k)
    #d = int(d)
    #names = []
    #owned = []
    #prices = []
    #for data in range(k):
    #    temp = raw_input().strip().split()
    #    names.append(temp[0])
    #    owned.append(int(temp[1]))
    #    prices.append([float(i) for i in temp[2:7]])
    
    #read in from file rather than stdin for my own testing purposes
    myfile = open('stdin.txt', 'r')

    m, k, d = [float(i) for i in myfile.readline().strip().split()]
    k = int(k)
    d = int(d)

    names = []
    owned = []
    prices = []
    for line in myfile:
        temp = line.strip().split()
        names.append(temp[0])
        owned.append(int(temp[1]))
        prices.append([float(i) for i in temp[2:7]])

    myfile.close()

    printTransactions(m, k, d, names, owned, prices)

