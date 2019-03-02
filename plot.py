import matplotlib.pyplot as plt

with open("result.txt", "r") as f:
	line1 = f.readline()
	x = line1.strip('\r\n[]').split(',')
	x = map(float, x)
	line2 = f.readline()
	y = line2.strip('\r\n[]').split(',')
	y = map(float, y)
	line3 = f.readline()
	angle = line3.strip('\r\n[]').split(',')
	angle = map(float, angle)

print x
print y
print angle

plt.plot(x, y)
plt.show()