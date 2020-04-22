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

def sep():
	print('----------------------------------------------------------')

st='start'
while st == 'start':
	V0 = []
	S = []
	oV0 = []
	oS = []
	cls()
	print('''What would you like to access?
	1-Execute program
	2-References
	3-Licence
	4-End program''')
	ii = input()
	if ii == '4':
		break
	elif ii == '1':
		cls()
		print('''Would you like to insert values of V0 and [S] or 1/V0 and 1/[S]?
	1- V0 and [S]
	2- 1/V0 and 1/[S]''')
		k = input()
		print('''\nWhich are the the unities your data use?
V0:''')
		u = input()
		uV = u.split('/')
		print('[S]:')
		v = input()
		print('''\nWhat input format do you prefer?
	1- Separated by commas (x, y, z, h, i, j)
	2- Individually (x)''')
		h = input()
		if k == '0':
			continue
		if k == '1':
			if h == '1':
				print('\nInsert V0 values:')
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
				print('\nHow many values would you like to insert?')
				l = int(input())
				n=0
				while n < l:
					if n == 0:
						print('\nInsert V0 values:')
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
			n = 0
			if h == '2':
				print('How many values would you like to insert?')
				l = int(input())
				while n < l:
					if n == 0:
						print('Insert 1/V0 values:')
						print('1/V0'+str(n+1)+':')
						oV0.append(float(input()))
						n += 1
					else:
						print('1/V0'+str(n+1)+':')
						oV0.append(float(input()))
						n += 1
				m = 0
				while m < l:
					if m == 0:
						print('Insert 1/[S] values:')
						print('1/[S]'+str(m+1)+':')
						oS.append(float(input()))
						m += 1
					else:
						print('1/[S]'+str(m+1)+':')
						oS.append(float(input()))
						m += 1

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
		y = oV0

		plt.scatter(x, y)

		slope, intercept, rv, pv, std_err = stats.linregress(x, y)

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
		if len(uV) == 1:
			plt.ylabel('1/V0 '+'(1/'+u+')', color='#01DFD7')
		elif len(uV) == 2:
			plt.ylabel('1/V0 '+'('+str(uV[1])+'/'+str(uV[0])+')', color='#01DFD7')
		plt.legend()
		plt.grid()
		cls()
		print('                        DATA SET\n')
		sep()
		print('|   |     V0     |    1/V0    |     [S]     |    1/[S]   |')
		sep()
		for a in range(0,len(tmpV0)):
			print('| '+str(a+1)+' |  '+str("{:.2e}".format(float(tmpV0[a])))+'  |  '+str("{:.2e}".format(float(oV0[a])))+'  |  '+str("{:.2e}".format(float(tmpS[a])))+'   |  '+str("{:.2e}".format(float(oS[a])))+'  |')
		sep()
		print('\n                       KM AND VMAX\n')
		sep()
		print('| Michaelis constant (Km)                 '+str("{:.5e}".format(slope/intercept))+'    |\n| Maximum Reaction Rate (Vmax)            '+str("{:.5e}".format(1/intercept))+'    |\n| Slope (Km/Vmax)                         '+str("{:.5e}".format(slope)) +'    |')
		sep()
		print('\n                    LINEAR REGRESSION\n')
		sep()
		print('| Correlation Coefficient (R)             '+str("{:.5e}".format(rv))+'    |\n| Coefficient of Determination (R^2)      '+str("{:.5e}".format(rv**2))+'    |\n| Standard error                          '+str("{:.5e}".format(std_err))+'    |\n| P-Value                                 '+str("{:.5e}".format(pv))+'    |')
		sep()
		print('\n                 VARIANCES AND DEVIATIONS\n')
		sep()
		print('| Population Variance (σ^2)               '+str("{:.5e}".format(errorg2))+'    |\n| Population Standard Deviation (σ)       '+str("{:.5e}".format(errorg)) +'    |\n| Sample Variance (S^2)                   '+str("{:.5e}".format(errors2))+'    |\n| Sample Standard Deviation (S)           '+str("{:.5e}".format(errors)) +'    |')
		sep()
		plt.show()

		print ('''\nWould you like to return to the main menu?
		1-Yes, return to main menu
		2-No, reopen graph
		3-No, end program''')
		sm = 'start'
		while sm == 'start':
			me = input()
			if me == '1':
				sm = 'end'
				continue
			elif me == '2':
				plt.plot(x, mymodel, '-r')
				plt.plot([(0-int(intercept/slope))], [0],'co', label= 'Vmax = '+str((1/intercept)))
				plt.plot([0], [intercept],'go', label = 'Km = '+str((slope/intercept)))
				plt.suptitle('Lineweaver-Burk double reciprocal plot')
				plt.xlabel('1/[S] '+'(1/'+v+')', color='#298A08')
				if len(uV) == 1:
					plt.ylabel('1/V0 '+'(1/'+u+')', color='#01DFD7')
				elif len(uV) == 2:
					plt.ylabel('1/V0 '+'('+str(uV[1])+'/'+str(uV[0])+')', color='#01DFD7')
				plt.legend()
				plt.grid()
				plt.show()
			elif me == '3':
				st = 'end'
				break

	if ii=='2':
		cls()
		print('''REFERENCES

-Lineweaver, H., & Burk, D. (1934). The Determination of Enzyme Dissociation Constants. Journal of the American Chemical Society, 56(3), 658–666. doi:10.1021/ja01318a036

-Michaelis, L., and Menten, M. L. (1913) Die Kinetik der Invertinwirkung. Biochem. Z. 49, 333–369

-Evans, M.; Hastings, N.; and Peacock, B. Statistical Distributions, 3rd ed. New York: Wiley, p. 12-14, 2000.

-Weisstein, Eric W. "Hypothesis Testing." From MathWorld--A Wolfram Web Resource. https://mathworld.wolfram.com/HypothesisTesting.html 

-Weisstein, Eric W. "Standard Error." From MathWorld--A Wolfram Web Resource. https://mathworld.wolfram.com/StandardError.html 

-Weisstein, Eric W. "Correlation Coefficient." From MathWorld--A Wolfram Web Resource. https://mathworld.wolfram.com/CorrelationCoefficient.html ''')
		menu()
		me = input()
		if me == '1':
			continue
		if me == '2':
			break

	if ii=='3':
		cls()
		print('''MIT License

Copyright (c) 2020 Hector Fugihara Kroes

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''')
		ma = '0'
		while ma!='1':
			print('\nInput 1 to continue:')
			ma = input()
		cls()
		print('''Note: It would be very kind if you could email me saying if you used this program and perhaps suggest improvements.

Contact: hector.kroes@outlook.com

Thank you!''')
		menu()
		me = input()
		if me == '1':
			continue
		if me == '2':
			break

print('\nProgram suspended!')
