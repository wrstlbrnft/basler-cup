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

print("Configuration loaded!")

swimmer_factory = SwimmerFactory(configuration["genders"]["male"], configuration["genders"]["female"])
race_factory = RaceFactory()

swimmers = []

file_name = "sw.txt"
print("Reading input file {}".format(file_name))
with open(file_name) as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    print("File contains the following columns: {}".format(reader.fieldnames))

    number_of_races = len([n for n in reader.fieldnames if n.startswith(eventnumber_column)])
    print("File contains results of {} races".format(number_of_races))

    for row in reader:
        # print(', '.join(row))

        name = row[name_column]
        gender = row[gender_column]
        shortclubname = row[shortclub_column]
        clubname = row[club_column]

        if name == name_column:
            # we are reading the header line now --> skip it
            continue

        races = []
        # for ??? in row:
        #     race = row[configuration.columns.race]
        #     time = row[configuration.columns.time]
        #     points = row[configuration.columns.points]
        #
        #     races.append(race_factory.create(race, time, points))

        print("Swimmer: {}; {}; {}; {}".format(name, gender, shortclubname, clubname))
        swimmers.append(swimmer_factory.create(gender, name, clubname, shortclubname, races))

    print(swimmers)
