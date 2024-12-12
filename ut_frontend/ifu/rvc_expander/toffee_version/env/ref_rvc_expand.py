def ref_rvc_expander(opcode, fsIsOff):
    op_str = bin(opcode)[2:].zfill(32)
    lowest2 = opcode[-2:]
    if lowest2 == "11":
        return opcode, True
    
    func = op_str[-16:-13]
    stack_p = "00010"
    x0 = "00000"
    illegal = False
    rs2p = "01" + op_str[-5:-2]
    rs1p = "01" + op_str[-10:-7]
    rd = op_str[-12:-7]
    rs2 = op_str[-7:-2]

    addi_imm = op_str[-13] * 7 + op_str[-7:-2]
    ld_imm = "0000" + op_str[-7:-5] + op_str[-13:-10]+ "000"
    lw_imm = "00000" + op_str[-6] + op_str[-13:-10]+ op_str[-7] + "00"
    j_imm = 10 * op_str[-13] + op_str[-9] + op_str[-11:-9] + op_str[-7] + op_str[-8] + op_str[-3] + op_str[-12] + op_str[-6:-3] + '0'
    b_imm = 5 * op_str[-13] + op_str[-7:-5] + op_str[-12:-10] + op_str[-3] + op_str[-5:-3] + '0'

    if lowest2 == "00": #C0
        if func == "000": # addi4spn
            imm = op_str[-11:-7] + op_str[-13:-11] + op_str[-6] + op_str[-7] + "00"
            if int(imm, 2) == 0:
                illegal = True
            return int(imm + stack_p + "000"+ rs2p + "0010011", 2), illegal
        
        if func == "001": # fld
            imm = ld_imm
            
            return int(imm + rs1p + "011" + rs2p +"0000111", 2), fsIsOff
        
        if func == "010": #LW
            imm = lw_imm

            return int(imm + rs1p + "010" + rs2p + "0000011", 2), illegal
        
        if func == "011": # ld in kunminghu
            imm = ld_imm
            if fsIsOff:
                illegal = True
            return int(imm + rs1p + "011" + rs2p + "0000011", 2), illegal
        if func == "100":
            zcb_code = op_str[-12:-10]
            b_imm = "0000000000" + op_str[-6] + op_str[-7]
            h_imm = "0000000000" + op_str[-6] + 0
            zcb_l = "0000011"
            zcb_s = "0100011"
            if zcb_code[-13] == '1':
                illegal = True
            if zcb_code == "00": # lbu for "000"
                instr_zcb = b_imm + rs1p + "100" + rs2p + zcb_l

            elif zcb_code == "01": # lhu and lh for "001"
                if op_str[-7] == '0': # lhu
                    funct_lh = "101"
                else:
                    funct_lh = "001"
                # TODO: not yet finished, still some zcb extension instrs to be add
                instr_zcb = h_imm + rs1p + funct_lh + rs2p + zcb_l
            
            elif zcb_code == "10": # sb
                instr_zcb = b_imm[0:7] + rs2p + rs1p + "000" + b_imm[7:] + zcb_s    

            else: # 11
                if opcode[-7] == '1':
                    illegal = True
                instr_zcb = h_imm[0:7] + rs2p + rs1p + "001" + h_imm[7:] + zcb_s    
            return int(instr_zcb, 2), illegal
        
        if func == "101": #fsd
            imm = ld_imm
            return int(imm[0:7] + rs2p + rs1p + "011" + imm[7:] + "0100111", 2), fsIsOff

        if func == "110": #sw
            imm = lw_imm
            return int(imm[0:7] + rs2p + rs1p + "010" + imm[7:] + "0100011", 2), illegal

        if func == "111": #sd
            imm = ld_imm
            return int(imm[0:7] + rs2p + rs1p + "011" + imm[7:] + "0100011", 2), illegal
        
    elif lowest2 == "01": #C1
        if func == "000": # addi
            imm = addi_imm
            return int(imm + rd + "000" + rd + "0010011", 2), illegal
        
        if func == "001": # addiw   
            imm = addi_imm
            funct = "0011011"
            if int(rd, 2) == 0:
                illegal = True
                funct = "0011111"
            
            return int(imm + rd + "000" + rd + funct, 2), illegal
        
        if func == "010": #LI
            imm = addi_imm

            return int(imm + x0 + "000" + rd + "0000011", 2), illegal
        
        if func == "011": # lui/addi16sp/zcm
            if int(rd, 2) == 2: # addi16sp
                imm = op_str[-13] + op_str[-5:-3] + op_str[-6] + op_str[-3] + op_str[-7] 
                if int(imm, 2) == 0:
                    illegal = True
                instr = '0' * 6 + imm + stack_p + "000" + stack_p + "0010011"
            else:
                if int(op_str[-13:-11], 2)==0 and op_str[-8] == '1' and int(op_str[-7:-2], 2) == 0: #zcmop
                    instr = '0' * 17 + '1' * 3 + '0' * 5 + '0010011' 
                else: #lui
                    imm = 15 * op_str[-13] + op_str[-7:-2]
                    if int(imm, 2) == 0:
                        illegal = True
                    instr = imm + rd + "0110111"

            return int(instr, 2), illegal

        if func == "100": # arith  
            higher = op_str[-12:-10]
            if higher == "00": # SRLI
                imm = op_str[-13] + op_str[-7:-2]
                instr = '0' * 6 + imm + rs1p + "101" + rs1p + "0010011"
            elif higher == "01": # SRAI
                imm = op_str[-13] + op_str[-7:-2]
                instr = "010000" + imm + rs1p + "101" + rs1p + "0010011"
            elif higher == "10": #ANDI
                imm = '0' * 6 + op_str[-13] + op_str[-7:-2]
                instr = imm + rs1p + "111" + rs1p + "0010011"
            else: # SUB,XOR,OR,AND,SUBW, ADDW, ZCB extensions
                lower = op_str[-7:-5]
                if op_str[-13] == '0': #SUB,XOR,OR,AND
                    if lower == '00': #SUB
                        instr = "0100000" + rs2p + rs1p + "000" + rs1p + "0110011"
                    elif lower == '01': # XOR
                        instr = "0000000" + rs2p + rs1p + "100" + rs1p + "0110011"
                    elif lower == '10': # OR
                        instr = "0000000" + rs2p + rs1p + "110" + rs1p + "0110011"
                    else: # AND
                        instr = "0000000" + rs2p + rs1p + "111" + rs1p + "0110011"
                else: # SUBW, ADDW, ZCB extensions
                    if lower == '00': #SUBW
                        instr = "0100000" + rs2p + rs1p + "000" + rs1p + "0111011"
                    elif lower == '01': #ADDW
                        instr = "0000000" + rs2p + rs1p + "000" + rs1p + "0111011"
                    elif lower == "10": #MUL
                        instr = "0000001" + rs2p + rs1p + "000" + "rd" + "0110011"
                    else: #zcbs, 11
                        funct3 = op_str[-5:-2]
                        if funct3 == "000": # c.zext.b
                            instr = '0' * 4 + '1' * 8 + rs1p + "111" + rs1p + "0010011"
                        elif funct3 == "001": # c.sext.b
                            instr = "011000000100" + rs1p + "001" + rs1p + "0010011" 
                            
                    
            return instr, illegal
        
        if func == "101": #J
            imm = j_imm[-21] + j_imm[-11:-1] + j_imm[-12] + j_imm[-19:-12]

            return int(imm + x0 + "1101111", 2), illegal

        if func == "101": #BEQZ
            imm = j_imm[-21] + j_imm[-11:-1] + j_imm[-12] + j_imm[-19:-12]

            return int(imm[-13] + imm[-11:-5] + x0 + rs1p + "000" + imm[-5:-1] + imm[-12] + "1100011", 2), illegal

        if func == "101": #BNEZ
            imm = j_imm[-21] + j_imm[-11:-1] + j_imm[-12] + j_imm[-19:-12]

            return int(imm[-13] + imm[-11:-5] + x0 + rs1p + "001" + imm[-5:-1] + imm[-12] + "1100011", 2), illegal
    
    elif op_str == "10": # C2 code
        if func == "000": # slli
            shamt = op_str[-13] + op_str[-7:-2]

            return int('0' * 6 + shamt + rd + "001" + rd + "0010011", 2), illegal
        
        if func == "001": # fldsp
            imm = '0' * 3 + op_str[-5:-2] + op_str[-13] + op_str[-7:-5] + "000"

            return int(imm + stack_p + "011" + rd + "0000111", 2), illegal
        
        if func == "010" : # lwsp
            imm = '0' * 4 + op_str[-4:-2] + op_str[-13] + op_str[-7:-4] + "00"
            if int(rd, 2) == 0:
                illegal = False
            return int(imm + stack_p + "010" + rd + "0000011", 2), fsIsOff
        
        if func == "011" : # ldsp
            imm = '0' * 3 + op_str[-5:-2] + op_str[-13] + op_str[-7:-5] + "000"
            if int(rd, 2) == 0:
                illegal = False
            return int(imm + stack_p + "011" + rd + "0000011", 2), illegal         
        
        if func == "100" : # jr/mv/ebreak/jalr/add
            if op_str[-13] == '0': # JR, MV
                if int(rs2, 2) == 0: # JR
                    if int(rd, 2) == 0:
                        illegal = False
                    instr = '0' * 12 + rd + "000" + x0 + "1100111"
                
                else: #MV
                    # mv will be expanded as addi
                    instr = '0' * 12 + rs2 + "000" + rd + "0010011"
            else: #EBREAK, JALR, ADD
                if int(rs2, 2):

                    if int(rd, 2) == 0: # EBREAK
                        instr = '0' * 11 + '1' + '0' * 13 + "1110011"
                    
                    else: # JALR
                        instr = '0' * 12 + rd + "000" + "00001" + "1100111"
                else: # ADD
                    instr = '0' * 7 + rs2 + rd + "000" + rd + "0110011"
        
        if func == "101": # fsdsp
            imm = "000" + op_str[-10:-7] + op_str[-13:-10] + "000"
            return int(imm[0:7] + rs2 + stack_p + "011" + imm[7:] + "0100111"), fsIsOff
        
        if func == "110": #swsp
            imm = "0000" + imm[-9:-7] + imm[-13:-9] + "00"
            return int(imm[0:7] + rs2 + stack_p + "010" + imm[7:] + "0100011"), illegal
        
        if func == "111": #sdsp
            imm = "000" + op_str[-10:-7] + op_str[-13:-10] + "000"
            return int(imm[0:7] + rs2 + stack_p + "011" + imm[7:] + "0100011"), illegal
            
