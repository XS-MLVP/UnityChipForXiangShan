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

class _5Bundle(Bundle):
	_0 = _4Bundle.from_prefix("_0")
	_1 = _4Bundle.from_prefix("_1")

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
	_perf = _5Bundle.from_prefix("_perf")

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
	_offset, _REG, _REG_32, _REG_42, _REG_9, _REG_68, _REG_70, _REG_60, _REG_16, _REG_46, _REG_66, _REG_28, _REG_48, _REG_5, _REG_51, _REG_53, _REG_29, _REG_11, _REG_33, _REG_36, _REG_47, _REG_30, _REG_20, _REG_57, _REG_6, _REG_8, _REG_22, _REG_1, _REG_21, _REG_45, _REG_27, _REG_12, _REG_38, _REG_39, _REG_40, _REG_58, _REG_64, _REG_44, _REG_10, _REG_50, _REG_24, _REG_3, _REG_55, _REG_13, _REG_19, _REG_62, _REG_61, _REG_59, _REG_67, _REG_65, _REG_54, _REG_17, _REG_15, _REG_18, _REG_4, _REG_37, _REG_71, _REG_25, _REG_23, _REG_49, _REG_7, _REG_43, _REG_31, _REG_41, _REG_56, _REG_26, _REG_14, _REG_63, _REG_52, _REG_35, _REG_34, _REG_2, _REG_69 = Signals(73)

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
	_GEN, _GEN_367, _GEN_844, _GEN_256, _GEN_42, _GEN_159, _GEN_200, _GEN_338, _GEN_706, _GEN_267, _GEN_422, _GEN_498, _GEN_717, _GEN_442, _GEN_82, _GEN_309, _GEN_381, _GEN_21, _GEN_250, _GEN_238, _GEN_483, _GEN_261, _GEN_13, _GEN_153, _GEN_276, _GEN_0, _GEN_341, _GEN_631, _GEN_434, _GEN_640, _GEN_707, _GEN_500, _GEN_288, _GEN_286, _GEN_595, _GEN_813, _GEN_572, _GEN_297, _GEN_665, _GEN_473, _GEN_599, _GEN_607, _GEN_705, _GEN_117, _GEN_16, _GEN_716, _GEN_183, _GEN_549, _GEN_541, _GEN_220, _GEN_30, _GEN_562, _GEN_234, _GEN_216, _GEN_125, _GEN_574, _GEN_798, _GEN_738, _GEN_316, _GEN_361, _GEN_460, _GEN_808, _GEN_96, _GEN_201, _GEN_429, _GEN_260, _GEN_475, _GEN_485, _GEN_826, _GEN_50, _GEN_211, _GEN_98, _GEN_581, _GEN_406, _GEN_416, _GEN_639, _GEN_812, _GEN_198, _GEN_7, _GEN_305, _GEN_231, _GEN_565, _GEN_161, _GEN_298, _GEN_502, _GEN_693, _GEN_722, _GEN_496, _GEN_755, _GEN_206, _GEN_868, _GEN_376, _GEN_138, _GEN_815, _GEN_409, _GEN_154, _GEN_86, _GEN_76, _GEN_456, _GEN_249, _GEN_524, _GEN_526, _GEN_816, _GEN_53, _GEN_11, _GEN_643, _GEN_351, _GEN_47, _GEN_262, _GEN_552, _GEN_301, _GEN_108, _GEN_369, _GEN_465, _GEN_295, _GEN_583, _GEN_789, _GEN_6, _GEN_353, _GEN_178, _GEN_199, _GEN_843, _GEN_660, _GEN_525, _GEN_608, _GEN_725, _GEN_667, _GEN_384, _GEN_494, _GEN_145, _GEN_811, _GEN_772, _GEN_817, _GEN_150, _GEN_536, _GEN_482, _GEN_615, _GEN_385, _GEN_23, _GEN_679, _GEN_31, _GEN_834, _GEN_325, _GEN_842, _GEN_100, _GEN_203, _GEN_683, _GEN_266, _GEN_331, _GEN_336, _GEN_727, _GEN_230, _GEN_345, _GEN_335, _GEN_474, _GEN_558, _GEN_472, _GEN_857, _GEN_653, _GEN_654, _GEN_130, _GEN_106, _GEN_495, _GEN_476, _GEN_611, _GEN_452, _GEN_38, _GEN_129, _GEN_852, _GEN_766, _GEN_774, _GEN_831, _GEN_391, _GEN_62, _GEN_72, _GEN_497, _GEN_571, _GEN_642, _GEN_168, _GEN_580, _GEN_666, _GEN_827, _GEN_15, _GEN_866, _GEN_448, _GEN_804, _GEN_787, _GEN_833, _GEN_726, _GEN_375, _GEN_364, _GEN_214, _GEN_670, _GEN_271, _GEN_805, _GEN_2, _GEN_235, _GEN_758, _GEN_420, _GEN_264, _GEN_46, _GEN_723, _GEN_398, _GEN_48, _GEN_320, _GEN_463, _GEN_806, _GEN_365, _GEN_737, _GEN_428, _GEN_567, _GEN_407, _GEN_564, _GEN_695, _GEN_553, _GEN_659, _GEN_318, _GEN_729, _GEN_423, _GEN_91, _GEN_171, _GEN_648, _GEN_814, _GEN_835, _GEN_651, _GEN_823, _GEN_514, _GEN_592, _GEN_624, _GEN_636, _GEN_749, _GEN_582, _GEN_539, _GEN_718, _GEN_269, _GEN_566, _GEN_347, _GEN_186, _GEN_584, _GEN_240, _GEN_284, _GEN_511, _GEN_120, _GEN_34, _GEN_504, _GEN_523, _GEN_619, _GEN_169, _GEN_671, _GEN_681, _GEN_213, _GEN_32, _GEN_9, _GEN_535, _GEN_625, _GEN_151, _GEN_155, _GEN_346, _GEN_860, _GEN_537, _GEN_33, _GEN_140, _GEN_486, _GEN_770, _GEN_436, _GEN_568, _GEN_765, _GEN_75, _GEN_598, _GEN_867, _GEN_22, _GEN_546, _GEN_468, _GEN_440, _GEN_208, _GEN_258, _GEN_114, _GEN_254, _GEN_479, _GEN_652, _GEN_268, _GEN_396, _GEN_711, _GEN_454, _GEN_531, _GEN_629, _GEN_360, _GEN_326, _GEN_142, _GEN_224, _GEN_237, _GEN_321, _GEN_227, _GEN_753, _GEN_446, _GEN_103, _GEN_173, _GEN_748, _GEN_769, _GEN_35, _GEN_837, _GEN_109, _GEN_354, _GEN_505, _GEN_801, _GEN_742, _GEN_551, _GEN_674, _GEN_417, _GEN_97, _GEN_771, _GEN_492, _GEN_356, _GEN_478, _GEN_547, _GEN_632, _GEN_630, _GEN_134, _GEN_1, _GEN_800, _GEN_328, _GEN_735, _GEN_362, _GEN_90, _GEN_538, _GEN_322, _GEN_119, _GEN_355, _GEN_371, _GEN_174, _GEN_349, _GEN_373, _GEN_387, _GEN_471, _GEN_421, _GEN_754, _GEN_37, _GEN_516, _GEN_678, _GEN_207, _GEN_167, _GEN_709, _GEN_764, _GEN_26, _GEN_279, _GEN_87, _GEN_221, _GEN_357, _GEN_133, _GEN_435, _GEN_312, _GEN_242, _GEN_588, _GEN_107, _GEN_66, _GEN_28, _GEN_489, _GEN_760, _GEN_793, _GEN_638, _GEN_430, _GEN_177, _GEN_293, _GEN_714, _GEN_768, _GEN_104, _GEN_27, _GEN_803, _GEN_591, _GEN_180, _GEN_64, _GEN_282, _GEN_712, _GEN_836, _GEN_401, _GEN_432, _GEN_85, _GEN_243, _GEN_445, _GEN_74, _GEN_669, _GEN_782, _GEN_313, _GEN_163, _GEN_676, _GEN_289, _GEN_449, _GEN_112, _GEN_548, _GEN_715, _GEN_780, _GEN_785, _GEN_809, _GEN_193, _GEN_219, _GEN_241, _GEN_647, _GEN_99, _GEN_739, _GEN_419, _GEN_323, _GEN_194, _GEN_300, _GEN_856, _GEN_189, _GEN_869, _GEN_609, _GEN_84, _GEN_573, _GEN_263, _GEN_839, _GEN_324, _GEN_829, _GEN_135, _GEN_299, _GEN_650, _GEN_570, _GEN_229, _GEN_418, _GEN_439, _GEN_290, _GEN_777, _GEN_830, _GEN_366, _GEN_532, _GEN_527, _GEN_372, _GEN_115, _GEN_576, _GEN_855, _GEN_602, _GEN_377, _GEN_490, _GEN_575, _GEN_585, _GEN_605, _GEN_685, _GEN_656, _GEN_626, _GEN_233, _GEN_253, _GEN_661, _GEN_40, _GEN_700, _GEN_862, _GEN_77, _GEN_44, _GEN_359, _GEN_596, _GEN_672, _GEN_405, _GEN_95, _GEN_579, _GEN_319, _GEN_424, _GEN_710, _GEN_67, _GEN_851, _GEN_606, _GEN_668, _GEN_821, _GEN_152, _GEN_223, _GEN_673, _GEN_175, _GEN_141, _GEN_540, _GEN_181, _GEN_348, _GEN_635, _GEN_752, _GEN_158, _GEN_467, _GEN_861, _GEN_204, _GEN_41, _GEN_310, _GEN_736, _GEN_205, _GEN_663, _GEN_126, _GEN_277, _GEN_721, _GEN_157, _GEN_162, _GEN_404, _GEN_334, _GEN_796, _GEN_713, _GEN_529, _GEN_849, _GEN_848, _GEN_600, _GEN_691, _GEN_701, _GEN_469, _GEN_292, _GEN_455, _GEN_327, _GEN_374, _GEN_225, _GEN_658, _GEN_593, _GEN_386, _GEN_8, _GEN_259, _GEN_692, _GEN_307, _GEN_45, _GEN_342, _GEN_491, _GEN_594, _GEN_515, _GEN_339, _GEN_840, _GEN_251, _GEN_370, _GEN_55, _GEN_196, _GEN_179, _GEN_116, _GEN_127, _GEN_403, _GEN_232, _GEN_302, _GEN_732, _GEN_358, _GEN_308, _GEN_794, _GEN_399, _GEN_517, _GEN_797, _GEN_767, _GEN_191, _GEN_113, _GEN_781, _GEN_368, _GEN_520, _GEN_252, _GEN_703, _GEN_560, _GEN_89, _GEN_143, _GEN_425, _GEN_477, _GEN_392, _GEN_337, _GEN_128, _GEN_136, _GEN_618, _GEN_604, _GEN_751, _GEN_614, _GEN_776, _GEN_746, _GEN_39, _GEN_378, _GEN_554, _GEN_10, _GEN_792, _GEN_139, _GEN_144, _GEN_730, _GEN_195, _GEN_395, _GEN_775, _GEN_239, _GEN_841, _GEN_343, _GEN_784, _GEN_819, _GEN_637, _GEN_415, _GEN_688, _GEN_750, _GEN_555, _GEN_677, _GEN_687, _GEN_501, _GEN_278, _GEN_410, _GEN_131, _GEN_105, _GEN_118, _GEN_543, _GEN_528, _GEN_589, _GEN_92, _GEN_734, _GEN_182, _GEN_110, _GEN_859, _GEN_311, _GEN_212, _GEN_702, _GEN_443, _GEN_283, _GEN_29, _GEN_761, _GEN_704, _GEN_779, _GEN_79, _GEN_744, _GEN_414, _GEN_847, _GEN_363, _GEN_510, _GEN_786, _GEN_274, _GEN_431, _GEN_627, _GEN_78, _GEN_275, _GEN_380, _GEN_59, _GEN_534, _GEN_719, _GEN_394, _GEN_747, _GEN_296, _GEN_306, _GEN_88, _GEN_49, _GEN_197, _GEN_379, _GEN_763, _GEN_508, _GEN_649, _GEN_340, _GEN_294, _GEN_513, _GEN_389, _GEN_124, _GEN_121, _GEN_137, _GEN_559, _GEN_601, _GEN_699, _GEN_783, _GEN_344, _GEN_70, _GEN_60, _GEN_623, _GEN_697, _GEN_853, _GEN_530, _GEN_102, _GEN_148, _GEN_622, _GEN_314, _GEN_412, _GEN_603, _GEN_132, _GEN_393, _GEN_586, _GEN_458, _GEN_745, _GEN_484, _GEN_587, _GEN_438, _GEN_810, _GEN_466, _GEN_518, _GEN_694, _GEN_217, _GEN_807, _GEN_123, _GEN_65, _GEN_209, _GEN_550, _GEN_408, _GEN_176, _GEN_18, _GEN_824, _GEN_481, _GEN_563, _GEN_330, _GEN_662, _GEN_453, _GEN_644, _GEN_156, _GEN_822, _GEN_56, _GEN_122, _GEN_265, _GEN_413, _GEN_828, _GEN_215, _GEN_680, _GEN_686, _GEN_81, _GEN_696, _GEN_507, _GEN_825, _GEN_506, _GEN_226, _GEN_533, _GEN_778, _GEN_613, _GEN_578, _GEN_499, _GEN_457, _GEN_854, _GEN_863, _GEN_675, _GEN_20, _GEN_470, _GEN_444, _GEN_160, _GEN_450, _GEN_655, _GEN_12, _GEN_390, _GEN_315, _GEN_383, _GEN_58, _GEN_317, _GEN_3, _GEN_773, _GEN_795, _GEN_19, _GEN_94, _GEN_61, _GEN_720, _GEN_633, _GEN_248, _GEN_54, _GEN_17, _GEN_411, _GEN_597, _GEN_757, _GEN_244, _GEN_147, _GEN_257, _GEN_303, _GEN_4, _GEN_25, _GEN_333, _GEN_185, _GEN_641, _GEN_426, _GEN_43, _GEN_519, _GEN_790, _GEN_864, _GEN_612, _GEN_273, _GEN_63, _GEN_14, _GEN_689, _GEN_756, _GEN_682, _GEN_287, _GEN_488, _GEN_247, _GEN_441, _GEN_759, _GEN_577, _GEN_388, _GEN_818, _GEN_68, _GEN_664, _GEN_437, _GEN_512, _GEN_545, _GEN_350, _GEN_5, _GEN_791, _GEN_493, _GEN_850, _GEN_521, _GEN_111, _GEN_228, _GEN_799, _GEN_698, _GEN_164, _GEN_272, _GEN_245, _GEN_270, _GEN_146, _GEN_802, _GEN_464, _GEN_556, _GEN_708, _GEN_192, _GEN_427, _GEN_509, _GEN_400, _GEN_845, _GEN_352, _GEN_280, _GEN_590, _GEN_165, _GEN_71, _GEN_733, _GEN_634, _GEN_724, _GEN_255, _GEN_503, _GEN_101, _GEN_487, _GEN_617, _GEN_728, _GEN_788, _GEN_838, _GEN_865, _GEN_52, _GEN_628, _GEN_184, _GEN_83, _GEN_281, _GEN_610, _GEN_557, _GEN_646, _GEN_743, _GEN_820, _GEN_246, _GEN_402, _GEN_616, _GEN_291, _GEN_304, _GEN_51, _GEN_329, _GEN_645, _GEN_522, _GEN_731, _GEN_36, _GEN_832, _GEN_858, _GEN_561, _GEN_236, _GEN_462, _GEN_741, _GEN_188, _GEN_740, _GEN_57, _GEN_285, _GEN_332, _GEN_447, _GEN_480, _GEN_461, _GEN_166, _GEN_149, _GEN_210, _GEN_690, _GEN_762, _GEN_657, _GEN_218, _GEN_382, _GEN_24, _GEN_684, _GEN_451, _GEN_172, _GEN_544, _GEN_621, _GEN_459, _GEN_620, _GEN_190, _GEN_93, _GEN_846, _GEN_80, _GEN_222, _GEN_187, _GEN_433, _GEN_569, _GEN_397, _GEN_542, _GEN_170, _GEN_202, _GEN_69 = Signals(870)

class _29Bundle(Bundle):
	_value = Signal()

class _30Bundle(Bundle):
	_1 = _29Bundle.from_prefix("_1")
	_0 = _29Bundle.from_prefix("_0")

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
	_perf = _30Bundle.from_prefix("_perf")
	_release = _38Bundle.from_prefix("_release")
	_ldWbPtr = _14Bundle.from_prefix("_ldWbPtr")
	_query = _35Bundle.from_prefix("_query")
	_lqFull = Signal()

class LoadQueueRARBundle(Bundle):
	LoadQueueRAR_ = _28Bundle.from_prefix("LoadQueueRAR_")
	LoadQueueRAR = _17Bundle.from_prefix("LoadQueueRAR")
	io = _39Bundle.from_prefix("io")
	reset, clock = Signals(2)

