from flask import render_template,request
from app import app
import pymssql
import datetime
import time

@app.route('/')
@app.route('/index')
def index():
	thisyear=datetime.datetime.now().year
	month=datetime.datetime.now().month
	yearchoices=range(2015,thisyear+1)
	#YEAR
	yvs=getYearData(thisyear-1)
	#MONTH
	m_year=''
	m_month=''
	if month>1:
		m_year=str(thisyear)
		m_month="%02d" % (month-1)
	else:
		m_year=str(thisyear-1)
		m_month='12'
	mvs=getMonthData(m_year,m_month)
	#REALTOTAL
	realvals=getRealdata()
	#FLOOR
	flrs=getFloordata()
	#COMPARE THIS MONTH WITH THE SAME MONTH LASTYEAR
	mdts=getCompareData()
	#RENDER HTML
	return render_template('index.html',title='公共机构能源消耗监管系统',yearchoices=yearchoices,year=str(thisyear),m_year=m_year,m_month=m_month,yeardatas=yvs,hpdatas=mvs,realvalue=realvals[1],monthdatas=mdts,realfloors=flrs[0],pievals=flrs[1],floornumber=len(flrs[0]),datatime=realvals[0])

@app.route('/yearquery',methods=["GET","POST"])
def yearquery():
	year=request.form['year']
	y=str(year)
	yint=int(y)
	yvs=getYearData(yint)
	return render_template('_year.html',yeardatas=yvs,year=y)

@app.route('/monthquery',methods=["GET","POST"])
def monthquery():
	year=request.form['year']
	month=request.form['month']
	mvs=getMonthData(year,month)
	return render_template('_month.html',m_year=year,m_month=month,hpdatas=mvs)

@app.route('/realdataquery',methods=["GET","POST"])
def realdataquery():
	currenttime=request.form['datatime']
	currentflrs=request.form['floornumber']
	realvals=getRealdata()
	strtime=str(realvals[0])
	flrs=getFloordata()
	if len(flrs[0])>int(currentflrs) or strtime!=currenttime:
		mdts=getCompareData()
		return render_template('_real.html',datatime=realvals[0],realvalue=realvals[1],monthdatas=mdts,realfloors=flrs[0],floornumber=len(flrs[0]),pievals=flrs[1])
	else:
		return 'NULL'

def getRealdata():
	server=app.config['MAIL_SERVER']
	user=app.config['MAIL_USERNAME']
	password=app.config['MAIL_PASSWORD']
	database=app.config['MAIL_DATABASE']
	conn=pymssql.connect(server,user,password,database)
	cursor=conn.cursor()
	realvalue=0
	cursor.execute("select top 1 datetime,sum(value) from dbLatest where LEFT(ID,1)='E' group by datetime order by datetime desc")
	row=cursor.fetchone()
	datatime=row[0]
	value1=row[1]
	strtoday=datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
	cursor.execute("select sum(value) from dbCurrent where LEFT(ID,1)='E' and datetime='"+strtoday+"' group by datetime")
	row=cursor.fetchone()
	if row:
		value0=row[0]
		realvalue=value1-value0
	conn.close()
	return [datatime,realvalue]

def getFloordata():
	server=app.config['MAIL_SERVER']
	user=app.config['MAIL_USERNAME']
	password=app.config['MAIL_PASSWORD']
	database=app.config['MAIL_DATABASE']
	conn=pymssql.connect(server,user,password,database)
	cursor=conn.cursor()
	strtoday=datetime.datetime.now().strftime('%Y-%m-%d')
	cursor.execute("select ID,value from dbcurrent where LEFT(ID,3)='E01' and datetime in (select top 1 datetime from dbcurrent where datetime<'"+strtoday+" 00:00:00' order by datetime desc) order by ID desc")
	t_prevs=[]
	row=cursor.fetchone()
	while row:
		t_prevs.append([row[0],row[1]])
		row=cursor.fetchone()
	cursor.execute("select ID,value from dbcurrent where LEFT(ID,3)='E01' and datetime in (select top 1 datetime from dbcurrent order by datetime desc) order by ID desc")
	floorvals=[]
	pievals=[]
	row=cursor.fetchone()
	while row:
		fv=0
		for item in t_prevs:
			if item[0]==row[0]:
				fv=round(row[1]-item[1],2)
				break
		if fv<0:
			fv=0
		floorvals.append([row[0][5:7]+'层',fv])
		pievals.append([row[0][5:7]+'层日常用电',fv])
		row=cursor.fetchone()
	cursor.execute("select sum(value) from dbcurrent where LEFT(ID,3)='E03' and datetime in (select top 1 datetime from dbcurrent where datetime<'"+strtoday+" 00:00:00' order by datetime desc) group by LEFT(ID,3)")
	c_prev=0
	row=cursor.fetchone()
	if row:
		c_prev=row[0]
	cursor.execute("select sum(value) from dbcurrent where LEFT(ID,3)='E03' and datetime in (select top 1 datetime from dbcurrent order by datetime desc) group by LEFT(ID,3)")
	row=cursor.fetchone()
	if row:
		pievals.append(['中央空调',round(row[0]-c_prev,2)])
	conn.close()

	return [floorvals,pievals]
	
