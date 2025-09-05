from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_32, _42, _9, _68, _70, _60, _16, _46, _66, _28, _48, _5, _51, _53, _29, _11, _33, _36, _47, _30, _20, _57, _6, _8, _22, _1, _21, _45, _27, _12, _38, _39, _40, _58, _64, _44, _10, _50, _24, _3, _55, _13, _19, _62, _61, _59, _67, _65, _54, _17, _15, _18, _4, _37, _71, _25, _23, _49, _7, _43, _31, _41, _56, _26, _14, _63, _52, _35, _34, _2, _69 = Signals(71)

class _1Bundle(Bundle):
	_2, _1, _0 = Signals(3)

class _2Bundle(Bundle):
	_32, _42, _9, _68, _70, _60, _16, _46, _66, _28, _48, _5, _51, _53, _29, _11, _33, _36, _47, _30, _20, _57, _6, _8, _22, _1, _21, _45, _27, _12, _38, _39, _40, _58, _64, _44, _10, _50, _24, _3, _55, _13, _19, _62, _61, _59, _67, _65, _54, _0, _17, _15, _18, _4, _37, _71, _25, _23, _49, _7, _43, _31, _41, _56, _26, _14, _63, _52, _35, _34, _2, _69 = Signals(72)

class _3Bundle(Bundle):
	_1 = Signal()

class _4Bundle(Bundle):
	_value_REG, _value_REG_1 = Signals(2)

class _6Bundle(Bundle):
	_0 = Signal()

class _7Bundle(Bundle):
	_req_ready = _6Bundle.from_prefix("_req_ready")
	_resp_valid_REG = Signal()

class _8Bundle(Bundle):
	_0 = _7Bundle.from_prefix("_0")
	_2 = _7Bundle.from_prefix("_2")
	_1 = _7Bundle.from_prefix("_1")

class _9Bundle(Bundle):
	_query = _8Bundle.from_prefix("_query")

class _10Bundle(Bundle):
	_r = Signal()

class _11Bundle(Bundle):
	_0 = _10Bundle.from_prefix("_0")
	_1 = _10Bundle.from_prefix("_1")
	_2 = _10Bundle.from_prefix("_2")

class _12Bundle(Bundle):
	_32, _42, _9, _68, _70, _60, _16, _46, _66, _28, _48, _5, _51, _53, _29, _11, _33, _36, _47, _30, _20, _57, _6, _8, _22, _45, _1, _21, _27, _12, _38, _39, _40, _58, _64, _44, _10, _50, _24, _3, _55, _13, _19, _62, _61, _59, _67, _65, _54, _0, _17, _15, _18, _4, _37, _71, _25, _23, _49, _7, _43, _31, _41, _56, _26, _14, _2, _52, _63, _35, _34, _69, _1_32, _1_42, _1_9, _1_68, _1_70, _1_60, _1_16, _1_46, _1_66, _1_28, _1_48, _1_5, _1_51, _1_53, _1_29, _1_11, _1_33, _1_36, _1_47, _1_30, _1_20, _1_57, _1_6, _1_8, _1_22, _1_1, _1_21, _1_45, _1_27, _1_12, _1_38, _1_39, _1_40, _1_58, _1_64, _1_44, _1_10, _1_50, _1_24, _1_3, _1_55, _1_13, _1_19, _1_62, _1_61, _1_59, _1_67, _1_65, _1_54, _1_0, _1_17, _1_15, _1_18, _1_4, _1_37, _1_71, _1_25, _1_23, _1_49, _1_7, _1_43, _1_31, _1_41, _1_56, _1_26, _1_14, _1_63, _1_52, _1_35, _1_34, _1_2, _1_69, _2_32, _2_42, _2_9, _2_68, _2_70, _2_60, _2_16, _2_46, _2_66, _2_28, _2_48, _2_5, _2_51, _2_53, _2_29, _2_11, _2_33, _2_36, _2_47, _2_30, _2_20, _2_57, _2_6, _2_8, _2_22, _2_1, _2_21, _2_45, _2_27, _2_12, _2_38, _2_39, _2_40, _2_58, _2_64, _2_44, _2_10, _2_50, _2_24, _2_3, _2_55, _2_13, _2_19, _2_62, _2_61, _2_59, _2_67, _2_65, _2_54, _2_0, _2_17, _2_15, _2_18, _2_4, _2_37, _2_71, _2_25, _2_23, _2_49, _2_7, _2_43, _2_31, _2_41, _2_56, _2_26, _2_14, _2_63, _2_52, _2_35, _2_34, _2_2, _2_69 = Signals(216)

