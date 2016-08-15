import os
import time
from datetime import datetime
import sqlite3

startDate=""
endDate=""
Continue=""
listfile = []
rootFolder = './data/'

conn = sqlite3.connect('/home/rio/gsirs.db')
conn.text_factory = str
cursor = conn.cursor()

def valid_date(datestring):
    try:
        datetime.strptime(datestring, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def scanFiles():
	global listfile
	global rootFolder
	print "["+time.strftime("%Y-%m-%d %H:%M:%S")+"] Scanning ./data/ folder and populating selected files"
	for subdir, dirs, files in os.walk(rootFolder):
		for file in files:
			prop = file.split('-')
			tanggal = prop[2][:4]+"-"+prop[2][4:6]+"-"+prop[2][6:]
			if startDate <= datetime.strptime(tanggal, '%Y-%m-%d') <= endDate :
				listfile.append({"url":rootFolder+file,"date":tanggal})

while True:
	startDate = raw_input('Enter start date (YYYY-MM-DD): ')
	if valid_date(startDate):
		startDate = datetime.strptime(startDate, '%Y-%m-%d')
		break
	else:
		print "Your input "+startDate+" does not match format '%Y-%m-%d'"

while True:
	endDate = raw_input('Enter end date (YYYY-MM-DD): ')
	if valid_date(endDate):
		endDate = datetime.strptime(endDate, '%Y-%m-%d')
		break
	else:
		print "Your input "+endDate+" does not match format '%Y-%m-%d'"

if startDate > endDate:
	temp = startDate
	startDate = endDate
	endDate = temp

if (endDate-startDate).days > 6 :
	print "The days between "+startDate.strftime('%Y-%m-%d')+" and "+endDate.strftime('%Y-%m-%d')+" are more than a week"
	while True:
		Continue = raw_input('Do you want to continue?: ')
		if(Continue.lower() == 'y' or Continue.lower() == 'yes'):
			Continue = True
			break
		elif(Continue.lower() == 'n' or Continue.lower() == 'no'):
			Continue = False
			break
else:
	Continue = True

if Continue:
	scanFiles()
	for file in listfile:
		oFile = open(file['url'],"r")
		print "["+time.strftime("%Y-%m-%d %H:%M:%S")+"] Reading file "+file['url']
		data ={}
		for line in oFile:
			splt = line[:len(line)-1].split('\t')
			asn = splt[2].strip().split('_')
			for AS in asn:
				if ',' not in AS:
					if AS not in data:
						data[AS] = {}
						for i in range (8,33):
							data[AS][str(i)]=0
					data[AS][splt[1].strip()]+=1
		oFile.close()
		print "["+time.strftime("%Y-%m-%d %H:%M:%S")+"] Writing data from date "+file['date']+" files into output files"
		for item in data:
			cursor.execute(
				'INSERT INTO `RV-SUMMARY` VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(
					item,
					file['date'],
					data[item]['8'],
					data[item]['9'],
					data[item]['10'],
					data[item]['11'],
					data[item]['12'],
					data[item]['13'],
					data[item]['14'],
					data[item]['15'],
					data[item]['16'],
					data[item]['17'],
					data[item]['18'],
					data[item]['19'],
					data[item]['20'],
					data[item]['21'],
					data[item]['22'],
					data[item]['23'],
					data[item]['24'],
					data[item]['25'],
					data[item]['26'],
					data[item]['27'],
					data[item]['28'],
					data[item]['29'],
					data[item]['30'],
					data[item]['31'],
					data[item]['32']
				)
			)
		conn.commit()
conn.close()
