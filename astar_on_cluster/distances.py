def power_mean(list, p):
	if p:
		psum = reduce(lambda x,y: x+y, map(lambda x: x**p, list))
		return (float(psum)/len(list))**(1.0/p)
	else:
		prod = reduce(lambda x,y: x*y, list)
		return prod**(1.0/len(list))

def root_mean_square(list):
	return power_mean(list, 2)

def arithmetic_mean(list):
	return power_mean(list, 1)

def geometric_mean(list):
	return power_mean(list, 0)

def harmonic_mean(list):
	return power_mean(list, -1)

def harmonic_mean_unit(list):
	return harmonic_mean(list)/len(list)
