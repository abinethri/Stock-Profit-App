from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render
from .models import StockValues
from django.template import RequestContext
import datetime
from datetime import datetime
import requests
from requests.auth import HTTPDigestAuth
import json
import time
from chartit import DataPool, Chart
from googlefinance import getQuotes

maxStocksPerStrategy = 5

def index(request):
    
    return render(request, 'stockProfit/index.html')

def self(request):
    
    return render(request, 'stockProfit/chart1.html')


def update(request):
    id = eval("request." + request.method + "['id']")
    post = Post.objects(id=id)[0]
    
    if request.method == 'POST':
        # update field values and save to mongo
        post.title = request.POST['title']
        post.last_update = datetime.datetime.now() 
        post.content = request.POST['content']
        post.save()
        template = 'stockProfit/index.html'
        params = {'Posts': Post.objects} 

    elif request.method == 'GET':
        template = 'stockProfit/update.html'
        params = {'post':post}
   
    return render(request, template, params)
                              

def delete(request):
    id = request.POST.get('id')
    print "Print ID"
    print id;

    if request.method == 'POST':
        post = Post.objects(id=id)[0]
        post.delete() 
        template = 'stockProfit/index.html'
        params = {'Posts': Post.objects} 
    elif request.method == 'GET':
        template = 'stockProfit/delete.html'
        params = { 'id': id } 

    return render(request, template, params)

    return render(request, "stockProfit/home.html")

def home(request):
    return render(request, "stockProfit/home.html")

def chart(request):
    company = ['GOOG', 'AAPL', 'YHOO']
    
    for i in range(len(company)):
        stockValues = StockValues(company[i])

        url = "https://www.quandl.com/api/v3/datasets/WIKI/"+company[i]+".json?api_key=Qj3hVb4abNZYbdEFxp27"
        myResponse=requests.get(url)
        if(myResponse.ok):
            jData = json.loads(myResponse.content)
            stock_price = jData["dataset"]["data"][0][1]
            value_change = jData["dataset"]["data"][0][4]-jData["dataset"]["data"][0][1]
            percentage_change=(value_change/stock_price)*100
            name = jData["dataset"]["name"]
            print "Current date and time is "+time.strftime("%c")+time.strftime(" %Z")
            print "Company name is "+name
            print "Company stock price is ",stock_price
            print "Value change is ",value_change
            print "Percentage change  is ",percentage_change,"%"
            stockValues.name=name
            stockValues.price = stock_price
            stockValues.valuechange = value_change

            stockValues.save()
   
    return render(request, "stockProfit/charts.html") 

    

def historyData (request):


    symList  = ["GOOG", "AAPL", "JCI", "ADBE", "NVDA",
                 "QCOM", "CI", "TWX", "TMUS", "EXPE",
                 "CTSH", "KORS", "DKS", "NKE", "TSLA",
                 "COST", "AMZN", "NFLX", "XOM", "FB",
                 "GIS", "INTC", "CSCO", "WMT", "BA"]

    #symList = ["GOOG", "AAPL"]
    for j in range(len(symList)):
        company = symList[j]
        for i in range(5):

            url = "https://www.quandl.com/api/v3/datasets/WIKI/"+company+".json?api_key=Qj3hVb4abNZYbdEFxp27";
            myResponse=requests.get(url, verify= False)
            if(myResponse.ok):
                jData = json.loads(myResponse.content)
                date = jData["dataset"]["data"][i][0]
                dateObj = datetime.strptime(date, '%Y-%m-%d').date()
                stock_price = jData["dataset"]["data"][i][1]

                stockValues = StockValues()
                stockValues.date = dateObj;
                stockValues.name=jData["dataset"]["name"]
                stockValues.price = stock_price
                stockValues.ticker = company
                stockValues.save()
   
    return render(request, "stockProfit/historyData.html")

def queryDB(request):
    stock = StockValues.objects.filter(ticker__exact="GOOG").order_by('date')
    priceList = list()
    dateList = list()
    print "Number of elemnets returned is: ", len(stock)
    for i in range(len(stock)):
        p = stock[i].price
        d = stock[i].date.strftime('%m-%d-%Y')
        print "Date: "+d+ ":: Stock GOOG had the value ", d
        priceList.append(p)
        dateList.append(d)

    return render(request, "stockProfit/charts.html",{'priceList': priceList,'dateList': dateList})

