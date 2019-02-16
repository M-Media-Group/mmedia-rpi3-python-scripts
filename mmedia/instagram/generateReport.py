from datetime import datetime
import xlsxwriter
from .. import config
from ..memail import memail

# Create a dictionary that will house the collected data
dates_dict = dict()

# Set the date format used by InstaPy logs
date_format = "%Y-%m-%d"

# Set up the global variables
start_date = None
last_day = None
end_date = None
run_days = None
best_date = None
worst_date = None
gain_followers = None
gain_following = None
expenditure = None

# Create the dictionary dates and add the followers to the dictionary
def addFollowers():

	# Set global here so we can overwrite the global vars
	global start_date, last_day, end_date, run_days, expenditure

	# Open InstaPy log
	with open('followerNum.txt', 'r') as file:
		# Iterate over the rows of the log
		for row in file:
			# Split the row columns (space delimited)
			a, b, c = row.split()
			dates_dict[a] = [c]

	# Set other calculated vars
	start_date = datetime.strptime(sorted(dates_dict)[0], date_format)
	last_day = sorted(dates_dict)[-1]
	end_date = datetime.strptime(last_day, date_format)
	run_days = (end_date - start_date)
	expenditure = diff_month(end_date, start_date)*15;

# Add the following to the dictionary by date
def addFollowing():
	with open('followingNum.txt', 'r') as file:
		for row in file:
			a, b, c = row.split()
			if len(dates_dict[a]) > 1:
				# If the record exists, skip (sometimes InstaPy makes two logs on the same day, will skip the second one)
				continue
			elif a in dates_dict:
				# append the new number to the existing array at this slot
				dates_dict[a].append(c)
			else:
				# create a new array in this slot
				dates_dict[a] = [c]

# Calculate and add the change in followers to the dictionary by date
def calculateChangeInFollowers():
	global best_date, worst_date, gain_followers
	previous = None
	for row in sorted(dates_dict):
		# Can't subtract the 1st entry from nothing, so put 0 instead
		if previous == None:
			dates_dict[row].append(0)
		else:
			dates_dict[row].append(int(dates_dict[row][0]) - previous)
		previous = int(dates_dict[row][0])

	# Set other calculated vars
	best_date = max(dates_dict.keys(), key=(lambda key: dates_dict[key][2]));
	worst_date = min(dates_dict.keys(), key=(lambda key: dates_dict[key][2]));
	gain_followers = sum(dates_dict[row][2] for row in dates_dict);

# Calculate and add the change in following to the dictionary by date
def calculateChangeInFollowing():
	global gain_following
	previous = None
	for row in sorted(dates_dict):
		if previous == None:
			dates_dict[row].append(0)
		else:
			dates_dict[row].append(int(dates_dict[row][1]) - previous)
		previous = int(dates_dict[row][1])
	gain_following = sum(dates_dict[row][3] for row in dates_dict);

def diff_month(d1, d2):
	return (d1.year - d2.year) * 12 + d1.month - d2.month

