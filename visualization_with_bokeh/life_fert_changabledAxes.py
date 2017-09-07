import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, CategoricalColorMapper, HoverTool
from bokeh.plotting import figure
from bokeh.layouts import widgetbox, column

# prepare data
data = pd.read_csv('gapminder_clean.csv', index_col='Year')
sc = ColumnDataSource(data={
        'fertility':data.loc[1970].fertility,
        'life':     data.loc[1970].life,
        'country':  data.loc[1970].Country,
        'region':   data.loc[1970].region,
        'popu':     data.loc[1970].scaled_popu
        })
mapper = CategoricalColorMapper(
        factors = ['South Asia', 'Europe & Central Asia',
                   'Middle East & North Africa','Sub-Saharan Africa',
                   'America', 'East Asia & Pacific'],
        palette = ['violet', 'skyblue',
                   'palegoldenrod', 'sandybrown',
                   'salmon', 'lightgreen'])

# init widget
slider = Slider(title='year', start=1970, end=2006, step=1, value=1970)

# init figure
p = figure(plot_width=800, plot_height=500,
       x_axis_label='Fertility', y_axis_label='Life Expectancy')
p.add_tools(HoverTool(tooltips='@country'))

p.circle(x='fertility', y='life', source=sc, size='popu',
     color={'field':'region',
            'transform': mapper},
     legend='region')
p.legend.location='bottom_left'



# update func to change source data
def update_year(attr, old, new):
    year = slider.value
    # update graph title
    p.title.text  = 'Gapminder data for %d' % year

    # note here only change 'data' attribute of 'sc' variable
    # 'sc' variable is fetched from outside this func scope
    sc.data={
            'fertility':data.loc[year].fertility,
            'life':     data.loc[year].life,
            'country':  data.loc[year].Country,
            'region':   data.loc[year].region,
            'popu':     data.loc[year].scaled_popu
            }

# attach update func to 'value' attr of slider
slider.on_change('value', update_year)

layout = column(widgetbox(slider, width=800), p)
curdoc().add_root(layout)
