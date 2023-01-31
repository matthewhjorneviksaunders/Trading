import tkinter as tk
import yfinance as yf
import time
import threading

balance = 1000


def main():
    isLev = False
    stock = stockEntry.get().upper()
    investment = int(investmentEntry.get())

    if investment > balance:
        livePriceLabel.config(text='Error: Not enough balance')
        return

    if (var.get() == 1):
        type = "BUY"
    else:
        type = "SELL"

    if (var2.get() == 1):
        levAmount = int(levAmountEntry.get())
        isLev = True
    else:
        levAmount = 1

    df = yf.download(stock, interval="1m")
    startPrice = df["Close"].iloc[-1]
    t = threading.Thread(target=trade, args=(
        investment, stock, type, levAmount, isLev, startPrice))
    t.start()


def trade(investment, stock, type, levAmount, isLev, startPrice):

    global balance
    while True:
        orBalance = balance
        df = yf.download(stock, interval="1m")
        livePrice = df["Close"].iloc[-1]
        if (type == 'BUY'):
            diff = livePrice/startPrice
        else:
            diff = startPrice/livePrice
        if (isLev):
            balance = (balance - investment) + ((investment * levAmount * diff) -
                                                (investment * levAmount) + investment)
        else:
            balance = (balance - investment) + investment * diff
        livePriceLabel.config(
            text=f'Live price: {round(livePrice, 2)}')

        if (balance > orBalance):
            balanceLabel.config(
                text=f'Balance: {round(balance, 2)}', fg='#0f0')
        elif (balance < orBalance):
            balanceLabel.config(
                text=f'Balance: {round(balance, 2)}', fg='#f00')
        time.sleep(60)


# GUI
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