# Create and add the data to an Excel workbook
def addToExcel():
	workbook = xlsxwriter.Workbook('InstagramStats.xlsx')

	excel_date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})

	workbook.set_properties({
	'title':    'Instagram Stats',
	'subject':  'Your Instagram stats from the Instagram Bot Management Service',
	'author':   'M Media',
	'manager':  'Mr. Michal Wargan',
	'company':  'M Media',
	'category': 'Instagram data',
	'keywords': 'Instagram, Data, Stats',
	'created':  datetime.strptime(sorted(dates_dict)[-1], date_format),
	'comments': 'Automatically created.'})

	worksheet = workbook.add_worksheet('Data')

	worksheet.set_header('M Media Instagram Bot Management Service Data')
	worksheet.set_footer('&CPage &P of &N')

	erow = 0
	col = 0
	worksheet.write(erow, col,     "Date")
	worksheet.write(erow, col + 1, "Followers")
	worksheet.write(erow, col + 2, "Following")
	worksheet.write(erow, col + 3, "Change in followers")
	worksheet.write(erow, col + 4, "Change in following")
	worksheet.write(erow, col + 5, "Following to follower ratio")
	worksheet.write(erow, col + 6, "Change in following to follower ratio")

	erow += 1

	# Iterate over the data and write it out row by row.
	for row in sorted(dates_dict):
		worksheet.write_datetime(erow, col, datetime.strptime(row, date_format), excel_date_format)
		worksheet.write(erow, col + 1, int(dates_dict[row][0]))
		worksheet.write(erow, col + 2, int(dates_dict[row][1]))
		worksheet.write(erow, col + 3, int(dates_dict[row][2]))
		worksheet.write(erow, col + 4, int(dates_dict[row][3]))
		worksheet.write_formula(erow, col + 5, '=C'+str(erow+1)+'/B'+str(erow+1))
		if erow > 1:
			worksheet.write_formula(erow, col + 6, '=F'+str(erow+1)+'-F'+str(erow))
		else:
			worksheet.write(erow, col + 6, 0)
		erow += 1

	worksheet.write_formula(erow, col + 3, '=sum(D2:D'+str(erow)+')')
	worksheet.write_formula(erow, col + 4, '=sum(E2:E'+str(erow)+')')
	worksheet.write_formula(erow, col + 5, '=average(F2:F'+str(erow)+')')
	worksheet.write_formula(erow, col + 6, '=sum(G2:G'+str(erow)+')')

	# Add table, but ovverides column names already set above :( <-- to be fixed
	# worksheet.add_table(0, 0, erow, col + 6, {'first_column': True})

	worksheet.conditional_format('D2:D'+str(len(dates_dict)+1), {'type': '3_color_scale'})
	worksheet.conditional_format('E2:E'+str(len(dates_dict)+1), {'type': '3_color_scale'})
	worksheet.conditional_format('G2:G'+str(len(dates_dict)+1), {'type': '3_color_scale', 'max_color': '#F8696B', 'min_color': '#63BE7B'})
	worksheet.conditional_format('G2:G'+str(len(dates_dict)+1), {'type': 'icon_set',
							  'icon_style': '3_arrows',
							  'icons': [{'criteria': '>', 'type': 'number', 'value': 0},
							   {'criteria': '=',  'type': 'number', 'value': 0},
							   {'criteria': '<', 'type': 'number',    'value': 0}],
							  'reverse_icons': True})

	#First chart
	chart = workbook.add_chart({'type': 'line'})
	chart.add_series({
		'name': '=Data!B1',
		'categories': '=Data!$A$2:$A$'+str(len(dates_dict)+1),
		'values':     '=Data!$B$2:$B$'+str(len(dates_dict)+1),
		'line':       {'color': 'blue'},
		'trendline': {
			'type': 'linear',
			'forward': 7,
			'display_r_squared': True,
		}
	})
	chart.add_series({
		'name': '=Data!C1', 'values': '=Data!$C$2:$C$'+str(len(dates_dict)+1),
		'trendline': {
			'type': 'linear',
			'forward': 7,
			'display_r_squared': True,
		}
	 })
	chart.set_title({'name': 'Followers and following over time'})
	chart.set_x_axis({
		'name': 'Date',
		'date_axis':  True,
		'num_format': 'yyyy-mm-dd',
	})
	chart.set_y_axis({'name': 'People'})

	chartsheet = workbook.add_chartsheet('Activity over time')
	chartsheet.set_chart(chart)

	#Second chart
	chart2 = workbook.add_chart({'type': 'line'})
	chart2.add_series({
		'name': '=Data!D1',
		'categories': '=Data!$A$2:$A$'+str(len(dates_dict)+1),
		'values':     '=Data!$D$2:$D$'+str(len(dates_dict)+1),
		'line':       {'color': 'blue'},
	})
	chart2.add_series({'name': '=Data!E1', 'values': '=Data!$E$2:$E$'+str(len(dates_dict)+1)})
	chart2.set_title({'name': 'Followers and following change over time'})
	chart2.set_x_axis({
		'name': 'Date',
		'date_axis':  True,
		'num_format': 'yyyy-mm-dd',
	})
	chart2.set_y_axis({'name': 'People'})

	chartsheet2 = workbook.add_chartsheet('Change over time')
	chartsheet2.set_chart(chart2)

	#third chart
	chart3 = workbook.add_chart({'type': 'line'})
	chart3.add_series({
		'name': '=Data!D1',
		'categories': '=Data!$A$2:$A$'+str(len(dates_dict)+1),
		'values':     '=Data!$F$2:$F$'+str(len(dates_dict)+1),
		'line':       {'color': 'blue'},
	})
	chart3.set_title({'name': 'Following to followers ratio over time'})
	chart3.set_x_axis({
		'name': 'Date',
		'date_axis':  True,
		'num_format': 'yyyy-mm-dd',
	})
	chart3.set_y_axis({'name': 'People you follow for every follower you have'})

	chartsheet3 = workbook.add_chartsheet('Ratio over time')
	chartsheet3.set_chart(chart3)

	workbook.close()
	print("Excel sheet created \n")

