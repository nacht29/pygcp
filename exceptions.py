'''
Custom Exceptions (errors)
'''
class CustomError(Exception):
	def __init__(self, message, error_code=None):
		super().__init__(message)
		self.error_code = error_code

class SliceError(CustomError):
	def __init__(self, message="Invalid slice length. Must be at least 1."):
		super().__init__(message)