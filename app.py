import dash
from dash import dcc, callback, Output, Input
import dash_html_components as html
from database import get_collection, connect
import plotly.express as px
import pandas as pd
from unidecode import unidecode

STYLES = {  

    'div':{'textAlign': 'center',
    'fontFamily': 'Roboto'},
    'h1': {'fontsize': '20px'},
    'p': {'fontsize': '10px'},    
    'dropdown': {'fontsize': '10px', 'width': '50%', 'margin': 'auto'},

}

db = connect()

def get_data(collection_name: str = 'Product_Data'):
    collection = get_collection(db, collection_name=collection_name)
    data = collection.find()
    return pd.DataFrame(data)

def get_queries():
    with open('queries.txt', encoding = 'utf-8') as f:
        lines = f.readlines()
        queries = []
        for line in lines:
            print(line.strip())
            print(unidecode(line.strip()))
            queries.append(unidecode(line.strip()))
    return queries

app = dash.Dash(__name__)

products = get_data('Product_Data')
reviews = get_data('Product_Reviews')
characteristics = get_data('Product_Characteristics')
queries = get_queries()
app.layout = html.Div([
    html.H1(children='Decathlon product data analyzer', style=STYLES['h1']),
    html.P(children='This app allows to visualize the results of the data scrapped from the Decathlon website.', style=STYLES['p']),
    html.P(children='The data is fetched from the database and displayed in the graph below.', style=STYLES['p']),
    html.P(children='Select the type of product:', style=STYLES['p']),
    
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': query, 'value': query} for query in queries],
        value=queries[0],
        style=STYLES['dropdown']
    ),
    dcc.Dropdown(
        id='discount-dropdown',
        options=[{'label':'With discount', 'value':True}, {'label':'Without discount', 'value':False}],
        value=True,
        style=STYLES['dropdown']
    ),
    dcc.Graph(id='graph-content'), 
],style=STYLES['div'])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown', 'value'),
    Input('discount-dropdown', 'value')
)
def update_graph(query: str, discount:bool):
    product_data = products[products['query'] == query]
    product_data = product_data[product_data['discount'] == discount]
    return px.scatter(product_data, x='price', y='rating', color= 'brand',title='Price vs Rating of Decathlon products')

if __name__ == '__main__':
    app.run(debug=True)