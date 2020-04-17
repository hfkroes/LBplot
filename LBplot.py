import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

V0 = []
S = []

oV0 = []
oS = []

print('''Would you like to insert values of V0 and [S] or 1/V0 and 1/[S]?
	1- V0 and [S]
	2- 1/V0 and 1/[S]''')
k = input()
print('''What input format do you prefer?
	1- Separated by commas (x, y, z, h, i, j)
	2- Individually (x)''')
h = input()
if k == '1':
	if h == '1':
		print('Insert V0 values:')
		tmpV0 = (input().replace(' ', '')).split(',')
		print('Insert [S] values:')
		tmpS = (input().replace(' ', '')).split(',')

		for a in tmpV0:
			oa = 1.0/float(a)
			oV0.append(oa)

		for b in tmpS:
			ob = 1.0/float(b)
			oS.append(ob)

	elif h == '2':
		print('How many values would you like to insert?')
		l = int(input())
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

		for a in V0:
			oa = 1.0/float(a)
			oV0.append(oa)

		for b in S:
			ob = 1.0/float(b)
			oS.append(ob)

elif k == '2':
	n=0
	if h == '2':
		print('How many values would you like to insert?')
		l = int(input())
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

	elif h == '1':
		print('Insert 1/V0 values:')
		tmpV0 = (input().replace(' ', '')).split(',')
		print('Insert 1/[S] values:')
		tmpS = (input().replace(' ', '')).split(',')

		for a in tmpV0:
			oa = float(a)
			oV0.append(oa)

		for b in tmpS:
			ob = float(b)
			oS.append(ob)

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
plt.plot([(0-int(intercept/slope))], [0],'co')
plt.plot([0], [intercept],'go')
plt.title('Lineweaver-Burk double reciprocal plot')
plt.xlabel('1/[S]', color='#298A08')
plt.ylabel('1/V0', color='#01DFD7')
plt.legend()
plt.grid()
plt.show()


