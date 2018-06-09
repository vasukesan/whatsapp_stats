from datetime import datetime
import re
import collections
import matplotlib.pyplot as plt
import matplotlib
from operator import itemgetter
import numpy as np
from collections import namedtuple,OrderedDict
from matplotlib.dates import date2num
from matplotlib import rcParams

Message = namedtuple('Message', ['timestamp', 'sender', 'data'])

my_colors = ["lightslategray","mediumseagreen","mediumslateblue"]



def run():
	mpl_formatting()
	messages = {} #{name : [Message tuples]}
	read_parse("chat.txt",messages)
	generate_stats(messages)



def read_parse(filename,messages):
	#Example Whatsapp message: "11/24/15, 5:24 AM - Varun: This is a message."
	pattern = "(\d{1,2}\/\d{1,2}\/\d{2}, \d{1,2}:\d{2} (?:A|P)M - [^:]+: )(.+)"
	with open(filename,'r') as fh: 

		buff = re.match(pattern,fh.readline())
		buff = buff.group(1), buff.group(2) #seperates message metadata and the text itself
		for line in fh:

			match = re.match(pattern,line)

			if match:
				timestamp,sender = buff[0].split("-",1)
				timestamp = datetime.strptime(timestamp, '%m/%d/%y, %I:%M %p ')
				sender = sender[1:-2]
				data = buff[1]
				msg = Message(timestamp, sender, data)

				if msg.sender not in messages.keys():
					messages[msg.sender] = [msg]

				else:
					messages[msg.sender].append(msg)

				#Update buff to be the next message
				buff = match.group(1), match.group(2)

			else: #reading the file by line splits messages with newlines, this puts them back together
				buff = buff[0],buff[1]+line;

def generate_stats(messages):
	lim = 1500

	weekday_cnt = collections.OrderedDict() #{name : {(num,dayofweek) : count}}
	for sender in messages:
		weekday_cnt[sender] = collections.Counter()
		for msg in messages[sender]:
			weekday_cnt[sender][(msg.timestamp.strftime("%w"),msg.timestamp.strftime("%A"))]+=1
			# monthly_cnt[(msg.timestamp.month,msg.timestamp.strftime("%B"),msg.sender)]+=1
			# cnt_total[msg[1]+str(msg[0].weekday())]+=1
			# cnt_total.update(msg[2].split())
			# cnt_total[msg[1]+" "+str(msg[0].hour)]+=1


		weekday_cnt[sender] = sorted(weekday_cnt[sender],key=itemgetter(0,1))


	# plot_count(messages)
	mpl_formatting()
	# plot_messages_over_time(messages)
	plot_byweekday(weekday_cnt)

def mpl_formatting():
	plt.style.use('dark_background')
	# hfont = {'fontname':'Helvetica'}

	plt.grid(True)
	plt.rcParams["font.family"] = "tahoma"

	plt.rcParams.update({
	    "lines.color": my_colors[0],
	    "patch.edgecolor": my_colors[0],
	    "text.color": my_colors[0],
	    "axes.edgecolor": my_colors[0],
	    "axes.labelcolor": my_colors[0],
	    "xtick.color": my_colors[0],
	    "ytick.color": my_colors[0],
	    "grid.color": '#333333'})
	

def mpl_ax_format(ax):
	ax.xaxis.label.set_color(my_colors[0])
	ax.tick_params(axis='x', colors=my_colors[0])
	ax.yaxis.label.set_color(my_colors[0])
	ax.tick_params(axis='y', colors=my_colors[0])
	ax.grid(linewidth=.5,linestyle=(0,([1,10])))
	
def plot_test(data):
	t = np.arange(0.0, 2.0, 0.01)
	s = 1 + np.sin(2*np.pi*t)
	plt.plot(t, s)

	plt.xlabel('time (s)')
	plt.ylabel('voltage (mV)')
	plt.title('About as simple as it gets, folks')
	plt.grid(True)
	plt.savefig("test.png")
	savefig('foo.png', bbox_inches='tight')
	plt.show()

	# plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

