from Bytecode     import *
from FuncMetaData import *
from Context      import *

class VM():
	'''A simple stack-based interpreter'''
	def __init__(self,code = [],nglobals = 0,metadata = []):
		## registers
		self.sp       = -1 ## instruction pointer register
		self.ip       = -1 ## stack pointer register
		
		## memory 
		self.code     = code					## word-addressable code memory but still bytecodes.
		self.globals  = list(range(nglobals))   ## global variable space
		self.stack    = list(range(1024*4))     ## Operand stack, grows upwards
		self.ctx      = None 					## the active context
		
		## Metadata about the functions allows us to refer to functions by
		## their index in this table. It makes code generation easier for
		## the bytecode compiler because it doesn't have to resolve
		## addresses for forward references. It can generate simply
		## "CALL i" where i is the index of the function. Later, the
		## compiler can store the function address in the metadata table
		## when the code is generated for that function.
		self.metadata = metadata
		self.trace    = False
		if self.trace == True:
			print(self.dumpCodeMemory())
			print()
	
	def execute(self,startip = -1):
		self.ip = self.metadata[0].address if startip == -1 else startip
		self.ctx = Context(None,0,self.metadata[0]); ## simulate a call to main()
		self.cpu()
		
	def push(self,value):
		self.sp = self.sp + 1
		self.stack[self.sp] = value
	
	def pop(self):
		value = self.stack[self.sp]
		self.sp = self.sp - 1
		return value
		
	def cpu(self):
		''' Simulate the fetch-decode execute cycle '''
		opcode = self.code[self.ip]
		while opcode != HALT and self.ip < len(self.code):
			if self.trace == True:
				print('{}'.format(self.disInstr()))	
			self.ip = self.ip + 1 ## jump to next instruction or to operand
			if opcode == IADD:
				b = self.pop()   ## 2nd opnd at top of stack
				a = self.pop()   ## 1st opnd 1 below top
				self.push(a + b) ## push the result
			elif opcode == ISUB:
				b = self.pop()
				a = self.pop()
				self.push(a - b)
			elif opcode == IMUL:
				b = self.pop()
				a = self.pop()
				self.push(a * b)
			elif opcode == ILT:
				b = self.pop()
				a = self.pop()
				self.push(a < b)
			elif opcode == IEQ:
				b = self.pop()
				a = self.pop()
				self.push(a == b)
			elif opcode == BR:
				self.ip = self.code[self.ip]
			elif opcode == BRT:
				addr = self.code[self.ip]
				self.ip = self.ip + 1
				if self.pop() == True:
					self.ip = addr
			elif opcode == BRF:
				addr = self.code[self.ip]
				self.ip = self.ip + 1
				if self.pop() == False:
					self.ip = addr
			elif opcode == ICONST:
				self.push(self.code[self.ip]) ## push operand
				self.ip = self.ip + 1
			elif opcode == LOAD: ## load local or arg
				offset = self.code[self.ip]
				self.ip = self.ip + 1
				self.push(self.ctx.locals[offset])
			elif opcode == GLOAD: ## load from global memory
				addr = self.code[self.ip]
				self.ip = self.ip + 1
				self.push(self.globals[addr])
			elif opcode == STORE:
				offset = self.code[self.ip]
				self.ip = self.ip + 1
				self.ctx.locals[offset] = self.pop()
			elif opcode == GSTORE:
				addr = self.code[self.ip]
				self.ip = self.ip + 1
				self.globals[addr] = self.pop()
			elif opcode == PRINT:
				print('{}'.format(self.pop()))
			elif opcode == POP:
				self.pop()
			elif opcode == CALL:
				## expects all args on stack
				findex  = self.code[self.ip] ## index of target function
				self.ip = self.ip + 1
				nargs    = self.metadata[findex].nargs	## how many args got pushed
				self.ctx = Context(self.ctx,self.ip,self.metadata[findex])	
				## copy args into new context
				firstarg = self.sp-nargs+1;
				i = 0	
				while i < nargs:
					self.ctx.locals[i] = self.stack[firstarg+i]
					i = i+ 1
				self.sp = self.sp - nargs;
				self.ip = self.metadata[findex].address; ## jump to function
			elif opcode == RET:
				self.ip  = self.ctx.returnip
				self.ctx = self.ctx.ctx       ## pop
			else:
				raise Exception('{:04} {} INVALID OPCODE'.format(self.ip-1,opcode))
			if self.trace == True:
				print('{}'.format(self.stackString()))
				print('{}'.format(self.callStackString()))
			opcode = self.code[self.ip]
		if self.trace == True:
			print('{}'.format(self.disInstr()))	
			print('{}'.format(self.stackString()))
			print('{}'.format(self.callStackString()))
			print('{}'.format(self.dumpDataMemory()))
			print()	
	
	def disInstr(self):
		opcode = self.code[self.ip] 
		opName = instructions[opcode][0]
		nargs  = instructions[opcode][1]
		buf    = ''
		buf    = buf + '{} '.format(opName)
		if opcode == CALL:
			buf    = buf + '{} '.format(self.metadata[self.code[self.ip+1]].name)
		elif nargs > 0:
			operands = []
			i = self.ip + 1
			while i <= self.ip + nargs:
				operands.append(str(self.code[i]))
				i = i + 1
			buf = buf + '{} '.format(' '.join(operands))	
		buf = '{:04}: {:}'.format(self.ip,buf)
		return buf
	
	def dumpCodeMemory(self):
		buf = 'Code Memory(Assembly):\n\n'
		ip = 0
		while ip < len(self.code):
			opcode = self.code[ip] 
			opName = instructions[opcode][0]
			nargs  = instructions[opcode][1]
			j = 0
			while j < len(self.metadata):
				if ip == self.metadata[j].address:
					buf = buf + '\n{}\n'.format(str(self.metadata[j]))
				j = j + 1
			buf    = buf + '    {:04} {} '.format(ip,opName)
			if opcode == CALL:
				buf    = buf + '{} '.format(self.metadata[self.code[ip+1]].name)
				ip = ip + 1
			elif nargs > 0:
				operands = []
				i = ip + 1
				while i <= ip + nargs:
					operands.append(str(self.code[i]))
					i = i + 1
				ip = ip + nargs
				buf = buf + '{} '.format(' '.join(operands))	
			ip = ip + 1
			buf = '{}\n'.format(buf)
		return buf
	
	def dumpDataMemory(self):
		buf = 'Data Memory:\n\n'
		addr = 0
		while addr < len(self.globals):
			buf = '{}{:04} : {}\n'.format(buf,addr,self.globals[addr])
			addr = addr + 1
		return buf
	
	def stackString(self):
		buf = ''
		buf = '{}{} '.format(buf,'stack=[')
		i = 0
		while i <= self.sp:
			buf = '{}{} '.format(buf,str(self.stack[i]))
			i = i + 1
		buf = '{}{} '.format(buf,']')
		return buf
	
	def callStackString(self):
		buf = ''
		buf = '{}{} '.format(buf,'calls=[')
		c = self.ctx
		while c != None:
			if c.metadata != None:
				buf = '{}{} '.format(buf,c.metadata.name)
			c = c.ctx	
		buf = '{}{} '.format(buf,']')
		return buf
	
