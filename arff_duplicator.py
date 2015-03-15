#We got 2431 instances, of which 2392 are -
#To get a 1:1 proportion we take the + classified instances and take them 61 times
#afterwards there should be 2379 + and 2392 -

#lets see if this makes a difference

output = []
with open("ontolo_new_trop.arff") as fileobject:
		for line in fileobject:
			test = line.split(",")
			if len(test) == 4:
				if test[3] == "+\n":
					for i in range(0,61):
						output += [line]
				else:
					output += [line]
			else:
				output += [line]
print "".join(output)
			