def getCompareData():
	server=app.config['MAIL_SERVER']
	user=app.config['MAIL_USERNAME']
	password=app.config['MAIL_PASSWORD']
	database=app.config['MAIL_DATABASE']
	conn=pymssql.connect(server,user,password,database)
	cursor=conn.cursor()
	tvs=[]
	lvs=[]
	thisyear=datetime.datetime.now().year
	month=datetime.datetime.now().month
	lastyear=thisyear-1
	strmonth="%02d" % month
	cursor.execute("select ID,value from dbcurrent where LEFT(ID,1)='E' and datetime in (select top 1 datetime from dbcurrent where datetime<'"+str(thisyear)+"-"+strmonth+"-01 00:00:00' order by datetime desc)")
	m_prev=0
	row=cursor.fetchone()
	while row:
		m_prev=m_prev+row[1]
		row=cursor.fetchone()
	cursor.execute("select ID,RIGHT(convert(varchar(10),datetime,20),2) as day,max(value) as evalue from dbcurrent where LEFT(ID,1)='E' and convert(varchar(7),datetime,20)='"+str(thisyear)+"-"+strmonth+"' group by ID,RIGHT(convert(varchar(10),datetime,20),2) order by RIGHT(convert(varchar(10),datetime,20),2)")
	day=''
	temprows=[]
	sum_e=0
	row=cursor.fetchone()
	if row:
		day=row[1]
	while row:
		if day!=row[1]:
			temprows.append([day,sum_e])
			sum_e=row[2]
			day=row[1]
		else:
			sum_e=sum_e+row[2]
		row=cursor.fetchone()
	if day!='':
		temprows.append([day,sum_e])
	for item in temprows:
		val=item[1]-m_prev
		m_prev=item[1]
		if val<5000 and val>0:
			tvs.append([item[0],round(val)])
	cursor.execute("select ID,value from dbcurrent where LEFT(ID,1)='E' and datetime in (select top 1 datetime from dbcurrent where datetime<'"+str(lastyear)+"-"+strmonth+"-01 00:00:00' order by datetime desc)")
	m_prev=0
	row=cursor.fetchone()
	while row:
		m_prev=m_prev+row[1]
		row=cursor.fetchone()
	cursor.execute("select ID,RIGHT(convert(varchar(10),datetime,20),2) as day,max(value) as evalue from dbcurrent where LEFT(ID,1)='E' and convert(varchar(7),datetime,20)='"+str(lastyear)+"-"+strmonth+"' group by ID,RIGHT(convert(varchar(10),datetime,20),2) order by RIGHT(convert(varchar(10),datetime,20),2)")
	day=''
	temprows=[]
	sum_e=0
	row=cursor.fetchone()
	if row:
		day=row[1]
	while row:
		if day!=row[1]:
			temprows.append([day,sum_e])
			sum_e=row[2]
			day=row[1]
		else:
			sum_e=sum_e+row[2]
		row=cursor.fetchone()
	if day!='':
		temprows.append([day,sum_e])
	for item in temprows:
		val=item[1]-m_prev
		m_prev=item[1]
		if val<5000 and val>0:
			lvs.append([item[0],round(val)])
	mdts=[]
	index=1
	while index<32:
		strday="%02d" % index
		lv=0
		tv=0
		for item in tvs:
			if item[0]==strday:
				tv=item[1]
				break
		for item in lvs:
			if item[0]==strday:
				lv=item[1]
				break
		if lv>0 or tv>0:
			mdts.append([strday,tv,lv])
		index=index+1

	conn.close()

	return mdts

