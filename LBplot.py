'''
Program: LBplot v3.1
Author: Hector Kroes
Released: 06/10/2020
Available in <https://github.com/HectorKroes/LBplot>
'''

##REFERENCES##

References = ('''
-Lineweaver, H., & Burk, D. (1934). The Determination of Enzyme Dissociation Constants. Journal of the American Chemical Society, 56(3), 658–666. doi:10.1021/ja01318a036

-Michaelis, L., and Menten, M. L. (1913) Die Kinetik der Invertinwirkung. Biochem. Z. 49, 333–369

-Evans, M.; Hastings, N.; and Peacock, B. Statistical Distributions, 3rd ed. New York: Wiley, p. 12-14, 2000.

-Weisstein, Eric W. "Hypothesis Testing." From MathWorld--A Wolfram Web Resource. https://mathworld.wolfram.com/HypothesisTesting.html 

-Weisstein, Eric W. "Standard Error." From MathWorld--A Wolfram Web Resource. https://mathworld.wolfram.com/StandardError.html 

-Weisstein, Eric W. "Correlation Coefficient." From MathWorld--A Wolfram Web Resource. https://mathworld.wolfram.com/CorrelationCoefficient.html ''')

##IMPORTS##

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time, math, copy, os, sys, codecs, datetime, calendar
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import NullFormatter
import matplotlib.pyplot as plt
from datetime import datetime
import PySimpleGUI as sg
from scipy import stats
import pandas as pd
import numpy as np

##FUNCTIONS##

def erro(x, z):
	a = []
	xm = sum(x)/len(x)
	for r in range(0,len(x)):
		at = ((x[r]-xm)**2)
		a.append(at)
	atot = (sum(a)/(len(x)-z))
	return atot

def floatit(a):
	b = []
	for aa in a:
		b.append(float(aa))
	return b

def breaqui():
	global sm
	sm = 'end'
	global st
	st = 'end'

def format(a, j):
	c = []
	for b in a:
		c.append(j.format(float(b)))
	return c

def DI():
	layout1 = [  [sg.Image(os.getcwd()+os.sep+'Logo.png')],
			[sg.Text('')],
			[sg.Button('Start new project', size = (40,1))],
			[sg.Button('Load previous projects', size = (40,1))],
			[sg.Button('References', size = (40,1))],
			[sg.Button('Credits', size = (40,1))],
			[sg.Button('End program', size = (40,1))],
			[sg.Text('')]]

	global de
	de = sg.Window('LBplot', layout1, element_justification = 'center')

def pdftable(df):
	RNG3 = [[sg.Text("What should be the archive name?")],
		[sg.InputText('', size = (51,1), key= '-archnam-')],
		[sg.Text("                                             "), sg.Button('Continue', size = (20,1), key = '-namt-')]]
	dp = sg.Window('LBplot', RNG3, element_justification = 'left')
	eventp, valuep = dp.read()
	namt = ((str(valuep['-archnam-']).replace('.pdf', ''))+'.pdf')
	dp.close()
	fig, ax =plt.subplots(figsize=(12,4))
	ax.axis('tight')
	ax.axis('off')
	the_table = ax.table(cellText=df.values, colLabels=df.columns, loc= 'center')
	pp = PdfPages(arq+namt)
	pp.savefig(fig, bbox_inches='tight')
	pp.close()
	RNG4 = [[sg.Text(namt+" created successfully!")],
		[sg.Button('Continue', size = (21,1), key = '-rnm2-')]]
	dc = sg.Window('LBplot', RNG4, element_justification = 'center')
	eventc, valuec = dc.read()
	dc.close()
	plt.clf()
	plt.close()

def exceltable(df):
	RNG3 = [[sg.Text("What should be the archive name?")],
		[sg.InputText('', size = (51,1), key= '-archnam-')],
		[sg.Text("                                             "), sg.Button('Continue', size = (20,1), key = '-namt-')]]
	dp = sg.Window('LBplot', RNG3, element_justification = 'left')
	eventp, valuep = dp.read()
	namt = ((str(valuep['-archnam-']).replace('.xlsx', ''))+'.xlsx')
	dp.close()
	df.to_excel (arq+namt, index = False, header=True)
	RNG4 = [[sg.Text(namt+" created successfully!")],
		[sg.Button('Continue', size = (21,1), key = '-rnm2-')]]
	dc = sg.Window('LBplot', RNG4, element_justification = 'center')
	eventc, valuec = dc.read()
	dc.close()
	plt.clf()
	plt.close()

