'''
Program: LBplot v2.3
Author: Hector Kroes
Released: 04/23/2020
Available in <https://github.com/HectorKroes/LBplot>
'''

##LICENSE##

License = ('''MIT License

Copyright (c) 2020 Hector Fugihara Kroes

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.''')

##REFERENCES##

References = ('''
-Lineweaver, H., & Burk, D. (1934). The Determination of Enzyme Dissociation Constants. Journal of the American Chemical Society, 56(3), 658–666. doi:10.1021/ja01318a036

-Michaelis, L., and Menten, M. L. (1913) Die Kinetik der Invertinwirkung. Biochem. Z. 49, 333–369

-Evans, M.; Hastings, N.; and Peacock, B. Statistical Distributions, 3rd ed. New York: Wiley, p. 12-14, 2000.

-Weisstein, Eric W. "Hypothesis Testing." From MathWorld--A Wolfram Web Resource. https://mathworld.wolfram.com/HypothesisTesting.html 

-Weisstein, Eric W. "Standard Error." From MathWorld--A Wolfram Web Resource. https://mathworld.wolfram.com/StandardError.html 

-Weisstein, Eric W. "Correlation Coefficient." From MathWorld--A Wolfram Web Resource. https://mathworld.wolfram.com/CorrelationCoefficient.html ''')

##IMPORTS##

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import numpy as np
import time
import math
import copy
import os

##FUNCTIONS##

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    print('LBplot - Lineweaver-Burk linear graph plotter for Michaelis-Menten enzime kinetics\n')

def menu():
	print ('''\nWould you like to return to the main menu?
	1-Yes, return to main menu
	2-No, end program''')

def sep():
	print('----------------------------------------------------------')

def format(a, j):
	c = []
	for b in a:
		c.append(j.format(float(b)))
	return c

def pdftable(df):
	print('\nHow should the pdf file be called?')
	fileDST = input()
	fig, ax =plt.subplots(figsize=(12,4))
	ax.axis('tight')
	ax.axis('off')
	the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
	pp = PdfPages(fileDST.replace('.pdf', '')+'.pdf')
	pp.savefig(fig, bbox_inches='tight')
	pp.close()
	print(('\n'+fileDST.replace('.pdf', '')+'.pdf')+ ' created successfully!')
	time.sleep(2)

def exceltable(df):
	print('\nHow should the excel file be called?')
	fileDST = input()
	df.to_excel ((fileDST.replace('.xlsx', '')+'.xlsx'), index = False, header=True)
	print('\n'+fileDST.replace('.xlsx', '')+'.xlsx'+ ' created successfully!')
	time.sleep(3)

def opt():
	print('''\nWould you like to
	1-Save as PDF
	2-Export to Excel
	3-Return to data hub''')

def savefig(ext):
	print('\nHow should the pdf file be called?')
	namt = ((input().replace(ext, ''))+ext)
	plt.savefig(namt)
	print('\n'+namt+' created successfully!')
	time.sleep(3)

def myfunc(x):
	return slope * x + intercept

def erro(x, z):
	a = []
	xm = sum(x)/len(x)
	for r in range(0,len(x)):
		at = ((x[r]-xm)**2)
		a.append(at)
	atot = (sum(a)/(len(x)-z))
	return atot

