# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from CRUD import AnimalShelter

###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name

username = "aacuser"
password = "SNHU1234"

# Connect to database via CRUD Module
db = AnimalShelter()

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(db.Read({}))

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
app = JupyterDash(__name__)

# FIX ME Add in Grazioso Salvare’s logo
image_filename = 'pic.png'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
# FIX ME Also remember to include a unique identifier such as your name or date
# html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

app.layout = html.Div([
    #    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('CS-340 Dashboard'))),
    html.Hr(),
    html.Div(
        dcc.Dropdown(
            options=[
                {'label': 'Water Rescue', 'value': '1'},
                {'label': 'Mountain or Wilderness Rescue', 'value': '2'},
                {'label': 'Disaster Rescue or Individual Tracking', 'value': '3'},
                {'label': 'Reset', 'value': '4'}
            ],
            id='filter_type',
            style={"width": "375px"}
        )

    ),
    html.Hr(),
    dash_table.DataTable(id='datatable-id',
                         columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
                         data=df.to_dict('records'),
                         row_selectable="single",
                         selected_rows=[]
                         ),
    html.Br(),
    html.Hr(),
    # This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
             style={'display': 'flex'},
             children=[
                 html.Div(
                     id='graph-id',
                     className='col s12 m6',

                 ),
                 html.Div(
                     id='map-id',
                     className='col s12 m6',
                 )
             ])
])


#############################################
# Interaction Between Components / Controller
#############################################
# Dropdown filter

@app.callback([Output('datatable-id', 'data'),
               Output('datatable-id', 'columns')],
              [Input('filter_type', 'value')])
def update_dashboard(filter_type):
    if filter_type == '1':
        df = pd.DataFrame.from_records(db.Read({'$and': [{'sex_upon_outcome': 'Intact Female'},
                               {'$or': [
                                   {'breed': {"$regex": "Newfoundland"}},
                                   {'breed': {"$regex": "Chesa"}},
                                   {'breed': {"$regex": "Labrador Retriever"}}]
                               },
                               {
                                   '$and': [{'age_upon_outcome_in_weeks': {'$gte': 26, '$lte': 156}}]
                               }]
                      }))
    if filter_type == '2':
        df = pd.DataFrame.from_records(db.Read({'$and': [{'sex_upon_outcome': 'Intact Male'},
                         {'$or': [
                             {'breed': {"$regex": "German Shepherd"}},
                             {'breed': {"$regex": "Alaskan Malamute"}},
                             {'breed': {"$regex": "Old English Sheepdog"}},
                             {'breed': {"$regex": "Siberian Husky"}},
                             {'breed': {"$regex": "Rottweiler"}},
                         ]
                         },
                         {
                             '$and': [{'age_upon_outcome_in_weeks': {'$gte': 26, '$lte': 156}}]
                         }]
                }))
    if filter_type == '3':
        df = pd.DataFrame.from_records(db.Read({'$and': [{'sex_upon_outcome': 'Intact Male'},
                         {'$or': [
                             {'breed': {"$regex": "Doberman Pinscher"}},
                             {'breed': {"$regex": "German Shepherd"}},
                             {'breed': {"$regex": "Golden Retriever"}},
                             {'breed': {"$regex": "Bloodhound"}},
                             {'breed': {"$regex": "Rottweiler"}},
                         ]
                         },
                         {
                             '$and': [{'age_upon_outcome_in_weeks': {'$gte': 20, '$lte': 300}}]
                         }]
                }))
    if filter_type == '4':
        df = pd.DataFrame.from_records(db.Read({}))

    columns = [{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data = df.to_dict('records')
    #
    #
    return data, columns


# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")])
def update_graphs(viewData):

    dfg = pd.DataFrame.from_dict(viewData)
    names= dfg['breed'].value_counts().keys().tolist()
    values = dfg['breed'].value_counts().tolist()

    return [
        dcc.Graph(
            figure=px.pie(dfg, values= values, names=names, title='Preferred Animals')
        )
    ]


# This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')])
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
                   center=[30.75, -97.48], zoom=9, children=[
                    dl.TileLayer(id="base-layer-id"),
                    # Marker with tool tip and popup
                    # Column 13 and 14 define the grid-coordinates for
                    # the map
                    # Column 4 defines the breed for the animal
                    # Column 9 defines the name of the animal
                    dl.Marker(position=[dff.iloc[row, 13], dff.iloc[row, 14]],
                              children=[
                                  dl.Tooltip(dff.iloc[row, 4]),
                                  dl.Popup([
                                      html.H1("Animal Name"),
                                      html.P(dff.iloc[row, 9])
                                  ])
                              ])
                ])
        ]


app.run_server(debug=True)
