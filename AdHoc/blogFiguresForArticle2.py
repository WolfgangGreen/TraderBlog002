import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ReportProcessing.intradayDetailReport import read_intraday_details_report, extract_symbol_details
from ReportProcessing.dailySummaryReport import read_daily_summary
from Util.pathsAndStockSets import set_stock_set, StockSet
from Util.datesAndTimestamps import timestamp

set_stock_set(StockSet.DEVELOPMENT)

# Show each symbol as a single timeline (daily resolution)
if False:
    df = read_daily_summary()
    scaled_df = pd.DataFrame()
    for symbol in df['symbol'].unique():
        symbol_df = df[df['symbol'] == symbol].copy()
        symbol_df['open'] /= symbol_df['open'].iloc[0]
        scaled_df = pd.concat([scaled_df, symbol_df])
    fig = px.line(scaled_df, x='date', y='open', color='symbol')
    fig.show()

# Show each symbol as a single timeline (5-minute resolution) -- add slider -- WORKS!
if False:
    df = read_intraday_details_report(timestamp('2024-06-03'))
    scaled_df = pd.DataFrame()
    fig = go.Figure()
    for symbol in df['symbol'].unique():
        symbol_df = df[df['symbol'] == symbol].copy()
        symbol_df['open'] /= symbol_df['open'].iloc[0]
        scaled_df = pd.concat([scaled_df, symbol_df])
        fig.add_trace(go.Scatter(x=symbol_df['timestamp'], y=symbol_df['open']))
    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True), type='date'))
    fig.show()

# Candlestick Chart
if False:
    df = read_intraday_details_report(timestamp('2024-06-03'))
    symbol_details = extract_symbol_details(df, 'TSLA')
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.3,
                        subplot_titles=('Bars', 'Volume'), row_width=[0.2, 0.5])
    fig.add_trace(go.Candlestick(x=symbol_details['timestamp'], open=symbol_details['open'],
                                 high=symbol_details['high'], low=symbol_details['low'],
                                 close=symbol_details['close']),
                  row=1, col=1)
    fig.add_trace(go.Bar(x=symbol_details['timestamp'], y=symbol_details['volume'], showlegend=False),
                  row=2, col=1)
    fig.show()

if True:
    symbol = 'TSLA'
    df = read_intraday_details_report(timestamp('2024-06-03'))
    symbol_details = extract_symbol_details(df, symbol)
    candlesticks = go.Candlestick(x=symbol_details['timestamp'], open=symbol_details['open'],
                                  high=symbol_details['high'], low=symbol_details['low'],
                                  close=symbol_details['close'], name=symbol)
    volume_bars = go.Bar(x=symbol_details['timestamp'], y=symbol_details['volume'], showlegend=False,
                         marker={'color': 'rgba(128,128,128,0.25)'})
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(candlesticks, secondary_y=False)
    fig.add_trace(volume_bars, secondary_y=True)
    fig.update_yaxes(secondary_y=False, title='Price', showgrid=False)
    fig.update_yaxes(secondary_y=True, title='Volume', showgrid=False)
    fig.update_layout(xaxis={'rangeslider': {'visible': False}})
    fig.show()

