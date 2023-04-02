import csv
import matplotlib.pyplot as plt
import pandas as pd


def openCSV(samples, dates, name):
    with open(name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i, row in enumerate(reader):
            if i == 0:
                continue
            if i > 1000:
                break
            samples.append(row[2])
            dates.append(row[0])

def doPlot(samples, dates, MACD, SIGNAL, firma):
    dates = [date for date in dates]
    prices = [float(sample) for sample in samples]
    pricesMACD = [float(a) for a in MACD]
    pricesSIGNAL = [float(a) for a in SIGNAL]
    # Tworzenie wykresu
    plt.plot(dates, prices, label = "Akcje")
    plt.plot(dates, pricesSIGNAL, label = "SIGNAL")
    plt.plot(dates, pricesMACD, label="MACD")

    # Dodawanie tytułu i etykiet osi
    plt.title('Ceny akcji ' + firma)
    plt.xlabel('Data')
    plt.ylabel('Wartosc')
    plt.legend()

    # Ustawienie etykiet tylko dla lat
    plt.xticks([i for i, date in enumerate(dates) if date.endswith('09-01')])

    # Wyświetlanie wykresu
    plt.show()

    plt.plot(dates, pricesSIGNAL, label="SIGNAL")
    plt.plot(dates, pricesMACD, label="MACD")
    plt.title('Wskaźnik macd ' + firma)
    plt.xlabel('Data')
    plt.ylabel('Wartosc')
    plt.legend()
    plt.xticks([i for i, date in enumerate(dates) if date.endswith('09-01')])
    plt.show()


def calculateMACD(samples):
    EMA12 = calculateEMA(12, samples)
    EMA26 = calculateEMA(26, samples)
    MACD = []
    for i in range(0, len(EMA12)):
        MACD.append(EMA12[i] - EMA26[i])

    return MACD

def calculateEMA(N, samples):
    alpha = 2 / (N + 1)
    EMA = []
    curEMA1 = 0
    curEMA2 = 0
    for i in range(0, len(samples)):
        for j in range(0, N+1):
            if len(samples) <= i + j:
                continue
            curEMA1 += pow(1-alpha,j) * float(samples[i + j])
            curEMA2 += pow(1-alpha,j)
        EMA.append(curEMA1/curEMA2);
        curEMA1 = 0
        curEMA2 = 0

    return EMA

def calculateSIGNAL(MACD):
    SIGNAL = []
    SIGNAL = calculateEMA(9, MACD)
    return SIGNAL

def simulate(samples, MACD, SIGNAL, firma):
    money = 1000
    actions = 0
    print(firma)
    print("Start money: " + str(money))
    print("Start actions: " + str(actions))
    for i in range(0, len(samples)):
        if(MACD[i] <= SIGNAL[i] and MACD[i-1] > SIGNAL[i-1]):
            if(actions == 0):
                actions += money / float(samples[i])
                money = 0
                #print(actions)
        elif (MACD[i] >= SIGNAL[i] and MACD[i-1] < SIGNAL[i-1]):
            if(money == 0):
                money += actions * float(samples[i])
                actions = 0
                #print(money)

    money_rounded = round(money,2)
    actionsInMoney = round(actions*float(samples[len(samples)-1]),2)
    actionsRounded = round(actions,2)

    print("Current money: " + str(money_rounded))
    print("Current actions: " + str(actionsRounded))
    print("Current actions in money: " + str(actionsInMoney))
    print()

def makeMACD(csvName, companyName):
    samples = []
    MACD = []
    SIGNAL = []
    dates = []
    openCSV(samples, dates, csvName)
    MACD = calculateMACD(samples)
    SIGNAL = calculateSIGNAL(MACD)
    samples.reverse()  # odwraca wektor
    MACD.reverse()  # odwraca wektor
    SIGNAL.reverse()  # odwraca wektor
    dates.reverse()
    doPlot(samples, dates, MACD, SIGNAL, companyName)
    simulate(samples, MACD, SIGNAL, companyName)


if __name__ == '__main__':

    makeMACD("moneypl_Budimex.csv", "Budimex SA")
    makeMACD("moneypl_Millennium.csv", "Bank Millennium")
    makeMACD("moneypl_Apator.csv", "Apator SA")



    #for row in samples:
        #print(row)
    #for row in MACD:
        #print(row)
    #for row in SIGNAL:
        #print(row)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
