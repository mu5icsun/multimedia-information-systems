import cv2
import numpy as np
from os import listdir
from os.path import isfile,join
import Utility as util


def pc1 (yFrameValues):
    return yFrameValues

def pc2(yFrameValues):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    print("Setting in initial value to ", yFrameValues[0,0])
    lastValue = yFrameValues[0,0]

    for i in range(0,10):
        for j in range (0,10):
            result[i][j] = yFrameValues[i,j] - lastValue
            lastValue = yFrameValues[i,j]

    return result

def pc3(yFrameValues):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    print("Setting in initial values to ", yFrameValues[0,0], yFrameValues[0,1])

    for i in range(0,10):
        for j in range (0,10):
            previous_1 = yFrameValues[util.goBack(i,j,1,10)]
            previous_2 = yFrameValues[util.goBack(i,j,2,10)]
            predicted = (previous_1 + previous_2)/ 2
            result[i][j] = yFrameValues[i,j] - predicted

    return result

def pc4(yFrameValues):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    print("Setting in initial values to ", yFrameValues[0,0], yFrameValues[0,1])
    alpha1 = .5
    alpha2 = .5
    for i in range(0,10):
        for j in range (0,10):
            s1 = yFrameValues[util.goBack(i,j,1,10)]
            s2 = yFrameValues[util.goBack(i,j,2,10)]
            s3 = yFrameValues[util.goBack(i,j,3,10)]
            s4 = yFrameValues[util.goBack(i,j,4,10)]
            # predicted = (previous_1 + previous_2)/ 2
            alpha2 = (s1 * s3 - s2^2)/(s3^2-s4*s2)
            alpha1 = 1.0- alpha2
            result[i][j] = yFrameValues[i,j] - predicted
            print result

    return result

def writeToFile(file, values,frameNum,initialValue,initialValue2):
    rows = len(values)
    cols = len(values[0])

    if (initialValue2):
        # file.write(str("{" + initialValue + "," + intialValue2 + "}") + "\n")
        file.write("{" + str(initialValue) + "," + str(initialValue2) + "}" + "\n")
    else:
        # file.write(str("{" + initialValue + "}") + "\n")
        file.write("{" + str(initialValue) + "}" + "\n")


    for i in range(rows):
        for j in range(cols):
            contents = "< f" + str(frameNum) + ",(" + str(i) + "," + str(j) + "), " + str(values[i][j]) + " >\n"
            file.write(contents)
# rootDir = "/home/perry/Desktop/Project 2/multimedia-information-systems/Project 2/Part 1"#util.safeGetDirectory()
rootDir = util.safeGetDirectory()
allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
videoForProcessing = util.getVideoFile(allFiles)
x,y = util.getPixelRegion()
encodingOption = util.getEncodingOption()

videoName = rootDir + "/" + videoForProcessing
video = cv2.VideoCapture(videoName)

fileName = videoForProcessing.strip('.mp4') + "_" + encodingOption +".tpc"
outputFile = open(fileName, 'w')
frameNum = 0
while(video.isOpened()):
    channels = 0
    ret,frame = video.read()
    if ret: #if video is still running...
        frameNum += 1
        croppedFrame = frame[x:x+10, y:y+10]
        YCC_CroppedFrame = cv2.cvtColor(croppedFrame, cv2.COLOR_BGR2YCR_CB)
        yFrameValues = cv2.split(YCC_CroppedFrame)[0]
        #print yFrameValues

        if encodingOption == "1":
            writeToFile(outputFile, pc1(yFrameValues), frameNum,yFrameValues[0,0])
        elif encodingOption == "2":
            writeToFile(outputFile, pc2(yFrameValues), frameNum,yFrameValues[0,0])
        elif encodingOption == "3":
            writeToFile(outputFile, pc3(yFrameValues), frameNum,yFrameValues[0,0],yFrameValues[0,1])
            #print pc3(yFrameValues)
        elif encodingOption == "4":
            print pc4(yFrameValues)
            writeToFile(outputFile, pc4(yFrameValues), frameNum,yFrameValues[0,0])

    else:
        break
