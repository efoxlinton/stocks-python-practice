#!/usr/bin/py
import subprocess

#for testing stocks.py over multiple turns.
#reads in larger data file "stocks_data_short.txt" for the input stock prices on each turn
#then repeatedly rewrites stdin.txt with appropriate input and calls stocks.py
#stdin.txt contains:
#m (money you have) k (number of stocks) d (days left to trade)
#then on next k rows:
#stock name shares owned prices for last five days (with current price last)
#results printed to stdout.txt

data = []
myfile = open("stock_data_short.txt", 'r')

for line in myfile:
    data.append(line)
    
myfile.close()

split_data = []

for i in range(len(data)):  
    data_row = data[i].split()
    if len(data_row) > 0:
        split_data.append(data_row)

#myfile = open("results", 'w')

num_turns = len(split_data[0])-5
num_stocks = len(split_data)

print "num_turns = ", num_turns

#write stdin.txt for first turn
stdin_file = open("stdin.txt", 'w')

money = 100
file_line = str(money)

file_line += " " + str(num_stocks) + " " + str(num_turns) + "\n"
stdin_file.write(file_line)

name_list = []

for i in range(num_stocks):
    name_list.append(split_data[i][0])

owned_list = {name: 0 for name in name_list}
owned_list[name_list[0]] = 10

price_list = {arr[0]: arr for arr in split_data}

for i in range(num_stocks):
    file_line = split_data[i][0]  
    file_line += " " + str(owned_list[name_list[i]])

    for j in range(1,6):
        file_line += " " + str(split_data[i][j])
    file_line += "\n"
    stdin_file.write(file_line)

stdin_file.close()  #finished writing stdin

#loop through turns
for turn in range(num_turns):
    #print "turn number", turn+1
    stdout_file = open("stdout.txt", 'w')

    subprocess.call(['python', 'stocks.py'], stdout = stdout_file)  #call stocks.py

    stdout_file.close()

    #open stdout.txt so we can update amount of money we have and number of shares of stocks owned
    stdout_file = open("stdout.txt", 'r')


    for line in stdout_file:
        split_line = line.rstrip().split()

        if len(split_line) >= 3:

            if split_line[1] == "BUY":
                owned_list[split_line[0]] += int(split_line[2])
                money -= int(split_line[2]) * float(price_list[split_line[0]][turn+5])
                print turn, " buy ", split_line[0], " at ", price_list[split_line[0]][turn+5]
            else:
                owned_list[split_line[0]] -= int(split_line[2])
                money += int(split_line[2]) * float(price_list[split_line[0]][turn+5])
                print turn, " sell ", split_line[0], " at ", price_list[split_line[0]][turn+5]
                #print money, " += ", int(split_line[2]), " * ", float(price_list[split_line[0]][turn+5])

    stdout_file.close()

    print turn, ": ", money


    #write next stdin.txt if not last turn
    if turn < num_turns-1:
        stdin_file = open("stdin.txt", 'w')

        file_line = str(int(100*money)/100.0)

        file_line += " " + str(num_stocks) + " " + str(num_turns-turn-1) + "\n"
        stdin_file.write(file_line)

    
        for i in range(num_stocks):
            file_line = split_data[i][0]  
            file_line += " " + str(owned_list[split_data[i][0]])

            for j in range(turn+2,turn+7):
                file_line += " " + str(split_data[i][j])

            file_line += "\n"
            stdin_file.write(file_line)

        stdin_file.close()
