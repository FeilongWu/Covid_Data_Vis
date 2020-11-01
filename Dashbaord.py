### python -m bokeh serve --show Dashbaord.py

import pandas as pd
import numpy as np
from bokeh.plotting import figure,show,ColumnDataSource,curdoc
from bokeh.models import HoverTool,PreText, TextAreaInput
from bokeh.models.widgets import Dropdown
from bokeh.layouts import column
import copy

## define text for intro
pre = PreText(text="""
Use the dropdown menu below to select the option. You can choose the new confirmed case or new death case for California in August, 2020.
Your selection will be displayed in the box below. Hover on the line to see the details of a particular day. If the data is missing
for a particular day, this means that the data is not available in the dataset.
""",
width=500, height=100)
## define text box
textbox = TextAreaInput(value='New confirmed cases', rows=1, title='You are viewing:')
data = pd.read_csv('latimes-state-totals.csv')
# select dates in August
data = data[data['date']>='2020-08-01']
data = data[data['date']<'2020-09-01']

width = 1200 # plot width
data['date_time']=pd.to_datetime(data['date'])
df = pd.DataFrame({'x':data['date_time'],'y':data['new_confirmed_cases']})
source = ColumnDataSource(df)
p=figure(y_axis_label='Number of New Cases',title='New Cases vs. Date',
         x_axis_label='Date',x_axis_type='datetime',plot_width=width)
r = p.line('x','y',source=source)
p.add_tools(HoverTool(tooltips=[('date','@x{%Y-%m-%d}'),
                                ('new cases','@y')],
                      formatters={'@x':'datetime'}))
def update(event):
    sel = event.item
    if sel=='Cases':
        r.data_source.data['y'] = data['new_confirmed_cases']
        textbox.value = 'New confirmed cases'
    elif sel == 'Deaths':
        r.data_source.data['y'] = data['new_deaths']
        textbox.value = 'New death cases'
menu_type = [('New confirmed cases',"Cases"),('Deaths',  "Deaths")]
dropdown_state = Dropdown(label="Case confirmed or death", button_type="warning", menu=menu_type)
dropdown_state.on_click(update)

### second graph for races

## define a pretext as a textbox
pre2 = TextAreaInput(value="""Use the dropdown menu below to select the option. You can choose the confirmed case percentage or death case percentage by rance for
California in August, 2020. Your selections will be displayed in the boxes below. Hover on the line to see the details of a
particular day. If the data is missing for a particular day, this means that the data is not available in the dataset.""", rows=5)
class display_opt():
    def __init__(self):
        self.type='confirmed_cases_percent'
        self.race='asian'
display = display_opt()
menu_type_per = [('New confirmed cases',"confirmed_cases_percent"),
                 ('Deaths',  "deaths_percent")]
menu_race = [('Asian',"asian"),  ('Black',"black"),
        ('Latino', 'latino'), ('White','white'),('Other','cdph-other')]
dropdown_race = Dropdown(label="Race", button_type="warning", menu=menu_race)
dropdown_race_type = Dropdown(label="Percent confirmed or death", button_type="warning", menu=menu_type_per)
data_race = pd.read_csv('cdph-race-ethnicity.csv')
data_race = data_race[data_race['age']=='all']
data_race['date_time']=pd.to_datetime(data_race['date'])


subset = data_race[data_race['race']=='asian']
data_x = np.array(subset['date_time'],dtype=np.datetime64)
data_y = np.array(subset['confirmed_cases_percent'])
df2 = pd.DataFrame({'x':data_x,'y':data_y})
source2 = ColumnDataSource(df2)
p2=figure(y_axis_label='Total Percentage',title='Tatoal Percentage by Race vs. Date',
         x_axis_label='Date',x_axis_type='datetime',plot_width=width)
r2 = p2.line('x','y',source=source2)
p2.add_tools(HoverTool(tooltips=[('date','@x{%Y-%m-%d}'),
                                ('percentage','@y')],
                      formatters={'@x':'datetime'}))
# define text box
textbox2 = TextAreaInput(value='Asian', rows=1, title='Selection of race:')
textbox3 = TextAreaInput(value='Percentage of confirmed cases', rows=1, title='You are viewing:')

def update_type(event):
    sel = event.item
    display.type = copy.copy(sel)
    r2.data_source.data['y'] = data_race[data_race['race']==display.race][sel]
    if sel == 'confirmed_cases_percent':
        textbox3.value = 'Percentage of confirmed cases'
    elif sel == 'deaths_percent':
        textbox3.value = 'Percentage of death cases'
def update_race(event):
    sel = event.item
    display.race = copy.copy(sel)
    r2.data_source.data['y'] = data_race[data_race['race']==sel][display.type]
    if sel == 'asian':
        textbox2.value = 'Asian'
    elif sel == 'black':
        textbox2.value = 'Black'
    elif sel == 'cdph-other':
        textbox2.value = 'Other'
    elif sel == 'latino':
        textbox2.value = 'Latino'
    elif sel == 'white':
        textbox2.value = 'White'
dropdown_race_type.on_click(update_type)
dropdown_race.on_click(update_race)

layout = column(pre, dropdown_state,textbox,p, pre2,
                dropdown_race,dropdown_race_type,textbox2,textbox3,p2)
curdoc().add_root(layout)