def ethicalStrategy(request):
    perctDist= [0.30, 0.25, 0.20, 0.15 , 0.10]
    amount1 = request.POST['amount']
    #amount = 5000
    amount=float(amount1)
    stockList = ["GOOG", "AAPL", "JCI", "ADBE", "NVDA"]

    # priceList_i is 5 day values of a stock[i]
    priceList0 = list()
    priceList1 = list()
    priceList2 = list()
    priceList3 = list()
    priceList4 = list()
    portFolioList = list()
    dateList = list()

    for i in range(len(stockList)):
        ticker = stockList[i]
        stock = StockValues.objects.filter(ticker__exact=ticker).order_by('date')
        for j in range(len(stock)):
            p = stock[j].price
            d = stock[j].date.strftime('%m-%d-%Y')
            if i == 0:
                #print "Date: "+d+ ":: Stock GOOG had the value ", d
                priceList0.append(p)
                dateList.append(d)
            elif i == 1:
                priceList1.append(p)
            elif i == 2:
                priceList2.append(p)
            elif i == 3:
                priceList3.append(p)
            elif i == 4:
                priceList4.append(p)

    day = 4
    shareBought = [0,0,0,0,0]
    leftOverMoney = amount
    for rounds in range(5):
        temp = list()
        for snum in range(len(stockList)):
            if snum == 0:
                num = int((leftOverMoney * perctDist[snum]) / priceList0[day])
                temp.append(num)
            elif snum == 1:
                num = int((leftOverMoney * perctDist[snum]) / priceList1[day])
                temp.append(num)
            elif snum == 2:
                num = int((leftOverMoney * perctDist[snum]) / priceList2[day])
                temp.append(num)
            elif snum == 3:
                num = int((leftOverMoney * perctDist[snum]) / priceList3[day])
                temp.append(num)
            elif snum == 4:
                num = int((leftOverMoney * perctDist[snum]) / priceList4[day])
                temp.append(num)

        temp2 = [x + y for x, y in zip(shareBought, temp)]
        shareBought = temp2
        moneyInvested = shareBought[0] * priceList0[day] + shareBought[1] * priceList1[day] + \
                        shareBought[2] * priceList2[day] + shareBought[3] * priceList3[day] + \
                        shareBought[4] * priceList4[day]
        leftOverMoney = amount - moneyInvested

    # PF = Portfolio
    for day in range(5):
        valPF = 0
        for snum in range(len(shareBought)):
            if snum == 0:
                valPF = valPF + (shareBought[snum] * priceList0[day])
            elif snum == 1:
                valPF = valPF + (shareBought[snum] * priceList1[day])
            elif snum == 2:
                valPF = valPF + (shareBought[snum] * priceList2[day])
            elif snum == 3:
                valPF = valPF + (shareBought[snum] * priceList3[day])
            elif snum == 4:
                valPF = valPF + (shareBought[snum] * priceList4[day])

        portFolioList.append(valPF)

    return render(request, "stockProfit/ethical.html",{'priceList0': priceList0,
        'priceList1': priceList1,
        'priceList2': priceList2,
        'priceList3': priceList3,
        'priceList4': priceList4,
        'portFolioList': portFolioList,
        'shareBought':shareBought,
        'stockList':stockList,
        'dateList': dateList,
        'perctDist': perctDist})


