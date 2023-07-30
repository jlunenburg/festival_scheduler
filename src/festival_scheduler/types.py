from dataclasses import dataclass


@dataclass
class Show:
    """Class with show data"""
    name: str
    start_idx: int
    end_idx: int

    def interferes(self, show) -> bool:
        """Checks if the passed in show interferes with this one"""
        if self.start_idx <= show.start_idx <= self.end_idx:
            return True
        if self.start_idx <= show.end_idx <= self.end_idx:
            return True
        if show.start_idx <= self.start_idx <= show.end_idx:
            return True
        if show.start_idx <= self.end_idx <= show.end_idx:
            return True
        return False


@dataclass
class Stage:
    shows: list[Show]

    def could_add(self, show: Show) -> bool:
        """
        Checks if the show that is passed would fit on this stage
        :param show:
        :return:
        """
        for s in self.shows:
            if s.interferes(show):
                return False
        return True


@dataclass
class Schedule:
    stages: list[Stage]

