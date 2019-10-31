import matplotlib.pyplot as plt
import numpy as np
r=2
plt.figure(dpi=300)
def create_circle(r,l, col):
	circle = plt.Circle((0,0), radius= r, fill=False, linewidth=l*5, color=col)
	return circle


def show_shape(patch):
	ax=plt.gca()
	ax.add_patch(patch)

for i in [1,2.2,3.2,3.9,4.5,5]:
	a=create_circle(i,1/(i), 'black')
	b=create_circle(i+0.2/(i),1/(i), 'red')
	c=create_circle(i-0.2/(i),1/(i), 'blue')
	show_shape(a)
	#show_shape(b)
	#show_shape(c)

plt.axis('scaled')
plt.grid()
plt.xlabel('x / cm')
plt.ylabel('y / cm')
plt.savefig("Bild1.png")