class _13Bundle(Bundle):
	_valid_REG, _bits_paddr = Signals(2)

class _14Bundle(Bundle):
	_value, _flag = Signals(2)

class _15Bundle(Bundle):
	_robIdx = _14Bundle.from_prefix("_robIdx")
	_lqIdx = _14Bundle.from_prefix("_lqIdx")

class _16Bundle(Bundle):
	_59 = _15Bundle.from_prefix("_59")
	_49 = _15Bundle.from_prefix("_49")
	_58 = _15Bundle.from_prefix("_58")
	_20 = _15Bundle.from_prefix("_20")
	_22 = _15Bundle.from_prefix("_22")
	_65 = _15Bundle.from_prefix("_65")
	_0 = _15Bundle.from_prefix("_0")
	_29 = _15Bundle.from_prefix("_29")
	_51 = _15Bundle.from_prefix("_51")
	_31 = _15Bundle.from_prefix("_31")
	_48 = _15Bundle.from_prefix("_48")
	_32 = _15Bundle.from_prefix("_32")
	_34 = _15Bundle.from_prefix("_34")
	_35 = _15Bundle.from_prefix("_35")
	_7 = _15Bundle.from_prefix("_7")
	_6 = _15Bundle.from_prefix("_6")
	_67 = _15Bundle.from_prefix("_67")
	_45 = _15Bundle.from_prefix("_45")
	_9 = _15Bundle.from_prefix("_9")
	_27 = _15Bundle.from_prefix("_27")
	_28 = _15Bundle.from_prefix("_28")
	_13 = _15Bundle.from_prefix("_13")
	_23 = _15Bundle.from_prefix("_23")
	_3 = _15Bundle.from_prefix("_3")
	_33 = _15Bundle.from_prefix("_33")
	_12 = _15Bundle.from_prefix("_12")
	_19 = _15Bundle.from_prefix("_19")
	_40 = _15Bundle.from_prefix("_40")
	_61 = _15Bundle.from_prefix("_61")
	_43 = _15Bundle.from_prefix("_43")
	_30 = _15Bundle.from_prefix("_30")
	_21 = _15Bundle.from_prefix("_21")
	_24 = _15Bundle.from_prefix("_24")
	_66 = _15Bundle.from_prefix("_66")
	_26 = _15Bundle.from_prefix("_26")
	_39 = _15Bundle.from_prefix("_39")
	_25 = _15Bundle.from_prefix("_25")
	_37 = _15Bundle.from_prefix("_37")
	_18 = _15Bundle.from_prefix("_18")
	_4 = _15Bundle.from_prefix("_4")
	_57 = _15Bundle.from_prefix("_57")
	_63 = _15Bundle.from_prefix("_63")
	_41 = _15Bundle.from_prefix("_41")
	_8 = _15Bundle.from_prefix("_8")
	_71 = _15Bundle.from_prefix("_71")
	_10 = _15Bundle.from_prefix("_10")
	_17 = _15Bundle.from_prefix("_17")
	_47 = _15Bundle.from_prefix("_47")
	_70 = _15Bundle.from_prefix("_70")
	_11 = _15Bundle.from_prefix("_11")
	_44 = _15Bundle.from_prefix("_44")
	_38 = _15Bundle.from_prefix("_38")
	_54 = _15Bundle.from_prefix("_54")
	_50 = _15Bundle.from_prefix("_50")
	_62 = _15Bundle.from_prefix("_62")
	_15 = _15Bundle.from_prefix("_15")
	_46 = _15Bundle.from_prefix("_46")
	_60 = _15Bundle.from_prefix("_60")
	_5 = _15Bundle.from_prefix("_5")
	_53 = _15Bundle.from_prefix("_53")
	_68 = _15Bundle.from_prefix("_68")
	_14 = _15Bundle.from_prefix("_14")
	_42 = _15Bundle.from_prefix("_42")
	_56 = _15Bundle.from_prefix("_56")
	_36 = _15Bundle.from_prefix("_36")
	_55 = _15Bundle.from_prefix("_55")
	_69 = _15Bundle.from_prefix("_69")
	_1 = _15Bundle.from_prefix("_1")
	_16 = _15Bundle.from_prefix("_16")
	_2 = _15Bundle.from_prefix("_2")
	_52 = _15Bundle.from_prefix("_52")
	_64 = _15Bundle.from_prefix("_64")

