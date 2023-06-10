# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#### FIX ME #####<--------------------------
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from CRUD import AnimalShelter

###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name. NOTE: You will
# likely need more variables for your constructor to handle the hostname and port of the MongoDB
# server, and the database and collection names

# USER = "doadmin"
# PASS = "KoAq3251F409TiO7"

username = "doadmin"
password = "KoAq3251F409TiO7"
shelter = AnimalShelter()

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
search = {}
df = pd.DataFrame.from_records(shelter.Read(search))

# MongoDB v5+ is going to return the '_id' column and that is going to have an
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
# df.drop(columns=['_id'], inplace=True)


## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)


#########################
# Dashboard Layout / View
#########################
app = JupyterDash('SimpleExample')

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display': 'none'}),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    html.Hr(),

    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        # FIXME: Set up the features for your interactive data table to make it user-friendly for your client
        row_selectable="single",
        selected_rows=[]

    ),
    html.Br(),
    html.Hr(),
    html.Div(
        id='map-id',
        className='col s12 m6',
    )
])


#############################################
# Interaction Between Components / Controller
#############################################
# This callback will highlight a row on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, derived_virtual_selected_rows):
    dff = pd.DataFrame.from_dict(viewData)
    # Because we only allow single row selection, the list can
    # be converted to a row index here
    if derived_virtual_selected_rows is None:
        row = 0
    else:
        row = derived_virtual_selected_rows[0]

        # Austin TX is at [30.75,-97.48]
        return [
            dl.Map(style={'width': '1000px', 'height': '500px'},
                   center=[30.75, -97.48], zoom=10, children=[
                    dl.TileLayer(id="base-layer-id"),
                    # Marker with tool tip and popup
                    # Column 13 and 14 define the grid-coordinates for
                    # the map
                    # Column 4 defines the breed for the animal
                    # Column 9 defines the name of the animal
                    dl.Marker(position=[dff.iloc[row, 11], dff.iloc[row, 12]],
                              children=[
                                  dl.Tooltip(dff.iloc[row, 4]),
                                  dl.Popup([
                                      html.H1("Animal Name"),
                                      html.P(dff.iloc[row, 8])
                                  ])
                              ])
                ])
        ]


# FIXME Add in the code for your geolocation chart

app.run_server()
