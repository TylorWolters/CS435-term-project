# Casey Evitts, siu850557754

from csv_parser import *
import pandas as pd
from geojson import load
import plotly.express

# data: population_data, death_data, or case_file csv file.
# county: county name,   state: state abbreviation,   comparison: {>,<,>=,<=}
# quantity: value cases/deaths will be compared against,   time_size: today, week, month,
# time_distance: if using week or month for time size, give how many weeks or months back you are pulling from.
# time: (if using week or month, give how many weeks or months back you are pulling from.)
def search_df(data, county=None, state=None, comparison=None, quantity=None, time_size=None, time_distance=None):
    results = pd.DataFrame()

    if state != None:
        if county != None:  # collects data for a single county
            results = results.append(data.query('State == @state & county_name == @county'), ignore_index=True)

        else:  # collects unfiltered data for entire state
            results = results.append(data.query('State == @state'), ignore_index=True)

    if comparison != None:
        temp_df = pd.DataFrame(columns=data.columns)

        # comparison of data within an individual state
        if state != None:
            if time_distance != None:

                for i, row in results.iterrows():
                    case_change = date_specified_numbers(results.iloc[[i]], time_size, time_distance, "county",
                                                results["State"].iloc[i], results["county_name"].iloc[i])

                    # filters state data for results with a number of occurrences in a given timeframe
                    if comparison == ">":
                        if case_change > quantity:
                            temp_df = temp_df.append(results.iloc[i], ignore_index=True)

                    elif comparison == "<":
                        if case_change < quantity:
                            temp_df = temp_df.append(results.iloc[i], ignore_index=True)

                    elif comparison == ">=":
                        if case_change >= quantity:
                            temp_df = temp_df.append(results.iloc[i], ignore_index=True)

                    elif comparison == "<=":
                        if case_change <= quantity:
                            temp_df = temp_df.append(results.iloc[i], ignore_index=True)

            # filters state level data for results with a number of occurrences
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

            results = temp_df

        # comparison of data among all states
        else:
            results = pd.DataFrame(columns=data.columns)

            # filters all data for results with a number of occurrences in a timeframe
            if time_distance != None:
                for i, row in data.iterrows():
                    case_change = date_specified_numbers(data.iloc[[i]], time_size, time_distance,
                                                "state", data["State"].iloc[i], county=None)
                    if comparison == ">":
                        if case_change > quantity:
                            results = results.append(data.iloc[i])

                    elif comparison == "<":
                        if case_change < quantity:
                            results = results.append(data.iloc[i], ignore_index=True)

                    elif comparison == ">=":
                        if case_change >= quantity:
                            results = results.append(data.iloc[i], ignore_index=True)

                    elif comparison == "<=":
                        if case_change <= quantity:
                            results = results.append(data.iloc[i], ignore_index=True)

            # filters all data for results with a number of occurrences
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

    map_data = pd.DataFrame()
    map_data["countyFIPS"] = data["countyFIPS"].astype(str)
    map_data["county_name"] = data["county_name"]

    # pads 'countyFIPS' to the correct length for states with single digit FIPS codes
    for i, row in map_data.iterrows():
        if len(map_data["countyFIPS"].iloc[i]) < 5:
            map_data["countyFIPS"].iloc[i] = "0" + map_data["countyFIPS"].iloc[i]

    if data_to_display == 'deaths':
        map_data["Deaths"] = data[data.columns[len(data.columns) - 1]].astype(int)
        scale = (0, 100)
        color_label = "Deaths"
        color_scale = "reds"

    elif data_to_display == 'cases':
        map_data["Cases"] = data[data.columns[len(data.columns) - 1]].astype(int)
        scale = (0, 1500)
        color_label = "Cases"
        color_scale = "blues"

    # escape for unsupported input
    else:
        return

    # generates a county level choropleth map of the United States
    fig = plotly.express.choropleth(map_data, geojson=counties, locations='countyFIPS', color=color_label,
                                    color_continuous_scale=color_scale, featureidkey='properties.GEOID',
                                    scope="usa", range_color=scale,  hover_data=["county_name"])

    # adjusts the map's margins and disables the ability to drag it
    fig.update_layout(height=300, margin={"r": 15, "t": 15, "l": 15, "b": 15})
    fig.show()

