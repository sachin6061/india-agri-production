"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State
from pages import home
from pages import state_wise
from pages import district_wise
from pages import Contactus
import pandas as pd
import plotly.express as px
import numpy as np

df = pd.read_csv("Agriculture Crop Production.csv")
crop_production_df = df.groupby(['State', 'Year', 'year_wise', 'Crop']).agg(
    {'Production_Tonnes': 'sum', 'Area': 'sum'}).reset_index()
unique_states = df["State"].unique()
unique_year = df["year_wise"].unique()
home_df = df.groupby(['Year', 'year_wise', 'Crop']).agg(
    {'Production_Tonnes': 'sum', 'Area': 'sum'}).reset_index()

dist_df = df.groupby(['State', 'District', 'Year', 'year_wise', 'Crop']).agg(
    {'Production_Tonnes': 'sum', 'Area': 'sum'}).reset_index()
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 73.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#d3dcde",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 73,
    "left": "-11.5rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#d3dcde",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    # "position": "fixed",
    "top": 73,
    "width": "80rem",
    "transition": "margin-left .5s",
    "margin-left": "16.2rem",
    "margin-right": "0.2rem",
    # "margin-top": "0.3rem",
    "padding": "2rem 1rem",
    "background-color": "#f0f3f4",
}

CONTENT_STYLE1 = {
    # "position": "fixed",
    "top": 71.6,
    "width": "95rem",
    "transition": "margin-left .5s",
    "margin-left": "3.5rem",
    "margin-right": "0.2rem",
    "padding": "2rem 1rem",
    "background-color": "#f0f3f4",
}
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About Us", href="#")),
        dbc.NavItem(dbc.NavLink("Contact Us", href="#")),
        # dbc.NavItem(dbc.NavLink("About Us", href="#")),
    ],
    brand="Brand",
    # brand_href="#",
    # color="dark",
    # dark=True,
    # fluid=True,
    className='navbar navbar-expand-lg navbar-dark bg-dark',
    # style={"position": "fixed", "width": "100%", "top": 0, }
)

sidebar = html.Div([dbc.Row([dbc.Col(html.H2("INDIA's"),
                                     style={
                                         'background': 'repeating-radial-gradient(circle farthest-corner at center center, #121FCF 0%, #CF1512 100%)',
                                         '-webkit-background-clip': 'text',
                                         '-webkit-text-fill-color': 'transparent'
                                     }), ]),
                    #  dbc.Col(
                    #      dbc.Button(">", outline=True, color="secondary", className="mr-1", id="btn_sidebar"))],
                    # justify='center'),
                    html.P('Crop Production Year wise from 2001 to 2019', style={'color': 'white'}),

                    html.Hr(style={'color': 'white', 'height': '3px'}),
                    dbc.Nav(
                        [
                            dbc.NavLink("Home", href="/", active="exact"),
                            dbc.NavLink("State Wise Report", href="/state_wise_report", active="exact"),
                            dbc.NavLink("District Wise Report", href="/district_wise_report", active="exact"),
                            dbc.NavLink("About Me", href="/about_me", active="exact"),
                        ],
                        vertical=True,
                        # pills=True,
                    ),
                    ], id="sidebar",
                   # style=SIDEBAR_STYLE,
                   )

# content = html.Div(id="page-content", style=CONTENT_STYLE)
content = html.Div(id="page-content")
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
server = app.server
app.layout = dbc.Container([dcc.Store(id='side_click'), dcc.Location(id="url"),
                            # dbc.Row(navbar,style={'margin-bottom': '5px','position': 'fixed'}),
                            dbc.Row(
                                [dbc.Col(sidebar, width=2, style={"background-color": "#4c6067", 'padding': '10px'}),
                                 dbc.Col(content, width=10,
                                         style={'background-color': '#f0f3f4', 'padding': '10px'})])],
                           fluid=True, style={'padding': '20px'})


# @app.callback(
#     [
#         Output("sidebar", "style"),
#         Output("page-content", "style"),
#         Output("side_click", "data"),
#         Output("btn_sidebar", "children"),
#     ],
#
#     [Input("btn_sidebar", "n_clicks")],
#     [
#         State("side_click", "data"),
#     ]
# )
# def toggle_sidebar(n, nclick):
#     sign = '<'
#     if n:
#         if nclick == "SHOW":
#             sidebar_style = SIDEBAR_HIDEN
#             content_style = CONTENT_STYLE1
#             cur_nclick = "HIDDEN"
#             sign = '>'
#         else:
#             sidebar_style = SIDEBAR_STYLE
#             content_style = CONTENT_STYLE
#             cur_nclick = "SHOW"
#     else:
#         sidebar_style = SIDEBAR_STYLE
#         content_style = CONTENT_STYLE
#         cur_nclick = 'SHOW'
#
#     return sidebar_style, content_style, cur_nclick, sign


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return dcc.Loading(home.fnHome(unique_year, home_df), type="cube")
    elif pathname == "/state_wise_report":
        return dcc.Loading(html.Div(state_wise.fnStateWise(unique_states, unique_year)), type='cube')
    elif pathname == "/district_wise_report":
        return dcc.Loading(html.Div(district_wise.fnDistrictWise(unique_states, unique_year)), type='cube')
    elif pathname == "/about_me":
        return dcc.Loading(html.Div(Contactus.fnAboutMe(app)), type='cube')