def savefig(ext):
	RNG1 = [[sg.Text("What should be the archive name?")],
		[sg.InputText('', size = (51,1), key= '-archnam-')],
		[sg.Text("                                             "), sg.Button('Continue', size = (20,1), key = '-namt-')]]
	dp = sg.Window('LBplot', RNG1, element_justification = 'left')
	kt = 'a'
	while kt == 'a':
		eventp, valuep = dp.read()
		if eventp == '-namt-':
			namt = ((str(valuep['-archnam-']).replace(ext, ''))+ext)
			dp.close()
			plt.savefig(arq+namt)
			RNG2 = [[sg.Text(namt+" created successfully!")],
			[sg.Button('Continue', size = (21,1), key = '-rnm2-')]]
			dc = sg.Window('LBplot', RNG2, element_justification = 'center')
			kd = 'a'
			while kd == 'a':
				eventc, valuec = dc.read()
				if eventc == '-rnm2-':
					dc.close()
					kt='b'
					kd='b'
					break
				elif event in (None, 'Exit'):
					dc.close()
					kt='b'
					kd='b'
					breaqui()
					break

def pltnow(title, xx, yy, mymodel, x, uV, v):
	plt.plot(x, mymodel, '-r')
	plt.plot([xx], [yy], 'bo')
	plt.xlim(0,)
	plt.ylim(0,)
	plt.suptitle(title)
	plt.xlabel('1/[S] '+'(1/'+v+')', color='#298A08')
	if len(uV) == 1:
		plt.ylabel('1/V0 '+'(1/'+u+')', color='#B40404')
	elif len(uV) == 2:
		plt.ylabel('1/V0 '+'('+str(uV[1])+'/'+str(uV[0])+')', color='#B40404')
	plt.grid()

