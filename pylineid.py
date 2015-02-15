import numpy as np

import matplotlib.lines as mlines

__version__ = '0.1'


def _convert_to_array(x, size, name):
    """
    Check length of array or convert scalar to array.
    Check to see is `x` has the given length `size`. If this is true
    then return Numpy array equivalent of `x`. If not then raise
    ValueError, using `name` as an identification. If len(x) returns
    TypeError, then assume it is a scalar and create a Numpy array of
    length `size`. Each item of this array will have the value as `x`.

    Notes (N. Rusomarov)
    --------------------
    Taken verbatim from https://github.com/phn/lineid_plot
    """
    try:
        l = len(x)
        if l != size:
            raise ValueError(
                "{0} must be scalar or of length {1}".format(
                    name, size))
    except TypeError:
        # Only one item
        xa = np.array([x] * size)  # Each item is a diff. object.
    else:
        xa = np.array(x)

    return xa


def adjust_boxes(line_wave, box_widths, left_edge, right_edge,
                 max_iter=1000, adjust_factor=0.35,
                 factor_decrement=3.0, fd_p=0.75):
    """
    Adjust given boxes so that they don't overlap.
    Parameters
    ----------
    line_wave: list or array of floats
        Line wave lengths. These are assumed to be the initial y (wave
        length) location of the boxes.
    box_widths: list or array of floats
        Width of box containing labels for each line identification.
    left_edge: float
        Left edge of valid data i.e., wave length minimum.
    right_edge: float
        Right edge of valid data i.e., wave lengths maximum.
    max_iter: int
        Maximum number of iterations to attempt.
    adjust_factor: float
        Gap between boxes are reduced or increased by this factor after
        each iteration.
    factor_decrement: float
        The `adjust_factor` itself if reduced by this factor, after
        certain number of iterations. This is useful for crowded
        regions.
    fd_p: float
        Percentage, given as a fraction between 0 and 1, after which
        adjust_factor must be reduced by a factor of
        `factor_decrement`. Default is set to 0.75.
    Returns
    -------
    wlp, niter, changed: (float, float, float)
        The new y (wave length) location of the text boxes, the number
        of iterations used and a flag to indicated whether any changes to
        the input locations were made or not.
    Notes
    -----
    This is a direct translation of the code in lineid_plot.pro file in
    NASA IDLAstro library.
    Positions are returned either when the boxes no longer overlap or
    when `max_iter` number of iterations are completed. So if there are
    many boxes, there is a possibility that the final box locations
    overlap.
    References
    ----------
    + http://idlastro.gsfc.nasa.gov/ftp/pro/plot/lineid_plot.pro
    + http://idlastro.gsfc.nasa.gov/

    Notes (N. Rusomarov)
    --------------------
    Taken from https://github.com/phn/lineid_plot
    """
    # Adjust positions.
    niter = 0
    changed = True

    wlp = np.copy(line_wave)
    nlines = wlp.size
    while changed:
        changed = False
        for i in range(nlines):
            if i > 0:
                diff1 = wlp[i] - wlp[i - 1]
                separation1 = (box_widths[i] + box_widths[i - 1]) / 2.0
            else:
                diff1 = wlp[i] - left_edge + box_widths[i] * 1.01
                separation1 = box_widths[i]
            if i < nlines - 1:
                diff2 = wlp[i + 1] - wlp[i]
                separation2 = (box_widths[i] + box_widths[i + 1]) / 2.0
            else:
                diff2 = right_edge + box_widths[i] * 1.01 - wlp[i]
                separation2 = box_widths[i]

            if diff1 < separation1 or diff2 < separation2:
                if wlp[i] == left_edge:
                    diff1 = 0
                if wlp[i] == right_edge:
                    diff2 = 0
                if diff2 > diff1:
                    wlp[i] = wlp[i] + separation2 * adjust_factor
                    wlp[i] = wlp[i] if wlp[i] < right_edge else \
                        right_edge
                else:
                    wlp[i] = wlp[i] - separation1 * adjust_factor
                    wlp[i] = wlp[i] if wlp[i] > left_edge else \
                        left_edge
                changed = True
            niter += 1
        if niter == max_iter * fd_p:
            adjust_factor /= factor_decrement
        if niter >= max_iter:
            break

    return wlp, changed, niter


