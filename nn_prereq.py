# Arquivo de includes criado para ser usado no inicio de programas que usam
# sklearn, numpy, pandas etc

from pandas_datareader import data
import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
from matplotlib.dates import date2num
#from matplotlib.finance import candlestick_ohlc as candlestick
import datetime

from datetime import timedelta

import os
import pickle
import quandl

from pandas_datareader import data, wb
import pandas_datareader as pdr

from sklearn.neural_network import MLPRegressor
from sklearn import datasets
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split