def growthStrategy(request):
    perctDist= [0.20, 0.20, 0.20, 0.20 , 0.20]
    #amount = request.POST['amount']
    amount1 = request.POST['amount']
    #amount = 5000
    amount=float(amount1)

    stockList = ["CTSH", "KORS", "DKS", "NKE", "TSLA",]

    # priceList_i is 5 day values of a stock[i]
    priceList0 = list()
    priceList1 = list()
    priceList2 = list()
    priceList3 = list()
    priceList4 = list()
    portFolioList = list()
    dateList = list()

    for i in range(len(stockList)):
        ticker = stockList[i]
        stock = StockValues.objects.filter(ticker__exact=ticker).order_by('date')
        for j in range(len(stock)):
            p = stock[j].price
            d = stock[j].date.strftime('%m-%d-%Y')
            if i == 0:
                #print "Date: "+d+ ":: Stock GOOG had the value ", d
                priceList0.append(p)
                dateList.append(d)
            elif i == 1:
                priceList1.append(p)
            elif i == 2:
                priceList2.append(p)
            elif i == 3:
                priceList3.append(p)
            elif i == 4:
                priceList4.append(p)

    day = 4
    shareBought = [0,0,0,0,0]
    leftOverMoney = amount
    for rounds in range(5):
        temp = list()
        for snum in range(len(stockList)):
            if snum == 0:
                num = int((leftOverMoney * perctDist[snum]) / priceList0[day])
                temp.append(num)
            elif snum == 1:
                num = int((leftOverMoney * perctDist[snum]) / priceList1[day])
                temp.append(num)
            elif snum == 2:
                num = int((leftOverMoney * perctDist[snum]) / priceList2[day])
                temp.append(num)
            elif snum == 3:
                num = int((leftOverMoney * perctDist[snum]) / priceList3[day])
                temp.append(num)
            elif snum == 4:
                num = int((leftOverMoney * perctDist[snum]) / priceList4[day])
                temp.append(num)

        temp2 = [x + y for x, y in zip(shareBought, temp)]
        shareBought = temp2
        moneyInvested = shareBought[0] * priceList0[day] + shareBought[1] * priceList1[day] + \
                        shareBought[2] * priceList2[day] + shareBought[3] * priceList3[day] + \
                        shareBought[4] * priceList4[day]
        leftOverMoney = amount - moneyInvested


    # PF = Portfolio
    for day in range(5):
        valPF = 0
        for snum in range(len(shareBought)):
            if snum == 0:
                valPF = valPF + (shareBought[snum] * priceList0[day])
            elif snum == 1:
                valPF = valPF + (shareBought[snum] * priceList1[day])
            elif snum == 2:
                valPF = valPF + (shareBought[snum] * priceList2[day])
            elif snum == 3:
                valPF = valPF + (shareBought[snum] * priceList3[day])
            elif snum == 4:
                valPF = valPF + (shareBought[snum] * priceList4[day])

        portFolioList.append(valPF)

    return render(request, "stockProfit/growth.html",{'priceList0': priceList0,
        'priceList1': priceList1,
        'priceList2': priceList2,
        'priceList3': priceList3,
        'priceList4': priceList4,
        'portFolioList': portFolioList,
        'shareBought':shareBought,
        'stockList':stockList,
        'dateList': dateList,
        'perctDist': perctDist})

def indexStrategy(request):
    perctDist= [0.30, 0.30, 0.20, 0.10 , 0.10]
    amount1 = request.POST['amount']
    #amount = 5000
    amount=float(amount1)

    stockList = [ "COST", "AMZN", "NFLX", "XOM", "FB"]

    # priceList_i is 5 day values of a stock[i]
    priceList0 = list()
    priceList1 = list()
    priceList2 = list()
    priceList3 = list()
    priceList4 = list()
    portFolioList = list()
    dateList = list()

    for i in range(len(stockList)):
        ticker = stockList[i]
        stock = StockValues.objects.filter(ticker__exact=ticker).order_by('date')
        for j in range(len(stock)):
            p = stock[j].price
            d = stock[j].date.strftime('%m-%d-%Y')
            if i == 0:
                #print "Date: "+d+ ":: Stock GOOG had the value ", d
                priceList0.append(p)
                dateList.append(d)
            elif i == 1:
                priceList1.append(p)
            elif i == 2:
                priceList2.append(p)
            elif i == 3:
                priceList3.append(p)
            elif i == 4:
                priceList4.append(p)

    day = 4
    shareBought = [0,0,0,0,0]
    leftOverMoney = amount
    for rounds in range(5):
        temp = list()
        for snum in range(len(stockList)):
            if snum == 0:
                num = int((leftOverMoney * perctDist[snum]) / priceList0[day])
                temp.append(num)
            elif snum == 1:
                num = int((leftOverMoney * perctDist[snum]) / priceList1[day])
                temp.append(num)
            elif snum == 2:
                num = int((leftOverMoney * perctDist[snum]) / priceList2[day])
                temp.append(num)
            elif snum == 3:
                num = int((leftOverMoney * perctDist[snum]) / priceList3[day])
                temp.append(num)
            elif snum == 4:
                num = int((leftOverMoney * perctDist[snum]) / priceList4[day])
                temp.append(num)

        temp2 = [x + y for x, y in zip(shareBought, temp)]
        shareBought = temp2
        moneyInvested = shareBought[0] * priceList0[day] + shareBought[1] * priceList1[day] + \
                        shareBought[2] * priceList2[day] + shareBought[3] * priceList3[day] + \
                        shareBought[4] * priceList4[day]
        leftOverMoney = amount - moneyInvested


    # PF = Portfolio
    for day in range(5):
        valPF = 0
        for snum in range(len(shareBought)):
            if snum == 0:
                valPF = valPF + (shareBought[snum] * priceList0[day])
            elif snum == 1:
                valPF = valPF + (shareBought[snum] * priceList1[day])
            elif snum == 2:
                valPF = valPF + (shareBought[snum] * priceList2[day])
            elif snum == 3:
                valPF = valPF + (shareBought[snum] * priceList3[day])
            elif snum == 4:
                valPF = valPF + (shareBought[snum] * priceList4[day])

        portFolioList.append(valPF)

    return render(request, "stockProfit/indexInvesting.html",{'priceList0': priceList0,
        'priceList1': priceList1,
        'priceList2': priceList2,
        'priceList3': priceList3,
        'priceList4': priceList4,
        'portFolioList': portFolioList,
        'shareBought':shareBought,
        'stockList':stockList,
        'dateList': dateList,
        'perctDist': perctDist})

