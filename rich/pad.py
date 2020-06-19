from .console import (
    Console,
    ConsoleOptions,
    RenderGroup,
    RenderResult,
    RenderableType,
)
from .jupyter import JupyterRenderable
from .measure import Measurement
from .segment import Segment
from .style import Style


class Pad(JupyterRenderable):
    """Pad renderables to a given width.

    Args:
        renderables (RenderableType): One or more renderables.
        width (int, optional): Desired width or None for full width of terminal. Defaults to None.
    """

    def __init__(self, *renderables: RenderableType, width: int = None) -> None:
        self.width = width
        self.renderables = renderables

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        width = console.width if self.width is None else self.width
        renderable = RenderGroup(*self.renderables)
        lines = console.render_lines(renderable, options.update(width=width))
        new_line = Segment.line()
        for line in lines:
            yield from line
            yield new_line

    def __measure__(self, console: Console, max_width: int) -> Measurement:
        width = console.width if self.width is None else self.width
        renderable = RenderGroup(*self.renderables)
        measurement = Measurement.get(console, renderable, width).with_maximum(width)
        return measurement
