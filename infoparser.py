
f = file("test2info.txt", 'r')
cnt = 0
prev = now = 0
A = list()
for line in f:
	A.append(float(line.split(":")[-1]))

diff = [A[i] - A[i-1] for i in range(1, len(A))]
print diff
avg = sum(diff)/len(diff)
stdev = (sum((i - avg) ** 2 for i in diff) / len(diff)) ** .5
print stdev
for i in range(len(diff)):
	if diff[i] > stdev : print i, diff[i]

print len(A) - 1
