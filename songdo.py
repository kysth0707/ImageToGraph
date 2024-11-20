allList = [
	[[2, -5, -1], [0, 4, 6], [-3, 7, 1]],
	[[3, -6, 7], [-2, 0, -4], [5, -9, 2]],
	[[-8, 2, 0], [1, 3, 0], [6, -5, 0]],
	[[1, 1, 1], [5, 5, 5], [-6, 4, 2]]
]

for vectors in allList:
	a,b,c = vectors
	u = ", ".join([str(b[i] - a[i]) for i in range(3)])
	v = ", ".join([str(c[i] - a[i]) for i in range(3)])
	print(f"x = {tuple(a)} + s({u}) + t({v})")