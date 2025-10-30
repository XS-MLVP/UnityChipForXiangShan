def rvc_expand_ref(rvc_instr,fsIsOff):
    ill = 0
    expanded = 0
    rvc_instr_16bit = rvc_instr & 0xFFFF
    opcode = rvc_instr_16bit & 0b11
    if opcode == 0b00:
        # C.ADDI4SPN指令
        if (rvc_instr_16bit & 0xE003) == 0x0000:
            nzuimm = (((rvc_instr_16bit >> 5) & 0x3C) << 4) | (((rvc_instr_16bit >> 5) & 0x1) << 3) | (((rvc_instr_16bit >> 5) & 0x2) << 1) |  (((rvc_instr_16bit >> 5) & 0xC0) >> 2)
            rd = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            expanded = 0x00000013 | (nzuimm << 20) | (rd << 7) |(2<<15) # ADDI
            if nzuimm == 0:
                ill = 1
            else :
                ill = 0
            return expanded,ill  #"C.ADDI4SPN -> ADDI"
        # C.FLD
        elif (rvc_instr_16bit & 0xE003) == 0x2000:
            rd  = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            nzuimm = (((rvc_instr_16bit >> 5) & 0x3) << 6) | (((rvc_instr_16bit >> 5) & 0xE0) >>2) 
            expanded = 0x00000007 | (nzuimm << 20) | (rd << 7) |(0b011 <<12) |(rs1 << 15) # ADDI
            if(fsIsOff==True):
                ill=1
            else:
                ill=0
            return expanded,ill
        #C.lw  lw的格式形如： | imm[11:0] | rs1 | 010 | rd | 0000011 |
        elif (rvc_instr_16bit & 0xE003) == 0x4000:
            rd  = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            nzuimm = (((rvc_instr_16bit >> 5) & 0x1) << 6) | (((rvc_instr_16bit >> 5) & 0xE0) >>2)| (((rvc_instr_16bit >> 5) & 0x2) << 1) 
            expanded = 0x00000003 | (nzuimm << 20) | (rd << 7) |(0b010 <<12) |(rs1 << 15) # ADDI
            return expanded,ill
        #C.ld 
        elif (rvc_instr_16bit & 0xE003) == 0x6000:
            rd2  = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            nzuimm = (((rvc_instr_16bit >> 5) & 0x3) << 6) | (((rvc_instr_16bit >> 5) & 0xE0) >>2)
            expanded = 0x00000003 | (nzuimm << 20) | (rd2 << 7) |(0b011 <<12) |(rs1 << 15) # ADDI
            return expanded,ill
        #c.lbu/lhu/lh/sb/sh
        elif (rvc_instr_16bit & 0xE003) == 0x8000:
            rs2  = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            fun6 = (rvc_instr_16bit>>10)&0x3F
            if(fun6==0b100000):#lbu
                nzuimm = ((rvc_instr_16bit >> 4) & 0x2) | ((rvc_instr_16bit >> 6) & 0x1)
                expanded = 0x00000003 | (rs2 << 7) | (0b100 <<12) | (rs1 << 15) |(nzuimm << 20)  #
                return expanded,ill
            elif(fun6==0b100001)&(((rvc_instr_16bit >> 6) & 0x1)==0):#lhu
                nzuimm = ((rvc_instr_16bit >> 4) & 0x2)
                expanded = 0x00000003 | (rs2 << 7) | (0b101 <<12) | (rs1 << 15) |(nzuimm << 20)  # 
                return expanded,ill
            elif(fun6==0b100001)&(((rvc_instr_16bit >> 6) & 0x1)==1):#lh
                nzuimm = ((rvc_instr_16bit >> 4) & 0x2)
                expanded = 0x00000003 | (rs2 << 7) | (0b001 <<12) | (rs1 << 15) |(nzuimm << 20)  # 
                return expanded,ill
            elif(fun6==0b100010):#sb
                nzuimm = ((rvc_instr_16bit >> 4) & 0x2) | ((rvc_instr_16bit >> 6) & 0x1)
                expanded = 0x00000023 | ((nzuimm & 0x1F) << 7) | (rs2 << 20) |(0b000 <<12) |(rs1 << 15) |((nzuimm & 0xFE0) << 20)# 
                return expanded,ill
            elif((fun6==0b100011)&(((rvc_instr_16bit >> 6) & 0x1)==0)):#sh
                nzuimm = ((rvc_instr_16bit >> 4) & 0x2)
                expanded = 0x00000023 | ((nzuimm & 0x1F) << 7) | (rs2 << 20) |(0b001 <<12) |(rs1 << 15) |((nzuimm & 0xFE0) << 20)# 
                return expanded,ill
            else:
                ill=2
                return expanded,ill
        #C.fsd 
        elif (rvc_instr_16bit & 0xE003) == 0xa000:
            rs2 = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            nzuimm = (((rvc_instr_16bit >> 5) & 0x3) << 6) | (((rvc_instr_16bit >> 5) & 0xE0) >>2) 
            expanded = 0x00000027 | ((nzuimm & 0x1F) << 7) | (rs2 << 20) |(0b011 <<12) |(rs1 << 15) |((nzuimm & 0xFE0) << 20)# 
            if(fsIsOff==True):
                ill=1
            else:
                ill=0
            return expanded,ill
           
        #C.sw  RVI的SW格式形如：| imm[11:5]| rs2 | rs1 | 010 | imm[4:0] | 0100011 |
        elif (rvc_instr_16bit & 0xE003) == 0xC000:
            rs2 = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            nzuimm = (((rvc_instr_16bit >> 5) & 0x1) << 6) | (((rvc_instr_16bit >> 5) & 0xE0) >>2)| (((rvc_instr_16bit >> 5) & 0x2) << 1) 
            expanded = 0x00000023 | ((nzuimm & 0x1F) << 7) | (rs2 << 20) |(0b010 <<12) |(rs1 << 15) |((nzuimm & 0xFE0) << 20)# 
            return expanded,ill
        #C.sd
        elif (rvc_instr_16bit & 0xE003) == 0xE000:
            rs2 = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            nzuimm = (((rvc_instr_16bit >> 5) & 0x3) << 6) | (((rvc_instr_16bit >> 5) & 0xE0) >>2)
            expanded = 0x00000023 | ((nzuimm & 0x1F) << 7) | (rs2 << 20) |(0b011 <<12) |(rs1 << 15) |((nzuimm & 0xFE0) << 20)# 
            return expanded,ill
        else:
            return expanded,ill
        
    elif opcode == 0b01:
        #C.addi
        if (rvc_instr_16bit & 0xE003) == 0x0001:
            rd  = ((rvc_instr_16bit >> 7) & 0x1F)
            rs1 = ((rvc_instr_16bit >> 7) & 0x1F)
            if ((rvc_instr_16bit >> 12) & 0x1):
                nzuimm = 0xFE0 | ((rvc_instr_16bit >> 2) & 0x1F) 
            else:
                nzuimm = 0x000 | ((rvc_instr_16bit >> 2) & 0x1F) 
            expanded = 0x00000013 | (rd << 7) | (0b000 << 12) |(rs1 << 15) | (nzuimm  << 20) # 
            return expanded,ill
        elif (rvc_instr_16bit & 0xE003) == 0x2001:
            rd  = ((rvc_instr_16bit >> 7) & 0x1F)
            rs1 = ((rvc_instr_16bit >> 7) & 0x1F)
            if ((rvc_instr_16bit >> 12) & 0x1):
                nzuimm = 0xFE0 | ((rvc_instr_16bit >> 2) & 0x1F) 
            else:
                nzuimm = 0x000 | ((rvc_instr_16bit >> 2) & 0x1F) 
            expanded = 0x0000001B | (rd << 7) | (0b000 << 12) |(rs1 << 15) | (nzuimm  << 20) # 
            if (rd == 0):
                ill = 1
            
            return expanded,ill

        elif (rvc_instr_16bit & 0xE003) == 0x4001:
            rd  = ((rvc_instr_16bit >> 7) & 0x1F)
            if ((rvc_instr_16bit >> 12) & 0x1):
                nzuimm = 0xFE0 | ((rvc_instr_16bit >> 2) & 0x1F) 
            else:
                nzuimm = 0x000 | ((rvc_instr_16bit >> 2) & 0x1F) 
            expanded = 0x00000013 | (rd << 7) | (0b000 << 12) |(0b00000 << 15) | (nzuimm  << 20) # 
          
            return expanded,ill
        elif (rvc_instr_16bit & 0xE003) == 0x6001:
            rd  = ((rvc_instr_16bit >> 7) & 0x1F)
            if(rd == 2) or (rd == 0):
                if ((rvc_instr_16bit >> 12) & 0x1):
                    nzuimm=0xE00|(((rvc_instr_16bit>>2)&0x1)<<5)|(((rvc_instr_16bit>>3)&0x3)<<7)|(((rvc_instr_16bit>>5)&0x1)<<6)|(((rvc_instr_16bit>>6)&0x1)<<4)  
                else:
                    nzuimm=0x000|(((rvc_instr_16bit>>2)&0x1)<<5)|(((rvc_instr_16bit>>3)&0x3)<<7)|(((rvc_instr_16bit>>5)&0x1)<<6)|(((rvc_instr_16bit>>6)&0x1)<<4) 
                if(nzuimm == 0):
                    ill = 1
                expanded = 0x00000013 | (rd << 7) | (0b000 << 12) |(rd << 15) | (nzuimm  << 20) #     
            else:#lui  lui指令的格式形如： | imm[31:12] | rd | 0110111 |        
                if ((rvc_instr_16bit >> 12) & 0x1):
                    nzuimm = 0xFFFE0000 | (((rvc_instr_16bit >> 2) & 0x1F) << 12)
                else:
                    nzuimm = 0x00000000 | (((rvc_instr_16bit >> 2) & 0x1F) << 12)
                expanded = 0x00000037 | (rd << 7) | (nzuimm)
                if(nzuimm == 0):
                    # ill = 1
                    ill = 2 # temperarily exclude this condition
                    expanded = 0x0000007F

            return expanded,ill
        elif (rvc_instr_16bit & 0xE003) == 0x8001:
            fun6  = (rvc_instr_16bit>>10) & 0x3F
            fun2  = (rvc_instr_16bit>>5 ) & 0x3
            fun3  = ((rvc_instr_16bit >> 2) & 0x7)
            rd  =  8+((rvc_instr_16bit >> 7) & 0x7)
            rs2  = 8+((rvc_instr_16bit >> 2) & 0x7)
            nzuimm = (rvc_instr_16bit>>2)&0x1F
            if(fun6 == 0x20):#SRLI
                expanded = 0x00000013 | (rd << 7) |0b101<<12| (rd << 15)| (nzuimm<<20)
                return expanded,ill
            elif(fun6 == 0x24):#SRLI
                expanded = 0x02000013 | (rd << 7) |0b101<<12| (rd << 15)| (nzuimm<<20)
                return expanded,ill
            elif(fun6 == 0x21):#SRAI
                expanded = 0x00000013 | (rd << 7) |0b101<<12| (rd << 15)| (nzuimm<<20)|(0b0100000<<25)
                return expanded,ill
            elif(fun6 == 0x25):#SRAI
                expanded = 0x00000013 | (rd << 7) |0b101<<12| (rd << 15)| (nzuimm<<20)|(0b0100001<<25)
                return expanded,ill
            elif(fun6 == 0x22):#andi
                expanded = 0x00000013 | (rd << 7) |0b111<<12| (rd << 15)| (nzuimm<<20)
                return expanded,ill
            elif(fun6 == 0x26):#andi
                expanded = 0x00000013 | (rd << 7) |0b111<<12| (rd << 15)| (nzuimm<<20)|(0b1111111<<25)
                return expanded,ill
            elif(fun6 == 0x23):#sub/xor/or/and
                if(fun2 == 0b00):#sub
                    expanded = 0x00000033 | (rd << 7) |0b000<<12| (rd << 15)| (rs2<<20)|(0b0100000<<25)
                    return expanded,ill
                elif(fun2 == 0b01):#xor
                    expanded = 0x00000033 | (rd << 7) |0b100<<12| (rd << 15)| (rs2<<20)|(0b0000000<<25)
                    return expanded,ill
                elif(fun2 == 0b10):#or
                    expanded = 0x00000033 | (rd << 7) |0b110<<12| (rd << 15)| (rs2<<20)|(0b0000000<<25)
                    return expanded,ill
                elif(fun2 == 0b11):
                    expanded = 0x00000033 | (rd << 7) |0b111<<12| (rd << 15)| (rs2<<20)|(0b0000000<<25)
                    return expanded,ill
            elif(fun6 == 0x27):# C.subw/addw/mul/not/zext.b/sext.b/zext.h/sext.h/zext.w/
                if(fun2 == 0b00):#subw
                    expanded = 0x0000003B | (rd << 7) |0b000<<12| (rd << 15)| (rs2<<20)|(0b0100000<<25)
                    return expanded,ill
                elif(fun2 == 0b01):#addw
                    expanded = 0x0000003B | (rd << 7) |0b000<<12| (rd << 15)| (rs2<<20)|(0b0000000<<25)
                    return expanded,ill
                elif(fun2 == 0b10):#mul
                    expanded = 0x00000033 | (rd << 7) |0b000<<12| (rd << 15)| (rs2<<20)|(0b0000001<<25)
                    return expanded,ill
                elif(fun2 == 0b11)&(fun3==0b000):#zext.b
                    expanded = 0x0ff00013 | (rd << 7) |0b111<<12| (rd << 15)
                    return expanded,ill
                elif(fun2 == 0b11)&(fun3==0b001):#sext.b
                    expanded = 0x00000013 | (rd << 7) |0b001<<12| (rd << 15)|(0b00100<<20)|(0b0110000<<25)
                    return expanded,ill
                elif(fun2 == 0b11)&(fun3==0b010):#zext.h
                    expanded = 0x0000003B | (rd << 7) |0b100<<12| (rd << 15)|(0b00000<<20)|(0b0000100<<25)
                    return expanded,ill
                elif(fun2 == 0b11)&(fun3==0b011):#sext.h
                    expanded = 0x00000013 | (rd << 7) |0b001<<12| (rd << 15)|(0b00101<<20)|(0b0110000<<25)
                    return expanded,ill
                elif(fun2 == 0b11)&(fun3==0b100):#zext.w
                    expanded = 0x0000003B | (rd << 7) |0b000<<12| (rd << 15)|(0b00000<<20)|(0b0000100<<25)
                    return expanded,ill
                elif(fun2 == 0b11)&(fun3==0b101):#not
                    expanded = 0xfff00013 | (rd << 7) |0b100<<12| (rd << 15)|(0b00000<<20)
                    return expanded,ill
                else:
                    ill =2
                    return expanded,ill
            else:
                return expanded,ill
        elif (rvc_instr_16bit & 0xE003) == 0xa001:
            nzuimm = 0xFFFE0000|(((rvc_instr_16bit>>2)&0x1)<<5)|(((rvc_instr_16bit>>2)&0xe))|(((rvc_instr_16bit>>2)&0x10)<<3)|(((rvc_instr_16bit>>2)&0x20)<<1)|(((rvc_instr_16bit>>2)&0x40)<<4)|(((rvc_instr_16bit>>2)&0x180)<<1)|(((rvc_instr_16bit>>2)&0x200)>>5)|(((rvc_instr_16bit>>2)&0x400)<<1)                                                                                                                                          
            if(((rvc_instr_16bit>>2)&0x400)>>10):
                expanded = 0x800FF06F|(0b00000 << 7)|((nzuimm &0x7fe) <<20)|((nzuimm &0x800) <<9)# 
            else: 
                expanded = 0x0000006F|(0b00000 << 7)|((nzuimm &0x7fe) <<20)|((nzuimm &0x800) <<9)# 
            return expanded,ill
        elif (rvc_instr_16bit & 0xE003) == 0xc001:
            rs1 = ((rvc_instr_16bit >> 7) & 0x7)+8
            nzuimm = 0xFF & ((((rvc_instr_16bit>>2)&0x1)<<4)|((((rvc_instr_16bit>>2)&0x6)>>1))|(((rvc_instr_16bit>>2)&0x18)<<2)|(((rvc_instr_16bit>>2)&0x300)>>6)|(((rvc_instr_16bit>>2)&0x400)>>3))
            if((((rvc_instr_16bit>>2)&0x400)>>10)):
                expanded = 0xF00000E3|((nzuimm&0x0F)<<8)|rs1<<15|((nzuimm&0xF0)<<21)
            else:
                expanded = 0x00000063|((nzuimm&0x0F)<<8)|rs1<<15|((nzuimm&0xF0)<<21)
            return expanded,ill
        elif (rvc_instr_16bit & 0xE003) == 0xe001:
            rs1 = ((rvc_instr_16bit >> 7) & 0x7)+8
            nzuimm = 0xFF & ((((rvc_instr_16bit>>2)&0x1)<<4)|((((rvc_instr_16bit>>2)&0x6)>>1))|(((rvc_instr_16bit>>2)&0x18)<<2)|(((rvc_instr_16bit>>2)&0x300)>>6)|(((rvc_instr_16bit>>2)&0x400)>>3))
            if((((rvc_instr_16bit>>2)&0x400)>>10)):
                expanded = 0xF00000E3|((nzuimm&0x0F)<<8)|0x001<<12|rs1<<15|((nzuimm&0xF0)<<21)
            else:
                expanded = 0x00000063|((nzuimm&0x0F)<<8)|0x001<<12|rs1<<15|((nzuimm&0xF0)<<21)
            return expanded,ill
    elif opcode == 0b10:
            if (rvc_instr_16bit & 0xE003) == 0x0002:
                rd  = ((rvc_instr_16bit >> 7) & 0x1F)
                rs1 = ((rvc_instr_16bit >> 7) & 0x1F)

                nzuimm = 0x000 | ((rvc_instr_16bit >> 2) & 0x1F) | ((rvc_instr_16bit >> 7) & 0x20)
                expanded = 0x00000013 | (rd << 7) | (0b001 << 12) |(rs1 << 15) | (nzuimm  << 20) # 
               
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0x2002:#fldsp
                rd  = ((rvc_instr_16bit >> 7) & 0x1F)
                rs1 = ((rvc_instr_16bit >> 7) & 0x1F)

                nzuimm = (((rvc_instr_16bit >> 2) & 0x7) <<6) | ((rvc_instr_16bit >> 7) & 0x20) | ((rvc_instr_16bit >> 2) & 0x18)
                expanded = 0x00000007 | (rd << 7) | (0b011 << 12) |(0b00010 << 15) | (nzuimm  << 20) # 
                if(fsIsOff==True):
                    ill=1
                else:
                    ill=0
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0x4002:#lwsp
                rd  = ((rvc_instr_16bit >> 7) & 0x1F)
                rs1 = ((rvc_instr_16bit >> 7) & 0x1F)

                nzuimm = (((rvc_instr_16bit >> 2) & 0x3) <<6) | ((rvc_instr_16bit >> 7) & 0x20) | ((rvc_instr_16bit >> 2) & 0x1c)
                expanded = 0x00000003 | (rd << 7) | (0b010 << 12) |(0b00010 << 15) | (nzuimm  << 20) # 
                if (rd == 0):
                    ill = 1
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0x6002:#ldsp
                rd  = ((rvc_instr_16bit >> 7) & 0x1F)
                rs1 = ((rvc_instr_16bit >> 7) & 0x1F)

                nzuimm = (((rvc_instr_16bit >> 2) & 0x7) <<6) | ((rvc_instr_16bit >> 7) & 0x20) | ((rvc_instr_16bit >> 2) & 0x18)
                expanded = 0x00000003 | (rd << 7) | (0b011 << 12) |(0b00010 << 15) | (nzuimm  << 20) # 
                if (rd == 0):
                    ill = 1
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0x8002:#JR/MV/EBREAK/JALR/ADD
                rs1  = ((rvc_instr_16bit >> 7) & 0x1F)
                rs2 =  ((rvc_instr_16bit >> 2) & 0x1F)
                funct4 = (rvc_instr_16bit>>12)&0x1
                nzuimm = (((rvc_instr_16bit >> 2) & 0x7) <<6) | ((rvc_instr_16bit >> 7) & 0x20) | ((rvc_instr_16bit >> 2) & 0x18)
                if((funct4==0)&(rs2==0)&(rs1!=0)): #JR
                    expanded = 0x00000067 | (0b00000 << 7) | (0b000 << 12) |(rs1 << 15) # 
                elif(funct4==0)&(rs2!=0):#&(rs1!=0)):#MV  0000000 rs2 rs1 000 rd 0110011 ADD
                    expanded = 0x00000013 | (rs1 << 7) | (0b000 << 12) |(rs2 << 15)  # 
                elif((funct4==1)&(rs2==0)&(rs1==0)): #ebreak
                    expanded = 0b00000000000100000000000001110011
                elif((funct4==1)&(rs2==0)&(rs1!=0)): #jalr
                    expanded = 0x00000067 | (0b00001 << 7) | (0b000 << 12) |(rs1 << 15) #
                elif(funct4==1)&(rs2!=0):#&(rs1!=0)): #add
                    expanded = 0x00000033 | (rs1 << 7) | (0b000 << 12) |(rs1 << 15) |(rs2 << 20) #              
                else: 
                    ill = 1
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0xa002:#fsdsp
                rs2 = ((rvc_instr_16bit >> 2) & 0x1F)
                nzuimm = ((rvc_instr_16bit >> 1) & 0x1C0) | ((rvc_instr_16bit >> 7) & 0x38) 
                expanded = 0x00000027 |((nzuimm & 0x1F)<<7)| (0b011 << 12 ) |  (0b00010 << 15)| (rs2 << 20)| ((nzuimm&0xFE0)<< 20) # 
                if(fsIsOff==True):
                    ill=1
                else:
                    ill=0
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0xc002:#swsp
                rs2 = ((rvc_instr_16bit >> 2) & 0x1F)
                nzuimm = ((rvc_instr_16bit >> 1) & 0xC0) | ((rvc_instr_16bit >> 7) & 0x3C) 
                expanded = 0x00000023 |((nzuimm & 0x1F)<<7)| (0b010 << 12 ) |  (0b00010 << 15)| (rs2 << 20)| ((nzuimm&0xFE0)<< 20) # 
              
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0xE002:#sdsp
                rs2 = ((rvc_instr_16bit >> 2) & 0x1F)
                nzuimm = ((rvc_instr_16bit >> 1) & 0x1C0) | ((rvc_instr_16bit >> 7) & 0x38) 
                expanded = 0x00000023 |((nzuimm & 0x1F)<<7)| (0b011 << 12 ) |  (0b00010 << 15)| (rs2 << 20)| ((nzuimm&0xFE0)<< 20) # 
              
                return expanded,ill
            else:
                return expanded,ill
    else:
        return rvc_instr, False