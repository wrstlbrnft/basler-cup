import csv
import config
from swimmer import *
from race import *


def __main__():

    configuration = config.load_config()

    swimmer_factory = SwimmerFactory(configuration.genders.male, configuration.genders.female)
    race_factory = RaceFactory()

    swimmers = []

    with open("sw.txt") as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        # read header line
        header = reader.get_line
        header.filter(configuration.columns.name)

        for row in reader:
            # print(', '.join(row))

            name = row[configuration.columns.name]
            gender = row[configuration.columns.gender]
            shortclubname = row[configuration.columns.shortclubname]
            clubname = row[configuration.columns.clubname]

            races = []
            # for ??? in row:
            #     race = row[configuration.columns.race]
            #     time = row[configuration.columns.time]
            #     points = row[configuration.columns.points]
            #
            #     races.append(race_factory.create(race, time, points))

            swimmers.append(swimmer_factory.create(gender, name, clubname, shortclubname, races))

        print(swimmers)
