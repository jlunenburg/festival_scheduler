from festival_scheduler.types import Schedule, Show, Stage
from festival_scheduler.visualization import visualize_schedule


# Inspiration: https://matplotlib.org/stable/gallery/lines_bars_and_markers/broken_barh.html#sphx-glr-gallery-lines-bars-and-markers-broken-barh-py


def test_simple() -> None:
    show = Show("show1", 1, 2)
    stage = Stage([show])
    schedule = Schedule([stage])
    visualize_schedule(schedule=schedule)


def test_multiple() -> None:
    show1 = Show("show1", 1, 2)
    show2 = Show("show2", 3, 5)
    stage1 = Stage([show1, show2])
    show3 = Show("show3", 2, 5)
    show4 = Show("show4", 7, 9)
    stage2 = Stage([show3, show4])
    schedule = Schedule([stage1, stage2])
    visualize_schedule(schedule=schedule)





    
