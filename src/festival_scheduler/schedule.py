import enum
import functools
from dataclasses import dataclass
from .types import Schedule, Show, Stage


class SolverMode(enum.Enum):
    FAST = 1
    OPTIMAL = 2


@dataclass
class State:
    schedule: Schedule
    unscheduled: list[Show]


def is_done(q: list[State]) -> bool:
    """Checks if the algorithm is done"""
    assert len(q) > 0, "Cannot check an empty queue"

    # If there's stuff left to schedule, we're not done
    if len(q[0].unscheduled) > 0:
        return False

    # If we've only got one option left, we're done
    if len(q) == 1:
        return True

    # The states should be sorted. Hence, if the number of stages of the first is equal or smaller than that of the next
    # option, we're also done (other results can only be worse)
    if len(q[0].schedule.stages) <= len(q[1].schedule.stages):
        return True

    # Else: let's continue to see if there are better options
    return False


def expand_queue(q: list[State], mode: SolverMode) -> list[State]:
    """Expands the queue. N.B.: this *modifies* the queue"""
    # Determine which state to expand
    for state_idx, state in enumerate(q):
        if len(state.unscheduled) > 0:
            state_to_expand = q.pop(state_idx)
            break

    assert len(state_to_expand.unscheduled) > 0, "There is nothing left to expand"

    # Get data from 'state' for easy access
    stages = state_to_expand.schedule.stages
    show_to_add = state_to_expand.unscheduled[0]
    remaining_shows = state_to_expand.unscheduled[1:]

    # For each of the existing stages in the schedule, see if we can fit another show. If so, add it as an option
    count = 0
    for idx, stage in enumerate(stages):
        if stage.could_add(show_to_add):
            q.append(State(
                Schedule(
                    stages[0:idx] + [Stage(stage.shows + [show_to_add])] + stages[idx+1:]
                ),
                remaining_shows
            ))
            # In fast mode, we return this solution. In optimal mode, we keep on adding 'states' massively increasing
            # search space but eventually leading to an optimal solution
            if mode == SolverMode.FAST:
                return q

    # Add a new state to make sure the 'optimal' solution is an option
    q.append(State(
        Schedule(stages + [Stage([show_to_add])]),
        remaining_shows
    ))

    return q


def compare_state(s1: State, s2: State):
    """
    Compares two states to determine which one is more interesting to expand
    """
    # First, compare the number of stages. Since we're looking for an optimum, expand the fewest stages first
    if len(s1.schedule.stages) > len(s2.schedule.stages):
        return 1
    elif len(s1.schedule.stages) < len(s2.schedule.stages):
        return -1

    # If both are equal, compare the number of unscheduled shows
    if len(s1.unscheduled) < len(s2.unscheduled):
        return 1
    elif len(s1.unscheduled) > len(s2.unscheduled):
        return 1

    return 0


def schedule_shows(unscheduled: list[Show], mode: SolverMode = SolverMode.FAST) -> Schedule:
    """
    Schedules the shows so that no two shows are scheduled at the same stage at the same time.

    :param unscheduled: list of shows to schedule
    :param mode: determines whether to solve fast or look for an optimal solution. The latter might become slow
    :return: Schedule with stages containing the shows
    """
    queue = [State(Schedule([]), unscheduled)]
    n = 0  # Debugging
    while True:
        if is_done(queue):
            return queue[0].schedule

        # Sort queue
        queue.sort(key=functools.cmp_to_key(compare_state))

        # Prune queue
        queue = queue[0:100]

        # Expand first option
        queue = expand_queue(queue, mode=mode)

        # Debugging
        n += 1
        if n == 10:
            n = 0
