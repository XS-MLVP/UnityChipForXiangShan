"""
    Checkpoint for prediction
"""

from dut.ITTage import DUTITTage


def is_hit_table_i(i: int):
    def hit_table_i(dut: DUTITTage):
        tn_hit = getattr(dut, f"ITTage_tables_{i}_io_resp_valid").value
        return tn_hit

    return hit_table_i


def is_hit_multi_table():
    def hit_multi_table(dut: DUTITTage):
        tn_hit = 0
        for i in range(5):
            tn_hit += is_hit_table_i(i)(dut)
        return tn_hit > 1

    return hit_multi_table


def is_hit_no_table():
    def hit_no_table(dut: DUTITTage):
        tn_hit = 0
        for i in range(5):
            tn_hit += is_hit_table_i(i)(dut)
        return tn_hit == 0

    return hit_no_table


def is_alt_from_ftb():
    def alt_from_ftb(dut: DUTITTage):
        provided = dut.ITTage_s3_provided.value
        alt_provided = dut.ITTage_s3_altProvided.value
        return alt_provided == 0 and provided == 0

    return alt_from_ftb


def is_alt_from_table_i(i: int):
    def alt_from_table_i(dut: DUTITTage):
        alt_provided = dut.ITTage_s3_altProvided.value
        alt_provider = dut.ITTage_s3_altProvider.value
        return alt_provided and alt_provider == i

    return alt_from_table_i


# final prediction target
def is_src_from_main():
    def src_from_main(dut: DUTITTage):
        provided = dut.ITTage_s3_provided.value
        provider_ctr = dut.ITTage_s3_providerCtr.value
        provider_target = dut.ITTage_s3_providerTarget.value
        pred_target = dut.io_out_s3_full_pred_3_jalr_target.value
        return provided > 0 and provider_ctr > 0 and provider_target == pred_target

    return src_from_main


def is_src_from_alt():
    def src_from_alt(dut: DUTITTage):
        provided = dut.ITTage_s3_provided.value
        provider_ctr = dut.ITTage_s3_providerCtr.value
        alt_provided = dut.ITTage_s3_altProvided.value
        alt_target = dut.ITTage_s3_altProviderTarget.value
        pred_target = dut.io_out_s3_full_pred_3_jalr_target.value
        return provided > 0 and provider_ctr == 0 and alt_provided > 0 and alt_target == pred_target

    return src_from_alt


def is_src_from_ftb():
    def src_from_ftb(dut: DUTITTage):
        provided = dut.ITTage_s3_provided.value
        alt_provided = dut.ITTage_s3_altProvided.value
        ftb_target = dut.io_in_bits_resp_in_0_s2_full_pred_3_jalr_target.value
        pred_target = dut.io_out_s3_full_pred_3_jalr_target.value
        return provided == 0 and alt_provided == 0 and ftb_target == pred_target

    return src_from_ftb