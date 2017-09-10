class SampleClass:
	variable = "hello"

	def function(self):
		print("earth")

objectx = SampleClass()
objecty = SampleClass()

objecty.variable = "world"

print(objectx.variable)
print(objecty.variable)
objectx.function()