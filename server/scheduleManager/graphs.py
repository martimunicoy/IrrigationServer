from django.utils import timezone

from plotly.offline import plot
import plotly.graph_objs as go

from .models import IrrigationHour


MAX_DAY_RANGE = int(4)
HOUR_DIVIDER = int(4)
SCHEDULE_GRAPH_TICKS = [i for i in range(-24 * MAX_DAY_RANGE,
                                         24 * MAX_DAY_RANGE, HOUR_DIVIDER)]
SCHEDULE_GRAPH_TEXTS = [i for i in range(0, 24, HOUR_DIVIDER)] * \
    MAX_DAY_RANGE * 2
WEEKDAYS_DICT = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}


def create_schedule_graph(hour_range=24):
    # Check up hour range
    if (hour_range > MAX_DAY_RANGE * 24):
        raise ValueError('hour_range needs to have a value lower than' +
                         '{}'.format(MAX_DAY_RANGE * 24))

    # Set plotly figure
    fig = go.Figure()

    # Get current weekday and hour
    datetime = timezone.localtime()
    weekday = datetime.weekday()
    hour = datetime.hour
    minute = datetime.minute

    # Get axis range
    left = hour + minute / 60 - hour_range / 2
    right = hour + minute / 60 + hour_range / 2

    # Set up axes
    fig.update_xaxes(range=[left, right],
                     tickvals=SCHEDULE_GRAPH_TICKS, fixedrange=True,
                     ticks="outside", tickwidth=2, ticklen=5,
                     ticktext=SCHEDULE_GRAPH_TEXTS, zeroline=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, range=[0, 1],
                     fixedrange=True, zeroline=False)

    # Initialize figure shapes
    shapes = []

    # Add current hour indicator as a vertical line
    shapes += add_hour_indicator(hour, minute)

    # Add weekday labels to graph
    shapes += add_weekdays_to_graph(fig, weekday, int(left), int(right))

    # Add weekday labels to graph
    shapes += add_scheduled_hours_to_graph(weekday, left, right)

    # Write figure shapes
    fig.update_layout(shapes=shapes, showlegend=False)

    # Add scheduled irrigation ranges as rectangles
    # @TODO

    # Get html div object
    plt_div = plot(fig, output_type='div', config={"displayModeBar": False},
                   include_plotlyjs=False, show_link=False, link_text="")

    return plt_div


def add_hour_indicator(hour, minute):
    shapes = []

    shapes.append(go.layout.Shape(type="line", x0=hour + minute / 60, y0=0,
                  x1=hour + minute / 60, y1=1,
                  line=dict(color="LightSeaGreen", width=2, dash="dot")))

    return shapes


def add_weekdays_to_graph(fig, weekday, left, right):
    shapes = []

    for i in range(left, right):
        if (i % 24 == 0):
            weekday_to_print = get_weekday_to_print(weekday, int(i / 24))

            if (int(i / 24) == 0):
                weekday_to_print = 'Today'

            fig.add_trace(go.Scatter(
                x=[i + (right - left) / 20], y=[0.95],
                mode="text",
                name="Weekday",
                text=['<b>' + weekday_to_print + '</b>'],
                textposition="bottom right",
                hoverinfo="none",
                textfont=dict(
                    family="calibri",
                    size=18,
                    color="coral"
                )))

            shapes.append(go.layout.Shape(type="line",
                                          x0=i, y0=0,
                                          x1=i, y1=1,
                                          line=dict(color="coral",
                                                    width=2.5,
                                                    dash="dash")))

    return shapes


def get_weekday_to_print(weekday, iterations):
    weekday_index = weekday

    if (iterations > 0):
        for i in range(0, iterations):
            if (weekday_index < 6):
                weekday_index += 1
            else:
                weekday_index = 0
    else:
        iterations = -iterations
        for i in range(0, iterations):
            if (weekday_index > 0):
                weekday_index -= 1
            else:
                weekday_index = 6

    return WEEKDAYS_DICT[weekday_index]


def add_scheduled_hours_to_graph(weekday, left, right):
    shapes = []

    irrigation_hours = IrrigationHour.objects.all()

    for i in irrigation_hours:
        print(i)

    return shapes
