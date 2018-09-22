import csv
import config
from swimmer import *
from race import *
from jinja2 import Environment, FileSystemLoader, Template
from datetime import date
from xhtml2pdf import pisa
import io


def _load_configuration():
    print("Loading config.json")
    configuration = config.load_config()

    name_column = configuration["columns"]["swimmers"]["name"]
    gender_column = configuration["columns"]["swimmers"]["gender"]
    club_column = configuration["columns"]["swimmers"]["clubname"]
    shortclub_column = configuration["columns"]["swimmers"]["shortclubname"]

    eventnumber_column = configuration["columns"]["races"]["eventnumber"]
    race_column = configuration["columns"]["races"]["race"]
    time_column = configuration["columns"]["races"]["time"]
    place_column = configuration["columns"]["races"]["place"]
    points_column = configuration["columns"]["races"]["points"]
    
    male = configuration["genders"]["male"]
    female = configuration["genders"]["female"]

    print("Configuration loaded")
    return {
        "name_column": name_column,
        "gender_column": gender_column,
        "club_column": club_column,
        "shortclub_column": shortclub_column,
        "eventnumber_column": eventnumber_column,
        "race_column": race_column,
        "time_column": time_column,
        "place_column": place_column,
        "points_column": points_column,
        "male": male,
        "female": female
    }

def _process_swimmers(config):
    swimmer_factory = SwimmerFactory(config["male"], config["female"])
    race_factory = RaceFactory()

    swimmers = []

    file_name = "sw-2018.txt"
    print("Reading input file {}".format(file_name))

    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        # print("File contains the following columns: {}".format(reader.fieldnames))

        max_number_of_races = len([n for n in reader.fieldnames if n.startswith(config["eventnumber_column"])])
        print("File contains results of {} races".format(max_number_of_races))

        for row in reader:
            name = row[config["name_column"]]
            gender = row[config["gender_column"]]
            shortclubname = row[config["shortclub_column"]]
            clubname = row[config["club_column"]]

            if name == config["name_column"]:
                # we are reading the header line now --> skip it
                continue

            races = []

            for i in range(1,  max_number_of_races):
                race = row["{}{}".format(config["race_column"], i)]
                time = row["{}{}".format(config["time_column"], i)]
                points = row["{}{}".format(config["points_column"], i)]

                if race == "":
                    # no more races for this swimmer
                    break
            
                races.append(race_factory.create(race, time, points))

            swimmer = swimmer_factory.create(gender, name, clubname, shortclubname, races)
            # print(swimmer)
            swimmers.append(swimmer)

    print("{} swimmers processed".format(len(swimmers)))
    return swimmers

def _create_rankings(swimmers):
    swimmers_with_points = list(filter(lambda swimmer: swimmer.points > 0, swimmers))
    swimmers_sorted_by_points = sorted(swimmers_with_points, key=lambda swimmer: swimmer.points, reverse=True)
    female_ranking = list(filter(lambda swimmer: isinstance(swimmer, FemaleSwimmer), swimmers_sorted_by_points))
    male_ranking = list(filter(lambda swimmer: isinstance(swimmer, MaleSwimmer), swimmers_sorted_by_points))
    return {
        "female_ranking": female_ranking,
        "male_ranking": male_ranking
    }

def _print_medal_ranks(rankings):
    print("\n--- Medal ranks female ---")
    for i in range(0, 3):
        swimmer = rankings["female_ranking"][i]
        print("{}. {} ({}), {} points".format(i+1, swimmer.name, swimmer.shortclubname, swimmer.points))

    print("\n--- Medal ranks male ---")
    for i in range(0, 3):
        swimmer = rankings["male_ranking"][i]
        print("{}. {} ({}), {} points".format(i+1, swimmer.name, swimmer.shortclubname, swimmer.points))


def _render_and_write_html(rankings, current_year):
    jinja_env = Environment(loader=FileSystemLoader("."))
    template = jinja_env.get_template("template.html")
    html = template.render(year=current_year, females=rankings["female_ranking"], males=rankings["male_ranking"])

    html_file_name = "ranking_{}.html".format(current_year)
    with open(html_file_name, "w") as html_file:
        html_file.write(html)
    print("Ranking written to {}".format(html_file_name))
    
    return html


def _write_pdf(html, current_year):
    pdf_output = io.BytesIO()
    pisa.CreatePDF(html, dest=pdf_output)

    pdf_file_name = "ranking_{}.pdf".format(current_year)
    with open(pdf_file_name, "w+b") as pdf_file:
        pdf_file.write(pdf_output.getvalue())
    print("Ranking written to {}".format(pdf_file_name))



if __name__ == "__main__":
    config = _load_configuration()
    current_year = date.today().year

    swimmers = _process_swimmers(config)
    rankings = _create_rankings(swimmers)

    _print_medal_ranks(rankings)
    html = _render_and_write_html(rankings, current_year)
    _write_pdf(html, current_year)