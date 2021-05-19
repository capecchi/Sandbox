import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

xx = [1, 2, 3, 4]
y1 = [8, 7, 6, 5]
y2 = [60. / y for y in y1]  # min/mile

pplotly = True
if pplotly:
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=xx, y=y1, name="speed data"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=xx, y=y2, name="pace data"),
        secondary_y=True,
    )
    fig.update_xaxes(title_text="distance")
    fig.update_yaxes(title_text="speed", secondary_y=False)
    fig.update_yaxes(title_text="pace", secondary_y=True)
    layout = go.Layout

    fig.show()
else:
    fig, ax = plt.subplots()

    ax.plot(xx, y1)
    ax.set_ylabel('speed (miles/hr)')
    ax.set_xlabel('distance (miles)')


    def spd2pac(y):
        return 60. / y


    def pac2spd(y):
        return 60. / y


    secax = ax.secondary_yaxis('right', functions=(spd2pac, pac2spd))
    secax.set_ylabel('pace (min/mile)')
    plt.show()
