### python -m bokeh serve --show Dashboard.py

import os
import datetime
import pandas as pd
import numpy as np
from bokeh.plotting import figure,show,ColumnDataSource,curdoc
from bokeh.models import DateFormatter,DatePicker
from bokeh.models import ColumnDataSource as ColumnDataSource1
from bokeh.models import HoverTool,PreText, TextAreaInput, DataTable, TableColumn,Title
from bokeh.models.widgets import Dropdown
from bokeh.layouts import column
import copy

def getDate(url):
    stamp = os.path.getmtime(url)
    time = datetime.datetime.fromtimestamp(stamp)
    string = str(time)
    return string[:string.index(' ')]
## the first graph is about statewide new cases
url1 = 'latimes-state-totals.csv'
g1_last_update = getDate(url1)
g1_source = 'aggregation of all local agency reports logged by Los Angeles Times for California statewide. '+\
            'URL: '+'https://github.com/datadesk/california-coronavirus-data/blob/master/latimes-state-totals.csv'
## define text for intro
pre = PreText(text="""
Use the dropdown menu below to select the option. You can choose the new confirmed case or new death case for California in August, 2020.
Your selection will be displayed in the box below. Hover on the line to see the details of a particular day. If the data is missing
for a particular day, this means that the data is not available in the dataset. 
""",
width=500, height=120,default_size=12)
## define text box
textbox = TextAreaInput(value='New confirmed cases', rows=1, title='You are viewing:')
data = pd.read_csv(url1)
# select dates in August
data = data[data['date']>='2020-08-01']
data = data[data['date']<'2020-09-01']

width = 1200 # plot width
data['date_time']=pd.to_datetime(data['date'])
df = pd.DataFrame({'x':data['date_time'],'y':data['new_confirmed_cases']})
source = ColumnDataSource(df)
p=figure(y_axis_label='Number of New Cases',title='California New Cases vs. Date',
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
citation1 = Title(text='Source: '+g1_source,text_font_size='11px')
citation2 = Title(text='Last update: '+g1_last_update,text_font_size='11px')
p.add_layout(citation1, 'above')
p.add_layout(citation2, 'above')






### second part: table for races
url2='cdph-race-ethnicity.csv'
def isNone(x):
    if x!=None:
        return False
    else:
        return True

def update1(attr,old,new):
    date=str(date_picker.value)
    #date = '2020-08-03'
    race_table.date=date
    race_table.update()
    tableData = dict(race=['Asian','Black', 'Cdph-other','Latino','White','Other'],
                 confirmed_cases_percent=race_table.confirm,
                 deaths_percent=race_table.death,
                 population_percent=race_table.percent,
                 last_update=race_table.last_update,
                 source=race_table.source)
    source2 = ColumnDataSource1(tableData)
    table.source=source2
    
t_last_update = getDate(url2)
t_source = 'California statewide data provided by California Department of Public Health on tallying race\n totals. URL: '+\
           'https://github.com/datadesk/california-coronavirus-data/blob/master/cdph-race-ethnicity.csv'
## define a pretext as a textbox
pre2=PreText(text="""Use the date picker below to select a date. Both columns 'Confirmed_cases_percent' and 'Deaths_percent' refer to the cumulative confirmed cases and deaths for
a particular race over the population of that race, respectively. The column 'Population_percent' refers to the population of a race over the population of all.
The data is showing the cases (confirmed or death) for all age. Missing data is displayed as 'N/A'. The source and the date for last update are displayed below the date picker.""",width=500, height=100,default_size=12)

data_race = pd.read_csv(url2)
class raceTable():
    def __init__(self,table,source,last_update,NA='N/A',date='2020-10-26'):
        self.table = copy.deepcopy(table)
        self.NA = NA
        self.date = date
        self.race=['asian','black', 'cdph-other','latino','white','other']
        NA_ = [NA]*len(self.race)
        self.confirm=copy.copy(NA_)
        self.death=copy.copy(NA_)
        self.percent=copy.copy(NA_)
        self.source=copy.copy(NA_)
        self.source_str=source
        self.last_update=copy.copy(NA_)
        self.last_update_str=last_update
        self.update()
    def update(self):
        NA = self.NA
        size=len(self.race)
        NA1=[NA]*size
        table=copy.deepcopy(self.table[self.table['date']==self.date])
        table=table[table['age']=='all']
        if table.empty:
            self.confirm=copy.copy(NA1)
            self.death=copy.copy(NA1)
            self.percent=copy.copy(NA1)
            self.source=copy.copy(NA1)
            self.last_update=copy.copy(NA1)
        else:
            for i,j in enumerate(self.race):
                x=0
                temp=table[table['race']==j]
                confirm=temp.iloc[0]['confirmed_cases_percent']
                death=temp.iloc[0]['deaths_percent']
                tot_per=temp.iloc[0]['population_percent']
                if isNone(confirm):
                    x+=1
                    self.confirm[i]=NA
                else:
                    self.confirm[i]=confirm
                if isNone(death):
                    x+=1
                    self.death[i]=NA
                else:
                    self.death[i]=death
                if isNone(tot_per):
                    x+=1
                    self.percent[i]=NA
                else:
                    self.percent[i]=tot_per
                if x>0:
                    self.source[i]=NA
                    self.last_update[i] = NA
                else:
                    self.source[i]=self.source_str
                    self.last_update[i] = self.last_update_str
            
race_table = raceTable(data_race,t_source,t_last_update)
                
            
            
tableData = dict(race=['Asian','Black', 'Cdph-other','Latino','White','Other'],
                 confirmed_cases_percent=race_table.confirm,
                 deaths_percent=race_table.death,
                 population_percent=race_table.percent,
                 last_update=race_table.last_update,
                 source=race_table.source)
source2 = ColumnDataSource1(tableData)
columns = [TableColumn(field="race",title="Race"),
           TableColumn(field='confirmed_cases_percent',title="Confirmed_cases_percent"),
           TableColumn(field="deaths_percent",title="Deaths_percent"),
           TableColumn(field="population_percent",title="Population_percent")]
# TableColumn(field="last_update",title="Last_update"),TableColumn(field="source",title="Source")
table = DataTable(source=source2,columns=columns, width=width, height=500)
date_picker = DatePicker(title='Select a date', value="2020-10-26", min_date="2020-05-01", max_date="2020-11-02")
date_picker.on_change('value',update1)
pre3=PreText(text='Source: '+t_source+'\nLast update: '+t_last_update,width=500, height=45)
layout = column(pre, dropdown_state,textbox,p, pre2,
                date_picker,pre3,table)
curdoc().add_root(layout)



