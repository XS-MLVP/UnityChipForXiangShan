// control which privilege modes are available
// MSU means that it can disassemble all instructions
// M
// MU: user = true
// MSU: user = supervisor = true
#define DEFAULT_PRIV "MSU"

// XiangShan ISA
#define CONFIG_DIFF_RVH
#define CONFIG_DIFF_RVV
#define CONFIG_DIFF_ZICOND
#define CONFIG_DIFF_ZICNTR
#define CONFIG_DIFF_ZIHPM
// #define CONFIG_DIFF_SDTRIG

#ifdef CONFIG_DIFF_RVH
    #define RVH_ISA_STRING "H"
#else
    #define RVH_ISA_STRING ""
#endif
#ifdef CONFIG_DIFF_RVV
    #define RVV_ISA_STRING "V"
#else
    #define RVV_ISA_STRING ""
#endif
#ifdef CONFIG_DIFF_ZICOND
    #define ZICOND_ISA_STRING "_zicond"
#else
    #define ZICOND_ISA_STRING ""
#endif
#ifdef CONFIG_DIFF_ZICNTR
    #define ZICNTR_ISA_STRING "_zicntr"
#else
    #define ZICNTR_ISA_STRING ""
#endif
#ifdef CONFIG_DIFF_ZIHPM
    #define ZIHPM_ISA_STRING "_zihpm"
#else
    #define ZIHPM_ISA_STRING ""
#endif
#ifdef CONFIG_DIFF_SDTRIG
    #define SDTRIG_ISA_STRING "_sdtrig"
#else
    #define SDTRIG_ISA_STRING ""
#endif

// Ensure that the isa string is consistent with the isa string of xiangshan.
#define CONFIG_DIFF_ISA_STRING \
    "RV64IMAFDC" \
    RVV_ISA_STRING \
    RVH_ISA_STRING \
    ZICOND_ISA_STRING \
    ZICNTR_ISA_STRING \
    ZIHPM_ISA_STRING \
    SDTRIG_ISA_STRING \
    "_zba_zbb_zbc_zbs_zbkb_zbkc_zbkx" \
    "_zknd_zkne_zknh_zksed_zksh_zkt" \
    "_zfa_zfhmin" \
    "_svinval_sscofpmf" \
    "_zcb_zicbom_zicboz_zcmop_zimop" \
    "_zfh_zvfh"

#define DEFAULT_ISA "RV64IMAFDC_zba_zbb_zbc_zbs_zbkb_zbkc_zbkx_zknd_zkne_zknh_zksed_zksh_svinval_zicbom_zicboz"
