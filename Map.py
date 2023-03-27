import plotly.colors as colors
from plotly.offline import iplot, init_notebook_mode
from matplotlib import cm
import plotly.io as pio
import plotly.express as px
import numpy as np
from json import load
import pandas as pd
import streamlit as st
import pydeck as pdk


st.set_page_config(layout="wide")
st.title("Bangladesh Road Accidents")
st.sidebar.info(
    "Choropleth Bangladesh Map\n"
    "Road accidents"
)


bd_districts = load(
    open('bangladesh_geojson_adm2_64_districts_zillas.json', 'r'))
bd_districts['features'][61].keys()
# bd_districts["features"][61]['properties']
dff = pd.read_csv('final_report.csv')

district_id_map = {}
for feature in bd_districts["features"]:
    feature["id"] = feature["id"]
    district_id_map[feature["properties"]["ADM2_EN"]] = feature["id"]
# district_id_map
default_value = None
dff['id'] = dff.District.apply(lambda x: district_id_map.get(x, default_value))
dff.to_csv('final_output.csv', index=False)
final_data = pd.read_csv('final_output.csv')
# final_data

# -------------------dividing time period------------------------
color = cm.inferno_r(np.linspace(.3, .7, 64))

grouped = final_data.groupby(['LOCATION', 'District', 'id', 'time', 'time_of_day', 'day', 'week',
                             'month', 'year', 'Vehicle 1', 'Vehicle 2', 'Vehicle 3']).size().reset_index(name='total_accidents')
time_data = grouped.copy()


grouped = final_data.groupby(['LOCATION', 'District', 'id', 'day', 'week', 'month', 'year',
                             'Vehicle 1', 'Vehicle 2', 'Vehicle 3']).size().reset_index(name='total_accidents')
day_data = grouped.copy()


grouped = final_data.groupby(['LOCATION', 'District', 'id', 'week', 'month', 'year']).size(
).reset_index(name='total_accidents')
week_data = grouped.copy()


grouped = final_data.groupby(
    ['LOCATION', 'District', 'id', 'month', 'year']).size().reset_index(name='total_accidents')
month_data = grouped.copy()


grouped = final_data.groupby(
    ['LOCATION', 'District', 'id', 'year']).size().reset_index(name='total_accidents')
year_data = grouped.copy()


# ---------------------------------------------------streamlit-----------------
row1_col1, row1_col2 = st.columns(
    [0.8, 2]
)
row2_col1, row2_col2 = st.columns(
    [1.5, 1.5]
)
row3_col1, row3_col2, row3_col3 = st.columns(
    [1, 1, 1]
)
row4_col1, row4_col2, row4_col3 = st.columns(
    [1, 1, 1]
)
row5_col1, row5_col2 = st.columns(
    [1, 1]
)
# --------------------------------------------------------------------------------
with row1_col1:
    time_period = st.selectbox(
        "Select time period:", ["Daily", "Weekly", "Monthly", "Yearly"])

# --------------------------------------- check if each row satisfies the condition


def year_func(yy):
    # create an empty DataFrame to hold the filtered data
    filtered = pd.DataFrame()
    for index, row in year_data.iterrows():
        if (row['year'] == yy):
            # if the condition is satisfied, add the row to the filtered DataFrame
            filtered = pd.concat([filtered, row.to_frame().T])
    return filtered


def month_func(yy, mm):
    filtered = pd.DataFrame()
    for index, row in month_data.iterrows():
        if ((row['year'] == yy) & (row['month'] == mm)):
            filtered = pd.concat([filtered, row.to_frame().T])
    return filtered


def week_func(yy, mm, ww):

    filtered = pd.DataFrame()
    for index, row in week_data.iterrows():
        if ((row['year'] == yy) & (row['month'] == mm) & (row['week'] == ww)):
            filtered = pd.concat([filtered, row.to_frame().T])
    return filtered


def day_func(yy, mm, dd):

    filtered = pd.DataFrame()
    for index, row in day_data.iterrows():
        #print(row['month'])

        if ((row['year'] == yy) & (row['month'] == mm) & (row['day'] == dd)):
            print(row['month'])

            filtered = pd.concat([filtered, row.to_frame().T])
    return filtered


def wday_func(yy, mm, ww, dd):
    filtered = pd.DataFrame()
    for index, row in time_data.iterrows():
        if ((row['year'] == yy) & (row['month'] == mm) & (row['week'] == ww) & (row['day'] == dd)):
            filtered = pd.concat([filtered, row.to_frame().T])
    return filtered
# ----------------------------------all parts-----------------------------


if time_period == "Yearly":
    with row2_col1:
        year = st.slider("Select year:", 2000, 2023, 2019)
    y = year
    filtered_data = year_func(y)

if time_period == "Monthly":
    with row2_col1:
        year = st.slider("Select year:", 2000, 2023, 2020)
    with row2_col2:
        month = st.slider("Select month:", 1, 12, 11)
    y = year
    m = month
    filtered_data = month_func(y, m)

