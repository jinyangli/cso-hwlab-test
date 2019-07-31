import sys

# ["name", "opcode", "f3", "f7/imm"]
ALUSels = { "add": 0x0, \
	 "and": 0x1,\
	"or": 0x2, \
	"xor": 0x3, \
	"srl": 0x4, \
	"sra": 0x5, \
	"sll": 0x6, \
	"slt": 0x7, \
	"divu": 0x8,\
	"remu": 0x9,\
	"mult": 0xa, \
	"mulhu": 0xb, \
	"sub": 0xc, \
	"bsel": 0xd, \
	"mulh": 0xe }

class Inst:
	def __init__(self, itype, name, opcode, f3, f7imm):
		self.inst_type = itype
		self.name = name
		self.opcode = opcode
		self.f3 = f3
		self.f7imm = f7imm
	def GetControlValue(self):
		name = self.name
		if name.endswith("i"):
			name = name[:-1]
		if self.inst_type == "R":
			return 0x0204 | (ALUSels[name] << 4)
		elif self.inst_type == "I":
			return 0x0304 | (ALUSels[name] << 4)
		else:
			raise Exception("Types other than R not supported yet")
	def GetControlAddr(self):
		address = self.opcode >> 2
		address |= (self.f3<<5)
		address |= (self.f7imm & 0x01)<<8
		address |= (self.f7imm & 0x10)<<9
		return address

instructions = [Inst("R", "add", 0x33, 0x0, 0x00), \
		Inst("R", "mult", 0x33, 0x0, 0x01),\
		Inst("R", "sub", 0x33, 0x0, 0x20),\
		Inst("R", "sll", 0x33, 0x1, 0x00),\
		Inst("R", "mulh", 0x33, 0x1, 0x01),\
		Inst("R", "mulhu", 0x33, 0x3, 0x01),\
		Inst("R", "slt", 0x33, 0x2, 0x00),\
		Inst("R", "xor", 0x33, 0x4, 0x00),\
		Inst("R", "divu", 0x33, 0x5, 0x01),\
		Inst("R", "srl", 0x33, 0x5, 0x00),\
		Inst("R", "or", 0x33, 0x6, 0x00),\
		Inst("R", "remu", 0x33, 0x7, 0x01),\
		Inst("R", "and", 0x33, 0x7, 0x00), \
		Inst("I", "addi", 0x13, 0x7, 0x00) ] # addi has don't care f7/imm

def main(args):
	results = []
	for i in instructions:
		results.append((i.GetControlAddr(), i.GetControlValue()))
	results.sort()
	for a,b in results:
		print hex(a), hex(b)

if __name__ == "__main__":
	main(sys.argv)