class _17Bundle(Bundle):
	_matchMaskReg = _12Bundle.from_prefix("_matchMaskReg")
	_matchMask_r = _12Bundle.from_prefix("_matchMask_r")
	_acceptedVec = _1Bundle.from_prefix("_acceptedVec")
	_needEnqueue = _1Bundle.from_prefix("_needEnqueue")
	_io = _9Bundle.from_prefix("_io")
	_uop = _16Bundle.from_prefix("_uop")
	_lastCanAccept_next_nextVec = _11Bundle.from_prefix("_lastCanAccept_next_nextVec")
	_lastAllocIndex_next_nextVec = _11Bundle.from_prefix("_lastAllocIndex_next_nextVec")
	_allocated = _2Bundle.from_prefix("_allocated")
	_released = _2Bundle.from_prefix("_released")
	_release2Cycle = _13Bundle.from_prefix("_release2Cycle")
	_offset = Signals(1)

class _18Bundle(Bundle):
	_367, _844, _256, _42, _159, _200, _338, _706, _267, _422, _498, _717, _442, _82, _309, _381, _21, _250, _238, _483, _261, _13, _153, _276, _0, _341, _631, _434, _640, _707, _500, _288, _286, _595, _813, _572, _297, _665, _473, _599, _607, _705, _117, _16, _716, _183, _549, _541, _220, _30, _562, _234, _216, _125, _574, _798, _738, _316, _361, _460, _808, _96, _201, _429, _260, _475, _485, _826, _50, _211, _98, _581, _406, _416, _639, _812, _198, _7, _305, _231, _565, _161, _298, _502, _693, _722, _496, _755, _206, _868, _376, _138, _815, _409, _154, _86, _76, _456, _249, _524, _526, _816, _53, _11, _643, _351, _47, _262, _552, _301, _108, _369, _465, _295, _583, _789, _6, _353, _178, _199, _843, _660, _525, _608, _725, _667, _384, _494, _145, _811, _772, _817, _150, _536, _482, _615, _385, _23, _679, _31, _834, _325, _842, _100, _203, _683, _266, _331, _336, _727, _230, _345, _335, _474, _558, _472, _857, _653, _654, _130, _106, _495, _476, _611, _452, _38, _129, _852, _766, _774, _831, _391, _62, _72, _497, _571, _642, _168, _580, _666, _827, _15, _866, _448, _804, _787, _833, _726, _375, _364, _214, _670, _271, _805, _2, _235, _758, _420, _264, _46, _723, _398, _48, _320, _463, _806, _365, _737, _428, _567, _407, _564, _695, _553, _659, _318, _729, _423, _91, _171, _648, _814, _835, _651, _823, _514, _592, _624, _636, _749, _582, _539, _718, _269, _566, _347, _186, _584, _240, _284, _511, _120, _34, _504, _523, _619, _169, _671, _681, _213, _32, _9, _535, _625, _151, _155, _346, _860, _537, _33, _140, _486, _770, _436, _568, _765, _75, _598, _867, _22, _546, _468, _440, _208, _258, _114, _254, _479, _652, _268, _396, _711, _454, _531, _629, _360, _326, _142, _224, _237, _321, _227, _753, _446, _103, _173, _748, _769, _35, _837, _109, _354, _505, _801, _742, _551, _674, _417, _97, _771, _492, _356, _478, _547, _632, _630, _134, _1, _800, _328, _735, _362, _90, _538, _322, _119, _355, _371, _174, _349, _373, _387, _471, _421, _754, _37, _516, _678, _207, _167, _709, _764, _26, _279, _87, _221, _357, _133, _435, _312, _242, _588, _107, _66, _28, _489, _760, _793, _638, _430, _177, _293, _714, _768, _104, _27, _803, _591, _180, _64, _282, _712, _836, _401, _432, _85, _243, _445, _74, _669, _782, _313, _163, _676, _289, _449, _112, _548, _715, _780, _785, _809, _193, _219, _241, _647, _99, _739, _419, _323, _194, _300, _856, _189, _869, _609, _84, _573, _263, _839, _324, _829, _135, _299, _650, _570, _229, _418, _439, _290, _777, _830, _366, _532, _527, _372, _115, _576, _855, _602, _377, _490, _575, _585, _605, _685, _656, _626, _233, _253, _661, _40, _700, _862, _77, _44, _359, _596, _672, _405, _95, _579, _319, _424, _710, _67, _851, _606, _668, _821, _152, _223, _673, _175, _141, _540, _181, _348, _635, _752, _158, _467, _861, _204, _41, _310, _736, _205, _663, _126, _277, _721, _157, _162, _404, _334, _796, _713, _529, _849, _848, _600, _691, _701, _469, _292, _455, _327, _374, _225, _658, _593, _386, _8, _259, _692, _307, _45, _342, _491, _594, _515, _339, _840, _251, _370, _55, _196, _179, _116, _127, _403, _232, _302, _732, _358, _308, _794, _399, _517, _797, _767, _191, _113, _781, _368, _520, _252, _703, _560, _89, _143, _425, _477, _392, _337, _128, _136, _618, _604, _751, _614, _776, _746, _39, _378, _554, _10, _792, _139, _144, _730, _195, _395, _775, _239, _841, _343, _784, _819, _637, _415, _688, _750, _555, _677, _687, _501, _278, _410, _131, _105, _118, _543, _528, _589, _92, _734, _182, _110, _859, _311, _212, _702, _443, _283, _29, _761, _704, _779, _79, _744, _414, _847, _363, _510, _786, _274, _431, _627, _78, _275, _380, _59, _534, _719, _394, _747, _296, _306, _88, _49, _197, _379, _763, _508, _649, _340, _294, _513, _389, _124, _121, _137, _559, _601, _699, _783, _344, _70, _60, _623, _697, _853, _530, _102, _148, _622, _314, _412, _603, _132, _393, _586, _458, _745, _484, _587, _438, _810, _466, _518, _694, _217, _807, _123, _65, _209, _550, _408, _176, _18, _824, _481, _563, _330, _662, _453, _644, _156, _822, _56, _122, _265, _413, _828, _215, _680, _686, _81, _696, _507, _825, _506, _226, _533, _778, _613, _578, _499, _457, _854, _863, _675, _20, _470, _444, _160, _450, _655, _12, _390, _315, _383, _58, _317, _3, _773, _795, _19, _94, _61, _720, _633, _248, _54, _17, _411, _597, _757, _244, _147, _257, _303, _4, _25, _333, _185, _641, _426, _43, _519, _790, _864, _612, _273, _63, _14, _689, _756, _682, _287, _488, _247, _441, _759, _577, _388, _818, _68, _664, _437, _512, _545, _350, _5, _791, _493, _850, _521, _111, _228, _799, _698, _164, _272, _245, _270, _146, _802, _464, _556, _708, _192, _427, _509, _400, _845, _352, _280, _590, _165, _71, _733, _634, _724, _255, _503, _101, _487, _617, _728, _788, _838, _865, _52, _628, _184, _83, _281, _610, _557, _646, _743, _820, _246, _402, _616, _291, _304, _51, _329, _645, _522, _731, _36, _832, _858, _561, _236, _462, _741, _188, _740, _57, _285, _332, _447, _480, _461, _166, _149, _210, _690, _762, _657, _218, _382, _24, _684, _451, _172, _544, _621, _459, _620, _190, _93, _846, _80, _222, _187, _433, _569, _397, _542, _170, _202, _69 = Signals(869)

