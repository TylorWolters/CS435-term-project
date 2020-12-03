import requests

# Links to updated CSV information downloads
known_cases = 'https://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv'
known_deaths = 'https://static.usafacts.org/public/data/covid-19/covid_deaths_usafacts.csv'
country_populations = 'https://static.usafacts.org/public/data/covid-19/covid_county_population_usafacts.csv'

# Download file function
def download_file(url, filename=''):
    try:

        if filename:
            pass
        else:

            filename = url[url.rfind('/') + 1:]

        with requests.get(url) as req:
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return filename
    except Exception as e:
        print(e)
        return None


download_file(known_cases)
download_file(known_deaths)
download_file(country_populations)