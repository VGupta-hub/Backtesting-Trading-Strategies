In this code, I have done a moving average analysis of a public listed company by taking its data from yahoo finance and calculating a 50-day simple moving average (SMA) and then plotting it on the graph to see when the price was above or below the 50-SMA.

import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

yf.pdr_override() #activate yahoo finance workaround
now = dt.datetime.now() #Runs until todays date
stock = input("Enter the stock ticker: ") #Query user for stock ticker

startyear = 2020
startmonth = 1
startday = 1
start = dt.datetime(startyear, startmonth, startday) # set starting time for datasample
now = dt.datetime.now()

df = pdr.get_data_yahoo(stock,start, now)
print(df)

Creating a list of moving averages

emasused = [3,5,8,10,12,15,30,35,40,45,50,60]
for x in emasused:
    ema = x
    df["Ema_" + str(ema)] = round(df.iloc[:,4].ewm(span=ema, adjust = False).mean(),2)
    
print(df.tail()) #prints last few values of our dataframe

Now we will check whether its a red white blue pattern at each date

pos = 0
num = 0
percent_change = []

for i in df.index:
    cmin = min(df["Ema_3"][i], df["Ema_5"][i], df["Ema_8"][i], df["Ema_10"][i], df["Ema_12"][i], df["Ema_15"][i])  #minimum of short term EMAs
    cmax = max(df["Ema_30"][i], df["Ema_35"][i], df["Ema_40"][i], df["Ema_45"][i], df["Ema_50"][i], df["Ema_60"][i]) #maximum of long term EMAs
    close = df["Adj Close"][i]
    
    if (cmin>cmax):
        print("Red White Blue")
        if(pos == 0):
            bp=round(close,2)
            pos=1
            print("Buying now at "+str(bp))
        
    elif(cmin<cmax):
        print("Blue White Red")
        if(pos==1):
            pos=0
            sp=round(close,2)
            print("Selling now at "+str(sp))
            pc = round(((sp/bp-1)*100),2)
            percent_change.append(pc)
    if (num == df["Adj Close"].count()-1 and pos == 1):
        pos=0
        sp=close
        print("Selling now at "+str(sp))
        pc = (sp/bp-1)*100
        percent_change.append(pc)
    
    num = num + 1
    
print(percent_change)
    

Simulating entry and exit of our trades



x = df.index
y = df["Adj Close"]
a = df["Ema_3"]
b = df["Ema_5"]
c = df["Ema_8"]
d = df["Ema_10"]
e = df["Ema_12"]
f = df["Ema_15"]
g = df["Ema_30"]
h = df["Ema_35"]
i = df["Ema_40"]
j = df["Ema_45"]
k = df["Ema_50"]
l = df["Ema_60"]

title = (stock, "Adjusted Close price till date and moving averages")

def df_plot(data, x, y, a, b, c, d, e, f, g, h, i, j, k, l, title="", xlabel = "Date", ylabel = "Adj Close", dpi =200):
    plt.figure(figsize=(16,5), dpi = dpi)
    plt.plot(x,y, color = "tab:blue")
    plt.plot(a, color = "tab:red")
    plt.plot(b, color = "tab:red")
    plt.plot(c, color = "tab:red")
    plt.plot(d, color = "tab:red")
    plt.plot(e, color = "tab:red")
    plt.plot(f, color = "tab:red")
    plt.plot(g, color = "tab:green")
    plt.plot(h, color = "tab:green")
    plt.plot(i, color = "tab:green")
    plt.plot(j, color = "tab:green")
    plt.plot(k, color = "tab:green")
    plt.plot(l, color = "tab:green")
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()

df_plot(df, x, y, a, b, c, d, e, f, g, h, i, j, k, l, title=title, xlabel = "Date", ylabel = "Adj Close", dpi =100)

gains = 0
ng = 0
losses = 0
nl = 0
totalR = 1
for i in percent_change:
    if i>0:
        gains = gains + i
        ng = ng + 1
    else:
        losses += i
        nl += 1
    totalR = totalR*((i/100)+1)

totalR = round((totalR-1)*100,2)

print("Gains: ", round(gains,2))
print("Net gain: ", ng)
print("Losses: ", round(losses,2))
print("Net loss: ", nl)
print("Total Return: ", totalR)

Finding the best trade

if(ng>0):
    avgGain=gains/ng
    maxR=str(max(percent_change))
    
else:
    avgGain=0
    maxR="undefined"
    
if(nl>0):
    avgLoss=losses/ng
    maxL=str(min(percent_change))
    ratio=str(-avgGain/avgLoss)
else:
    avgLoss=0
    maxL="undefined"
    ratio="infinite"
    

Calculating percentage of time a particular trade ended up in a gain

if(ng>0 or nl>0):
    battingAvg = ng/(ng+nl)
else:
    battingAvg = 0


print()
print("Results for "+ stock +" going back to "+str(df.index[0])+", Sample size: "+str(ng+nl)+" trades")
print("EMAs used: "+str(emasused))
print("Batting Avg: "+ str(battingAvg))
print("Gain/loss ratio: "+ ratio)
print("Average Gain: "+ str(avgGain))
print("Average Loss: "+ str(avgLoss))
print("Max Return: "+ maxR)
print("Max Loss: "+ maxL)
print("Total return over "+str(ng+nl)+ " trades: "+ str(totalR)+"%" )
#print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )
print()