if time_period == "Weekly":
    with row3_col1:
        year = st.slider("Select year:", 2000, 2023, 2020)
    with row3_col2:
        month = st.slider("Select month:", 1, 12, 11)
    with row3_col3:
        week = st.slider("Select week:", 1, 52, 1)
    y = year
    m = month
    w = week
    filtered_data = week_func(y, m, w)

if time_period == "Daily":
    with row4_col1:
        year = st.slider("Select year:", 2000, 2023, 2020)
    with row4_col2:
        month = st.slider("Select month:", 1, 12, 11)
    with row4_col3:
        day = st.slider("Select day of the month:", 1, 31, 1)
        with row5_col1:
            show_day = st.checkbox('Show week:')
    y = year
    m = month
    d = day
    filtered_data = day_func(y, m, d)
    if show_day:
        week = st.slider("Select week:", 1, 52, 1)
        w = week
        filtered_data = wday_func(y, m, w, d)


# ------------------------------------------------------------------------------------
init_notebook_mode(connected=True)
colorscale = ['white', 'rgb(255, 230, 230)', 'rgb(255, 204, 204)', 'rgb(255, 179, 179)',
              'rgb(255, 153, 153)', 'rgb(255, 128, 128)', 'rgb(255, 102, 102)', 'rgb(255, 77, 77)', 'rgb(255, 51, 51)', 'rgb(255, 26, 26)', 'red']

# Create a function to map the color scale to the data

colors = ['rgb(255, 230, 230)', 'rgb(255, 204, 204)', 'rgb(255, 179, 179)',
          'rgb(255, 153, 153)', 'rgb(255, 128, 128)', 'rgb(255, 102, 102)',
          'rgb(255, 77, 77)', 'rgb(255, 51, 51)', 'rgb(255, 26, 26)', 'red']
redscales = [[i/len(colors), c]
             for i, c in enumerate(colors)],


if 'total_accidents' in filtered_data:
    # Access the 'total_accidents' column
    max_accidents = filtered_data['total_accidents'].max()
    fig = px.choropleth_mapbox(filtered_data,
                               locations='id',
                               geojson=bd_districts,
                               color='total_accidents',
                               title=f'Bangladesh Road Accidents ({y} Year])',
                               hover_name='LOCATION',
                               hover_data=['LOCATION', 'District',
                                           'total_accidents', 'year', 'id'],
                               color_continuous_scale="redscales",
                               # range_color=[0, max_value],
                               mapbox_style='carto-positron',
                               center={'lat': 23.6850, 'lon': 90.3563},
                               zoom=6.0,
                               opacity=0.4,
                               # range_color=[
                               # 0, filtered_data['total_accidents'].max()],
                               # color_discrete_map={str(val): get_color(
                               # val) for val in filtered_data['total_accidents'].unique()}
                               )

    fig.update_geos(fitbounds='locations', visible=True)
    fig.update_layout(
        height=800,
        width=1000
        # Set the height to 800 pixels
    )
    st.plotly_chart(fig, use_container_width=True)

    show_table = st.checkbox('Show table of data')

    if show_table:
        row6_col1, row6_col2, row6_col3 = [1, 1, 1]
        num_rows = len(filtered_data)
        page_size = 10
        num_pages = num_rows // page_size + \
            (1 if num_rows % page_size > 0 else 0)
        start_row = st.session_state.get('start_row', 0)
        current_page = start_row // page_size + 1 if start_row > 0 else 1
        start_row = max(0, min(num_rows - page_size, start_row))
        end_row = start_row + page_size if start_row + \
            page_size <= num_rows else num_rows
        table_data = filtered_data.iloc[start_row:end_row].to_html(index=False)
        table_style = '<style>table {margin: 0 auto;}</style>'
        container_style = '<style>.container {display: flex; justify-content: center;}</style>'

        st.session_state.start_row = start_row

        st.markdown(
            f'<div class="container" style="overflow-x:auto;">{table_style}{table_data}</div>', unsafe_allow_html=True)

        prev_disabled = start_row == 0
        next_disabled = end_row == num_rows
        if st.button("<", key="prev", disabled=prev_disabled):
            st.session_state.start_row = max(0, start_row - page_size)
        if st.button(">", key="next", disabled=next_disabled):
            st.session_state.start_row = min(
                start_row + page_size, num_rows - page_size)

        start_row = st.session_state.get('start_row', 0)
        end_row = start_row + page_size if start_row + \
            page_size <= num_rows else num_rows
        page_info = f'<p>Showing rows {start_row+1}-{end_row} of {num_rows}</p>'

        st.markdown(
            f'<div class="container" style="text-align:center;">{page_info}</div>', unsafe_allow_html=True)


else:
    # Handle the error
    st.error('No data found !')
