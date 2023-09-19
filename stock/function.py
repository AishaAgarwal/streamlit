import numpy as np 
import yfinance as yf
import streamlit as st
import pandas as pd 
import plotly.graph_objs as go
from datetime import date, timedelta
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

def prediction(stock, n_days, selected_option):
    a = selected_option + "_scaled"
    df = yf.download(stock, period= '60d')
    df.reset_index(inplace =True)

    if df.empty:
        st.write("No data available for the selected stock")
        return 
    
    scaler = MinMaxScaler()
    df[a] = scaler.fit_transform(df[[selected_option]])

    X = df[[a]].values 
    Y = df[[a]].shift(-1).fillna(method='bfill').values

    x_train, x_test = X[:-n_days], X[-n_days:]
    y_train, y_test = Y[:-n_days], Y[-n_days:]

    x_train = x_train.reshape(x_train.shape[0], 1, x_train.shape[1])
    x_test = x_test.reshape(x_test.shape[0], 1, x_test.shape[1])

    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(1, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, epochs=50, batch_size=1)

    predicted_scaled = model.predict(x_test)

    predicted = scaler.inverse_transform(predicted_scaled)

    dates = [date.today() + timedelta(days=i) for i in range(n_days)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=predicted.flatten(), mode='lines+markers', name='predicted'))
    fig.update_layout(title="Predicted " + selected_option + " Price of Next " + str(n_days) + " Days",
                      xaxis_title="Date", yaxis_title=selected_option + " Price")
    
    st.plotly_chart(fig)
