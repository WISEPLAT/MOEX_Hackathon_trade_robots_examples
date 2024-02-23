import pandas as pd

import vizro.plotly.express as px
import plotly.graph_objects as go
from vizro import Vizro
import vizro.models as vm
from vizro.models.types import capture

df = pd.read_csv("test3.csv",sep=";")
print(df.head())

@capture("graph")
def m_bars(data_frame, color=None, size=None, hline=None):
    fig = go.Figure(data=[go.Candlestick(x=data_frame["end"],open=data_frame["open"],high=data_frame["high"],low=data_frame["low"],close=data_frame["close"])])
    return fig

page = vm.Page(
    title="SBER",
    components=[
        vm.Graph(id="candles", figure=m_bars(data_frame=df)),
        vm.Graph(id="line_chart", figure=px.line(df, x="end", y="open", title="общий портфель"))
    ],
    controls=[
        vm.Filter(column="close",selector=vm.RangeSlider(title="time")),
#            vm.Parameter(targets=["candles"], selector=Slider(min=0, max=1, default=0.8, title="Bubble opacity"))

    ],
)

dashboard = vm.Dashboard(pages=[page])

Vizro().build(dashboard).run()
