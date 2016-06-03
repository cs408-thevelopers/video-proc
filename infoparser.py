
f = file("test1info.txt", 'r')
cnt = 0
prev = now = 0
for line in f:
	prev = now
	now = float(line.split(":")[-1])
	if prev > 0 and (prev - now) > 0.6: print cnt
	cnt += 1
print cnt
	