def put_lines(ax, cwaves, fluxes, ypos2, ypos3, labels,
              bars=None, bscale=None, edges=None, barskwargs=dict(),
              adjustkwargs=dict(), linekwargs=dict(), textkwargs=dict()):
    """
    Automatic layout of labels for spectral lines in a plot.

    Parameters
    ----------
    ax : Matplotlib Axes
        The Axes in which the labels are to be placed.
    cwaves: list or array of floats
        Wavelength of the lines to be plotted.
    fluxes: list or array of floats
        Flux at each wavelength in cwaves.
    ypos2: float, list or array of floats
        Maximum value of the data on the y-axis.
    ypos3: float, list or array of floats
        Position of the text labels on the y-axis.
    labels: list of strings
        Label text for each line.
    bars: list or array of floats (optional)
        Relative strength (between 0 and 1) of each line.
    bscale: float (optional)
        The bars are rescaled to this value. If it's not
        given, the value of bscale is the max. height of all
        text labels. At the end we plot bars * bscale.
    edges: list or array of floats
        Gives the ranges where we can put the lines.
    barskwargs: key value pairs (optional)
        These keywords control the style of the vertical
        bars that show the relative line strength (passed
        to ax.vlines)
    linekwargs: key value pairs (optional)
        These keywords control the style of the line that
        connects the spectrum and the text label (line 1
        and line 2 in the sketch below.). This is passed
        to matplotlib.lines.Line2D.
    textkwargs: key value pairs (optional)
        These keywords control the style of the text
        labels (passed to ax.text)

    Returns
    -------
    A dictinary with fields: lines, texts, and vbars.
        lines: list of matplotlib.lines.Line2D instances.
            These are the lines that connect the spectrum
            and the text labels.
        texts: matplotlib Axes text instances of the text
            labels that were printed on the plot.
        vbars: collection of vertical lines (returned by
            ax.vlines), or None.

    Notes
    -----
    Elements of the plot for a single line:

    |(xpos3)
    |---x-------------- (ypos3 + bars)
    |   |
    |   | vbar
    |   |
    |---x-------------- (ypos3)
    |    \
    |     \
    |      \ line 2
    |       \
    |        \
    |---------x-------- (ypos2)
    |         |
    |         | line 1
    |         |
    |---------x-------- (flux)
    |      (cwave)

    cwaves and fluxes indicate the starting position of
    the line (matplotlib.lines.Line2D object)

    ypos2 and ypos3 indicate the y-axis position, where
    line 1 should connect with line 2.

    ypos3 is the level on the y-axis where we want to
    put the text labels. It can be one number, which is
    the same for all labels, or one for each label.

    xpos3 is the position of each text label on the x-axis
    (in data coordinates). This is  calculated automatically
    by the function adjust_boxes.

    labels contains the text for each line.

    bars can be additional list or array of floats with
    the same size as cwaves that gives the relative strength
    (between 0 and 1) of each line.
    """
    # prepare data
    fig = ax.get_figure()
    ypos2 = _convert_to_array(ypos2, len(cwaves), 'ypos2')
    ypos3 = _convert_to_array(ypos3, len(cwaves), 'ypos3')

    # update kwargs
    textkwargs_defaults = dict(size=9, rotation='vertical',
                               ha='right', va='bottom')
    textkwargs_defaults.update(textkwargs)

    linekwargs_defaults = dict(color='black', lw=0.75)
    linekwargs_defaults.update(linekwargs)

    adjustkwargs_defaults = dict(max_iter=10000, adjust_factor=0.35,
                                 factor_decrement=3.0, fd_p=0.75)
    adjustkwargs_defaults.update(adjustkwargs)

    barskwargs_defaults = dict(color='red', lw=1.25)
    barskwargs_defaults.update(barskwargs)

    # First plot the text labels at cwaves as first approximation
    texts = []
    textkwargs_defaults['size'] += 1
    for cwave, yp3, label in zip(cwaves, ypos3, labels):
        texts.append(ax.text(cwave, yp3, label, **textkwargs_defaults))

    # Update the figure with the texts.
    fig.canvas.draw()

    # Get annotation boxes and convert their dimensions from display
    # coordinates to data coordinates. Specifically, we want the width
    # in wavelength units. For each annotation box, transform the
    # bounding box into data coordinates and extract the width.
    ax_inv_trans = ax.transData.inverted()  # display to data
    text_widths = []  # text box width in wavelength units.
    text_heights = []  # text box height in units of y-axis
    # This doesn't work if the figure hasn't been drawn before.
    for text in texts:
        b_ext = text.get_window_extent()
        text_widths.append(b_ext.transformed(ax_inv_trans).width)
        text_heights.append(b_ext.transformed(ax_inv_trans).height)

    # Find final x locations of boxes so that they don't overlap.
    # Function adjust_boxes uses a direct translation of the equivalent
    # code in lineid_plot.pro in IDLASTRO.
    xlims = ax.get_xlim()
    if edges is None:
        edges = (xlims[0]+text_widths[0]*1.5, xlims[1]-text_widths[-1]*0.5)
    xpos3, niter, changed = adjust_boxes(np.copy(cwaves), text_widths,
                                         *edges, **adjustkwargs_defaults)

    # Redraw the boxes at their new x location.
    for text, xp3 in zip(texts, xpos3):
        text.set_x(xp3)
        text.set_size(textkwargs_defaults['size']-1)

    # Now connect the spectrum with the labels
    lines = []
    args = zip(cwaves, fluxes, ypos2, ypos3, xpos3)
    for cwave, flux, yp2, yp3, xp3 in args:
        line = mlines.Line2D([cwave, cwave, xp3], [flux, yp2, yp3],
                             **linekwargs_defaults)
        lines.append(ax.add_line(line))

    # Add vertical bars indicating the line strength (optional part)
    if bars is not None:
        if bscale is None:
            bscale = np.max(text_heights)
        vbars = ax.vlines(xpos3, ypos3, ypos3 + bars * bscale,
                          **barskwargs_defaults)
    else:
        vbars = None

    # Update the figure
    fig.canvas.draw()

    return dict(lines=lines, texts=texts, vbars=vbars)
