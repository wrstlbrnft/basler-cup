class Swimmer(object):

    def __init__(self, name: str, clubname: str, shortclubname: str, races) -> None:
        self.name = name
        self.clubname = clubname
        self.shortclubname = shortclubname
        self.races = races
        self.points = self._calculate_points()

    def __str__(self):
        return "{}; {}; {} -- {} races -- {} points".format(
            self.name, self.clubname, self.shortclubname, len(self.races), self.points)

    def __repr__(self):
        return self.__str__()

    def _calculate_points(self) -> int:
        best50 = 0
        best100 = 0
        best200 = 0

        for r in self.races:
            if r.distance == 50 and r.points > best50:
                best50 = r.points
            elif r.distance == 100 and r.points > best100:
                best100 = r.points
            elif r.distance == 200 and r.points > best200:
                best200 = r.points

        return best50 + best100 + best200

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
            raise Exception("Unknown gender {} for swimmer {}".format(gender, name))