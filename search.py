# Casey Evitts, siu850557754

from csv_parser import *
import pandas as pd
from geojson import load
import plotly.express

# Filters input data based on a variety of search conditions that can be mixed and matched
#
# data: death_data, case_data, or the results of a previous search
# county: county name in format "Jackson County", requires 'state'
# state: state as an abbreviation
# comparison: designates the method of comparison quantity is used for ( >, <, >=, <= ), requires 'quantity'
# quantity: value the number of cases/deaths will be compared against, requires 'comparison'
# time_size: increment of time you are looking back (today, week, month), requires 'time_distance'
# time_distance: if using time size, give how many days, weeks or months back you are pulling from, requires 'time_size'
def search_df(data, county=None, state=None, comparison=None, quantity=None, time_size=None, time_distance=None):
    results = pd.DataFrame()  # dataframe matching results will be stored in

    # handles base level search
    if state != None:
        if county != None:  # collects data for a specific county
            results = results.append(data.query('State == @state & county_name == @county'), ignore_index=True)

        else:  # collects unfiltered data for entire state
            results = results.append(data.query('State == @state'), ignore_index=True)

    # handles secondary search if a comparison is entered
    if comparison != None:
        temp_df = pd.DataFrame(columns=data.columns)  # temporary dataframe that facilitates a second level search

        # comparison of data within a specific state
        if state != None:

            # handles comparison of data within a state in the entered timeframe
            if time_size != None:
                quantity_list = []  # holds values for the change in data over the timeframe
                for i, row in results.iterrows():

                    # evaluates change in cases within given timeframe using date_specified_numbers() from csv_parser.py
                    case_change = date_specified_numbers(results.iloc[[i]], time_size, time_distance, "county",
                                                         results["State"].iloc[i], results["county_name"].iloc[i])

                    # filters state data for results with a number of occurrences in given timeframe, the number of
                    # occurrences is added to the results data as an additional column
                    if comparison == ">":
                        if case_change > quantity:
                            quantity_list.append(case_change)
                            temp_df = temp_df.append(results.iloc[i], ignore_index=True)

                    elif comparison == "<":
                        if case_change < quantity:
                            quantity_list.append(case_change)
                            temp_df = temp_df.append(results.iloc[i], ignore_index=True)

                    elif comparison == ">=":
                        if case_change >= quantity:
                            temp_df = temp_df.append(results.iloc[i], ignore_index=True)

                    elif comparison == "<=":
                        if case_change <= quantity:
                            quantity_list.append(case_change)
                            temp_df = temp_df.append(results.iloc[i], ignore_index=True)

                # adds data stored in quantity_list to temp_df as an extra column
                temp_df["Change in last " + str(time_distance) + " " + time_size + "s"] = quantity_list

            # handles comparison of data within a state over the entire data history
            else:
                for i, row in results.iterrows():
                    total = results.iloc[i:, -1]

                    if comparison == ">":
                        if total.iloc[0] > quantity:
                            temp_df = temp_df.append(results.iloc[i], ignore_index=True)

                    elif comparison == "<":
                        if total.iloc[0] < quantity:
                            temp_df = temp_df.append(results.iloc[i], ignore_index=True)

                    elif comparison == ">=":
                        if total.iloc[0] >= quantity:
                            temp_df = temp_df.append(results.iloc[i], ignore_index=True)

                    elif comparison == "<=":
                        if total.iloc[0] <= quantity:
                            temp_df = temp_df.append(results.iloc[i], ignore_index=True)

            # replaces the partially filtered data in results with the completed version
            results = temp_df

        # handles comparison of data over the entire country
        else:
            results = pd.DataFrame(columns=data.columns)  # ensures results data maintains the correct structure

            # filters all data for results with the specified number of occurrences in a timeframe, the number of
            # occurrences is added to the results data as an additional column
            if time_size != None:
                quantity_list = []  # holds values for the change in data over the timeframe
                for i, row in data.iterrows():
                    case_change = date_specified_numbers(data.iloc[[i]], time_size, time_distance,
                                                         "state", data["State"].iloc[i], county=None)
                    if comparison == ">":
                        if case_change > quantity:
                            quantity_list.append(case_change)
                            results = results.append(data.iloc[i], ignore_index=True)

                    elif comparison == "<":
                        if case_change < quantity:
                            quantity_list.append(case_change)
                            results = results.append(data.iloc[i], ignore_index=True)

                    elif comparison == ">=":
                        if case_change >= quantity:
                            quantity_list.append(case_change)
                            results = results.append(data.iloc[i], ignore_index=True)

                    elif comparison == "<=":
                        if case_change <= quantity:
                            quantity_list.append(case_change)
                            results = results.append(data.iloc[i], ignore_index=True)

                # adds data stored in quantity_list to results as an extra column
                results["Change in last " + str(time_distance) + " " + time_size + "s"] = quantity_list

            # handles comparison of all data over the entire data history
            else:
                for i, row in data.iterrows():
                    total = data.iloc[i:, -1]

                    if comparison == ">":
                        if total.iloc[0] > quantity:
                            results = results.append(data.iloc[i], ignore_index=True)

                    elif comparison == "<":
                        if total.iloc[0] < quantity:
                            results = results.append(data.iloc[i], ignore_index=True)

                    elif comparison == ">=":
                        if total.iloc[0] >= quantity:
                            results = results.append(data.iloc[i], ignore_index=True)

                    elif comparison == "<=":
                        if total.iloc[0] <= quantity:
                            results = results.append(data.iloc[i], ignore_index=True)

    # handles searching over a timeframe where no comparison is wanted
    elif time_size != None:
        quantity_list = []  # holds values for the change in data over the timeframe

        # collects results over the timeframe for country wide data
        if results.empty:
            results = data  # copies data into results to preserve original copy
            for i, row in data.iterrows():
                quantity_list.append(date_specified_numbers(data.iloc[[i]], time_size, time_distance, "county",
                                                            data["State"].iloc[i], data["county_name"].iloc[i]))

        # collects results over the timeframe for a single state or county
        else:
            for i, row in results.iterrows():
                quantity_list.append(date_specified_numbers(results.iloc[[i]], time_size, time_distance, "county",
                                                            results["State"].iloc[i], results["county_name"].iloc[i]))

        # adds data stored in quantity_list to results as an extra column
        results["Change in last " + str(time_distance) + " " + time_size + "s"] = quantity_list

    return results


