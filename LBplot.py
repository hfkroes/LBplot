import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

V0 = []
S = []

print('''Would you like to insert values of V0 and [S] or 1/V0 and 1/[S]?
	1- V0 and [S]
	2- 1/V0 and 1/[S]''')
k = input()
print('How many values would you like to insert?')
l=int(input())
if k == '1':
	n=0
	while n < l:
		if n == 0:
			print('Insert V0 values:')
			print('V0'+str(n+1)+':')
			V0.append(float(input()))
			n+=1
		else:
			print('V0'+str(n+1)+':')
			V0.append(float(input()))
			n+=1
	m=0
	while m < l:
		if m == 0:
			print('Insert [S] values:')
			print('[S]'+str(m+1)+':')
			S.append(float(input()))
			m+=1
		else:
			print('[S]'+str(m+1)+':')
			S.append(float(input()))
			m+=1

	oV0 = []
	oS = []

	for a in V0:
		oa = 1.0/float(a)
		oV0.append(oa)

	for b in S:
		ob = 1.0/float(b)
		oS.append(ob)

if k == '2':
	oV0 = []
	oS = []
	n=0
	while n < l:
		if n == 0:
			print('Insert 1/V0 values:')
			print('1/V0'+str(n+1)+':')
			oV0.append(float(input()))
			n+=1
		else:
			print('1/V0'+str(n+1)+':')
			oV0.append(float(input()))
			n+=1
	m=0
	while m < l:
		if m == 0:
			print('Insert 1/[S] values:')
			print('1/[S]'+str(m+1)+':')
			oS.append(float(input()))
			m+=1
		else:
			print('1/[S]'+str(m+1)+':')
			oS.append(float(input()))
			m+=1

x = oS
y= oV0

plt.scatter(x, y)

slope, intercept, r, p, std_err = stats.linregress(x, y)

x.append(0-(int(intercept/slope))-(0.1*(float(max(x)))))
x.append(1.1*(float(max(x))))

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))

plt.plot(x, mymodel, '-r', label= 'Vmax = '+str((1/intercept))+'\nKm = '+str((slope/intercept)))
plt.plot([0, (0-int(intercept/slope))], [intercept, 0],'go')
plt.title('Lineweaver-Burk double reciprocal plot')
plt.xlabel('1/[S]', color='#088A08')
plt.ylabel('1/V0', color='#088A08')
plt.legend()
plt.grid()
plt.show()


