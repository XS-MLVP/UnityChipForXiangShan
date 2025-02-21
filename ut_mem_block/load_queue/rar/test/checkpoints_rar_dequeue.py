from toffee.funcov import CovGroup
import numpy as np

__all__ = ["get_coverage_group_of_rar_dequeue"]

from comm import UT_FCOV
from dut.LoadQueueRAR import DUTLoadQueueRAR

def get_vecLdCancel(index: int):
    def calculate_vecLdCancel(dut: DUTLoadQueueRAR) -> bool:
        fbk = [dut.vecFeedback_0, dut.vecFeedback_1]
        vecLdCanceltmp = np.zeros(2, dtype=bool)
        allocate_name = f"allocated_{index}"
        for j in range(2):
            uop_name = 
            vecLdCanceltmp[j] := dut.inner[allocate_name].value && fbk(j)["valid"].value && fbk(j)["bits_feedback_0"] && uop(i).robIdx === fbk(j).bits.robidx && uop(i).uopIdx === fbk(j).bits.uopidx
        vecLdCancel := vecLdCanceltmp.reduce(_ || _)
        return valid

    return calculate_vecLdCancel

def get_coverage_group_of_rar_dequeue(dut: DUTLoadQueueRAR) -> CovGroup:
    slot_name = ["br_slot_0", "tail_slot"]

    g = CovGroup(UT_FCOV("../UT_LoadQueue_RAR"))

    # Calculate TotalSum in SC predict
    g.add_watch_point(
        dut,
        {slot_name[w]: is_calculate_predict_total_sum(w) for w in range(2)},
        name="SC Predict Calculate TotalSum "
    )
    # SC doesn't use as Alt is used
    for hit in range(2):
        s = "SC is Not Used and TAGE Use T0, Tn " + ("Hit" if hit else "Miss")
        g.add_watch_point(dut, {slot_name[w]: is_not_use_sc_as_tage_use_alt(w, hit) for w in range(2)}, name=s)

    # TAGE provider is used, and SC change/doesn't change prediction.
    for use_sc in range(2):
        s = " ".join(["SC", ("is used" if use_sc else "is NOT used"), ",", "TAGE use Tn"])
        g.add_watch_point(
            dut,
            {slot_name[w]: is_tage_taken_from_tn(w, use_sc) for w in range(2)},
            name=s
        )

    return g