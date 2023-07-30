import matplotlib.pyplot as plt
from .types import Schedule


def _add_bars(ax: plt.Axes, schedule: Schedule, y_increment: float) -> None:
    y_coordinate = 0
    for stage in reversed(schedule.stages):

        occupation = []
        y_coordinate += y_increment
        for show in stage.shows:
            occupation.append((show.start_idx, show.end_idx - show.start_idx + 0.999))
        ax.broken_barh(
            occupation,
            (y_coordinate, 8),
            facecolors=['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']
        )


def _add_ticks(ax: plt.Axes, schedule: Schedule) -> None:
    y_coordinate = 4.0
    y_ticks = []
    y_labels = []
    for idx, stage in enumerate(reversed(schedule.stages)):
        y_coordinate += 10
        y_ticks.append(y_coordinate)
        y_labels.append(f" Stage {len(schedule.stages) - idx}")
    ax.set_yticks(y_ticks, y_labels)


def _add_labels(ax: plt.Axes, schedule: Schedule, y_increment: float) -> None:
    y_coordinate = 4.0
    for stage in reversed(schedule.stages):
        y_coordinate += y_increment
        for show in stage.shows:
            ax.annotate(show.name, (show.start_idx + 0.1, y_coordinate))


def visualize_schedule(schedule: Schedule) -> None:
    fig, ax = plt.subplots(figsize=(19.2, 4.8))

    y_increment = 10

    # Create plot
    _add_bars(ax, schedule, y_increment)

    # Add axis data
    _add_ticks(ax, schedule)

    # Add show label
    _add_labels(ax, schedule, y_increment)

    ax.grid(True)
    plt.title("Festival Schedule")
    plt.show()
