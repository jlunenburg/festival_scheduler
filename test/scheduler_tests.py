import unittest
from festival_scheduler.schedule import schedule_shows, SolverMode
from festival_scheduler.types import Show


def test_single() -> None:
    unscheduled = [Show("show_1", 1, 3)]
    schedule = schedule_shows(unscheduled)
    nr_stages = len(schedule.stages)
    assert nr_stages == 1, f"Schedule has {nr_stages} stages instead of 1"
    nr_shows = len(schedule.stages[0].shows)
    assert nr_shows == 1, f"Stage has {nr_shows} shows instead of 1"


def test_two_on_one() -> None:
    """Checks if two shows that fit on one stage result in a schedule with one stage"""
    unscheduled = [Show("show_1", 1, 3), Show("show_2", 4, 5)]
    schedule = schedule_shows(unscheduled)
    nr_stages = len(schedule.stages)
    assert nr_stages == 1, f"Schedule has {nr_stages} stages instead of 1"
    nr_shows = len(schedule.stages[0].shows)
    assert nr_shows == 2, f"Stage has {nr_shows} shows instead of 2"


def test_two_on_two() -> None:
    """Checks if two shows that don't fit on one stage result in a schedule with two stages (with one show/stage)"""
    unscheduled = [Show("show_1", 1, 3), Show("show_2", 1, 3)]
    schedule = schedule_shows(unscheduled)
    nr_stages = len(schedule.stages)
    assert nr_stages == 2, f"Schedule has {nr_stages} stages instead of 2"
    nr_shows = len(schedule.stages[0].shows)
    assert nr_shows == 1, f"Stage has {nr_shows} shows instead of 1"
    nr_shows = len(schedule.stages[1].shows)
    assert nr_shows == 1, f"Stage has {nr_shows} shows instead of 1"


def test_three_on_two() -> None:
    """Checks if the third show is added on one of the existing stages instead of creating a new one"""
    unscheduled = [Show("show_1", 1, 3), Show("show_2", 1, 5), Show("show_3", 4, 5)]
    schedule = schedule_shows(unscheduled)
    nr_stages = len(schedule.stages)
    assert nr_stages == 2, f"Schedule has {nr_stages} stages instead of 2"
    nr_shows = len(schedule.stages[0].shows)
    assert nr_shows == 2, f"Stage has {nr_shows} shows instead of 2"
    nr_shows = len(schedule.stages[1].shows)
    assert nr_shows == 1, f"Stage has {nr_shows} shows instead of 1"


# @unittest.skip("No support for optimal solutions; this will become too slow with the current implementation")
def test_four_on_two_complex() -> None:
    """Checks if an 'optimal' solution is found where a naive implementation would fail (1+3 fits, 2+4 does not; 1+4 and
    2+3 also fits"""
    unscheduled = [Show("show_1", 1, 2), Show("show_2", 1, 3), Show("show_3", 4, 5), Show("show_4", 3, 4)]
    schedule = schedule_shows(unscheduled, SolverMode.OPTIMAL)
    nr_stages = len(schedule.stages)
    assert nr_stages == 2, f"Schedule has {nr_stages} stages instead of 2"
    nr_shows = len(schedule.stages[0].shows)
    assert nr_shows == 2, f"Stage has {nr_shows} shows instead of 2"
    nr_shows = len(schedule.stages[1].shows)
    assert nr_shows == 2, f"Stage has {nr_shows} shows instead of 2"


def test_length_difference() -> None:
    """Checks if show 1 starts before and ends after show 2"""
    unscheduled = [Show("show_1", 1, 4), Show("show_2", 2, 3)]
    schedule = schedule_shows(unscheduled)
    nr_stages = len(schedule.stages)
    assert nr_stages == 2, f"Schedule has {nr_stages} stages instead of 2"

    unscheduled = [Show("show_1", 2, 3), Show("show_2", 1, 4)]
    schedule = schedule_shows(unscheduled)
    nr_stages = len(schedule.stages)
    assert nr_stages == 2, f"Schedule has {nr_stages} stages instead of 2"


def test_adjacent() -> None:
    """Checks if just or just not overlapping shows work properly"""
    unscheduled = [Show("show_1", 1, 2), Show("show_2", 2, 3)]
    schedule = schedule_shows(unscheduled)
    nr_stages = len(schedule.stages)
    assert nr_stages == 2, f"Schedule has {nr_stages} stages instead of 2"

    unscheduled = [Show("show_1", 2, 3), Show("show_2", 1, 2)]
    schedule = schedule_shows(unscheduled)
    nr_stages = len(schedule.stages)
    assert nr_stages == 2, f"Schedule has {nr_stages} stages instead of 2"

    unscheduled = [Show("show_1", 1, 2), Show("show_2", 3, 4)]
    schedule = schedule_shows(unscheduled)
    nr_stages = len(schedule.stages)
    assert nr_stages == 1, f"Schedule has {nr_stages} stages instead of 1"

    unscheduled = [Show("show_1", 3, 4), Show("show_2", 1, 2)]
    schedule = schedule_shows(unscheduled)
    nr_stages = len(schedule.stages)
    assert nr_stages == 1, f"Schedule has {nr_stages} stages instead of 1"
