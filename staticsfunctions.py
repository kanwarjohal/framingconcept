def moment_simple_beam(fl_span, fl_width, fl_loading):
    """
    return midspan moment for a simply supported beam
    :param fl_span:
    :param fl_width:
    :param fl_loading:
    :return:
    """
    fl_mf = (fl_loading * fl_width * fl_span**2)/8

    return fl_mf
