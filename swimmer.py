class Swimmer(object):

    def __init__(self, name: str, clubname: str, shortclubname: str, races) -> None:
        self.name = name
        self.clubname = clubname
        self.shortclubname = shortclubname
        self.races = races


class MaleSwimmer(Swimmer):

    def __init__(self, name: str, clubname: str, shortclubname: str, races) -> None:
        super().__init__(name, clubname, shortclubname, races)


class FemaleSwimmer(Swimmer):

    def __init__(self, name: str, clubname: str, shortclubname: str, races) -> None:
        super().__init__(name, clubname, shortclubname, races)


class SwimmerFactory(object):

    def __init__(self, male: str, female: str):
        self.male = male
        self.female = female

    def create(self, gender: str, name: str, clubname: str, shortclubname: str, races) -> Swimmer:
        if gender == self.male:
            return MaleSwimmer(name, clubname, shortclubname, races)
        elif gender == self.female:
            return FemaleSwimmer(name, clubname, shortclubname, races)
        else:
            raise "Unknown gender {}".format(gender)