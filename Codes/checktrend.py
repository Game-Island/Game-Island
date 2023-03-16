import pandas as pd
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from pmdarima.arima import auto_arima
from statsmodels.tsa.holtwinters import Holt
data = pd.read_csv('https://raw.githubusercontent.com/Game-Island/Game-Island/main/data2.csv ')
# data = pd.read_csv('data2.csv')
data['Date'] = pd.to_datetime(data['Date'],dayfirst = True)
data['Start'] = pd.to_datetime(data['Start'])
data['End'] = pd.to_datetime(data['End'])
data['time_spent'] = (data['End'] - data['Start']).astype('timedelta64[m]')

daily_data = data.groupby(['Date']).sum()


model = Holt(daily_data).fit()

forecast = model.forecast(steps=7)
print(forecast)

fig, ax = plt.subplots(figsize=(8,4))

def close(event):
    path_timer = os.getcwd() + "/Timer.xlsx"
    os.remove(path_timer)

plt.Figure()
thismanager = plt.get_current_fig_manager()
# thismanager.window.wm_iconbitmap("graph_ico.ico")
# thismanager.window.setWindowIcon("graph_ico.ico")
thismanager.set_window_title('Graphs')
thismanager.canvas.mpl_connect('close_event',close)

fig.set_facecolor("#666666")
ax.set_facecolor("#666666")

ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')
ax.spines['top'].set_color('white')

ax.xaxis.label.set_color('black')
ax.yaxis.label.set_color('black')

ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

ax.plot(daily_data.index, daily_data, label='Actual')
ax.plot(forecast.index, forecast, label='Forecast')
ax.set_xlabel('Date')
ax.set_ylabel('Time Spent (minutes)')
ax.set_title('Holt\'s Linear Trend Model')
ax.legend()
plt.show()