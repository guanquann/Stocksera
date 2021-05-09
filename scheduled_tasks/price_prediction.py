import numpy as np
# import matplotlib.pyplot as plt
import yfinance.ticker as yf
import pandas as pd
import itertools
import datetime
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout


def get_stock_data(ticker):
    ticker = yf.Ticker(ticker)
    df = ticker.history(period="5y", interval="1d")
    df = df.reset_index()
    del df["Dividends"]
    del df["Stock Splits"]

    train_data = df.head(int(len(df) * 0.95))
    test_data = df.tail(int(len(df) * 0.05))

    # taking open price from data in 2d array , if we will do train.loc[:, 'open'].values it gives one d array
    # which wont be considered in scaling
    train_open = train_data.iloc[:, 1:2].values

    # Scaling the values between 0 to 1
    ss = MinMaxScaler(feature_range=(0, 1))
    train_open_scaled = ss.fit_transform(train_open)

    print(train_open_scaled[60])

    # Feature selection
    xtrain = []
    ytrain = []
    for i in range(60, len(train_open_scaled)):
        xtrain.append(train_open_scaled[i - 60:i, 0])
        ytrain.append(train_open_scaled[i, 0])

    xtrain, ytrain = np.array(xtrain), np.array(ytrain)

    # Reshaping the train data to make it as input for LTSM layer input_shape(batchzise,timesteps,input_dim)
    xtrain = np.reshape(xtrain, (xtrain.shape[0], xtrain.shape[1], 1))

    print(xtrain.shape)

    # initialisizng the model
    regression = Sequential()

    # First Input layer and LSTM layer with 0.2% dropout
    regression.add(
        LSTM(units=50, return_sequences=True, kernel_initializer='glorot_uniform', input_shape=(xtrain.shape[1], 1)))
    regression.add(Dropout(0.2))

    # Where:
    #     return_sequences: Boolean. Whether to return the last output in the output sequence, or the full sequence.

    # Second LSTM layer with 0.2% dropout
    regression.add(LSTM(units=50, kernel_initializer='glorot_uniform', return_sequences=True))
    regression.add(Dropout(0.2))

    # Third LSTM layer with 0.2% dropout
    regression.add(LSTM(units=50, kernel_initializer='glorot_uniform', return_sequences=True))
    regression.add(Dropout(0.2))

    # Fourth LSTM layer with 0.2% dropout, we wont use return sequence true in last layers as we dont want to previous output
    regression.add(LSTM(units=50, kernel_initializer='glorot_uniform'))
    regression.add(Dropout(0.2))
    # Output layer , we wont pass any activation as its continous value model
    regression.add(Dense(units=1))

    # Compiling the network
    regression.compile(optimizer='adam', loss='mean_squared_error')

    # fitting the network
    regression.fit(xtrain, ytrain, batch_size=30, epochs=100)

    test_open = test_data.iloc[:, 1:2].values  # taking  open price
    total = pd.concat([train_data['Open'], test_data['Open']],
                      axis=0)  # Concating train and test and then will take last 60 train point
    test_input = total[len(total) - len(test_data) - 60:].values
    test_input = test_input.reshape(-1, 1)  # reshaping it to get it transformed
    test_input = ss.transform(test_input)

    xtest = []
    for i in range(60, 80):
        xtest.append(test_input[i - 60:i, 0])  # creating input for lstm prediction





    return df




get_stock_data("GME")