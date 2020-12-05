## INSTRUCTION BYTECODES (byte is signed; use a short to keep 0..255)
IADD   =  1  ## int add
ISUB   =  2  ## int sub
IMUL   =  3  ## int mul
ILT    =  4  ## int less than
IEQ    =  5  ## int equal
BR     =  6  ## branch
BRT    =  7  ## branch if true
BRF    =  8  ## branch if true
ICONST =  9  ## push constant integer
LOAD   = 10  ## load from local context
GLOAD  = 11  ## load from global memory
STORE  = 12  ## store in local context
GSTORE = 13  ## store in global memory
PRINT  = 14  ## print stack top
POP    = 15  ## throw away top of stack
CALL   = 16  ## call function
RET    = 17  ## return with/without value
HALT   = 18  ## halt

instructions = [
	None,        ## INVALID OPCODE
	("iadd",0),  ## index is the opcode
	("isub",0),
	("imul",0),
	("ilt",0),
	("ieq",0),
	("br", 1),
	("brt", 1),
	("brf", 1),
	("iconst", 1),
	("load", 1),
	("gload", 1),
	("store", 1),
	("gstore", 1),
	("print",0),
	("pop",0),
	("call", 1),  ## call index of function in meta-info table
	("ret",0),
	("halt",0)
];
