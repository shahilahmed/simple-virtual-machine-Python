from Bytecode     import *
from FuncMetaData import *
from Context      import *
from VM           import *

class Test():
	def test_factorial(self):
		'''
			def factorial nargs: 1 nlocals: 0 address: 0
				0000 load 0
				0002 iconst 2
				0004 ilt
				0005 brf 10
				0007 iconst 1
				0009 ret
				0010 load 0
				0012 load 0
				0014 iconst 1
				0016 isub
				0017 call factorial
				0019 imul
				0020 ret

			def main nargs: 0 nlocals: 0 address: 21
				0021 iconst 6
				0023 call factorial
				0025 print
				0026 halt
		'''
		FACTORIAL_INDEX = 1;
		FACTORIAL_ADDRESS = 0;
		MAIN_ADDRESS = 21;
		factorial = [
		## DEF FACTORIAL: ARGS=1, LOCALS=0	
		## IF N < 2 RETURN 1
				LOAD, 0,				
				ICONST, 2,				
				ILT,					
				BRF, 10,				
				ICONST, 1,				
				RET,
		## CONT:
		## RETURN N * FACT(N-1)
				LOAD, 0,				
				LOAD, 0,				
				ICONST, 1,				
				ISUB,					
				CALL, FACTORIAL_INDEX,	
				IMUL,					
				RET,					
		## DEF MAIN: ARGS=0, LOCALS=0
		## PRINT FACT(1)
				ICONST, 5,			    ## <-- MAIN METHOD
				CALL, FACTORIAL_INDEX,	
				PRINT,					
				HALT					
		];
		factorial_metadata = [
			FuncMetaData("main", 0, 0, MAIN_ADDRESS),
			FuncMetaData("factorial", 1, 0, FACTORIAL_ADDRESS)
		]
		print('Program: factorial')
		v = VM(factorial,0,factorial_metadata)
		print(v.dumpCodeMemory())
		v.execute()
		print()
	
	def test_loop(self):
		'''
			def main nargs: 0 nlocals: 0 address: 0
				0000 iconst 10
				0002 gstore 0
				0004 iconst 0
				0006 gstore 1
				0008 gload 1
				0010 gload 0
				0012 ilt
				0013 brf 24
				0015 gload 1
				0017 iconst 1
				0019 iadd
				0020 gstore 1
				0022 br 8
				0024 halt
		'''	
		loop = [
		## GLOBALS 2; N, I
		## N = 10
			ICONST, 10,				
			GSTORE, 0,				
		## I = 0
			ICONST, 0,				
			GSTORE, 1,				
		## WHILE I<N:
		## START (8):
			GLOAD, 1,				
			GLOAD, 0,				
			ILT,					
			BRF, 24,
		## I = I + 1
			GLOAD, 1,				
			ICONST, 1,				
			IADD,					
			GSTORE, 1,				
			BR, 8,					
		## DONE (24):
		## PRINT "LOOPED "+N+" TIMES."
			HALT					
		]
		loop_metadata = [
			FuncMetaData("main", 0, 0, 0)
		]

		print('Program: loop')
		v = VM(loop,2,loop_metadata)
		print(v.dumpCodeMemory())
		v.execute()
		print(v.dumpDataMemory())
		print()
	
	def test_f(self):
		'''
			def main nargs: 0 nlocals: 0 address: 0
				0000 iconst 10
				0002 call f
				0004 print
				0005 halt

			def f nargs: 1 nlocals: 1 address: 6
				0006 load 0
				0008 store 1
				0010 load 1
				0012 iconst 2
				0014 imul
				0015 ret
		'''
		f = [
		## DEF MAIN() { PRINT F(10); }
			ICONST, 10,	
			CALL, 1,	
			PRINT,		
			HALT,
		## DEF F(X): ARGS=1, LOCALS=1
		##  A = X;
			LOAD, 0,  ## <-- START OF F METHOD	
			STORE, 1,
		## RETURN 2*A
			LOAD, 1,
			ICONST, 2,
			IMUL,
			RET
		]
		f_metadata = [
			FuncMetaData("main", 0, 0, 0),
			FuncMetaData("f", 1, 1, 6)
		]
		print('Program: f')
		v = VM(f,2,f_metadata)
		print(v.dumpCodeMemory())
		v.execute()
		print()
	
	def run(self):
		self.test_factorial()
		self.test_loop()
		self.test_f()

if __name__ == '__main__':
	try:
		t = Test()
		t.run()
	except Exception as e:
		print(e)