"""
Function to download the EGM2008 Global Earth Geoid from the GMT data server,
and load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""
from pygmt.datasets.load_remote_dataset import _load_remote_dataset
from pygmt.helpers import kwargs_to_strings


@kwargs_to_strings(region="sequence")
def load_earth_geoid(resolution="01d", region=None, registration=None):
    r"""
    Load the EGM2008 Global Earth Geoid in various resolutions.

    The grids are downloaded to a user data directory
    (usually ``~/.gmt/server/earth/earth_geoid/``) the first time you invoke
    this function. Afterwards, it will load the grid from the data directory.
    So you'll need an internet connection the first time around.

    These grids can also be accessed by passing in the file name
    **@earth_geoid**\_\ *res*\[_\ *reg*] to any grid plotting/processing
    function. *res* is the grid resolution (see below), and *reg* is grid
    registration type (**p** for pixel registration or **g** for gridline
    registration).

    Refer to :gmt-datasets:`earth-geoid.html` for more details.

    Parameters
    ----------
    resolution : str
        The grid resolution. The suffix ``d`` and ``m`` stand for
        arc-degree and arc-minute. It can be ``"01d"``, ``"30m"``,
        ``"20m"``, ``"15m"``, ``"10m"``, ``"06m"``, ``"05m"``, ``"04m"``,
        ``"03m"``, ``"02m"``, or ``"01m"``.

    region : str or list
        The subregion of the grid to load, in the forms of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*.
        Required for grids with resolutions higher than 5
        arc-minute (i.e., ``"05m"``).

    registration : str
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``None``, where
        a pixel-registered grid is returned unless only the
        gridline-registered grid is available.

    Returns
    -------
    grid : :class:`xarray.DataArray`
        The Earth geoid grid. Coordinates are latitude and
        longitude in degrees. Units are in meters.

    Note
    ----
    The :class:`xarray.DataArray` grid doesn't support slice operation, for
    Earth geoid grids with resolutions of 5 arc-minutes or higher,
    which are stored as smaller tiles.
    """
    grid = _load_remote_dataset(
        dataset_name="earth_geoid",
        dataset_prefix="earth_geoid_",
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid