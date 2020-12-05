from FuncMetaData import *

class Context():
	''' To call, push one of these and pop to return '''
	def __init__(self,ctx = None,returnip = -1,metadata = FuncMetaData()):
		self.ctx = ctx ## parent in the stack or "caller" 
		self.returnip = returnip
		self.metadata = metadata ## info about function we're executing
		self.locals   = list(range(self.metadata.nargs+self.metadata.nlocals)) ## args + locals, indexed from 0
		
	def __str__(self):
		return 'ctx: {} \nreturnip: {} \nmetadata: {} \nlocals: {}'.format(self.ctx,self.returnip,self.metadata,self.locals)
