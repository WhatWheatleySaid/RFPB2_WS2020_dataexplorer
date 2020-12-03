import numpy
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
with open('./data/adcs_data.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ';', quotechar = '"')
    header = next(csvreader)

    plot_data = []
    #init an empty list for each header name
    for i in range(0,len(header)):
        plot_data.append([])

    #collect data for each header
    for row in csvreader:
        for i in range(0,len(header)):
            value = row[i].replace(',','.')
            if value == '':
                value = 0
            try:
                value = float(value)
            except:
                #its a date, convert to datetime
                #format: 2020-11-28 12:38:02"
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            plot_data[i].append(value)

x_axis_label = 0
locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
formatter = mdates.ConciseDateFormatter(locator)
for pd, name in zip(plot_data, header):
    fig = plt.figure(figsize = (8,4))
    ax = fig.add_subplot(111)
    if type(pd[0]) == type(datetime.time):
        ydate = True
    else:
        ydate = False
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_title('Data of the BEESAT-4 - San Martin Base - Mission')
    ax.plot_date(plot_data[x_axis_label], pd, '-',ydate = ydate)
    ax.set_ylabel(name)
    ax.set_xlabel(header[x_axis_label])
    plt.savefig('./plots/San_Martin_Base_' + name.replace(' ', '_').replace('/', '_per_').replace(':','') + '.png')
    plt.close(fig)
