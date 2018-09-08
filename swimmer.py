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
        best50 = None
        best100 = None
        best200 = None

        for r in self.races:
            if r.distance == 50 and (best50 is None or r.points > best50.points):
                best50 = r
            elif r.distance == 100 and (best100 is None or r.points > best100.points):
                best100 = r
            elif r.distance == 200 and (best200 is None or r.points > best200.points):
                best200 = r

        points50 = points100 = points200 = 0
        if best50 is not None:
            best50.counts_for_ranking = True
            points50 = best50.points
        if best100 is not None:
            best100.counts_for_ranking = True
            points100 = best100.points
        if best200 is not None:
            best200.counts_for_ranking = True
            points200 = best200.points

        return points50 + points100 + points200

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