def bulk():

	x = copy.copy(oS)
	y = copy.copy(oV0)

	xx = copy.copy(x)
	yy = copy.copy(y)

	slope, intercept, rv, pv, std_err = stats.linregress(x, y)

	def myfunc(x):
		return slope * x + intercept

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

		layout3 = [[sg.T('DATA SET', size=(103,1), justification='center')]]

		headings1 = [' ','V0','1/V0','[S]','1/[S]']

		leg1 = [sg.T(a, size=(20,1), background_color='white', justification='center', pad=(1,1)) for a in headings1]
		layout3.append(leg1)

		for a in range(len(oV0)):
			data1 = [ a+1, "{:.2e}".format(float(tmpV0[a])), "{:.2e}".format(float(oV0[a])), "{:.2e}".format(float(tmpS[a])), "{:.2e}".format(float(oS[a]))]
			row = [sg.T(a, size=(20,1), background_color='white', justification='center', pad=(1,1)) for a in data1]
			layout3.append(row)

		line = [sg.T('', size=(20,1), justification='center', pad=(1,1))]
		layout3.append(line)

		title2 = [sg.T('KM AND VMAX', size=(103,1), justification='center', pad=(1,1))]
		layout3.append(title2)

		headings2 =['Michaelis constant (Km)', 'Maximum Reaction Rate (Vmax)', 'Slope (Km/Vmax)']
		leg2 = [sg.T(a, size=(34,1), background_color='white', justification='center', pad=(1,1)) for a in headings2]
		layout3.append(leg2)

		data2 = ["{:.5e}".format(slope/intercept), "{:.5e}".format(1/intercept), "{:.5e}".format(slope)]
		row2 = [sg.T(a, size=(34,1), background_color='white', justification='center', pad=(1,1)) for a in data2]
		layout3.append(row2)

		line = [sg.T('', size=(15,1), justification='center', pad=(1,1))]
		layout3.append(line)

		title3 = [sg.T('LINEAR REGRESSION', size=(103,1), justification='center', pad=(1,1))]
		layout3.append(title3)

		headings3 = ['Correlation Coefficient (R)', 'Coefficient of Determination (R^2)', 'Standard error', 'P-Value']
		leg3 = [sg.T(a, size=(25,1), background_color='white', justification='center', pad=(1,1)) for a in headings3]
		layout3.append(leg3)

		data3 = ["{:.5e}".format(rv), "{:.5e}".format(rv**2), "{:.5e}".format(std_err), "{:.5e}".format(pv)]
		row3 = [sg.T(a, size=(25,1), background_color='white', justification='center', pad=(1,1)) for a in data3]
		layout3.append(row3)

		line = [sg.T('', size=(15,1), justification='center', pad=(1,1))]
		layout3.append(line)

		title4 = [sg.T('VARIANCES AND DEVIATIONS', size=(103,1), justification='center', pad=(1,1))]
		layout3.append(title4)

		headings4 = ['Population Variance (σ^2)', 'Population Standard Deviation (σ)', 'Sample Variance (S^2)', 'Sample Standard Deviation (S)']
		leg4 = [sg.T(a, size=(25,1), background_color='white', justification='center', pad=(1,1)) for a in headings4]
		layout3.append(leg4)

		data4 = ["{:.5e}".format(errorg2), "{:.5e}".format(errorg), "{:.5e}".format(errors2), "{:.5e}".format(errors)]
		row4 = [sg.T(a, size=(25,1), background_color='white', justification='center', pad=(1,1)) for a in data4]
		layout3.append(row4)

		line = [sg.T('', size=(15,1), justification='center', pad=(1,1))]
		layout3.append(line)

		GBM = ['PLOT', ['&Show plot::-SHP-', '&Rename graph::-RNG-', '&Save as pdf::-GPDF-', '&Save as png::-GPNG-', '&Save as jpg::-GJPG-']]
		DSM = ['DSM', ['&Save as pdf::SPNG', '&Export to excel::-EXTE-']]
		OPT = ['OPT', ['&Return to main menu::-RTMM-', '&End program::-ENP-']]

		scroll = [[sg.Text('Project: '+prjname), sg.Text('Date of creation: '+doc)],
				 [sg.Col(layout3, size=(846, 500), scrollable=True, vertical_scroll_only=True)], 
				 [sg.ButtonMenu('PLOT', GBM, key='-GBM-', size=(38,1)), sg.ButtonMenu('DATA SET', DSM, key='-DSM-', size=(38,1)), sg.ButtonMenu('KM AND VMAX', DSM, key='-KAV-', size=(38,1))],
				 [sg.ButtonMenu('LINEAR REGRESSION', DSM, key='-LNR-', size=(38,1)), sg.ButtonMenu('VARIANCES AND DEVIATIONS', DSM, key='-VAD-', size=(38,1)), sg.ButtonMenu('OPTIONS', OPT, key='-OPT-', size=(38,1))]]

		dg = sg.FlexForm('LBplot', scroll)
		eventg, valueg = dg.read()

		if valueg == {'-GBM-': 'Show plot::-SHP-', '-DSM-': None, '-KAV-': None, '-LNR-': None, '-VAD-': None, '-OPT-': None}:
			print('a')
			dg.close()
			plt.subplot()
			pltnow(title, xx, yy, mymodel, x, uV, v)
			plt.gca().yaxis.set_minor_formatter(NullFormatter())
			plt.subplots_adjust(top=0.90, bottom=0.10, left=0.14, right=0.95, hspace=0.25,
			                    wspace=0.35)
			fig = plt.gcf()
			figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
			def draw_figure(canvas, figure, loc=(0, 0)):
			    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
			    figure_canvas_agg.draw()
			    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
			    return figure_canvas_agg
			layout = [[sg.Canvas(size=(figure_w, figure_h), key='canvas')],
			[sg.Button('Continue', size = (21,1), key = '-grphr-')]]
			window = sg.Window('LBplot', layout, finalize=True, element_justification = 'center')
			fig_canvas_agg = draw_figure(window['canvas'].TKCanvas, fig)
			event, values = window.read()
			if event in (None, 'Exit'):
				breaqui()
				window.close()
				break
			elif event == '-grphr-':
				window.close()
				plt.clf()
				plt.close()

		elif valueg == {'-GBM-': 'Rename graph::-RNG-', '-DSM-': None, '-KAV-': None, '-LNR-': None, '-VAD-': None, '-OPT-': None}:
			dg.close()
			RNG1 = [[sg.Text("What should be the graph's title?")],
			[sg.InputText('', size = (51,1), key= '-title-')],
			[sg.Text("                                             "), sg.Button('Continue', size = (20,1), key = '-rnm1-')]]
			dh = sg.Window('LBplot', RNG1, element_justification = 'left')
			kt = 'a'
			while kt == 'a':
				eventh, valueh = dh.read()
				if eventh == '-rnm1-':
					title = str(valueh['-title-'])
					dh.close()
					RNG2 = [[sg.Text(title+" is now the graph's title!")],
					[sg.Button('Continue', size = (21,1), key = '-rnm2-')]]
					dj = sg.Window('LBplot', RNG2, element_justification = 'center')
					kd = 'a'
					while kd == 'a':
						eventj, valuej = dj.read()
						if eventj == '-rnm2-':
							dj.close()
							kt='b'
							kd='b'
							break

		elif valueg == {'-GBM-': 'Save as pdf::-GPDF-', '-DSM-': None, '-KAV-': None, '-LNR-': None, '-VAD-': None, '-OPT-': None}:
			pltnow(title, xx, yy, mymodel, x, uV, u, v)
			dg.close()
			savefig('.pdf')
			plt.clf()
			plt.close()

		elif valueg == {'-GBM-': 'Save as png::-GPNG-', '-DSM-': None, '-KAV-': None, '-LNR-': None, '-VAD-': None, '-OPT-': None}:
			pltnow(title, xx, yy, mymodel, x, uV, u, v)
			dg.close()
			savefig('.png')
			plt.clf()
			plt.close()

		elif valueg == {'-GBM-': 'Save as jpg::-GJPG-', '-DSM-': None, '-KAV-': None, '-LNR-': None, '-VAD-': None, '-OPT-': None}:
			pltnow(title, xx, yy, mymodel, x, uV, u, v)
			dg.close()
			savefig('.jpg')
			plt.clf()
			plt.close()

		elif eventg == '-DSM-':
			plt.clf()
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
			df = pd.DataFrame(data, columns = ['','V0','1/V0','[S]','1/[S]'])
			if valueg == {'-GBM-': None, '-DSM-': 'Save as pdf::SPNG', '-KAV-': None, '-LNR-': None, '-VAD-': None, '-OPT-': None}:
				dg.close()
				pdftable(df)
			elif valueg == {'-GBM-': None, '-DSM-': 'Export to excel::-EXTE-', '-KAV-': None, '-LNR-': None, '-VAD-': None, '-OPT-': None}:
				dg.close()
				exceltable(df)

		elif eventg == '-KAV-':
			plt.clf()
			data = {
			'Michaelis constant (Km)': [("{:.5e}".format(slope/intercept))],
			'Maximum Reaction Rate (Vmax)': [("{:.5e}".format(1/intercept))],
			'Slope (Km/Vmax)': [("{:.5e}".format(slope))]}
			df = pd.DataFrame (data, columns = ['Michaelis constant (Km)', 'Maximum Reaction Rate (Vmax)', 'Slope (Km/Vmax)'])
			if valueg == {'-GBM-': None, '-DSM-': None, '-KAV-': 'Save as pdf::SPNG', '-LNR-': None, '-VAD-': None, '-OPT-': None}:
				dg.close()
				pdftable(df)
			elif valueg == {'-GBM-': None, '-DSM-': None, '-KAV-': 'Export to excel::-EXTE-', '-LNR-': None, '-VAD-': None, '-OPT-': None}:
				dg.close()
				exceltable(df)

		elif eventg == '-LNR-':
			plt.clf()
			data = {
			'Correlation Coefficient (R)': [("{:.5e}".format(rv))],
			'Coefficient of Determination (R^2)': [("{:.5e}".format(rv**2))],
			'Standard error': [("{:.5e}".format(std_err))],
			'P-Value': [("{:.5e}".format(pv))]}
			df = pd.DataFrame (data, columns = ['Correlation Coefficient (R)', 'Coefficient of Determination (R^2)','Standard error', 'P-Value'])
			if valueg == {'-GBM-': None, '-DSM-': None, '-KAV-': None, '-LNR-': 'Save as pdf::SPNG', '-VAD-': None, '-OPT-': None}:
				dg.close()
				pdftable(df)
			elif valueg == {'-GBM-': None, '-DSM-': None, '-KAV-': None, '-LNR-': 'Export to excel::-EXTE-', '-VAD-': None, '-OPT-': None}:
				dg.close()
				exceltable(df)

		elif eventg == '-VAD-':
			plt.clf()
			data = {
			'Population Variance (σ^2)': [str("{:.5e}".format(errorg2))],
			'Population Standard Deviation (σ)': [("{:.5e}".format(errorg))],
			'Sample Variance (S^2)': [("{:.5e}".format(errors2))],
			'Sample Standard Deviation (S)': [("{:.5e}".format(errors))]}
			df = pd.DataFrame (data, columns = ['Population Variance (σ^2)', 'Population Standard Deviation (σ)', 'Sample Variance (S^2)', 'Sample Standard Deviation (S)'])
			if valueg == {'-GBM-': None, '-DSM-': None, '-KAV-': None, '-LNR-': None, '-VAD-': 'Save as pdf::SPNG', '-OPT-': None}:
				dg.close()
				pdftable(df)
			elif valueg == {'-GBM-': None, '-DSM-': None, '-KAV-': None, '-LNR-': None, '-VAD-': 'Export to excel::-EXTE-', '-OPT-': None}:
				dg.close()
				exceltable(df)

		elif valueg == {'-GBM-': None, '-DSM-': None, '-KAV-': None, '-LNR-': None, '-VAD-': None, '-OPT-': 'End program::-ENP-'}:
			dg.close()
			breaqui()
			break

		elif valueg == {'-GBM-': None, '-DSM-': None, '-KAV-': None, '-LNR-': None, '-VAD-': None, '-OPT-': 'Return to main menu::-RTMM-'}:
			dg.close()
			sm = 'end'
			continue

		elif eventg in (None, 'Exit'):
			breaqui()
			break

