from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


import numpy as np

class Protocol(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel)
    )


class PlotData(Protocol):
    x: list
    y: list
    type: str = "scatter"  # Default to scatter plot
    mode: str = "lines"
    marker: dict = {"color": "red"}
    name: str | None = None


class PlotLayout(Protocol):
    title: dict = {"text": "My Plot"}
    xaxis: dict = {"title": "X-Axis"}
    yaxis: dict = {"title": "Y-Axis"}
    autosize: bool = True


class PlotResponse(BaseModel):
    data: list[PlotData] = []# A list of traces
    layout: PlotLayout = PlotLayout()