def getMonthData(year,month):
	day=getMonthDay(year,month)
	hours=[]
	days=[]
	for i in range(0,24):
		hours.append(("%02d" % i)+"时")
	for i in range(1,int(day)+1):
		daystr="%02d" % i
		days.append(daystr)
	server=app.config['MAIL_SERVER']
	user=app.config['MAIL_USERNAME']
	password=app.config['MAIL_PASSWORD']
	database=app.config['MAIL_DATABASE']
	conn=pymssql.connect(server,user,password,database)
	cursor=conn.cursor()
	cursor.execute("select ID,value from dbcurrent where LEFT(ID,1)='E' and datetime in (select top 1 datetime from dbcurrent where datetime<'"+year+"-"+month+"-01 00:00:00' order by datetime desc)")
	m_prev=0
	row=cursor.fetchone()
	while row:
		m_prev=m_prev+row[1]
		row=cursor.fetchone()
	cursor.execute("select ID,convert(varchar(13),datetime,20) as hour,max(value) as evalue from dbcurrent where datetime>='"+year+"-"+month+"-01 00:00:00' and datetime<='"+year+"-"+month+"-"+day+" 23:59:59' and LEFT(ID,1)='E' group by convert(varchar(13),datetime,20),ID order by convert(varchar(13),datetime,20)")
	hour=''
	mvs=[]
	temprows=[]
	sum_e=0
	row=cursor.fetchone()
	if row:
		hour=row[1]
	while row:
		if hour!=row[1]:
			temprows.append([hour,sum_e])
			sum_e=row[2]
			hour=row[1]
		else:
			sum_e=sum_e+row[2]
		row=cursor.fetchone()
	if hour!='':
		temprows.append([hour,sum_e])
	for item in temprows:
		val=item[1]-m_prev
		m_prev=item[1]
		if val<150 and val>0:
			mv=[str(item[0])[8:10],str(item[0])[11:13],round(val)]
			mvs.append(mv)
	conn.close()
	return [hours,days,mvs]

def getMonthDay(year,month):
	mon31={'01','03','05','07','08','10','12'}
	mon30={'04','06','09','11'}
	if month in mon31:
		return '31'
	elif month in mon30:
		return '30'
	else:
		if int(year)/4==0:
			return '29'
		else:
			return '28'

def getYearData(year):
	server=app.config['MAIL_SERVER']
	user=app.config['MAIL_USERNAME']
	password=app.config['MAIL_PASSWORD']
	database=app.config['MAIL_DATABASE']
	conn=pymssql.connect(server,user,password,database)
	cursor=conn.cursor()
	cursor.execute("select LEFT(ID,3),sum(value) from dbcurrent where datetime in (select top 1 datetime from dbcurrent where datetime<'"+str(year)+"-01-01 00:00:00' order by datetime desc) and LEFT(ID,1)='E' group by datetime,LEFT(ID,3)")
	row=cursor.fetchone()
	prev01=0
	prev03=0
	while row:
		if row[0]=='E01':
			prev01=row[1]
		if row[0]=='E03':
			prev03=row[1]
		row=cursor.fetchone()
	cursor.execute("select ID,convert(varchar(10),datetime,20) as day,max(value) as evalue from dbcurrent where datetime>='"+str(year)+"-01-01 00:00:00' and datetime<'"+str(year+1)+"-01-01 00:00:00' and LEFT(ID,1)='E' group by convert(varchar(10),datetime,20),ID order by convert(varchar(10),datetime,20)")
	sum_e01=0
	sum_e03=0
	temprows=[]
	day=''
	yvs=[]
	row=cursor.fetchone()
	if row:
		day=row[1]
	while row:
		if day!=row[1]:
			temprows.append([day,sum_e01,sum_e03])
			if (row[0])[0:3]=='E01':
				sum_e01=row[2]
				sum_e03=0
			if (row[0])[0:3]=='E03':
				sum_e01=0
				sum_e03=row[2]
			day=row[1]
		else:
			if (row[0])[0:3]=='E01':
				sum_e01=sum_e01+row[2]
			if (row[0])[0:3]=='E03':
				sum_e03=sum_e03+row[2]
		row=cursor.fetchone()
	if day!='':
		temprows.append([day,sum_e01,sum_e03])
	for item in temprows:
		val01=item[1]-prev01
		val03=item[2]-prev03
		valtotal=val01+val03
		prev01=item[1]
		prev03=item[2]
		if val01<2000 and val01>0 and val03<2000 and val03>0:
			yv=[(item[0])[0:4],(item[0])[5:7],(item[0])[8:10],round(val01),round(val03),round(valtotal)]
			yvs.append(yv)
	conn.close()
	return yvs
