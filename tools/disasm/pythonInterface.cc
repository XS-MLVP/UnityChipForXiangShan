#include "config.h"
#include "isa_parser.h"
#include "disasm.h"
#include <string>
#include <cstring>

extern "C" {
    char* disasm(insn_bits_t insn, uint64_t opcode) {
        isa_parser_t isa_parser(CONFIG_DIFF_ISA_STRING, DEFAULT_PRIV);
        disassembler_t* disassembler = new disassembler_t(&isa_parser);

        std::string disasm_insn = disassembler->disassemble(insn);

        char* result = new char[disasm_insn.length() + 1];
        std::strcpy(result, disasm_insn.c_str());

        delete disassembler;
        return result;
    }

    // This function will only disassemble the specified opcode instructions,
    // the instructions of other opcodes will return "unknown".
    char* disasm_custom_insn(insn_bits_t insn, uint64_t opcode) {
        isa_parser_t isa_parser(CONFIG_DIFF_ISA_STRING, DEFAULT_PRIV);
        disassembler_t* disassembler = new disassembler_t(&isa_parser);

        std::string disasm_insn = disassembler->disassemble_custom_insn(insn, opcode);

        char* result = new char[disasm_insn.length() + 1];
        std::strcpy(result, disasm_insn.c_str());

        delete disassembler;
        return result;
    }

    void disasm_free_mem(char* ptr) {
        delete[] ptr;
    }
}