def valueStrategy(request):
    perctDist= [0.20, 0.20, 0.20, 0.20 , 0.20]
    amount1 = request.POST['amount']
    #amount = 5000
    amount=float(amount1)

    stockList = ["QCOM", "CI", "TWX", "TMUS", "EXPE"]

    # priceList_i is 5 day values of a stock[i]
    priceList0 = list()
    priceList1 = list()
    priceList2 = list()
    priceList3 = list()
    priceList4 = list()
    portFolioList = list()
    dateList = list()

    for i in range(len(stockList)):
        ticker = stockList[i]
        stock = StockValues.objects.filter(ticker__exact=ticker).order_by('date')
        for j in range(len(stock)):
            p = stock[j].price
            d = stock[j].date.strftime('%m-%d-%Y')
            if i == 0:
                #print "Date: "+d+ ":: Stock GOOG had the value ", d
                priceList0.append(p)
                dateList.append(d)
            elif i == 1:
                priceList1.append(p)
            elif i == 2:
                priceList2.append(p)
            elif i == 3:
                priceList3.append(p)
            elif i == 4:
                priceList4.append(p)

    day = 4
    shareBought = [0,0,0,0,0]
    leftOverMoney = amount
    for rounds in range(5):
        temp = list()
        for snum in range(len(stockList)):
            if snum == 0:
                num = int((leftOverMoney * perctDist[snum]) / priceList0[day])
                temp.append(num)
            elif snum == 1:
                num = int((leftOverMoney * perctDist[snum]) / priceList1[day])
                temp.append(num)
            elif snum == 2:
                num = int((leftOverMoney * perctDist[snum]) / priceList2[day])
                temp.append(num)
            elif snum == 3:
                num = int((leftOverMoney * perctDist[snum]) / priceList3[day])
                temp.append(num)
            elif snum == 4:
                num = int((leftOverMoney * perctDist[snum]) / priceList4[day])
                temp.append(num)

        temp2 = [x + y for x, y in zip(shareBought, temp)]
        shareBought = temp2
        moneyInvested = shareBought[0] * priceList0[day] + shareBought[1] * priceList1[day] + \
                        shareBought[2] * priceList2[day] + shareBought[3] * priceList3[day] + \
                        shareBought[4] * priceList4[day]
        leftOverMoney = amount - moneyInvested


    # PF = Portfolio
    for day in range(5):
        valPF = 0
        for snum in range(len(shareBought)):
            if snum == 0:
                valPF = valPF + (shareBought[snum] * priceList0[day])
            elif snum == 1:
                valPF = valPF + (shareBought[snum] * priceList1[day])
            elif snum == 2:
                valPF = valPF + (shareBought[snum] * priceList2[day])
            elif snum == 3:
                valPF = valPF + (shareBought[snum] * priceList3[day])
            elif snum == 4:
                valPF = valPF + (shareBought[snum] * priceList4[day])

        portFolioList.append(valPF)

    return render(request, "stockProfit/value.html",{'priceList0': priceList0,
        'priceList1': priceList1,
        'priceList2': priceList2,
        'priceList3': priceList3,
        'priceList4': priceList4,
        'portFolioList': portFolioList,
        'shareBought':shareBought,
        'stockList':stockList,
        'dateList': dateList,
        'perctDist': perctDist})

