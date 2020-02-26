import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

#import data
df_pie_chart = pd.read_csv('https://raw.githubusercontent.com/rwedell/data/master/commute_data_stacked_v2.csv')
df_map = pd.read_csv('https://raw.githubusercontent.com/rwedell/data/master/commute_data.csv')


app = dash.Dash()
app.title = "Commute Visual"

markdown_text ="""
# Commuting to Work
The visuals below display how people commute to work by state.
Use the dropdowns or type in the box to search by state or commute type.
"""

#creating a dictionary of values for state and commute options
state_options = []
for state in df_pie_chart['State'].unique():
    state_options.append({'label':str(state),'value':state})
    
commute_options = [{'label':'Drive Alone','value':'Drive Alone'},
                   {'label':'Carpool','value':'Carpool'},
                   {'label':'Walk','value':'Walk'},
                   {'label':'Public Transportation','value':'Public Transportation'},
                   {'label':'Other Means','value':'Other Means'},
                   {'label':'Work at Home','value':'Work at Home'}]

app.layout = html.Div([
    dcc.Markdown(children = markdown_text),    
    #create divs for pie chart and map figures
    html.Div([#pie chart div
        dcc.Dropdown(id = 'state-picker', 
                     options = state_options,
                     value='District of Columbia',
                     style = {'width':'50%'}),
        dcc.Graph(id='pie_graph')        
    ],style={'width': '49%', 'display': 'inline-block'}),
    html.Div([#map div
        dcc.Dropdown(id = 'commute-picker', 
                     options = commute_options,
                     value='Drive Alone',
                     style = {'width':'50%'}),
        dcc.Graph(id='map_graph')        
    ],style={'width': '49%', 'display': 'inline-block'})
    
])

#callback for updating pie chart
@app.callback(Output('pie_graph', 'figure'),
              [Input('state-picker', 'value')])
def updatePieChart(selected_state):
    filtered_df = df_pie_chart[df_pie_chart['State'] == selected_state]
    trace = []
    trace.append(go.Pie(
        labels = filtered_df['Commute Type'],
        values = filtered_df['Rate'],
        hoverinfo = 'value+label',
        hole = 0.25
        )
    )
    return {'data': trace,
            'layout':go.Layout(
                xaxis = {'title': selected_state},
                yaxis = {'title': "Percent of Commuters"},
                hovermode = "closest",
                title = "Commute Method by Percent in " + selected_state
                )
           }

#callback for updating map
@app.callback(Output('map_graph', 'figure'),
              [Input('commute-picker', 'value')])
def updateMap(selected_commute):
    trace = []
    trace.append(go.Choropleth(
        locations = df_map['Code'], 
        z = df_map[selected_commute], 
        locationmode = 'USA-states', 
        colorscale = 'Reds',
        colorbar_title = "Percent",
        hovertemplate = df_map['Code']+': %{z}%<extra></extra>'
        )
    )
    return {'data': trace,
            'layout':go.Layout(
                title_text = selected_commute + ': Percent of Commuters',
                geo_scope='usa'
                )
           }


if __name__ == '__main__':
    app.run_server()