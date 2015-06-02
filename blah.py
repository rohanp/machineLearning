from numba import jit

@jit
def main():
	i = 0
	while True:
		print i
		i += 1

main()
