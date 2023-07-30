import sys
from festival_scheduler.read_input import get_shows
from festival_scheduler.schedule import schedule_shows
from festival_scheduler.visualization import visualize_schedule


def main() -> int:
    shows = get_shows()
    schedule = schedule_shows(shows)
    visualize_schedule(schedule)
    return 0


if __name__ == "__main__":
    sys.exit(main())
