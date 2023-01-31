#Aksje simulation med giring, henter live data fra aksjemarkedet, og viser gevinst/tap
import tkinter as tk
import yfinance as yf
import time
import threading

#Start Saldo 
balance = 1000


def main():
    #isLev er brukt til å sjekke om brukeren velger giring eller ikke
    isLev = False
    #Henter bruker data om hvordan aksje og hvor mye de vil investere 
    stock = stockEntry.get().upper()
    investment = int(investmentEntry.get())
    
    #Sjekker om investeringen er mer enn saldoen
    if investment > balance:
        livePriceLabel.config(text='Error: Not enough balance')
        return
    
    #Sjekker hvordan knapp brukeren valgte, selge eller kjøpe 
    if (var.get() == 1):
        type = "BUY"
    else:
        type = "SELL"
    
    #Sjekker om brukeren valgte giring knappen, og hvor mye giring brukeren vil ha
    if (var2.get() == 1):
        levAmount = int(levAmountEntry.get())
        isLev = True
    else:
        levAmount = 1
    
    #Laster ned aksje data og henter bare prisen, Bruker Aksje symbol for å hente data
    df = yf.download(stock, interval="1m")
    startPrice = df["Close"].iloc[-1]
    #Lager en thread for selve aksje kjøpet/salget, for å oppdatere UI 
    #og for å legge til muligheten til å kjøpe/selge flere aksjer senere 
    t = threading.Thread(target=trade, args=(
        investment, stock, type, levAmount, isLev, startPrice))
    t.start()


#Trading funksjonen som blir en thread
def trade(investment, stock, type, levAmount, isLev, startPrice):

    global balance
    while True:
        orBalance = balance
        #Laster ned aksje data og henter prisen hvert minutt
        df = yf.download(stock, interval="1m")
        livePrice = df["Close"].iloc[-1]
        #Differansen fra start prisen til aksjen og nå prisen, endres om man selger eller kjøper aksjen 
        if (type == 'BUY'):
            diff = livePrice/startPrice
        else:
            diff = startPrice/livePrice
        #Oppdatert saldo med giring eller uten
        if (isLev):
            balance = (balance - investment) + ((investment * levAmount * diff) -
                                                (investment * levAmount) + investment)
        else:
            balance = (balance - investment) + investment * diff
        #Viser oppdatert pris til UI 
        livePriceLabel.config(
            text=f'Live price: {round(livePrice, 2)}')
        #Hvis saldoen er mer nå så blir teksten grønn, og rød for motsatt
        if (balance > orBalance):
            balanceLabel.config(
                text=f'Balance: {round(balance, 2)}', fg='#0f0')
        elif (balance < orBalance):
            balanceLabel.config(
                text=f'Balance: {round(balance, 2)}', fg='#f00')
        time.sleep(60)


#GUI
root = tk.Tk()

stockLabel = tk.Label(root, text="Stock Symbol:")
stockLabel.grid(row=0, column=0)

stockEntry = tk.Entry(root)
stockEntry.grid(row=0, column=1)

investmentLabel = tk.Label(root, text="Investment:")
investmentLabel.grid(row=1, column=0)

investmentEntry = tk.Entry(root)
investmentEntry.grid(row=1, column=1)

var = tk.IntVar()
buyButton = tk.Radiobutton(root, text="Buy", variable=var, value=1)
buyButton.grid(row=2, column=0)

sellButton = tk.Radiobutton(root, text="Sell", variable=var, value=2)
sellButton.grid(row=2, column=1)

var2 = tk.IntVar()
leverage = tk.Radiobutton(root, text="Leverage", variable=var2, value=1)
leverage.grid(row=3, column=0)

levAmountLabel = tk.Label(root, text="Leverage Amount:")
levAmountLabel.grid(row=4, column=0)

levAmountEntry = tk.Entry(root)
levAmountEntry.grid(row=4, column=1)

livePriceLabel = tk.Label(root, text="Live price:")
livePriceLabel.grid(row=5, column=0)

balanceLabel = tk.Label(root, text="Balance:")
balanceLabel.grid(row=5, column=1)
balanceLabel.config(text=f'Balance: {balance}')

startButton = tk.Button(root, text="Start", command=main)
startButton.grid(row=6, column=0, columnspan=2)

root.mainloop()