##PROGRAM##

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

		x = copy.copy(oS)
		y = copy.copy(oV0)

		xx = copy.copy(x)
		yy = copy.copy(y)

		slope, intercept, rv, pv, std_err = stats.linregress(x, y)

		errorg2 = erro(x, 0)
		errorg = (math.sqrt(errorg2))
		errors2 = erro(x, 1)
		errors = (math.sqrt(errors2))

		x.append(0)
		x.append(1.1*(float(max(x))))

		mymodel = list(map(myfunc, x))

		title = 'Lineweaver-Burk double reciprocal plot'

		sm = 'start'
		while sm == 'start':
			cls()
			print('                        DATA SET')
			sep()
			print('|   |     V0     |    1/V0    |     [S]     |    1/[S]   |')
			sep()
			for a in range(0,len(tmpV0)):
				print('| '+str(a+1)+' |  '+str("{:.2e}".format(float(tmpV0[a])))+'  |  '+str("{:.2e}".format(float(oV0[a])))+'  |  '+str("{:.2e}".format(float(tmpS[a])))+'   |  '+str("{:.2e}".format(float(oS[a])))+'  |')
			sep()
			print('\n                       KM AND VMAX')
			sep()
			print('| Michaelis constant (Km)                 '+str("{:.5e}".format(slope/intercept))+'    |\n| Maximum Reaction Rate (Vmax)            '+str("{:.5e}".format(1/intercept))+'    |\n| Slope (Km/Vmax)                         '+str("{:.5e}".format(slope)) +'    |')
			sep()
			print('\n                    LINEAR REGRESSION')
			sep()
			print('| Correlation Coefficient (R)             '+str("{:.5e}".format(rv))+'    |\n| Coefficient of Determination (R^2)      '+str("{:.5e}".format(rv**2))+'    |\n| Standard error                          '+str("{:.5e}".format(std_err))+'    |\n| P-Value                                 '+str("{:.5e}".format(pv))+'    |')
			sep()
			print('\n                 VARIANCES AND DEVIATIONS')
			sep()
			print('| Population Variance (σ^2)               '+str("{:.5e}".format(errorg2))+'    |\n| Population Standard Deviation (σ)       '+str("{:.5e}".format(errorg)) +'    |\n| Sample Variance (S^2)                   '+str("{:.5e}".format(errors2))+'    |\n| Sample Standard Deviation (S)           '+str("{:.5e}".format(errors)) +'    |')
			sep()

			print ('''\nOPTIONS
	1-Open/Save Graph
	2-Save/Export data set table
	3-Save/Export Km and Vmax table
	4-Save/Export linear regression table
	5-Save/Export variances and deviations table
	6-Return to main menu
	7-End program''')
			me = input()
			if me == '1':
				cls()
				if title == 'Lineweaver-Burk double reciprocal plot':
					print('What will the graph title be?')
					title = input()
					cls()
				print(title.upper())
				print('''\nWould you like to
	1-Display plot
	2-Save as PDF
	3-Save as PNG
	4-Save as JPG
	5-Return to data hub''')
				mza = input()
				plt.plot(x, mymodel, '-r')
				plt.plot([xx], [yy], 'bo')
				plt.xlim(0,)
				plt.ylim(0,)
				plt.suptitle(title)
				plt.xlabel('1/[S] '+'(1/'+v+')', color='#298A08')
				if len(uV) == 1:
					plt.ylabel('1/V0 '+'(1/'+u+')', color='##B40404')
				elif len(uV) == 2:
					plt.ylabel('1/V0 '+'('+str(uV[1])+'/'+str(uV[0])+')', color='#B40404')
				plt.grid()
				if mza == '1':
					plt.show()
					plt.clf()
					time.sleep(1)
				elif mza == '2':
					savefig('.pdf')
				elif mza == '3':
					savefig('.png')
				elif mza == '4':
					savefig('.jpg')

			elif me == '2':
				cls()
				plt.clf()
				print('DATA SET')
				opt()
				cap=[]
				V0j = format(tmpV0, "{:.2e}")
				oV0j = format(oV0, "{:.2e}")
				Sj = format(tmpS, "{:.2e}")
				oSj = format(oS, "{:.2e}")
				for bap in range(0, len(tmpV0)):
					cap.append(str(bap+1))
				data = {'':  cap,
        		'V0': V0j,
        		'1/V0': oV0j,
        		'[S]': Sj,
        		'1/[S]': oSj 
        		}
				df = pd.DataFrame (data, columns = ['','V0','1/V0','[S]','1/[S]'])
				dst = input()
				if dst == '1':
					pdftable(df)
				elif dst == '2':
					exceltable(df)

			elif me == '3':
				cls()
				plt.clf()
				print('KM AND VMAX')
				opt()
				data = {
        		'Variables': ['Michaelis constant (Km)', 'Maximum Reaction Rate (Vmax)', 'Slope (Km/Vmax)'],
        		'Values': [("{:.5e}".format(slope/intercept)), ("{:.5e}".format(1/intercept)), ("{:.5e}".format(slope))]
        		}
				df = pd.DataFrame (data, columns = ['Variables', 'Values'])
				dst = input()
				if dst == '1':
					pdftable(df)
				elif dst == '2':
					exceltable(df)

			elif me == '4':
				cls()
				plt.clf()
				print('LINEAR REGRESSION')
				opt()
				data = {
        		'Variables': ['Correlation Coefficient (R)', 'Coefficient of Determination (R^2)', 'Standard error', 'P-Value'],
        		'Values': [("{:.5e}".format(rv)), ("{:.5e}".format(rv**2)), ("{:.5e}".format(std_err)), ("{:.5e}".format(pv))]
        		}
				df = pd.DataFrame (data, columns = ['Variables', 'Values'])
				dst = input()
				if dst == '1':
					pdftable(df)
				elif dst == '2':
					exceltable(df)

			elif me == '5':
				cls()
				plt.clf()
				print('VARIANCES AND DEVIATIONS')
				opt()
				data = {
        		'Variables': ['Population Variance (σ^2)', 'Population Standard Deviation (σ)', 'Sample Variance (S^2)', 'Sample Standard Deviation (S)'],
        		'Values': [str("{:.5e}".format(errorg2)), ("{:.5e}".format(errorg)), ("{:.5e}".format(errors2)), ("{:.5e}".format(errors))]
        		}
				df = pd.DataFrame (data, columns = ['Variables', 'Values'])
				dst = input()
				if dst == '1':
					pdftable(df)
				elif dst == '2':
					exceltable(df)

			elif me == '6':
				sm = 'end'
				continue

			elif me == '7':
				st = 'end'
				break

	if ii=='2':
		cls()
		print('REFERENCES')
		print(References)
		menu()
		me = input()
		if me == '1':
			continue
		if me == '2':
			break

	if ii=='3':
		cls()
		print(License)
		ma = '0'
		while ma!='1':
			print('\nInput 1 to continue:')
			ma = input()
		cls()
		print('''Note: If you find some error or have some improvement suggestion, it would be very nice of you to send it on the GitHub repository or email me at hector.kroes@outlook.com

Thank you!''')
		menu()
		me = input()
		if me == '1':
			continue
		if me == '2':
			break

print('\nProgram suspended!')