def qualityStrategy(request):
    perctDist= [0.30, 0.30, 0.20, 0.10 , 0.10]
    amount1 = request.POST['amount']
    #amount = 5000
    amount=float(amount1)

    stockList = [ "GIS", "INTC", "CSCO", "WMT", "BA"]

    # priceList_i is 5 day values of a stock[i]
    priceList0 = list()
    priceList1 = list()
    priceList2 = list()
    priceList3 = list()
    priceList4 = list()
    portFolioList = list()
    dateList = list()

    for i in range(len(stockList)):
        ticker = stockList[i]
        stock = StockValues.objects.filter(ticker__exact=ticker).order_by('date')
        for j in range(len(stock)):
            p = stock[j].price
            d = stock[j].date.strftime('%m-%d-%Y')
            if i == 0:
                #print "Date: "+d+ ":: Stock GOOG had the value ", d
                priceList0.append(p)
                dateList.append(d)
            elif i == 1:
                priceList1.append(p)
            elif i == 2:
                priceList2.append(p)
            elif i == 3:
                priceList3.append(p)
            elif i == 4:
                priceList4.append(p)

    day = 4
    shareBought = [0,0,0,0,0]
    leftOverMoney = amount
    for rounds in range(5):
        temp = list()
        for snum in range(len(stockList)):
            if snum == 0:
                num = int((leftOverMoney * perctDist[snum]) / priceList0[day])
                temp.append(num)
            elif snum == 1:
                num = int((leftOverMoney * perctDist[snum]) / priceList1[day])
                temp.append(num)
            elif snum == 2:
                num = int((leftOverMoney * perctDist[snum]) / priceList2[day])
                temp.append(num)
            elif snum == 3:
                num = int((leftOverMoney * perctDist[snum]) / priceList3[day])
                temp.append(num)
            elif snum == 4:
                num = int((leftOverMoney * perctDist[snum]) / priceList4[day])
                temp.append(num)

        temp2 = [x + y for x, y in zip(shareBought, temp)]
        shareBought = temp2
        moneyInvested = shareBought[0] * priceList0[day] + shareBought[1] * priceList1[day] + \
                        shareBought[2] * priceList2[day] + shareBought[3] * priceList3[day] + \
                        shareBought[4] * priceList4[day]
        leftOverMoney = amount - moneyInvested


    # PF = Portfolio
    for day in range(5):
        valPF = 0
        for snum in range(len(shareBought)):
            if snum == 0:
                valPF = valPF + (shareBought[snum] * priceList0[day])
            elif snum == 1:
                valPF = valPF + (shareBought[snum] * priceList1[day])
            elif snum == 2:
                valPF = valPF + (shareBought[snum] * priceList2[day])
            elif snum == 3:
                valPF = valPF + (shareBought[snum] * priceList3[day])
            elif snum == 4:
                valPF = valPF + (shareBought[snum] * priceList4[day])

        portFolioList.append(valPF)

    return render(request, "stockProfit/quality.html",{'priceList0': priceList0,
        'priceList1': priceList1,
        'priceList2': priceList2,
        'priceList3': priceList3,
        'priceList4': priceList4,
        'portFolioList': portFolioList,
        'shareBought':shareBought,
        'stockList':stockList,
        'dateList': dateList,
        'perctDist': perctDist})


def displayCurrVal(request):

    stockList = "GOOG"
    shareBought = 10

    currVal0 = list()
    ticker = stockList
    stock = LiveDataValue.objects(symbol=ticker).order_by('-date')
    print "Is this ready"

    for j in range(5):
        p = stock[j].price
        currVal0.append(p)

    print currVal0
    return render(request, "stockProfit/charts.html",{'priceList': currVal0})

def getCurStockPrice(symbol):
    try:
        data = getQuotes(symbol)
        stock_price = float(data[0]['LastTradeWithCurrency'])
        return stock_price
    except:
        return 0.0

def livePortFolio(request):
    stockList = request.POST.get('stockList')
    shareBought = request.POST.get('shareBought')

    stocks = stockList.split(',')
    numShares = shareBought.split(',')

    curPortfolioVal = list()
    portfolioVal = 0;
    for idx in range(maxStocksPerStrategy):
        curStockPrice = getCurStockPrice(stocks[idx])
        portfolioVal = portfolioVal + (float(numShares[idx]) * curStockPrice)
    curPortfolioVal.append(portfolioVal)

    return render(request, "stockProfit/livePortFolio.html",{'currValPF':curPortfolioVal})



