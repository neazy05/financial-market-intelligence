"""Experimental LSTM stock-return classification from the graduation project.

Research prototype only. This script is preserved for review, not presented as
a validated trading model. See README.md for limitations.
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 09:06:31 2022

@author: ASUS sa3d
"""
import torch
import numpy as np
import pandas as pd
import torch.nn as nn


import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def get_price_history(ticker, sdate, edate):
    # data = []
    data = yf.download(ticker, start=sdate, end=edate, interval="1d")
    return (data)

omx = ['ABB', 'ALFA.ST', 'ALIV-SDB.ST', 'ASSA-B.ST', 'ATCO-A.ST', 'ATCO-B.ST',
 'AZN.ST', 'BOL.ST', 'ELUX-B.ST', 'ERIC-B.ST', 'ESSITY-B.ST', 'EVO.ST',
 'GETI-B.ST', 'HEXA-B.ST', 'HM-B.ST', 'INVE-B.ST', 'KINV-B.ST', 'NDA-SE.ST',
 'SAND.ST', 'SCA-B.ST', 'SEB-A.ST', 'SECU-B.ST', 'SHB-A.ST', 'SKA-B.ST',
 'SKF-B.ST', 'SWED-A.ST', 'SWMA.ST', 'TEL2-B.ST', 'TELIA.ST', 'VOLV-B.ST']

ndaq = ["AAPL", "MSFT", "AMZN", "GOOG", "FB", "TSLA", "GOOGL", "NVDA", "PYPL", 
        "CMCSA", "ADBE", "INTC", "CSCO", "NFLX", "PEP", "AVGO", "TXN","TMUS", 
        "COST", "QCOM", "AMGN", "CHTR", "SBUX", "INTU", "AMAT", "ISRG",
        "BKNG", "AMD", "MU", "MDLZ", "LRCX"]

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class RNN(nn.Module):
  def __init__(self, n_inputs, n_hidden, n_rnnlayers, n_outputs):
    super(RNN, self).__init__()
    self.D = n_inputs
    self.M = n_hidden
    self.K = n_outputs
    self.L = n_rnnlayers

    self.rnn = nn.LSTM(
        input_size=self.D,
        hidden_size=self.M,
        num_layers=self.L,
        batch_first=True
        )
    self.fc = nn.Linear(self.M, self.K)
  
  def forward(self, X):
    h0 = torch.zeros(self.L, X.size(0), self.M).to(device)
    c0 = torch.zeros(self.L, X.size(0), self.M).to(device)
    out, _ = self.rnn(X, (h0, c0))
    return self.fc(out[:, -1, :])

def full_gradient_descent(model,
            criterion,
            optimizer,
            X_train,
            y_train,
            X_test,
            y_test,
            epochs=200):
  train_losses = np.zeros(epochs)
  test_losses = np.zeros(epochs)

  for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
      
    # Backward and optimize
    loss.backward()
    optimizer.step()

    # Save losses
    train_losses[epoch] = loss.item()

    # Test loss
    test_outputs = model(X_test)
    test_loss = criterion(test_outputs, y_test)
    test_losses[epoch] = test_loss.item()
      
    if (epoch + 1) % 5 == 0:
      print(f'Epoch {epoch+1}/{epochs}, Train Loss: {loss.item():.4f}, Test Loss: {test_loss.item():.4f}')
  
  return train_losses, test_losses

def train_and_test (ticker):
  # Get data
  df = get_price_history(ticker, '2011-01-01', '2021-01-01')

  # Compute returns for each day
  df['PrevClose'] = df['Close'].shift(1)
  df['Return'] = (df['Close'] - df['PrevClose']) / df['PrevClose']
  series = df['Return'].values[1:].reshape(-1, 1)
  df.dropna(inplace=True)

  # Define x and y
  input = df[['Open', 'High', 'Low', 'Close', 'Volume']].values
  targets = df['Return'].values

  T = 30 # the number of days will be included in our sliding window
  D = input.shape[1]

  N = len(input) - T # The number of windows in the dataset
  Ntrain = len(input) * 2 // 3

  scaler = StandardScaler()
  scaler.fit(input[:Ntrain + T - 1])
  input = scaler.transform(input)

  # Split the data into a train and test dataset
  X_train = np.zeros((Ntrain, T, D))
  Y_train = np.zeros((Ntrain, 1))

  for t in range(Ntrain):
    X_train[t, :, :] = input[t:t+T]
    Y_train[t] = (targets[t+T] > 0)

  X_test = np.zeros((N - Ntrain, T, D))
  Y_test = np.zeros((N - Ntrain, 1))

  for u in range(N - Ntrain):
    t = u + Ntrain
    X_test[u, :, :] = input[t:t+T]
    Y_test[u] = (targets[t+T] > 0)

  # Instantiate the neural network
  model = RNN(5, 50, 2, 1)
  model.to(device)

  # Use Binary Cross Entropy With Logits loss as loss function
  criterion = nn.BCEWithLogitsLoss()

  # Use the Adam Optimizer with learning rate of 1e-2
  optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

  # Transform inputs and targets
  X_train = torch.from_numpy(X_train.astype(np.float32))
  y_train = torch.from_numpy(Y_train.astype(np.float32))
  X_test = torch.from_numpy(X_test.astype(np.float32))
  y_test = torch.from_numpy(Y_test.astype(np.float32))

  # Move the test and train datasets to device
  X_train, y_train = X_train.to(device), y_train.to(device)
  X_test, y_test = X_test.to(device), y_test.to(device)

  # Start training
  train_losses, test_losses = full_gradient_descent(model,
                                    criterion,
                                    optimizer,
                                    X_train,
                                    y_train,
                                    X_test,
                                    y_test,
                                    epochs=300)
  
  with torch.no_grad():
    p_test = model(X_test)
    p_test = (p_test.cpu().numpy() > 0.0)
    targets = y_test.cpu().numpy() > 0.0

    # Get number of positive and negative samples and distribution
    number_of_positives = np.count_nonzero(y_test.cpu().numpy())
    number_of_samples = y_test.cpu().numpy().size
    ratio_positives = number_of_positives / number_of_samples

    # Measure accuracy on test data
    test_acc = np.mean(y_test.cpu().numpy() == p_test)
    print("Accuracy:", test_acc)

    # Count true and false positives and negatives
    tp, tn, fp, fn = 0, 0, 0, 0
    for i in range (0, len(targets)):
      if p_test[i] and targets[i][0]:
        tp += 1
      elif p_test[i] and not targets[i][0]:
        fp += 1
      elif not p_test[i] and targets[i][0]:
        fn += 1
      else:
        tn += 1

    # Compute precision and recall
    precision = tp / ((tp + fp) if (tp + fp) > 0 else 1)
    recall = tp / (tp + fn)
    print("Precision:", precision, "Recall:", recall)

    # The following block is only used to output the result as a CSV into Google Drive,
    # Adjust the file path to your own liking if you choose to use it
    # with open('/content/gdrive/My Drive/arbete/{ticker}.csv'.format(ticker=ticker), 'w') as writefile:
    #   writefile.write("Accuracy,Precision,Recall,Positive ratio,Data Length\n")
    #   writefile.write("{accuracy},{precision},{recall},{ratio_positives},{length}".format(accuracy=test_acc, precision=precision, recall=recall, ratio_positives=ratio_positives, length=len(df), ))
    
    
for t in ndaq:
  train_and_test(t)
for t in omx:
  train_and_test(t)