class _19Bundle(Bundle):
	_canAllocate = _1Bundle.from_prefix("_canAllocate")
	_allocateSlot = _1Bundle.from_prefix("_allocateSlot")

class _20Bundle(Bundle):
	_70 = Signal()

class _21Bundle(Bundle):
	_resp_bits_rep_frm_fetch_T = _20Bundle.from_prefix("_resp_bits_rep_frm_fetch_T")

class _22Bundle(Bundle):
	_2 = _21Bundle.from_prefix("_2")
	_0 = _21Bundle.from_prefix("_0")
	_1 = _21Bundle.from_prefix("_1")

class _23Bundle(Bundle):
	_286 = Signal()

class _24Bundle(Bundle):
	_2 = _2Bundle.from_prefix("_2")

class _25Bundle(Bundle):
	_0 = _2Bundle.from_prefix("_0")
	_1 = _2Bundle.from_prefix("_1")
	_2 = _2Bundle.from_prefix("_2")

class _26Bundle(Bundle):
	_releaseViolationMmask = _25Bundle.from_prefix("_releaseViolationMmask")
	_releaseMmask = _24Bundle.from_prefix("_releaseMmask")

class _27Bundle(Bundle):
	_10, _21, _32 = Signals(3)

class _28Bundle(Bundle):
	_needFlush_flushItself_T = _23Bundle.from_prefix("_needFlush_flushItself_T")
	_io_query = _22Bundle.from_prefix("_io_query")
	_paddrModule_io = _26Bundle.from_prefix("_paddrModule_io")
	_released_T = _27Bundle.from_prefix("_released_T")
	_freeList_io = _19Bundle.from_prefix("_freeList_io")