# Send the email and attachment
def sendEmail():
	subject = "Your Instagram Analytics Data"
	body = "Hi!\n\nIt's your Instagram Bot checking in! I've got the newest data from your Instagram account for you right here.\n\n-------"

	body += '\n\n'
	body += "Followed by " + dates_dict[last_day][0] + " people.\n"
	body += "Following " + dates_dict[last_day][1] + " people."

	body += '\n\n'
	body += "Best day was " + best_date + " with " + str(dates_dict[best_date][2]) + " new followers."

	body += '\n\n'
	body += "Net gain is " + str(gain_followers) + " new followers over "+ str(run_days.days) + " days.\n\n"
	body += "Average recorded gain per log period is " + str(gain_followers/len(dates_dict)) + " new followers. A log period is the time difference between two times I have checked your Instagram stats.\n\n"
	body += "Average calculated gain per day is " + str(gain_followers/run_days.days) + " new followers.\n\n"

	body += '\n\n'
	body += "Net new followed accounts is " + str(gain_following) + " over "+ str(run_days.days) + " days.\n\n"
	body += "Average new followed accounts per log period is " + str(gain_following/len(dates_dict)) + ".\n\n"
	body += "Average new followed accounts per day is " + str(gain_following/run_days.days) + ".\n\n"

	body += '\n\n'
	body += "Net gain ratio of following to follower is " + str(gain_following/gain_followers) + ". In general, the lower the ratio, the better perception other users have over the legitemacy of your account.\n\n"

	body += '-------\n\n'
	body += "I've created an Excel Workbook for you with more details. It's attached in this email!"

	filename = "InstagramStats.xlsx"
	return memail.sendEmail(subject, body, config.settings['client']['email'], filename)

# Print the data to console
def printData():
	print('\n')
	print("Currently followed by " + dates_dict[last_day][0])
	print("Currently following " + dates_dict[last_day][1])

	print('\n')
	print("Best day is " + best_date + " with " + str(dates_dict[best_date][2]) + " new followers")
	print("Worst day is " + worst_date + " with " + str(dates_dict[worst_date][2]) + " new followers")

	print('\n')
	print("The net gain is " + str(gain_followers) + " new followers over "+ str(run_days.days) + " days")
	print("The average recorded gain per log period is " + str(gain_followers/len(dates_dict)) + " new followers")
	print("The average calculated gain per day is " + str(gain_followers/run_days.days) + " new followers")

	print('\n')
	print("The net new followed accounts is " + str(gain_following) + " over "+ str(run_days.days) + " days")
	print("The recorded average new followed accounts per log period rate is " + str(gain_following/len(dates_dict)))
	print("The calculated average new followed accounts per day is " + str(gain_following/run_days.days))

	print('\n')
	print("The net gain ratio of following to follower is " + str(gain_following/gain_followers))

	print('\n')
	print("This clients expenditure is estimated at "+ str(expenditure) + " EUR over "+str(diff_month(end_date, start_date)) + " months")
	print("This client spends on average "+ str(expenditure/gain_followers) + " EUR per new follower")

	print('\n')

# Start the functions
addFollowers()
addFollowing()
calculateChangeInFollowers()
calculateChangeInFollowing()
addToExcel()
printData()
