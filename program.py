import csv
import config
from swimmer import *
from race import *


# def __main__():

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

print("Configuration loaded")

swimmer_factory = SwimmerFactory(configuration["genders"]["male"], configuration["genders"]["female"])
race_factory = RaceFactory()

swimmers = []

file_name = "sw-2018.txt"
print("Reading input file {}".format(file_name))

with open(file_name) as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    # print("File contains the following columns: {}".format(reader.fieldnames))

    max_number_of_races = len([n for n in reader.fieldnames if n.startswith(eventnumber_column)])
    print("File contains results of {} races".format(max_number_of_races))

    for row in reader:
        name = row[name_column]
        gender = row[gender_column]
        shortclubname = row[shortclub_column]
        clubname = row[club_column]

        if name == name_column:
            # we are reading the header line now --> skip it
            continue

        races = []

        for i in range(1,  max_number_of_races):
            race = row["{}{}".format(race_column, i)]
            time = row["{}{}".format(time_column, i)]
            points = row["{}{}".format(points_column, i)]

            if race == "":
                # no more races for this swimmer
                break
        
            races.append(race_factory.create(race, time, points))

        swimmer = swimmer_factory.create(gender, name, clubname, shortclubname, races)
        # print(swimmer)
        swimmers.append(swimmer)

print("{} swimmers processed".format(len(swimmers)))

swimmers_sorted_by_points = sorted(swimmers, key=lambda swimmer: swimmer.points, reverse=True)
female_ranking = list(filter(lambda swimmer: isinstance(swimmer, FemaleSwimmer), swimmers_sorted_by_points))
male_ranking = list(filter(lambda swimmer: isinstance(swimmer, MaleSwimmer), swimmers_sorted_by_points))

print("\n--- Medal ranks female ---")
for i in range(0, 3):
    swimmer = female_ranking[i]
    print("{}. {} ({}), {} points".format(i+1, swimmer.name, swimmer.shortclubname, swimmer.points))

print("\n--- Medal ranks male ---")
for i in range(0, 3):
    swimmer = male_ranking[i]
    print("{}. {} ({}), {} points".format(i+1, swimmer.name, swimmer.shortclubname, swimmer.points))
