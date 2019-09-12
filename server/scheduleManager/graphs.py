from django.utils import timezone

from plotly.offline import plot
import plotly.graph_objs as go


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
                     ticktext=SCHEDULE_GRAPH_TEXTS)
    fig.update_yaxes(showticklabels=False, showgrid=False, range=[0, 1],
                     fixedrange=True)

    shapes = add_weekdays_to_graph(fig, weekday, int(left), int(right))

    # Add current hour indicator as a vertical line
    shapes.append(go.layout.Shape(type="line", x0=hour + minute / 60, y0=0,
                                  x1=hour + minute / 60, y1=1, opacity=0.7,
                                  line=dict(color="LightSeaGreen",
                                            width=2.5, dash="dot")))

    fig.update_layout(shapes=shapes, showlegend=False)

    # Add scheduled irrigation ranges as rectangles
    # @TODO

    # Get html div object
    plt_div = plot(fig, output_type='div', config={"displayModeBar": False,
                                                   "showLegend": False},
                   include_plotlyjs=False, show_link=False, link_text="")

    return plt_div


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
                    color="crimson"
                )))

            shapes.append(go.layout.Shape(type="line",
                                          x0=i, y0=0,
                                          x1=i, y1=1,
                                          line=dict(color="crimson",
                                                    width=2.5)))

    return shapes


def get_weekday_to_print(weekday, iterations, reverse=False):
    weekday_index = weekday

    if (not reverse):
        for i in range(0, iterations):
            if (weekday_index < 6):
                weekday_index += 1
            else:
                weekday_index = 0
    else:
        for i in range(0, iterations):
            if (weekday_index > 0):
                weekday_index -= 1
            else:
                weekday_index = 6

    return WEEKDAYS_DICT[weekday_index]
