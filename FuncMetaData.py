class FuncMetaData():
	'''Stores the metadata of a function which include name,address,number of locals and arguments of a function'''
	def __init__(self,name = 'name',nargs = 0,nlocals = 0,address = -1):
		self.name = name
		self.nargs = nargs
		self.nlocals = nlocals
		self.address = address ## bytecode address
		
	def __str__(self):
		return 'def {} nargs: {} nlocals: {} address: {}'.format(self.name,self.nargs,self.nlocals,self.address)
