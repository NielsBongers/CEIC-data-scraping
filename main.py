import re 
import requests 

from pathlib import Path 

country_list = [] 

with open("data/country_list.csv") as f: 
    for country in f: 
        country_list.append(country.strip())

for country in country_list: 
    country = country.replace(" ", "-")
    if not Path("country svg/" + country + ".svg").exists(): 
        country_svg_path = "https://www.ceicdata.com/datapage/charts/ipc_" + country.lower() + "_external-debt-short-term--of-nominal-gdp/?type=area&from=2011-12-01&to=2022-12-01&lang=en"
        
        print(f"Downloading {country}.")
        
        try: 
            res = requests.get(country_svg_path)
            with open("country svg/" + country + ".svg", "w") as f: 
                f.write(res.text) 
        except Exception as e: 
            print(f"Country {country} not available, gave error {e}") 
        
path_list = list(Path("country svg").glob("**/*"))

country_data_dict = {} 

for svg_path in path_list:
    country_name = svg_path.stem 
    print(f"Processing {country_name}.")
    
    with open(svg_path) as f: 
        for line in f: 
            regex_results = re.findall('<tspan x="5" y="22">([0-9. ]+)', line) 
            country_data_dict[country_name] = [year_data.replace(" ", "") for year_data in regex_results] 
      
try: 
    with open("data/output_file.csv", "w") as f: 
        f.write("Country,") 
        [f.write(str(i) + ",") for i in range(2011, 2023)]
        f.write("\n")
        
        for country in country_data_dict.keys(): 
            country_data = country_data_dict[country] 
            
            f.write(country + ",") 
            [f.write(country + ",") for country in country_data]
            f.write("\n")
except Exception as e: 
    print(f"Can't open file, is it already opened? Exception: {e}")

print("Completed data extraction!") 