@app.callback(
    [Output('graph-with-slider', 'figure'), Output('area_wise-crop', 'figure')],
    [Input('year-slider', 'value'), Input('state', 'value')])
def update_figure(selected_year, state):
    state_df = crop_production_df[
        (crop_production_df['State'] == state)]
    filtered_df = state_df[
        (state_df['year_wise'] == selected_year)]

    fig1 = px.bar(filtered_df, x='Crop', y='Production_Tonnes', hover_data=['Crop', 'Production_Tonnes'], color='Crop',
                  text_auto='.2s',
                  title=f"Production in Tonnes in year {selected_year}"
                  )
    fig1.update_layout(paper_bgcolor='#d3dcde',
                       plot_bgcolor='#d3dcde')

    fig2 = px.bar(filtered_df, x='Crop', y='Area', hover_data=['Crop', 'Area'], color='Crop',
                  text_auto='.2s',
                  title=f"Area in Hector in Per crop in year {selected_year}"
                  )
    fig2.update_layout(paper_bgcolor='#d3dcde',
                       plot_bgcolor='#d3dcde')

    return fig1, fig2


@app.callback(
    [Output('home-productin-graph', 'figure'), Output('home-area_wise-crop', 'figure')],
    [Input('home-year-slider', 'value')])
def update_home_figure(selected_year):
    filtered_df = home_df[
        (home_df['year_wise'] == selected_year)]

    fig1 = px.bar(filtered_df, x='Crop', y='Production_Tonnes', hover_data=['Crop', 'Production_Tonnes'],
                  color='Crop', text_auto='.2s', title=f"Total Production in Tonnes in year {selected_year}")

    fig1.update_layout(paper_bgcolor='#d3dcde',
                       plot_bgcolor='#d3dcde')

    fig2 = px.bar(filtered_df, x='Crop', y='Area', hover_data=['Crop', 'Area'], color='Crop',
                  text_auto='.2s',
                  title=f" Total Area in Hector in Per crop in year {selected_year}"
                  )

    fig2.update_layout(paper_bgcolor='#d3dcde',
                       plot_bgcolor='#d3dcde')

    return fig1, fig2


@app.callback(
    [Output('dist_dist_name', 'options'), Output('dist_dist_name', 'value')],
    Input('dist_state_name', 'value'))
def update_dist_drp(selected_state):
    state_df = dist_df[
        (dist_df['State'] == selected_state)]
    dist_list = state_df['District'].unique()
    dist_list = list(dist_list)
    return [{"label": dist, "value": dist}
            for dist in dist_list], 'KOLHAPUR'


@app.callback(
    [Output('dist-prod-graph', 'figure'), Output('dist-area_wise-crop', 'figure')],
    [Input('dist_state_name', 'value'), Input('dist_dist_name', 'value'), Input('dist-year-slider', 'value')])
def update_dist_figure(state, dist, year):
    state_df = dist_df[
        (dist_df['State'] == state)]

    filtered_df1 = state_df[
        (state_df['year_wise'] == year)]

    filtered_df = filtered_df1[
        (filtered_df1['District'] == dist)]

    fig1 = px.bar(filtered_df, x='Crop', y='Production_Tonnes', hover_data=['Crop', 'Production_Tonnes'], color='Crop',
                  text_auto='.2s',
                  title=f"Production in Tonnes in year {year}"
                  )
    fig1.update_layout(paper_bgcolor='#d3dcde',
                       plot_bgcolor='#d3dcde')

    fig2 = px.bar(filtered_df, x='Crop', y='Area', hover_data=['Crop', 'Area'], color='Crop',
                  text_auto='.2s',
                  title=f"Area in Hector in Per crop in year {year}"
                  )
    fig2.update_layout(paper_bgcolor='#d3dcde',
                       plot_bgcolor='#d3dcde')

    return fig1, fig2


if __name__ == "__main__":
    app.run_server(debug=True)
