import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os
import math

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    print('LBplot - Lineweaver-Burk linear graph plotter for Michaelis-Menten enzime kinetics\n')

def menu():
	print ('''\nWould you like to return to the main menu?
	1-Yes, return to main menu
	2-No, end program''')

V0 = []
S = []

oV0 = []
oS = []

st='start'
while st == 'start':
	cls()
	print('''What would you like to access?
	1-Execute program
	2-References
	3-Licence''')
	ii = input()
	if ii == '1':
		cls()
		print('''Would you like to insert values of V0 and [S] or 1/V0 and 1/[S]?
	1- V0 and [S]
	2- 1/V0 and 1/[S]''')
		k = input()
		print('''Which are the the unities your data use?
V0:''')
		u = input()
		print('[S]:')
		v = input()
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

		def erro(x, z):
			a = []
			xm = sum(x)/len(x)
			for r in range(0,len(x)):
				at = ((x[r]-xm)**2)
				a.append(at)
			atot = (sum(a)/(len(x)-z))
			return atot


		errorg2 = erro(x, 0)
		errorg = (math.sqrt(errorg2))
		errors2 = erro(x, 1)
		errors = (math.sqrt(errors2))

		x.append(0-(int(intercept/slope)))
		x.append(1.1*(float(max(x))))

		def myfunc(x):
		  return slope * x + intercept

		mymodel = list(map(myfunc, x))

		plt.plot(x, mymodel, '-r')
		plt.plot([(0-int(intercept/slope))], [0],'co', label= 'Vmax = '+str((1/intercept)))
		plt.plot([0], [intercept],'go', label = 'Km = '+str((slope/intercept)))
		plt.suptitle('Lineweaver-Burk double reciprocal plot')
		plt.xlabel('1/[S] '+'(1/'+v+')', color='#298A08')
		plt.ylabel('1/V0 '+'(1/'+u+')', color='#01DFD7')
		plt.legend()
		plt.grid()
		cls()
		print('                        DATA SET')
		print('        V0          1/V0          [S]          1/[S]')
		print('   ------------ ------------ ------------- ------------')
		for a in range(0,len(tmpV0)):
			print(str(a+1)+' |  '+str("{:.2e}".format(float(tmpV0[a])))+'  |  '+str("{:.2e}".format(float(oV0[a])))+'  |  '+str("{:.2e}".format(float(tmpS[a])))+'   |  '+str("{:.2e}".format(float(oS[a])))+'  |')
		print('   ------------ ------------ ------------- ------------')
		print('\n                VARIANCES AND DEVIATIONS')
		print('\nPopulation Variance (σ^2) = '+str("{:.2e}".format(errorg2))+'\nPopulation Standard Deviation (σ) = '+str("{:.2e}".format(errorg))+'\nSample Variance (S^2) = '+str("{:.2e}".format(errors2))+'\nSample Standard Deviation (S) = '+str("{:.2e}".format(errors)))
		plt.show()

		menu()
		me = input()
		if me == '1':
			continue
		if me == '2':
			break

	if ii=='2':
		cls()
		print('''Lineweaver, H., & Burk, D. (1934). The Determination of Enzyme Dissociation Constants. 
Journal of the American Chemical Society, 56(3), 658–666. doi:10.1021/ja01318a036

Michaelis, L., and Menten, M. L. (1913) Die Kinetik der Invertinwirkung. Biochem. Z. 49, 333–369

Knight K. (2000), Mathematical Statistics, Chapman and Hall, New York. (proposition 2.11)''')
		menu()
		me = input()
		if me == '1':
			continue
		if me == '2':
			break

	if ii=='3':
		cls()
		print('''This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>''')
		ma = '0'
		while ma!='1':
			print('\nInput 1 to continue:')
			ma = input()
		cls()
		print('''Note: It would be very kind if you could email me saying if
you used this program and perhaps suggest improvements.

contact: hector.kroes@outlook.com

Thank you!''')
		menu()
		me = input()
		if me == '1':
			continue
		if me == '2':
			break

print('Program suspended!')