# exports 'data' as a .json or .csv file
# data: population_data, death_data, case_file csv file or results of a search.
# file_type: json or csv
def export_data(data, file_type):
    if file_type == "json":
        data.to_json(r'covid_data_output.json', orient="split")

    elif file_type == "csv":
        data.to_csv(r'covid_data_output.csv', index=False, header=True)


# generates a choropleth map based on the input data, defaults to total number of deaths
# data: data: death_data, case_file csv file or results of a search.
# data_to_display: 'deaths', 'cases' -> adjusts map labels, defaults to 'deaths'
def generate_map(data=death_data, data_to_display='deaths'):
    # opens a geojson file containing county outlines
    with open('us_counties.geojson') as file:
        counties = load(file)

    # creates a dataframe containing only countyFIPS, county_name
    map_data = pd.DataFrame()
    map_data["countyFIPS"] = data["countyFIPS"].astype(str)
    map_data["county_name"] = data["county_name"]

    # pads 'countyFIPS' to the correct length for states with single digit stateFIPS codes
    for i, row in map_data.iterrows():
        if len(map_data["countyFIPS"].iloc[i]) == 4:
            map_data["countyFIPS"].iloc[i] = "0" + map_data["countyFIPS"].iloc[i]

    # adjusts map settings for displaying death data
    if data_to_display == 'deaths':
        map_data["Deaths"] = data[data.columns[len(data.columns) - 1]].astype(int)
        scale = (0, 150)
        color_label = "Deaths"
        color_scale = "reds"

    # adjusts map settings for displaying case data
    elif data_to_display == 'cases':
        map_data["Cases"] = data[data.columns[len(data.columns) - 1]].astype(int)
        scale = (0, 4000)
        color_label = "Cases"
        color_scale = "blues"

    # escape for unsupported input
    else:
        return

    # generates a county level choropleth map of the United States using the plotly library
    fig = plotly.express.choropleth(map_data, geojson=counties, locations='countyFIPS', color=color_label,
                                    color_continuous_scale=color_scale, featureidkey='properties.GEOID',
                                    scope="usa", range_color=scale, hover_data=["county_name"])

    # adjusts the map's size and margins
    fig.update_layout(height=300, margin={"r": 15, "t": 15, "l": 15, "b": 15})

    # overlays state outlines onto the map, visibility is limited if displaying all counties due to overlap
    fig.update_geos(
        visible=False, resolution=110, scope="usa",
        showsubunits=True, subunitcolor="Black", subunitwidth=0.25
    )

    # displays map
    fig.show()
