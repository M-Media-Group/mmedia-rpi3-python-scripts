from . import generateReport
from ..memail import memail
from datetime import date

congrats_thresholds = [10000, 7000, 5000, 3500, 2500, 1000, 500, 300]
congrats_nahh = []
follower_count = int(generateReport.dates_dict[generateReport.last_day][0])

def main():
	global congrats_nahh
	# Open InstaPy log
	with open('sentCongrats.txt', 'r+') as file:
		# Iterate over the rows of the log
		for row in file:
			# Split the row columns (space delimited)
			a, b = row.split()
			congrats_nahh = [int(b)]

def congratulate():
	f=open("sentCongrats.txt", "a+")
	today = str(date.today())
	print(congrats_nahh)

	for congrats in congrats_thresholds:
		if congrats not in congrats_nahh and (congrats <= follower_count <= congrats+200):
			print("Congratulations on "+str("{:,}".format(congrats))+" followers!")
			f.write(today+" "+str(congrats)+'\n')
			break
main()
congratulate()