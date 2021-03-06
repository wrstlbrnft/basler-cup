class Race(object):

    def __init__(self, distance: int, style: str, time: str, points: int):
        self.distance = distance
        self.style = style
        self.time = time
        self.points = points
        self.counts_for_ranking = False


class RaceFactory(object):

    def create(self, race: str, time: str, points: str) -> Race:
        distance_and_style = race.split(" ")
        distance = int(distance_and_style[0].strip("m"))
        style = distance_and_style[1]
        parsed_points = 0
        if points != "":
            parsed_points = int(points)

        return Race(distance, style, time, parsed_points)
