import datetime
import gantt


def create_gantt(eventlist):

    # Create a resource
    #rGARDEN = gantt.Resource('rGARDEN')
    # Create a project
    p = gantt.Project(name='Projet 1')
    for e in eventlist:
        t = gantt.Task(name=e.vegetable.name,
                       start=e.seeding_start,
                       duration=(e.harvest_end-e.seeding_start).days,
                       color="#FF8080")
        p.add_task(t)

    p.make_svg_for_tasks(filename='planner/static/planner/ganttcharts/all_events.svg',
                         today=datetime.date.today(),
                         start=datetime.date(2018,1, 1), ## TODO : first seeding start
                         end=datetime.date(2019, 1, 14), ## TODO : last harvest end
                         scale=gantt.DRAW_WITH_WEEKLY_SCALE )