def plot_count(data):
	labels = data.keys()
	sizes = [len(x) for x in data.values()]

	fig, ax = plt.subplots()
	p, tx, autotexts = plt.pie(sizes, labels=labels, autopct="", startangle=90,colors=my_colors[1:])

	for i, a in enumerate(autotexts):
	    a.set_text("{}".format(sizes[i]))
	    a.set_color("black")

	# for spine in ax.spines.itervalues():
	# 	spine.set_visible(False)
	plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	plt.title("total message count")
	plt.show()

def plot_messages_over_time(messages):
	names = messages.keys()
	lst = messages.itervalues().next()
	dates = [x[0] for x in lst]
	lst = messages.itervalues().next()
	dates = date2num(dates), date2num([x[0] for x in lst])

	fig,ax = plt.subplots()

	plt.title('messages over time',color=my_colors[0])

	ax.hist(dates,bins=70,histtype='barstacked', width=10, color=my_colors[1:],label=names,edgecolor='none')
	ax.legend(prop={'size': 10})
	# ax.patch.set_facecolor('lemonchiffon')
	# ax.patch.set_visible(False)
	# fig.patch.set_visible(False)
	# ax.xaxis.set_ticks([])
	# ax.yaxis.set_ticks([])
	for spine in ax.spines.itervalues():
		spine.set_visible(False)
	ax.xaxis_date()

	plt.show()

def plot_bymonth(messages):
	print np.arange(1,14)

def plot_byweekday(weekday_cnt):
	weekdays = weekday_cnt[0].keys()
	values = messages.itervalues().next()
	values = values, messages.itervalues().next()



	N = 7

	ind = np.arange(N)  # the x locations for the groups
	width = 0.35       # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, men_means, width, color='r', yerr=men_std)

	women_means = (25, 32, 34, 20, 25)
	women_std = (3, 5, 2, 3, 3)
	rects2 = ax.bar(ind + width, women_means, width, color='y', yerr=women_std)

	# add some text for labels, title and axes ticks
	# ax.set_ylabel('Scores')
	ax.set_title('messages by weekday')
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(weekdays)

	ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))


	def autolabel(rects):
	    """
	    Attach a text label above each bar displaying its height
	    """
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%d' % int(height),
	                ha='center', va='bottom')

	autolabel(rects1)
	autolabel(rects2)

	plt.show()


	# N = 5
	# menMeans = (20, 35, 30, 35, 27
	# womenMeans = (25, 32, 34, 20, 25)
	# menStd = (2, 3, 4, 1, 2)
	# womenStd = (3, 5, 2, 3, 3)
	# ind = np.arange(N)    # the x locations for the groups
	# width = 0.35       # the width of the bars: can also be len(x) sequence

	# p1 = plt.bar(ind, menMeans, width, color='#d62728', yerr=menStd)
	# p2 = plt.bar(ind, womenMeans, width,
	#              bottom=menMeans, yerr=womenStd)

	# plt.ylabel('Scores')
	# plt.title('Scores by group and gender')
	# plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
	# plt.yticks(np.arange(0, 81, 10))
	# plt.legend((p1[0], p2[0]), ('Men', 'Women'))

	# plt.show()

# 	menMeans = (20, 35, 30, 35, 27)
# 	womenMeans = (25, 32, 34, 20, 25)
# 	menStd = (2, 3, 4, 1, 2)
# 	womenStd = (3, 5, 2, 3, 3)
# 	ind = np.arange(N)    # the x locations for the groups
# 	width = 0.35       # the width of the bars: can also be len(x) sequence

# 	p1 = plt.bar(ind, menMeans, width, color='#d62728', yerr=menStd)
# 	p2 = plt.bar(ind, womenMeans, width, bottom=menMeans, yerr=womenStd)

# 	plt.ylabel('Scores')
# 	plt.title('Scores by group and gender')
# 	plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
# 	plt.yticks(np.arange(0, 81, 10))
# 	plt.legend((p1[0], p2[0]), ('Men', 'Women'))

# 	plt.show()	



run()