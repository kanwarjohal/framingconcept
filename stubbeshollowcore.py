from staticsfunctions import *

def designstubbeshc(fl_uniform_live_load, fl_span, str_units, db_hollowcore):

    database_hc = db_hollowcore.query.all()
    design_dict = {}

    if str_units == 'imperial':
        fl_uniform_live_load = fl_uniform_live_load/20.9
        fl_span = fl_span*0.3048
        fl_mf_live = moment_simple_beam(fl_span = fl_span, fl_width = 1, fl_loading = fl_uniform_live_load)


        for hollow_core in database_hc:
            fl_mf_dead = moment_simple_beam(fl_span = fl_span, fl_width = 1, fl_loading = hollow_core.swkpa)
            fl_mu = 1.25 * fl_mf_dead + 1.5 * fl_mf_live
            fl_mr = hollow_core.mrnmm/1000000
            fl_utilization = fl_mu/fl_mr

            design_dict.update({"depth": hollow_core.depth,
                                "strands13mm": hollow_core.strands13mm,
                                "mr": hollow_core.mr,
                                "mu": fl_mu,
                                "utilization": fl_utilization})
    else:
        pass

    return design_dict
