from math import pi
import pandas as pd
import numpy as np
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, ColumnDataSource, CustomJS, RangeSlider
from bokeh.plotting import figure, show
from bokeh.layouts import layout

df = pd.read_feather("out.feather")
data = df.loc[:100, ['r3.er.snr', 'r3.er.srcAddr_1b', 'r3.er.dstAddr_1b', 'frame.time_epoch']]

data['r3.er.srcAddr_1b'] = data['r3.er.srcAddr_1b'].astype(int)
data['r3.er.dstAddr_1b'] = data['r3.er.dstAddr_1b'].astype(int)
data['frame.time_epoch'] = pd.to_datetime(data['frame.time_epoch'])
data['r3.er.snr'] = data['r3.er.snr'].astype(int)

data['link'] = data['r3.er.srcAddr_1b'].astype(str) +"-"+ data['r3.er.dstAddr_1b'].astype(str)
data= data.drop(columns=["r3.er.srcAddr_1b" ,"r3.er.dstAddr_1b"])
data = data.set_index(['frame.time_epoch'])

#Column names
data.index.name = 'time'
data=data.rename(columns={"r3.er.snr":"value"})
data.drop(data.index[data.value == 0], inplace=True)
data.fillna(0)
# data = data.resample('ms').transform("min")
print(data)
#color palette
colors = ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641']
mapper = LinearColorMapper(
    palette=colors, low=0, high=data.value.max())

# Define a figure
p = figure(
    plot_width=800,
    plot_height=700,
    title="SNR Presence",
    x_range=list(data.index.drop_duplicates().astype(str)),
    y_range=list(data.link.drop_duplicates().astype(str)),
    x_axis_location="above")
p.xaxis.major_label_orientation = pi / 3
source = ColumnDataSource(data=dict(
    x=list(data.index.astype(str)),
    y1=list(data.link.astype(str)),
    y2=list(data.value.astype(str)),
))

# Create rectangle for heatmap
p.rect(
    x='x',
    y='y1',
    width=1,
    height=1,
    source= source,
    fill_color={'field': 'y2', 'transform': mapper})
    
# Add legend
color_bar = ColorBar(
    color_mapper=mapper,
    location=(0, 0),
    ticker=BasicTicker(desired_num_ticks=len(colors)))
p.add_layout(color_bar, 'right')

show (p)
