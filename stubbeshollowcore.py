from staticsfunctions import *

def designstubbeshc(fl_uniform_live_load, fl_span, str_units, db_hollowcore):

    database_hc = db_hollowcore.query.all()
    design_array = []

    if str_units == 'imperial':
        """
        convert to metric
        """
        fl_uniform_live_load = fl_uniform_live_load/20.9
        fl_span = fl_span*0.3048

        fl_mf_live = moment_simple_beam(fl_span=fl_span, fl_width=1, fl_loading=fl_uniform_live_load)

        for hollow_core in database_hc:
            fl_mf_dead = moment_simple_beam(fl_span=fl_span, fl_width=1, fl_loading=float(hollow_core.swkpa))
            fl_mu = 1.25 * fl_mf_dead + 1.5 * fl_mf_live
            fl_mr = float(hollow_core.mrnmm)/1000000
            fl_utilization = round(fl_mu/fl_mr, 2)
            design = {"depth": round(hollow_core.depthmm/25.4, 1),
                      "strands13mm": hollow_core.strands13mm,
                      "mr": round(fl_mr/4.44, 0),
                      "mu": round(fl_mu/4.44, 0),
                      "utilization": fl_utilization
                      }

            design_array.append(design)

    else:
        pass

    return design_array