class _31Bundle(Bundle):
	_uop = _15Bundle.from_prefix("_uop")
	_paddr, _is_nc, _data_valid = Signals(3)

class _32Bundle(Bundle):
	_bits = _31Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _33Bundle(Bundle):
	_valid, _bits_rep_frm_fetch = Signals(2)

class _34Bundle(Bundle):
	_resp = _33Bundle.from_prefix("_resp")
	_req = _32Bundle.from_prefix("_req")
	_revoke = Signal()

class _35Bundle(Bundle):
	_1 = _34Bundle.from_prefix("_1")
	_0 = _34Bundle.from_prefix("_0")
	_2 = _34Bundle.from_prefix("_2")

class _36Bundle(Bundle):
	_robIdx = _14Bundle.from_prefix("_robIdx")
	_level = Signal()

class _37Bundle(Bundle):
	_bits = _36Bundle.from_prefix("_bits")
	_valid = Signal()

class _38Bundle(Bundle):
	_bits_paddr, _valid = Signals(2)

class _39Bundle(Bundle):
	_redirect = _37Bundle.from_prefix("_redirect")
	_release = _38Bundle.from_prefix("_release")
	_ldWbPtr = _14Bundle.from_prefix("_ldWbPtr")
	_query = _35Bundle.from_prefix("_query")
	_lqFull = Signal()

class LoadQueueRARBundle(Bundle):
	LoadQueueRAR_ = _28Bundle.from_prefix("LoadQueueRAR_")
	LoadQueueRAR = _17Bundle.from_prefix("LoadQueueRAR")
	io = _39Bundle.from_prefix("io")
	reset, clock = Signals(2)

