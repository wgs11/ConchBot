from xml.dom import minidom
from datetime import datetime, timedelta
from tkinter import *
from tkinter import filedialog, Tk
import re

def guidedSplits():
    #get split file from user
    #get goal time from user
    Tk().withdraw()
    filename = filedialog.askopenfilename(title="Select Split File", filetypes=(("Split Files","*.lss"),))
    print(filename)
    gt = input("Enter Your Goal Time (Format HH:MM:SS Only): ")
    while not re.match(r"\d{2}:\d{2}:\d{2}",gt):
        gt = input("Please enter a valid Time (HH:MM:SS): ")

    gt_strptime = datetime.strptime(gt, "%H:%M:%S")
    goal = timedelta(hours=gt_strptime.hour,minutes=gt_strptime.minute,seconds=gt_strptime.second, microseconds=0).total_seconds()
    splits = minidom.parse(filename)
    segments = splits.getElementsByTagName("Segment")
    averagesList = {}
    pbList = {}
    for segment in segments:
        timeList = []

        name = segment.getElementsByTagName("Name")
        splitName = name[0].firstChild.nodeValue
        sh = segment.getElementsByTagName("SegmentHistory")
        times = sh[0].getElementsByTagName("Time")
        pb = segment.getElementsByTagName("BestSegmentTime")
        pbt = pb[0].getElementsByTagName("RealTime")
        segment_best_string = pbt[0].firstChild.nodeValue
        segment_best_strptime = datetime.strptime(segment_best_string[:12], "%H:%M:%S.%f")
        segment_best_delta = timedelta(hours=segment_best_strptime.hour, minutes=segment_best_strptime.minute, seconds=segment_best_strptime.second, microseconds=segment_best_strptime.microsecond)
        pbList[splitName] = round(segment_best_delta.total_seconds(),3)
        for time in times:
            rt = time.getElementsByTagName("RealTime")
            if rt:
                duration = rt[0].firstChild.nodeValue
                if len(duration) < 12:
                    duration = duration+".0000000"
                t = datetime.strptime(duration[:12], "%H:%M:%S.%f")
                delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
##                print(delta.total_seconds())
                timeList.append(delta)
        timeSeconds = (sum(timeList, timedelta()) / len(timeList)).total_seconds()
        averagesList[splitName] = round(timeSeconds,3)
    # print(averagesList)
    # print(pbList)
    run_time = sum(averagesList.values())
    pb_time = sum(pbList.values())
    # while (run_time > goal and run_time > pb_time):
#    print(goal)
## we want to find the most time save, then subtract a % that equals the difference between 1st and 2nd save
##% save is defined as: (avg. - glod) / avg.
    if goal > pb_time:
        while(run_time > goal and run_time > pb_time):
            most_save = {}
            most_save['split_name'] = ""
            most_save['amount'] = 0.000
            second_save = {}
            second_save['split_name'] = ""
            second_save['amount'] = 0.000
            for key in averagesList.keys():
                save_key = round(getSave(averagesList, pbList, key),3)
                if save_key >= round(most_save['amount'],3):
                    most_save['split_name'] = key
                    most_save['amount'] = save_key
                else:
                    if save_key > round(second_save['amount'],3) and save_key > 0:
                        second_save['split_name'] = key
                        second_save['amount'] = save_key

#            print(most_save['split_name'],second_save['split_name'])
#            print(most_save['amount'],second_save['amount'])
            if not second_save['split_name'] == "":
                target_percent = second_save['amount']
            else:
                target_percent = round(most_save['amount'] * 0.750,3)
            left_side = (1 - target_percent) * averagesList[most_save['split_name']] - pbList[most_save['split_name']]
            n = round(left_side / (1 - target_percent),3)
            averagesList[most_save['split_name']] = round(averagesList[most_save['split_name']] - n,3)
            run_time = sum(averagesList.values())
    else:
        print("Get better before trying a time like that.")
        return
#    print(averagesList)
#    print(pbList)
#    print(run_time)
    runningTotal = timedelta(seconds=0)
    for segment in segments:
        insertTime = splits.createElement("RealTime")
        nameNode = segment.getElementsByTagName("Name")
        name = nameNode[0].firstChild.nodeValue
#        print(name)
        comparisons = segment.getElementsByTagName("SplitTime")
        for comparison in comparisons:
            if comparison.getAttribute('name') == "Goal":
                x = comparison.getElementsByTagName("RealTime")
                tdelta = convertTime(averagesList[name])
                runningTotal = runningTotal + tdelta
#                print(runningTotal)
                tString = str(runningTotal)
                tString = tString+"0"
                timeValue = splits.createTextNode(tString)
                if len(x) != 0:
                    a = x[0]
                    y = a.childNodes[0]
                    a.removeChild(y)
                    a.appendChild(timeValue)
                else:
                    insertTime.appendChild(timeValue)
                    comparison.appendChild(insertTime)
    f = open(filename,"w")
    f.write(splits.toxml())
    f.close()
    return

def convertTime(seconds):
    a = float(seconds)
    delta = timedelta(seconds=float(a))
    return delta


def getSave(averagesList, pbList, key):
    save_key = round((averagesList[key] - pbList[key]) / averagesList[key],3)
    return save_key


def representsInt(tag):

    try:
        int(tag)
        return True
    except ValueError:
        return False
