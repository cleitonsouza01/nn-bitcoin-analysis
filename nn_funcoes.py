from nn_prereq import *

########################################
#
# USEFUL FUNCTIONS TO DATA ANALYSIS
# created by Cleiton Souza (cleitonsouza01@gmail.com)
#

########################################
# DOWNLOAD DATA FUNCTIONS
today_date = datetime.datetime.now().strftime('%Y-%m-%d')

def get_data_local(market, tickInterval):
    cachefile_with_path = r'bittrex/{}/{}-{}.csv'.format(tickInterval.lower(), market, tickInterval)
    
    try:
        df = pd.DataFrame.from_csv(cachefile_with_path)
        print('Arquivo \'{}\' aberto com sucesso!'.format(cachefile_with_path))
    except ValueError:
        print('ERRO {}'.format(ValueError))
        
    return df


def get_data(symbol, source='quandl', janela='day', start_date='2010-01-01', end_date=today_date):
    '''
        Gets data from sources using pandas_datareader
    '''
    import pathlib
    if source == 'local':
        return get_data_local(symbol, janela)
    
    file = '{}-{}-{}_{}.pkl'.format(source.upper(), symbol, start_date, end_date).replace('/','-')
    data_dir_name = 'DATA'
    cachefile_with_path = os.path.join(data_dir_name, file)
    
    # If not exist directory create it to store datas        
    if not os.path.isdir(data_dir_name):
        import errno
        try:
            pathlib.Path(data_dir_name).mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass
    try:
        f = open(cachefile_with_path, 'rb')
        df = joblib.load(cachefile_with_path)
        print('Loaded {} from cache {}'.format(symbol, cachefile_with_path))
    except (IOError,OSError):
        print('Downloading {} from {} to {}'.format(symbol, source, cachefile_with_path) )
        df = data.DataReader(symbol, source, start_date, end_date)
        joblib.dump(df, cachefile_with_path)
        print('Cached {} at {}'.format(symbol, cachefile_with_path))
    return df


def tech_analisys(OHLCV, indicators, setup):
    open = OHLCV['open']
    high = OHLCV['high']
    low = OHLCV['low']
    close = OHLCV['close']
    volume = OHLCV['volume']

    analysis = pd.DataFrame(index= OHLCV['df_index'])

    #####################
    # Overlap Studies
    if 'bbands_uppper' in indicators:
        BBANDS_PERIOD = setup['BBANDS_PERIOD']
        analysis['bbands_uppper'], analysis['bbands_middle'], analysis['bbands_lower'] = ta.BBANDS(close, timeperiod=BBANDS_PERIOD, nbdevup=2, nbdevdn=2, matype=0)
    
    if 'sma_f' in indicators:
        SMA_FAST = setup['SMA_FAST']
        analysis['sma_f'] = ta.EMA(close, SMA_FAST)
    
    if 'sma_s' in indicators:
        SMA_SLOW = setup['SMA_SLOW']
        analysis['sma_s'] = ta.SMA(close, SMA_SLOW)

    if 'sma_100' in indicators:
        analysis['sma_100'] = ta.SMA(close, 100)

    if 'sma_200' in indicators:
        analysis['sma_200'] = ta.SMA(close, 200)

    if 'tema' in indicators: 
        TEMA_PERIOD = setup['TEMA_PERIOD']  
        analysis['tema'] = ta.TEMA(close, TEMA_PERIOD)
    

    #####################
    # Momentum Indicators
    if 'macd' in indicators: 
        MACD_FAST = setup['MACD_FAST'] 
        MACD_SLOW = setup['MACD_SLOW'] 
        MACD_SIGNAL = setup['MACD_SIGNAL'] 
        analysis['macd'], analysis['macdSignal'], analysis['macdHist'] = ta.MACD(close, fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)


    #####################
    # Volume Indicators


    #####################
    # Volatility Indicators
    if 'std_deviation' in indicators:
        STD_PERIOD = setup['STD_PERIOD'] 
        analysis['std_deviation'] = ta.STDDEV(close, STD_PERIOD, nbdev=1)


    #####################
    # Price Transform
    if 'price_weight' in indicators:
        analysis['price_weight'] = ta.WCLPRICE(high, low, close)


    #####################
    # Pattern Recognition


    #####################
    # Math Transform


    #####################
    # Test indicators
    

    return analysis

