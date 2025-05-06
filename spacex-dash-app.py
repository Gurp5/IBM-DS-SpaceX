# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
print(spacex_df['Launch Site'].unique())
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
print(spacex_df['Launch Site'].unique())
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'}
                                                ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                                value='ALL',
                                                placeholder="Select a launch site",
                                                searchable=True
                                            ),
                                  html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                              min=0, 
                                              max=10000, 
                                              step=1000,
                                              marks={i: str(i) for i in range(0, 10001, 1000)},  # Marks from 0 to 10000 with step 1000
                                              value=[0, 10000]  # Example range, adjust according to your needs
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df

    if entered_site == 'ALL':
        # If 'ALL' is selected, show pie chart for all sites
        fig = px.pie(filtered_df, 
        names='Launch Site',  # Name the pie chart segments by launch site
        values='class',  # 'class' represents success (1) or failure (0)
        title='Total Success vs. Failed Launches')
        return fig
    else:
      # Filter the data by the selected site and show the pie chart for that specific site
      filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
      
      # Count the success and failure occurrences for the selected site
      success_fail_counts = filtered_df['class'].value_counts()

      # Create the pie chart for the selected site's success/failure counts
      fig = px.pie(
          names=success_fail_counts.index,  # Success and Failure (0 and 1)
          values=success_fail_counts.values,  # Counts of success and failure
          title=f'Success vs. Failed Launches for {entered_site}',
          labels={0: 'Failed', 1: 'Successful'},  # Rename class values for better readability
          color=success_fail_counts.index,  # Color based on success/failure
          color_discrete_map={0: 'red', 1: 'green'}  # Red for failure, green for success
      )

      return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter data based on payload range
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                            (spacex_df['Payload Mass (kg)'] <= high)]

    if selected_site == 'ALL':
        # Scatter plot for all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Outcome for All Sites'
        )
    else:
        # Filter by site
        site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Outcome for {selected_site}'
        )

    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
