"""
shift_origin - Shift plot origin in x and/or y directions.
"""
from contextlib import contextmanager

from pygmt.clib import Session
from pygmt.helpers import build_arg_string
from pygmt.exceptions import GMTInvalidInput


@contextmanager
def shift_origin(self, xshift=None, yshift=None):
    """
    Shift plot origin in x and/or y directions.

    This method shifts the plot origin relative to the current origin by
    *xshift* and *yshift* in x and y directions, respectively. Optionally,
    append the length unit (**c** for centimeters, **i** for inches, or **p**
    for points) to the shifts. Default unit if not given is **c**.

    For *xshift*, a special character **w** can also be used, which represents
    the bounding box width of previous plot. The full syntax is
    [[±][*f*]\ **w**\ [/\ *d*\ ]±]\ *xoff*, where optional signs, factor *f* and
    divisor *d* can be used to compute an offset that may be adjusted further
    by ±*off*.

    Similarity, *yshift* can in general be [[±][*f*]\ **h**\ [/\ *d*\ ]±]\ *yoff*,
    in which **h** is the bounding box height of previous plot.

    Shiftting plot origin can be performed permanently or temporarily, depending
    on how the method is called.

    1. Calling :meth:`Figure.shift_origin` directly will shift plot origin
       permanently, which affects all subsequent plottings:

       .. code-block::

          Figure.shift_origin(xshift=..., yshift=...)

    2. Calling :meth:`Figure.shift_origin` as a context manager:

        .. code-block::

            with Figure.shift_origin(xshift=..., yshift=...):
                ...

    Parameters
    ----------
    xshift : float or str
        Shift plot origin in x direction.
    yshift : float or str
        Shift plot origin in y direction.

    Examples
    --------
    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    >>> fig.shift_origin(xshift=12)
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    >>> fig.shift_origin(xshift="w+2c")
    >>> fig.show()
    """
    self._preprocess()  # pylint: disable=protected-access

    kwargs = {"T": True}
    if xshift:
        kwargs["X"] = xshift
    if yshift:
        kwargs["Y"] = yshift

    try:
        with Session() as lib:
            lib.call_module(module="plot", args=build_arg_string(kwargs))
            saved_xshift = lib.get_common("X")  # False or xshift in inches
            saved_yshift = lib.get_common("Y")  # False or yshift in inches
            yield
    finally:
        if saved_xshift:
            kwargs["X"] = f"{-1.0 * saved_xshift}i"
        if saved_yshift:
            kwargs["Y"] = f"{-1.0 * saved_yshift}i"
        with Session() as lib:
            lib.call_module(module="plot", args=build_arg_string(kwargs))