##DIRECTORIES##

cwd = os.getcwd()
arq = cwd+os.sep+'Archives'+os.sep
pro = cwd+os.sep+'Projects'+os.sep

##GUI##

sg.theme('SystemDefault')

##PROGRAM##

st='start'
me = '0'
while st == 'start': 
	prjname = ''
	if st != 'start':
		break
	if me =='7':
		break
	V0 = []
	S = []
	oV0 = []
	oS = []

	DI()
	event, values = de.Read()

	if event in (None, 'Exit'):
		break

	elif event == 'Start new project':
		de.close()
		f_layout1 = [[sg.Text('What units does your data use?')],
			[sg.Text('V0 unit:'), sg.InputText("μM/s", size = (51,1), key= '-f2-')],
			[sg.Text('[S] unit:'), sg.InputText("μM", size = (51,1), key= '-f3-')]]  

		f_layout2 = [[sg.Text('Insert your data:')],
			[sg.Text('V0:'), sg.Multiline("0.11E-9, 0.25E-9, 0.34E-9, 0.45E-9, 0.58E-9, 0.61E-9", size = (52,6), key= '-f4-')],
			[sg.Text('[S]:'), sg.Multiline("0.1E-5, 0.3E-5, 0.5E-5, 1E-5, 3E-5, 5E-5", size = (52,6), key= '-f5-')]]            

		layout2 = [[sg.Text('Project name:'), sg.InputText('', size=(47,1), key = '-f1-')],
			[sg.Frame('Units', f_layout1)],
			[sg.Frame('Data Set', f_layout2)],
			[sg.Button('Continue', size = (20,1), key = '-ff-')]]

		df = sg.Window('LBplot', layout2, element_justification = 'center')
		buttonf, valuef = df.read()
		if buttonf == '-ff-':
			prjname = str(valuef['-f1-'])
			u = str(valuef['-f2-'])
			uV = u.split('/')
			v = str(valuef['-f3-'])
			tmpV0 = (str(valuef['-f4-']).replace(' ', '').replace('\n', '')).split(',')
			tmpS = (str(valuef['-f5-']).replace(' ', '').replace('\n', '')).split(',')
			for a in tmpV0:
				oa = 1.0/float(a)
				oV0.append(oa)

			for b in tmpS:
				ob = 1.0/float(b)
				oS.append(ob)

		depo = open(pro+prjname+'.txt', 'w', encoding='utf-8')
		depo.write(prjname+'\n')
		depo.write(str(tmpV0)+'\n')
		depo.write(str(tmpS)+'\n')
		depo.write(str(oV0)+'\n')
		depo.write(str(oS)+'\n')
		depo.write(str(uV)+'\n')
		depo.write(v)
		depo.close()

		totalnow = calendar.timegm(time.gmtime())
		localnow = calendar.timegm(datetime.now().timetuple())
		doct = os.path.getmtime(pro+prjname+'.txt')
		tx = totalnow - localnow
		tz = doct - tx
		doc = datetime.utcfromtimestamp(tz).strftime('%Y-%m-%d %H:%M:%S')

		df.close()

		bulk()

	elif event == 'Load previous projects':
		de.close()
		stb = 'prj'
		while stb == 'prj':
			olinda=[]
			files = [f for f in os.listdir(pro) if os.path.isfile(pro+f)]
			for a in range(len(files)):
				olinda.append((files[a]).replace('.txt',''))

			llpp = [[sg.Text('Which project would you like to load?')],
				[sg.Listbox(values=olinda, size=(35, 10), select_mode='LISTBOX_SELECT_MODE_EXTENDED', enable_events= True)],
				[sg.Button('Return to main menu', size = (30,1), key = '-CONT-')]]

			lpp = sg.Window('LBplot', llpp, element_justification = 'center')
			eventlpp, valuelpp = lpp.read()

			if eventlpp == '-CONT-':
				lpp.close()
				stb = 'stop'
				continue

			else:
				lpp.close()

				fopt = (str(valuelpp).replace("{0: ['", '').replace("']}", '')+'.txt')
				totalnow = calendar.timegm(time.gmtime())
				localnow = calendar.timegm(datetime.now().timetuple())
				doct = os.path.getmtime(pro+fopt)
				tx = totalnow - localnow
				tz = doct - tx
				doc = datetime.utcfromtimestamp(tz).strftime('%Y-%m-%d %H:%M:%S')

				llpa = [[sg.Text(str(valuelpp).replace("{0: ['", '').replace("']}", ''))],
				[sg.Text('Date of creation: ' + doc)],
				[sg.Button('Load', size = (15,1), key = '-LOAD-'), sg.Button('Delete', size = (15,1), key = '-DEL-')]]
				lpa = sg.Window('LBplot', llpa, element_justification = 'center')
				eventlpa, valuelpa = lpa.read()

				if eventlpa == '-LOAD-':
					fop = open(pro + fopt, 'r')
					rfop = fop.readlines()
					prjname = rfop[0].replace('\n', '')
					tmpV0 = (rfop[1].replace("['", '').replace("']\n", '').split("', '"))
					tmpV0 = floatit(tmpV0)
					tmpS = (rfop[2].replace("['", '').replace("']\n", '').split("', '"))
					tmpS = floatit(tmpS)
					oV0 = (rfop[3].replace("[", '').replace("]\n", '').split(", "))
					oV0 = floatit(oV0)
					oS = (rfop[4].replace("[", '').replace("]\n", '').split(", "))
					oS = floatit(oS)
					if ',' in rfop[5]:
						uV = (rfop[5].replace("['", '').replace("']\n", '').replace('Î¼', 'μ').split("', '"))
					else:
						uV = rfop[5].replace('\n', '').replace('Î¼', 'μ')
					v = (rfop[6].replace('Î¼', 'μ'))

					stb = 'stop'
					lpa.close()

					bulk()

				elif eventlpa == '-DEL-':
					lpa.close()
					llpb = [[sg.Text('Are you sure you want to delete')],
					[sg.Text((str(valuelpp).replace("{0: ['", '').replace("']}", '')) + '?')],
					[sg.Button('Yes, delete it', size = (15,1), key = '-YES-'), sg.Button('No, keep it', size = (15,1), key = '-NO-')]]
					lpb = sg.Window('LBplot', llpb, element_justification = 'center')
					eventlpb, valuelpb = lpb.read()

					if eventlpb == '-YES-':
						arch = pro + fopt
						os.remove(arch)
						lpb.close()

					else:
						continue

	elif event == 'References':
		de.close()
		lzo = [[sg.Text('REFERENCES', justification='center')],
			[sg.Text(References+'\n')],
			[sg.Button('Return to main menu', size = (30,1))]]
		llzo = sg.Window('LBplot', lzo, element_justification = 'center')
		eventlzo, valuelzo = llzo.read()
		llzo.close()

	elif event == 'Credits':
		de.close()
		lzo = [[sg.Text('CREDITS', justification='center')],
			[sg.Text("LBplot was made by Hector Kroes and it's available for\nfree download at <https://github.com/HectorKroes/LBplot>.\nIf you find errors, problems, or have a suggestion, please\nsubmit it at the GitHub repository or send an email to\nhector.kroes@outlook.com\n\nThank you!"+'\n')],
			[sg.Button('Return to main menu', size = (30,1))]]
		llzo = sg.Window('LBplot', lzo, element_justification = 'center')
		eventlzo, valuelzo = llzo.read()
		llzo.close()

	elif event == 'End program':
		break
