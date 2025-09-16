from toffee import Bundle
from toffee import Signals, Signal

class InnerBundle(Bundle):
	REG, REG_1, REG_10, REG_11, REG_12, REG_13, REG_14, REG_15, REG_16, REG_17, REG_18, REG_19, REG_2, REG_20, REG_21, \
	REG_22, REG_23, REG_24, REG_25, REG_26, REG_27, REG_28, REG_29, REG_3, REG_30, REG_31, REG_32, REG_33, REG_34, \
	REG_35, REG_36, REG_37, REG_38, REG_39, REG_4, REG_40, REG_41, REG_42, REG_43, REG_44, REG_45, REG_46, REG_47, \
	REG_48, REG_49, REG_5, REG_50, REG_51, REG_52, REG_53, REG_54, REG_55, REG_56, REG_57, REG_58, REG_59, REG_6, \
	REG_60, REG_61, REG_62, REG_63, REG_64, REG_65, REG_66, REG_67, REG_68, REG_69, REG_7, REG_70, REG_71, REG_8, \
	REG_9, _freeList_io_allocateSlot_0, _freeList_io_allocateSlot_1, _freeList_io_allocateSlot_2, _freeList_io_canAllocate_0, \
	_freeList_io_canAllocate_1, _freeList_io_canAllocate_2, _io_query_0_resp_bits_rep_frm_fetch_T_70, \
	_io_query_1_resp_bits_rep_frm_fetch_T_70, _io_query_2_resp_bits_rep_frm_fetch_T_70, _needFlush_flushItself_T_286, \
	_paddrModule_io_releaseMmask_2_0, _paddrModule_io_releaseMmask_2_1, _paddrModule_io_releaseMmask_2_10, \
	_paddrModule_io_releaseMmask_2_11, _paddrModule_io_releaseMmask_2_12, _paddrModule_io_releaseMmask_2_13, \
	_paddrModule_io_releaseMmask_2_14, _paddrModule_io_releaseMmask_2_15, _paddrModule_io_releaseMmask_2_16, \
	_paddrModule_io_releaseMmask_2_17, _paddrModule_io_releaseMmask_2_18, _paddrModule_io_releaseMmask_2_19, \
	_paddrModule_io_releaseMmask_2_2, _paddrModule_io_releaseMmask_2_20, _paddrModule_io_releaseMmask_2_21, \
	_paddrModule_io_releaseMmask_2_22, _paddrModule_io_releaseMmask_2_23, _paddrModule_io_releaseMmask_2_24, \
	_paddrModule_io_releaseMmask_2_25, _paddrModule_io_releaseMmask_2_26, _paddrModule_io_releaseMmask_2_27, \
	_paddrModule_io_releaseMmask_2_28, _paddrModule_io_releaseMmask_2_29, _paddrModule_io_releaseMmask_2_3, \
	_paddrModule_io_releaseMmask_2_30, _paddrModule_io_releaseMmask_2_31, _paddrModule_io_releaseMmask_2_32, \
	_paddrModule_io_releaseMmask_2_33, _paddrModule_io_releaseMmask_2_34, _paddrModule_io_releaseMmask_2_35, \
	_paddrModule_io_releaseMmask_2_36, _paddrModule_io_releaseMmask_2_37, _paddrModule_io_releaseMmask_2_38, \
	_paddrModule_io_releaseMmask_2_39, _paddrModule_io_releaseMmask_2_4, _paddrModule_io_releaseMmask_2_40, \
	_paddrModule_io_releaseMmask_2_41, _paddrModule_io_releaseMmask_2_42, _paddrModule_io_releaseMmask_2_43, \
	_paddrModule_io_releaseMmask_2_44, _paddrModule_io_releaseMmask_2_45, _paddrModule_io_releaseMmask_2_46, \
	_paddrModule_io_releaseMmask_2_47, _paddrModule_io_releaseMmask_2_48, _paddrModule_io_releaseMmask_2_49, \
	_paddrModule_io_releaseMmask_2_5, _paddrModule_io_releaseMmask_2_50, _paddrModule_io_releaseMmask_2_51, \
	_paddrModule_io_releaseMmask_2_52, _paddrModule_io_releaseMmask_2_53, _paddrModule_io_releaseMmask_2_54, \
	_paddrModule_io_releaseMmask_2_55, _paddrModule_io_releaseMmask_2_56, _paddrModule_io_releaseMmask_2_57, \
	_paddrModule_io_releaseMmask_2_58, _paddrModule_io_releaseMmask_2_59, _paddrModule_io_releaseMmask_2_6, \
	_paddrModule_io_releaseMmask_2_60, _paddrModule_io_releaseMmask_2_61, _paddrModule_io_releaseMmask_2_62, \
	_paddrModule_io_releaseMmask_2_63, _paddrModule_io_releaseMmask_2_64, _paddrModule_io_releaseMmask_2_65, \
	_paddrModule_io_releaseMmask_2_66, _paddrModule_io_releaseMmask_2_67, _paddrModule_io_releaseMmask_2_68, \
	_paddrModule_io_releaseMmask_2_69, _paddrModule_io_releaseMmask_2_7, _paddrModule_io_releaseMmask_2_70, \
	_paddrModule_io_releaseMmask_2_71, _paddrModule_io_releaseMmask_2_8, _paddrModule_io_releaseMmask_2_9, \
	_paddrModule_io_releaseViolationMmask_0_0, _paddrModule_io_releaseViolationMmask_0_1, \
	_paddrModule_io_releaseViolationMmask_0_10, _paddrModule_io_releaseViolationMmask_0_11, \
	_paddrModule_io_releaseViolationMmask_0_12, _paddrModule_io_releaseViolationMmask_0_13, \
	_paddrModule_io_releaseViolationMmask_0_14, _paddrModule_io_releaseViolationMmask_0_15, \
	_paddrModule_io_releaseViolationMmask_0_16, _paddrModule_io_releaseViolationMmask_0_17, \
	_paddrModule_io_releaseViolationMmask_0_18, _paddrModule_io_releaseViolationMmask_0_19, \
	_paddrModule_io_releaseViolationMmask_0_2, _paddrModule_io_releaseViolationMmask_0_20, \
	_paddrModule_io_releaseViolationMmask_0_21, _paddrModule_io_releaseViolationMmask_0_22, \
	_paddrModule_io_releaseViolationMmask_0_23, _paddrModule_io_releaseViolationMmask_0_24, \
	_paddrModule_io_releaseViolationMmask_0_25, _paddrModule_io_releaseViolationMmask_0_26, \
	_paddrModule_io_releaseViolationMmask_0_27, _paddrModule_io_releaseViolationMmask_0_28, \
	_paddrModule_io_releaseViolationMmask_0_29, _paddrModule_io_releaseViolationMmask_0_3, \
	_paddrModule_io_releaseViolationMmask_0_30, _paddrModule_io_releaseViolationMmask_0_31, \
	_paddrModule_io_releaseViolationMmask_0_32, _paddrModule_io_releaseViolationMmask_0_33, \
	_paddrModule_io_releaseViolationMmask_0_34, _paddrModule_io_releaseViolationMmask_0_35, \
	_paddrModule_io_releaseViolationMmask_0_36, _paddrModule_io_releaseViolationMmask_0_37, \
	_paddrModule_io_releaseViolationMmask_0_38, _paddrModule_io_releaseViolationMmask_0_39, \
	_paddrModule_io_releaseViolationMmask_0_4, _paddrModule_io_releaseViolationMmask_0_40, \
	_paddrModule_io_releaseViolationMmask_0_41, _paddrModule_io_releaseViolationMmask_0_42, \
	_paddrModule_io_releaseViolationMmask_0_43, _paddrModule_io_releaseViolationMmask_0_44, \
	_paddrModule_io_releaseViolationMmask_0_45, _paddrModule_io_releaseViolationMmask_0_46, \
	_paddrModule_io_releaseViolationMmask_0_47, _paddrModule_io_releaseViolationMmask_0_48, \
	_paddrModule_io_releaseViolationMmask_0_49, _paddrModule_io_releaseViolationMmask_0_5, \
	_paddrModule_io_releaseViolationMmask_0_50, _paddrModule_io_releaseViolationMmask_0_51, \
	_paddrModule_io_releaseViolationMmask_0_52, _paddrModule_io_releaseViolationMmask_0_53, \
	_paddrModule_io_releaseViolationMmask_0_54, _paddrModule_io_releaseViolationMmask_0_55, \
	_paddrModule_io_releaseViolationMmask_0_56, _paddrModule_io_releaseViolationMmask_0_57, \
	_paddrModule_io_releaseViolationMmask_0_58, _paddrModule_io_releaseViolationMmask_0_59, \
	_paddrModule_io_releaseViolationMmask_0_6, _paddrModule_io_releaseViolationMmask_0_60, \
	_paddrModule_io_releaseViolationMmask_0_61, _paddrModule_io_releaseViolationMmask_0_62, \
	_paddrModule_io_releaseViolationMmask_0_63, _paddrModule_io_releaseViolationMmask_0_64, \
	_paddrModule_io_releaseViolationMmask_0_65, _paddrModule_io_releaseViolationMmask_0_66, \
	_paddrModule_io_releaseViolationMmask_0_67, _paddrModule_io_releaseViolationMmask_0_68, \
	_paddrModule_io_releaseViolationMmask_0_69, _paddrModule_io_releaseViolationMmask_0_7, \
	_paddrModule_io_releaseViolationMmask_0_70, _paddrModule_io_releaseViolationMmask_0_71, \
	_paddrModule_io_releaseViolationMmask_0_8, _paddrModule_io_releaseViolationMmask_0_9, \
	_paddrModule_io_releaseViolationMmask_1_0, _paddrModule_io_releaseViolationMmask_1_1, \
	_paddrModule_io_releaseViolationMmask_1_10, _paddrModule_io_releaseViolationMmask_1_11, \
	_paddrModule_io_releaseViolationMmask_1_12, _paddrModule_io_releaseViolationMmask_1_13, \
	_paddrModule_io_releaseViolationMmask_1_14, _paddrModule_io_releaseViolationMmask_1_15, \
	_paddrModule_io_releaseViolationMmask_1_16, _paddrModule_io_releaseViolationMmask_1_17, \
	_paddrModule_io_releaseViolationMmask_1_18, _paddrModule_io_releaseViolationMmask_1_19, \
	_paddrModule_io_releaseViolationMmask_1_2, _paddrModule_io_releaseViolationMmask_1_20, \
	_paddrModule_io_releaseViolationMmask_1_21, _paddrModule_io_releaseViolationMmask_1_22, \
	_paddrModule_io_releaseViolationMmask_1_23, _paddrModule_io_releaseViolationMmask_1_24, \
	_paddrModule_io_releaseViolationMmask_1_25, _paddrModule_io_releaseViolationMmask_1_26, \
	_paddrModule_io_releaseViolationMmask_1_27, _paddrModule_io_releaseViolationMmask_1_28, \
	_paddrModule_io_releaseViolationMmask_1_29, _paddrModule_io_releaseViolationMmask_1_3, \
	_paddrModule_io_releaseViolationMmask_1_30, _paddrModule_io_releaseViolationMmask_1_31, \
	_paddrModule_io_releaseViolationMmask_1_32, _paddrModule_io_releaseViolationMmask_1_33, \
	_paddrModule_io_releaseViolationMmask_1_34, _paddrModule_io_releaseViolationMmask_1_35, \
	_paddrModule_io_releaseViolationMmask_1_36, _paddrModule_io_releaseViolationMmask_1_37, \
	_paddrModule_io_releaseViolationMmask_1_38, _paddrModule_io_releaseViolationMmask_1_39, \
	_paddrModule_io_releaseViolationMmask_1_4, _paddrModule_io_releaseViolationMmask_1_40, \
	_paddrModule_io_releaseViolationMmask_1_41, _paddrModule_io_releaseViolationMmask_1_42, \
	_paddrModule_io_releaseViolationMmask_1_43, _paddrModule_io_releaseViolationMmask_1_44, \
	_paddrModule_io_releaseViolationMmask_1_45, _paddrModule_io_releaseViolationMmask_1_46, \
	_paddrModule_io_releaseViolationMmask_1_47, _paddrModule_io_releaseViolationMmask_1_48, \
	_paddrModule_io_releaseViolationMmask_1_49, _paddrModule_io_releaseViolationMmask_1_5, \
	_paddrModule_io_releaseViolationMmask_1_50, _paddrModule_io_releaseViolationMmask_1_51, \
	_paddrModule_io_releaseViolationMmask_1_52, _paddrModule_io_releaseViolationMmask_1_53, \
	_paddrModule_io_releaseViolationMmask_1_54, _paddrModule_io_releaseViolationMmask_1_55, \
	_paddrModule_io_releaseViolationMmask_1_56, _paddrModule_io_releaseViolationMmask_1_57, \
	_paddrModule_io_releaseViolationMmask_1_58, _paddrModule_io_releaseViolationMmask_1_59, \
	_paddrModule_io_releaseViolationMmask_1_6, _paddrModule_io_releaseViolationMmask_1_60, \
	_paddrModule_io_releaseViolationMmask_1_61, _paddrModule_io_releaseViolationMmask_1_62, \
	_paddrModule_io_releaseViolationMmask_1_63, _paddrModule_io_releaseViolationMmask_1_64, \
	_paddrModule_io_releaseViolationMmask_1_65, _paddrModule_io_releaseViolationMmask_1_66, \
	_paddrModule_io_releaseViolationMmask_1_67, _paddrModule_io_releaseViolationMmask_1_68, \
	_paddrModule_io_releaseViolationMmask_1_69, _paddrModule_io_releaseViolationMmask_1_7, \
	_paddrModule_io_releaseViolationMmask_1_70, _paddrModule_io_releaseViolationMmask_1_71, \
	_paddrModule_io_releaseViolationMmask_1_8, _paddrModule_io_releaseViolationMmask_1_9, \
	_paddrModule_io_releaseViolationMmask_2_0, _paddrModule_io_releaseViolationMmask_2_1, \
	_paddrModule_io_releaseViolationMmask_2_10, _paddrModule_io_releaseViolationMmask_2_11, \
	_paddrModule_io_releaseViolationMmask_2_12, _paddrModule_io_releaseViolationMmask_2_13, \
	_paddrModule_io_releaseViolationMmask_2_14, _paddrModule_io_releaseViolationMmask_2_15, \
	_paddrModule_io_releaseViolationMmask_2_16, _paddrModule_io_releaseViolationMmask_2_17, \
	_paddrModule_io_releaseViolationMmask_2_18, _paddrModule_io_releaseViolationMmask_2_19, \
	_paddrModule_io_releaseViolationMmask_2_2, _paddrModule_io_releaseViolationMmask_2_20, \
	_paddrModule_io_releaseViolationMmask_2_21, _paddrModule_io_releaseViolationMmask_2_22, \
	_paddrModule_io_releaseViolationMmask_2_23, _paddrModule_io_releaseViolationMmask_2_24, \
	_paddrModule_io_releaseViolationMmask_2_25, _paddrModule_io_releaseViolationMmask_2_26, \
	_paddrModule_io_releaseViolationMmask_2_27, _paddrModule_io_releaseViolationMmask_2_28, \
	_paddrModule_io_releaseViolationMmask_2_29, _paddrModule_io_releaseViolationMmask_2_3, \
	_paddrModule_io_releaseViolationMmask_2_30, _paddrModule_io_releaseViolationMmask_2_31, \
	_paddrModule_io_releaseViolationMmask_2_32, _paddrModule_io_releaseViolationMmask_2_33, \
	_paddrModule_io_releaseViolationMmask_2_34, _paddrModule_io_releaseViolationMmask_2_35, \
	_paddrModule_io_releaseViolationMmask_2_36, _paddrModule_io_releaseViolationMmask_2_37, \
	_paddrModule_io_releaseViolationMmask_2_38, _paddrModule_io_releaseViolationMmask_2_39, \
	_paddrModule_io_releaseViolationMmask_2_4, _paddrModule_io_releaseViolationMmask_2_40, \
	_paddrModule_io_releaseViolationMmask_2_41, _paddrModule_io_releaseViolationMmask_2_42, \
	_paddrModule_io_releaseViolationMmask_2_43, _paddrModule_io_releaseViolationMmask_2_44, \
	_paddrModule_io_releaseViolationMmask_2_45, _paddrModule_io_releaseViolationMmask_2_46, \
	_paddrModule_io_releaseViolationMmask_2_47, _paddrModule_io_releaseViolationMmask_2_48, \
	_paddrModule_io_releaseViolationMmask_2_49, _paddrModule_io_releaseViolationMmask_2_5, \
	_paddrModule_io_releaseViolationMmask_2_50, _paddrModule_io_releaseViolationMmask_2_51, \
	_paddrModule_io_releaseViolationMmask_2_52, _paddrModule_io_releaseViolationMmask_2_53, \
	_paddrModule_io_releaseViolationMmask_2_54, _paddrModule_io_releaseViolationMmask_2_55, \
	_paddrModule_io_releaseViolationMmask_2_56, _paddrModule_io_releaseViolationMmask_2_57, \
	_paddrModule_io_releaseViolationMmask_2_58, _paddrModule_io_releaseViolationMmask_2_59, \
	_paddrModule_io_releaseViolationMmask_2_6, _paddrModule_io_releaseViolationMmask_2_60, \
	_paddrModule_io_releaseViolationMmask_2_61, _paddrModule_io_releaseViolationMmask_2_62, \
	_paddrModule_io_releaseViolationMmask_2_63, _paddrModule_io_releaseViolationMmask_2_64, \
	_paddrModule_io_releaseViolationMmask_2_65, _paddrModule_io_releaseViolationMmask_2_66, \
	_paddrModule_io_releaseViolationMmask_2_67, _paddrModule_io_releaseViolationMmask_2_68, \
	_paddrModule_io_releaseViolationMmask_2_69, _paddrModule_io_releaseViolationMmask_2_7, \
	_paddrModule_io_releaseViolationMmask_2_70, _paddrModule_io_releaseViolationMmask_2_71, \
	_paddrModule_io_releaseViolationMmask_2_8, _paddrModule_io_releaseViolationMmask_2_9, _released_T_19, \
	_released_T_29, _released_T_9, _vecLdCanceltmp_0_1_T_2, _vecLdCanceltmp_10_1_T_2, _vecLdCanceltmp_11_1_T_2, \
	_vecLdCanceltmp_12_1_T_2, _vecLdCanceltmp_13_1_T_2, _vecLdCanceltmp_14_1_T_2, _vecLdCanceltmp_15_1_T_2, \
	_vecLdCanceltmp_16_1_T_2, _vecLdCanceltmp_17_1_T_2, _vecLdCanceltmp_18_1_T_2, _vecLdCanceltmp_19_1_T_2, \
	_vecLdCanceltmp_1_1_T_2, _vecLdCanceltmp_20_1_T_2, _vecLdCanceltmp_21_1_T_2, _vecLdCanceltmp_22_1_T_2, \
	_vecLdCanceltmp_23_1_T_2, _vecLdCanceltmp_24_1_T_2, _vecLdCanceltmp_25_1_T_2, _vecLdCanceltmp_26_1_T_2, \
	_vecLdCanceltmp_27_1_T_2, _vecLdCanceltmp_28_1_T_2, _vecLdCanceltmp_29_1_T_2, _vecLdCanceltmp_2_1_T_2, \
	_vecLdCanceltmp_30_1_T_2, _vecLdCanceltmp_31_1_T_2, _vecLdCanceltmp_32_1_T_2, _vecLdCanceltmp_33_1_T_2, \
	_vecLdCanceltmp_34_1_T_2, _vecLdCanceltmp_35_1_T_2, _vecLdCanceltmp_36_1_T_2, _vecLdCanceltmp_37_1_T_2, \
	_vecLdCanceltmp_38_1_T_2, _vecLdCanceltmp_39_1_T_2, _vecLdCanceltmp_3_1_T_2, _vecLdCanceltmp_40_1_T_2, \
	_vecLdCanceltmp_41_1_T_2, _vecLdCanceltmp_42_1_T_2, _vecLdCanceltmp_43_1_T_2, _vecLdCanceltmp_44_1_T_2, \
	_vecLdCanceltmp_45_1_T_2, _vecLdCanceltmp_46_1_T_2, _vecLdCanceltmp_47_1_T_2, _vecLdCanceltmp_48_1_T_2, \
	_vecLdCanceltmp_49_1_T_2, _vecLdCanceltmp_4_1_T_2, _vecLdCanceltmp_50_1_T_2, _vecLdCanceltmp_51_1_T_2, \
	_vecLdCanceltmp_52_1_T_2, _vecLdCanceltmp_53_1_T_2, _vecLdCanceltmp_54_1_T_2, _vecLdCanceltmp_55_1_T_2, \
	_vecLdCanceltmp_56_1_T_2, _vecLdCanceltmp_57_1_T_2, _vecLdCanceltmp_58_1_T_2, _vecLdCanceltmp_59_1_T_2, \
	_vecLdCanceltmp_5_1_T_2, _vecLdCanceltmp_60_1_T_2, _vecLdCanceltmp_61_1_T_2, _vecLdCanceltmp_62_1_T_2, \
	_vecLdCanceltmp_63_1_T_2, _vecLdCanceltmp_64_1_T_2, _vecLdCanceltmp_65_1_T_2, _vecLdCanceltmp_66_1_T_2, \
	_vecLdCanceltmp_67_1_T_2, _vecLdCanceltmp_68_1_T_2, _vecLdCanceltmp_69_1_T_2, _vecLdCanceltmp_6_1_T_2, \
	_vecLdCanceltmp_70_1_T_2, _vecLdCanceltmp_71_0_T_3, _vecLdCanceltmp_71_1_T_2, _vecLdCanceltmp_71_1_T_3, \
	_vecLdCanceltmp_7_1_T_2, _vecLdCanceltmp_8_1_T_2, _vecLdCanceltmp_9_1_T_2, acceptedVec_0, acceptedVec_1, \
	acceptedVec_2, allocated_0, allocated_1, allocated_10, allocated_11, allocated_12, allocated_13, allocated_14, \
	allocated_15, allocated_16, allocated_17, allocated_18, allocated_19, allocated_2, allocated_20, allocated_21, \
	allocated_22, allocated_23, allocated_24, allocated_25, allocated_26, allocated_27, allocated_28, allocated_29, \
	allocated_3, allocated_30, allocated_31, allocated_32, allocated_33, allocated_34, allocated_35, allocated_36, \
	allocated_37, allocated_38, allocated_39, allocated_4, allocated_40, allocated_41, allocated_42, allocated_43, \
	allocated_44, allocated_45, allocated_46, allocated_47, allocated_48, allocated_49, allocated_5, allocated_50, \
	allocated_51, allocated_52, allocated_53, allocated_54, allocated_55, allocated_56, allocated_57, allocated_58, \
	allocated_59, allocated_6, allocated_60, allocated_61, allocated_62, allocated_63, allocated_64, allocated_65, \
	allocated_66, allocated_67, allocated_68, allocated_69, allocated_7, allocated_70, allocated_71, allocated_8, \
	allocated_9, bypassPAddr_0, bypassPAddr_1, bypassPAddr_2, io_query_0_req_ready_0, io_query_0_resp_valid_REG, \
	io_query_1_req_ready_0, io_query_1_resp_valid_REG, io_query_2_req_ready_0, io_query_2_resp_valid_REG, \
	lastAllocIndex_next_nextVec_0_r, lastAllocIndex_next_nextVec_1_r, lastAllocIndex_next_nextVec_2_r, \
	lastCanAccept_next_nextVec_0_r, lastCanAccept_next_nextVec_1_r, lastCanAccept_next_nextVec_2_r, \
	lastReleasePAddrMatch_0, lastReleasePAddrMatch_1, lastReleasePAddrMatch_2, matchMaskReg_0, matchMaskReg_1, \
	matchMaskReg_10, matchMaskReg_11, matchMaskReg_12, matchMaskReg_13, matchMaskReg_14, matchMaskReg_15, \
	matchMaskReg_16, matchMaskReg_17, matchMaskReg_18, matchMaskReg_19, matchMaskReg_1_0, matchMaskReg_1_1, \
	matchMaskReg_1_10, matchMaskReg_1_11, matchMaskReg_1_12, matchMaskReg_1_13, matchMaskReg_1_14, matchMaskReg_1_15, \
	matchMaskReg_1_16, matchMaskReg_1_17, matchMaskReg_1_18, matchMaskReg_1_19, matchMaskReg_1_2, matchMaskReg_1_20, \
	matchMaskReg_1_21, matchMaskReg_1_22, matchMaskReg_1_23, matchMaskReg_1_24, matchMaskReg_1_25, matchMaskReg_1_26, \
	matchMaskReg_1_27, matchMaskReg_1_28, matchMaskReg_1_29, matchMaskReg_1_3, matchMaskReg_1_30, matchMaskReg_1_31, \
	matchMaskReg_1_32, matchMaskReg_1_33, matchMaskReg_1_34, matchMaskReg_1_35, matchMaskReg_1_36, matchMaskReg_1_37, \
	matchMaskReg_1_38, matchMaskReg_1_39, matchMaskReg_1_4, matchMaskReg_1_40, matchMaskReg_1_41, matchMaskReg_1_42, \
	matchMaskReg_1_43, matchMaskReg_1_44, matchMaskReg_1_45, matchMaskReg_1_46, matchMaskReg_1_47, matchMaskReg_1_48, \
	matchMaskReg_1_49, matchMaskReg_1_5, matchMaskReg_1_50, matchMaskReg_1_51, matchMaskReg_1_52, matchMaskReg_1_53, \
	matchMaskReg_1_54, matchMaskReg_1_55, matchMaskReg_1_56, matchMaskReg_1_57, matchMaskReg_1_58, matchMaskReg_1_59, \
	matchMaskReg_1_6, matchMaskReg_1_60, matchMaskReg_1_61, matchMaskReg_1_62, matchMaskReg_1_63, matchMaskReg_1_64, \
	matchMaskReg_1_65, matchMaskReg_1_66, matchMaskReg_1_67, matchMaskReg_1_68, matchMaskReg_1_69, matchMaskReg_1_7, \
	matchMaskReg_1_70, matchMaskReg_1_71, matchMaskReg_1_8, matchMaskReg_1_9, matchMaskReg_2, matchMaskReg_20, \
	matchMaskReg_21, matchMaskReg_22, matchMaskReg_23, matchMaskReg_24, matchMaskReg_25, matchMaskReg_26, \
	matchMaskReg_27, matchMaskReg_28, matchMaskReg_29, matchMaskReg_2_0, matchMaskReg_2_1, matchMaskReg_2_10, \
	matchMaskReg_2_11, matchMaskReg_2_12, matchMaskReg_2_13, matchMaskReg_2_14, matchMaskReg_2_15, matchMaskReg_2_16, \
	matchMaskReg_2_17, matchMaskReg_2_18, matchMaskReg_2_19, matchMaskReg_2_2, matchMaskReg_2_20, matchMaskReg_2_21, \
	matchMaskReg_2_22, matchMaskReg_2_23, matchMaskReg_2_24, matchMaskReg_2_25, matchMaskReg_2_26, matchMaskReg_2_27, \
	matchMaskReg_2_28, matchMaskReg_2_29, matchMaskReg_2_3, matchMaskReg_2_30, matchMaskReg_2_31, matchMaskReg_2_32, \
	matchMaskReg_2_33, matchMaskReg_2_34, matchMaskReg_2_35, matchMaskReg_2_36, matchMaskReg_2_37, matchMaskReg_2_38, \
	matchMaskReg_2_39, matchMaskReg_2_4, matchMaskReg_2_40, matchMaskReg_2_41, matchMaskReg_2_42, matchMaskReg_2_43, \
	matchMaskReg_2_44, matchMaskReg_2_45, matchMaskReg_2_46, matchMaskReg_2_47, matchMaskReg_2_48, matchMaskReg_2_49, \
	matchMaskReg_2_5, matchMaskReg_2_50, matchMaskReg_2_51, matchMaskReg_2_52, matchMaskReg_2_53, matchMaskReg_2_54, \
	matchMaskReg_2_55, matchMaskReg_2_56, matchMaskReg_2_57, matchMaskReg_2_58, matchMaskReg_2_59, matchMaskReg_2_6, \
	matchMaskReg_2_60, matchMaskReg_2_61, matchMaskReg_2_62, matchMaskReg_2_63, matchMaskReg_2_64, matchMaskReg_2_65, \
	matchMaskReg_2_66, matchMaskReg_2_67, matchMaskReg_2_68, matchMaskReg_2_69, matchMaskReg_2_7, matchMaskReg_2_70, \
	matchMaskReg_2_71, matchMaskReg_2_8, matchMaskReg_2_9, matchMaskReg_3, matchMaskReg_30, matchMaskReg_31, \
	matchMaskReg_32, matchMaskReg_33, matchMaskReg_34, matchMaskReg_35, matchMaskReg_36, matchMaskReg_37, \
	matchMaskReg_38, matchMaskReg_39, matchMaskReg_4, matchMaskReg_40, matchMaskReg_41, matchMaskReg_42, \
	matchMaskReg_43, matchMaskReg_44, matchMaskReg_45, matchMaskReg_46, matchMaskReg_47, matchMaskReg_48, \
	matchMaskReg_49, matchMaskReg_5, matchMaskReg_50, matchMaskReg_51, matchMaskReg_52, matchMaskReg_53, \
	matchMaskReg_54, matchMaskReg_55, matchMaskReg_56, matchMaskReg_57, matchMaskReg_58, matchMaskReg_59, \
	matchMaskReg_6, matchMaskReg_60, matchMaskReg_61, matchMaskReg_62, matchMaskReg_63, matchMaskReg_64, \
	matchMaskReg_65, matchMaskReg_66, matchMaskReg_67, matchMaskReg_68, matchMaskReg_69, matchMaskReg_7, \
	matchMaskReg_70, matchMaskReg_71, matchMaskReg_8, matchMaskReg_9, matchMask_r_0, matchMask_r_1, matchMask_r_10, \
	matchMask_r_11, matchMask_r_12, matchMask_r_13, matchMask_r_14, matchMask_r_15, matchMask_r_16, matchMask_r_17, \
	matchMask_r_18, matchMask_r_19, matchMask_r_1_0, matchMask_r_1_1, matchMask_r_1_10, matchMask_r_1_11, \
	matchMask_r_1_12, matchMask_r_1_13, matchMask_r_1_14, matchMask_r_1_15, matchMask_r_1_16, matchMask_r_1_17, \
	matchMask_r_1_18, matchMask_r_1_19, matchMask_r_1_2, matchMask_r_1_20, matchMask_r_1_21, matchMask_r_1_22, \
	matchMask_r_1_23, matchMask_r_1_24, matchMask_r_1_25, matchMask_r_1_26, matchMask_r_1_27, matchMask_r_1_28, \
	matchMask_r_1_29, matchMask_r_1_3, matchMask_r_1_30, matchMask_r_1_31, matchMask_r_1_32, matchMask_r_1_33, \
	matchMask_r_1_34, matchMask_r_1_35, matchMask_r_1_36, matchMask_r_1_37, matchMask_r_1_38, matchMask_r_1_39, \
	matchMask_r_1_4, matchMask_r_1_40, matchMask_r_1_41, matchMask_r_1_42, matchMask_r_1_43, matchMask_r_1_44, \
	matchMask_r_1_45, matchMask_r_1_46, matchMask_r_1_47, matchMask_r_1_48, matchMask_r_1_49, matchMask_r_1_5, \
	matchMask_r_1_50, matchMask_r_1_51, matchMask_r_1_52, matchMask_r_1_53, matchMask_r_1_54, matchMask_r_1_55, \
	matchMask_r_1_56, matchMask_r_1_57, matchMask_r_1_58, matchMask_r_1_59, matchMask_r_1_6, matchMask_r_1_60, \
	matchMask_r_1_61, matchMask_r_1_62, matchMask_r_1_63, matchMask_r_1_64, matchMask_r_1_65, matchMask_r_1_66, \
	matchMask_r_1_67, matchMask_r_1_68, matchMask_r_1_69, matchMask_r_1_7, matchMask_r_1_70, matchMask_r_1_71, \
	matchMask_r_1_8, matchMask_r_1_9, matchMask_r_2, matchMask_r_20, matchMask_r_21, matchMask_r_22, matchMask_r_23, \
	matchMask_r_24, matchMask_r_25, matchMask_r_26, matchMask_r_27, matchMask_r_28, matchMask_r_29, matchMask_r_2_0, \
	matchMask_r_2_1, matchMask_r_2_10, matchMask_r_2_11, matchMask_r_2_12, matchMask_r_2_13, matchMask_r_2_14, \
	matchMask_r_2_15, matchMask_r_2_16, matchMask_r_2_17, matchMask_r_2_18, matchMask_r_2_19, matchMask_r_2_2, \
	matchMask_r_2_20, matchMask_r_2_21, matchMask_r_2_22, matchMask_r_2_23, matchMask_r_2_24, matchMask_r_2_25, \
	matchMask_r_2_26, matchMask_r_2_27, matchMask_r_2_28, matchMask_r_2_29, matchMask_r_2_3, matchMask_r_2_30, \
	matchMask_r_2_31, matchMask_r_2_32, matchMask_r_2_33, matchMask_r_2_34, matchMask_r_2_35, matchMask_r_2_36, \
	matchMask_r_2_37, matchMask_r_2_38, matchMask_r_2_39, matchMask_r_2_4, matchMask_r_2_40, matchMask_r_2_41, \
	matchMask_r_2_42, matchMask_r_2_43, matchMask_r_2_44, matchMask_r_2_45, matchMask_r_2_46, matchMask_r_2_47, \
	matchMask_r_2_48, matchMask_r_2_49, matchMask_r_2_5, matchMask_r_2_50, matchMask_r_2_51, matchMask_r_2_52, \
	matchMask_r_2_53, matchMask_r_2_54, matchMask_r_2_55, matchMask_r_2_56, matchMask_r_2_57, matchMask_r_2_58, \
	matchMask_r_2_59, matchMask_r_2_6, matchMask_r_2_60, matchMask_r_2_61, matchMask_r_2_62, matchMask_r_2_63, \
	matchMask_r_2_64, matchMask_r_2_65, matchMask_r_2_66, matchMask_r_2_67, matchMask_r_2_68, matchMask_r_2_69, \
	matchMask_r_2_7, matchMask_r_2_70, matchMask_r_2_71, matchMask_r_2_8, matchMask_r_2_9, matchMask_r_3, \
	matchMask_r_30, matchMask_r_31, matchMask_r_32, matchMask_r_33, matchMask_r_34, matchMask_r_35, matchMask_r_36, \
	matchMask_r_37, matchMask_r_38, matchMask_r_39, matchMask_r_4, matchMask_r_40, matchMask_r_41, matchMask_r_42, \
	matchMask_r_43, matchMask_r_44, matchMask_r_45, matchMask_r_46, matchMask_r_47, matchMask_r_48, matchMask_r_49, \
	matchMask_r_5, matchMask_r_50, matchMask_r_51, matchMask_r_52, matchMask_r_53, matchMask_r_54, matchMask_r_55, \
	matchMask_r_56, matchMask_r_57, matchMask_r_58, matchMask_r_59, matchMask_r_6, matchMask_r_60, matchMask_r_61, \
	matchMask_r_62, matchMask_r_63, matchMask_r_64, matchMask_r_65, matchMask_r_66, matchMask_r_67, matchMask_r_68, \
	matchMask_r_69, matchMask_r_7, matchMask_r_70, matchMask_r_71, matchMask_r_8, matchMask_r_9, needEnqueue_0, \
	needEnqueue_1, needEnqueue_2, offset, release2Cycle_bits_paddr, release2Cycle_valid, release2Cycle_valid_REG, \
	released_0, released_1, released_10, released_11, released_12, released_13, released_14, released_15, released_16, \
	released_17, released_18, released_19, released_2, released_20, released_21, released_22, released_23, \
	released_24, released_25, released_26, released_27, released_28, released_29, released_3, released_30, \
	released_31, released_32, released_33, released_34, released_35, released_36, released_37, released_38, \
	released_39, released_4, released_40, released_41, released_42, released_43, released_44, released_45, \
	released_46, released_47, released_48, released_49, released_5, released_50, released_51, released_52, \
	released_53, released_54, released_55, released_56, released_57, released_58, released_59, released_6, \
	released_60, released_61, released_62, released_63, released_64, released_65, released_66, released_67, \
	released_68, released_69, released_7, released_70, released_71, released_8, released_9, uop_0_lqIdx_flag, \
	uop_0_lqIdx_value, uop_0_robIdx_flag, uop_0_robIdx_value, uop_0_uopIdx, uop_10_lqIdx_flag, uop_10_lqIdx_value, \
	uop_10_robIdx_flag, uop_10_robIdx_value, uop_10_uopIdx, uop_11_lqIdx_flag, uop_11_lqIdx_value, uop_11_robIdx_flag, \
	uop_11_robIdx_value, uop_11_uopIdx, uop_12_lqIdx_flag, uop_12_lqIdx_value, uop_12_robIdx_flag, \
	uop_12_robIdx_value, uop_12_uopIdx, uop_13_lqIdx_flag, uop_13_lqIdx_value, uop_13_robIdx_flag, \
	uop_13_robIdx_value, uop_13_uopIdx, uop_14_lqIdx_flag, uop_14_lqIdx_value, uop_14_robIdx_flag, \
	uop_14_robIdx_value, uop_14_uopIdx, uop_15_lqIdx_flag, uop_15_lqIdx_value, uop_15_robIdx_flag, \
	uop_15_robIdx_value, uop_15_uopIdx, uop_16_lqIdx_flag, uop_16_lqIdx_value, uop_16_robIdx_flag, \
	uop_16_robIdx_value, uop_16_uopIdx, uop_17_lqIdx_flag, uop_17_lqIdx_value, uop_17_robIdx_flag, \
	uop_17_robIdx_value, uop_17_uopIdx, uop_18_lqIdx_flag, uop_18_lqIdx_value, uop_18_robIdx_flag, \
	uop_18_robIdx_value, uop_18_uopIdx, uop_19_lqIdx_flag, uop_19_lqIdx_value, uop_19_robIdx_flag, \
	uop_19_robIdx_value, uop_19_uopIdx, uop_1_lqIdx_flag, uop_1_lqIdx_value, uop_1_robIdx_flag, uop_1_robIdx_value, \
	uop_1_uopIdx, uop_20_lqIdx_flag, uop_20_lqIdx_value, uop_20_robIdx_flag, uop_20_robIdx_value, uop_20_uopIdx, \
	uop_21_lqIdx_flag, uop_21_lqIdx_value, uop_21_robIdx_flag, uop_21_robIdx_value, uop_21_uopIdx, uop_22_lqIdx_flag, \
	uop_22_lqIdx_value, uop_22_robIdx_flag, uop_22_robIdx_value, uop_22_uopIdx, uop_23_lqIdx_flag, uop_23_lqIdx_value, \
	uop_23_robIdx_flag, uop_23_robIdx_value, uop_23_uopIdx, uop_24_lqIdx_flag, uop_24_lqIdx_value, uop_24_robIdx_flag, \
	uop_24_robIdx_value, uop_24_uopIdx, uop_25_lqIdx_flag, uop_25_lqIdx_value, uop_25_robIdx_flag, \
	uop_25_robIdx_value, uop_25_uopIdx, uop_26_lqIdx_flag, uop_26_lqIdx_value, uop_26_robIdx_flag, \
	uop_26_robIdx_value, uop_26_uopIdx, uop_27_lqIdx_flag, uop_27_lqIdx_value, uop_27_robIdx_flag, \
	uop_27_robIdx_value, uop_27_uopIdx, uop_28_lqIdx_flag, uop_28_lqIdx_value, uop_28_robIdx_flag, \
	uop_28_robIdx_value, uop_28_uopIdx, uop_29_lqIdx_flag, uop_29_lqIdx_value, uop_29_robIdx_flag, \
	uop_29_robIdx_value, uop_29_uopIdx, uop_2_lqIdx_flag, uop_2_lqIdx_value, uop_2_robIdx_flag, uop_2_robIdx_value, \
	uop_2_uopIdx, uop_30_lqIdx_flag, uop_30_lqIdx_value, uop_30_robIdx_flag, uop_30_robIdx_value, uop_30_uopIdx, \
	uop_31_lqIdx_flag, uop_31_lqIdx_value, uop_31_robIdx_flag, uop_31_robIdx_value, uop_31_uopIdx, uop_32_lqIdx_flag, \
	uop_32_lqIdx_value, uop_32_robIdx_flag, uop_32_robIdx_value, uop_32_uopIdx, uop_33_lqIdx_flag, uop_33_lqIdx_value, \
	uop_33_robIdx_flag, uop_33_robIdx_value, uop_33_uopIdx, uop_34_lqIdx_flag, uop_34_lqIdx_value, uop_34_robIdx_flag, \
	uop_34_robIdx_value, uop_34_uopIdx, uop_35_lqIdx_flag, uop_35_lqIdx_value, uop_35_robIdx_flag, \
	uop_35_robIdx_value, uop_35_uopIdx, uop_36_lqIdx_flag, uop_36_lqIdx_value, uop_36_robIdx_flag, \
	uop_36_robIdx_value, uop_36_uopIdx, uop_37_lqIdx_flag, uop_37_lqIdx_value, uop_37_robIdx_flag, \
	uop_37_robIdx_value, uop_37_uopIdx, uop_38_lqIdx_flag, uop_38_lqIdx_value, uop_38_robIdx_flag, \
	uop_38_robIdx_value, uop_38_uopIdx, uop_39_lqIdx_flag, uop_39_lqIdx_value, uop_39_robIdx_flag, \
	uop_39_robIdx_value, uop_39_uopIdx, uop_3_lqIdx_flag, uop_3_lqIdx_value, uop_3_robIdx_flag, uop_3_robIdx_value, \
	uop_3_uopIdx, uop_40_lqIdx_flag, uop_40_lqIdx_value, uop_40_robIdx_flag, uop_40_robIdx_value, uop_40_uopIdx, \
	uop_41_lqIdx_flag, uop_41_lqIdx_value, uop_41_robIdx_flag, uop_41_robIdx_value, uop_41_uopIdx, uop_42_lqIdx_flag, \
	uop_42_lqIdx_value, uop_42_robIdx_flag, uop_42_robIdx_value, uop_42_uopIdx, uop_43_lqIdx_flag, uop_43_lqIdx_value, \
	uop_43_robIdx_flag, uop_43_robIdx_value, uop_43_uopIdx, uop_44_lqIdx_flag, uop_44_lqIdx_value, uop_44_robIdx_flag, \
	uop_44_robIdx_value, uop_44_uopIdx, uop_45_lqIdx_flag, uop_45_lqIdx_value, uop_45_robIdx_flag, \
	uop_45_robIdx_value, uop_45_uopIdx, uop_46_lqIdx_flag, uop_46_lqIdx_value, uop_46_robIdx_flag, \
	uop_46_robIdx_value, uop_46_uopIdx, uop_47_lqIdx_flag, uop_47_lqIdx_value, uop_47_robIdx_flag, \
	uop_47_robIdx_value, uop_47_uopIdx, uop_48_lqIdx_flag, uop_48_lqIdx_value, uop_48_robIdx_flag, \
	uop_48_robIdx_value, uop_48_uopIdx, uop_49_lqIdx_flag, uop_49_lqIdx_value, uop_49_robIdx_flag, \
	uop_49_robIdx_value, uop_49_uopIdx, uop_4_lqIdx_flag, uop_4_lqIdx_value, uop_4_robIdx_flag, uop_4_robIdx_value, \
	uop_4_uopIdx, uop_50_lqIdx_flag, uop_50_lqIdx_value, uop_50_robIdx_flag, uop_50_robIdx_value, uop_50_uopIdx, \
	uop_51_lqIdx_flag, uop_51_lqIdx_value, uop_51_robIdx_flag, uop_51_robIdx_value, uop_51_uopIdx, uop_52_lqIdx_flag, \
	uop_52_lqIdx_value, uop_52_robIdx_flag, uop_52_robIdx_value, uop_52_uopIdx, uop_53_lqIdx_flag, uop_53_lqIdx_value, \
	uop_53_robIdx_flag, uop_53_robIdx_value, uop_53_uopIdx, uop_54_lqIdx_flag, uop_54_lqIdx_value, uop_54_robIdx_flag, \
	uop_54_robIdx_value, uop_54_uopIdx, uop_55_lqIdx_flag, uop_55_lqIdx_value, uop_55_robIdx_flag, \
	uop_55_robIdx_value, uop_55_uopIdx, uop_56_lqIdx_flag, uop_56_lqIdx_value, uop_56_robIdx_flag, \
	uop_56_robIdx_value, uop_56_uopIdx, uop_57_lqIdx_flag, uop_57_lqIdx_value, uop_57_robIdx_flag, \
	uop_57_robIdx_value, uop_57_uopIdx, uop_58_lqIdx_flag, uop_58_lqIdx_value, uop_58_robIdx_flag, \
	uop_58_robIdx_value, uop_58_uopIdx, uop_59_lqIdx_flag, uop_59_lqIdx_value, uop_59_robIdx_flag, \
	uop_59_robIdx_value, uop_59_uopIdx, uop_5_lqIdx_flag, uop_5_lqIdx_value, uop_5_robIdx_flag, uop_5_robIdx_value, \
	uop_5_uopIdx, uop_60_lqIdx_flag, uop_60_lqIdx_value, uop_60_robIdx_flag, uop_60_robIdx_value, uop_60_uopIdx, \
	uop_61_lqIdx_flag, uop_61_lqIdx_value, uop_61_robIdx_flag, uop_61_robIdx_value, uop_61_uopIdx, uop_62_lqIdx_flag, \
	uop_62_lqIdx_value, uop_62_robIdx_flag, uop_62_robIdx_value, uop_62_uopIdx, uop_63_lqIdx_flag, uop_63_lqIdx_value, \
	uop_63_robIdx_flag, uop_63_robIdx_value, uop_63_uopIdx, uop_64_lqIdx_flag, uop_64_lqIdx_value, uop_64_robIdx_flag, \
	uop_64_robIdx_value, uop_64_uopIdx, uop_65_lqIdx_flag, uop_65_lqIdx_value, uop_65_robIdx_flag, \
	uop_65_robIdx_value, uop_65_uopIdx, uop_66_lqIdx_flag, uop_66_lqIdx_value, uop_66_robIdx_flag, \
	uop_66_robIdx_value, uop_66_uopIdx, uop_67_lqIdx_flag, uop_67_lqIdx_value, uop_67_robIdx_flag, \
	uop_67_robIdx_value, uop_67_uopIdx, uop_68_lqIdx_flag, uop_68_lqIdx_value, uop_68_robIdx_flag, \
	uop_68_robIdx_value, uop_68_uopIdx, uop_69_lqIdx_flag, uop_69_lqIdx_value, uop_69_robIdx_flag, \
	uop_69_robIdx_value, uop_69_uopIdx, uop_6_lqIdx_flag, uop_6_lqIdx_value, uop_6_robIdx_flag, uop_6_robIdx_value, \
	uop_6_uopIdx, uop_70_lqIdx_flag, uop_70_lqIdx_value, uop_70_robIdx_flag, uop_70_robIdx_value, uop_70_uopIdx, \
	uop_71_lqIdx_flag, uop_71_lqIdx_value, uop_71_robIdx_flag, uop_71_robIdx_value, uop_71_uopIdx, uop_7_lqIdx_flag, \
	uop_7_lqIdx_value, uop_7_robIdx_flag, uop_7_robIdx_value, uop_7_uopIdx, uop_8_lqIdx_flag, uop_8_lqIdx_value, \
	uop_8_robIdx_flag, uop_8_robIdx_value, uop_8_uopIdx, uop_9_lqIdx_flag, uop_9_lqIdx_value, uop_9_robIdx_flag, \
	uop_9_robIdx_value, uop_9_uopIdx = Signals(1411)

bundle = InnerBundle.from_prefix("LoadQueueRAR_")

