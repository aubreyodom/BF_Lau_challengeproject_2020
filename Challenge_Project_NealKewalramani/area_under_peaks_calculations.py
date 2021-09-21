############################################################################################
##################### FUNCTIONS FOR CALCULATING AREA UNDER PEAKS ###########################
############################################################################################


## Use as::
# from area_under_peaks_calculations import calc_aup
# area_under_peaks,aup_normed,smooth_error = calc_aup(file)
#



import numpy as np
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import statistics as stat
from scipy import spatial,stats
from scipy.signal import savgol_filter,argrelextrema
import sys
from scipy.optimize import curve_fit
from math import sin, pi
from heapq import nsmallest,nlargest




### Variables for area_under_peaks function ###

# parameters for the savgol_filter smoothing of the curves
windowsize1 = 11
polyorder1 = 2
windowsize2 = 11
polyorder2 = 3

peak_width = 5 # distance the trough has to be from the peak to count it as a peak

def triangle_area(left,peak,right):
    '''estimate the area of a peak assuming it is a triangle'''
    leftx,lefty = left[0],left[1]
    peakx,peaky = peak[0],peak[1]
    rightx,righty = right[0],right[1]

    base = rightx - leftx
    height = peaky - np.mean([lefty,righty])
    area = base * height / 2
    return base,height,area

def findmaxes(y):
    return argrelextrema(y,np.greater)[0]

def findmins(y):
    return argrelextrema(y,np.less)[0]

def single_peak(MAX,mins,yhat,x,nt_to_position,print_out = False):
    '''
    Takes in a single peak and outputs the area under it. To do this it needs to find the closest
    troughs on either side and verify that they aren't too close to be considered troughs.

    INPUT:
    MAX = the peak this function is operating on
    mins = the local minimas for the whole curve
    yhat = the smoothed y values
    x = nucleotide positions
    nt_to_position = dict, look up the element number of the nucleotide position
    print_out = whether to print information

    OUTPUT:
    area = area under this peak
    left = left trough for this peak
    right = right trough for this peak
    height = height of this peak to its base
    '''
    first_trough = mins[0]
    #finding closest two peaks to a trough
    closest_trough = min(mins, key=lambda x:abs(x-MAX)) # closest trough

    #finding the closest trough on the other side of MAX
    closest_x = np.where(mins == closest_trough)[0][0] # position in mins list of closest trough
    if closest_trough < MAX:
        mins = mins[closest_x+1:] # exclude left trough from search for other_trough
    else:
        mins = mins[:closest_x] # exclude right trough from search for other_trough
    try:
        other_trough = min(mins, key=lambda x:abs(x-MAX))
    except:
        return 0,0,0,0

    left_x = min(closest_trough,other_trough)
    right_x = max(closest_trough,other_trough)

    try:
        left_xpos = nt_to_position[left_x]
        right_xpos = nt_to_position[right_x]
    except:
        return 0,0,0,0

    left_y = yhat[left_xpos]
    right_y = yhat[right_xpos]

    # ignore peaks that do not have a trough on either side (ie the beginning and end)
    if left_x > MAX:
        return 0,0,0,0
    elif right_x < MAX:
        return 0,0,0,0
    elif MAX - left_x < peak_width or right_x - MAX < peak_width:
        return 0,0,0,0

    if left_y > right_y:
        yhat_trim = yhat[left_xpos+peak_width:right_xpos] # exclude this trough from future search
        x_trim = np.array(x[left_xpos+peak_width:right_xpos])

        # finding the x coordinate that shares a y-coordinate with the higher trough
        right_y = min(yhat_trim, key=lambda k:abs(k-left_y))
        right_x = x_trim[np.where(yhat_trim == right_y)][-1]

        # Re-trim to the point we found
        right_xpos = nt_to_position[right_x]
        x_trim = np.array(x[left_xpos:right_xpos+1])
        yhat_trim = yhat[left_xpos:right_xpos+1]
    else:

        yhat_trim = yhat[left_xpos:right_xpos-peak_width] # exclude this trough from future search
        x_trim = np.array(x[left_xpos:right_xpos-peak_width])

        # finding the x coordinate that shares a y-coordinate with the higher trough
        left_y = min(yhat_trim, key=lambda x:abs(x-right_y))
        left_x = x_trim[np.where(yhat_trim == left_y)][0]

        # Re-trim to the point we found
        left_xpos = nt_to_position[left_x]
        yhat_trim = yhat[left_xpos:right_xpos+1]
        x_trim = np.array(x[left_xpos:right_xpos+1])


    left = [left_x,left_y]
    right = [right_x,right_y]

    area = np.trapz(yhat_trim - min(yhat_trim)) #bring bottom of the peak to 0
    peak_y = yhat[nt_to_position[MAX]]
    peak = [MAX,peak_y]
    base,height,est_area = triangle_area(left,peak,right)
    if print_out:
        print('xtrim:: ',x_trim)
        print('Peak::',peak,'  Closest troughs::',[left_x,left_y],[right_x,right_y])
        print('AREA::',area)
        print('ESTIMATED AREA::',est_area,'\n')
    return area,left,right,height

def calc_aup(file):

    '''
    Input: a single excel file with a curve in it.

    Normalizes the curve y-values without the large peak at 0, smooths the curve,
    identifies peaks, and calculates the area under each peak.

    Returns:
    area_under_peaks = sum of the area under each peak identified
    aup_normed = area_under_peaks divided by the area of the two largest peaks
    smooth_error = sum of the distance between the smoothed curve and the original curve
    '''

    try:
        df = pd.read_excel(file)
    except:
        df = pd.read_csv(file, sep='\t')
    end_trim = 1 # remove last nucleotide because of huge dip artifact
    offset = 5 # avoiding giant peak at 0 nucleotides
    y = np.array(df['Value'][200+offset:-end_trim])
    x = np.array(df['Position'][200+offset:-1])

    #smoothing y to be able to find relative extrema
    try:
        yhat = savgol_filter(y, windowsize1, polyorder1) #(yvals, window size, polynomial order)
        yhat = savgol_filter(yhat, windowsize2, polyorder2)
    except:
        print('Bad Data:: ',file)
        return 0,0,1000
    maxes = findmaxes(yhat) + offset
    mins = findmins(yhat) + offset
    last_x = int(x[-1])
    mins = np.append(mins,last_x) # otherwise numpy converts the array to strings

    if len(maxes) == 0 or len(mins) == 0:
        print('No maxes or No mins Found:: ',file)
        return 0,0,1000
    first_trough = mins[0] # used to trim peak at x=0 for normalization

    ############################################################################################
    ### TRIM THE CURVE BEFORE THE FIRST TROUGH #################################################
    ############################################################################################
    # This way we normalize the curve's y-values without any part of the giant peak at 0
    y = np.array(df['Value'][200+first_trough:-end_trim])
    y = (y - np.mean(y)) / np.std(y) # normalize to stdDev and mean
    y = y + abs(min(y)) # all values positive
    x = np.array(df['Position'][200+first_trough:-1])

    #smoothing y to be able to find relative extrema
    yhat = savgol_filter(y, windowsize1, polyorder1) #(yvals, window size, polynomial order)
    yhat = savgol_filter(yhat, windowsize2, polyorder2)
    smooth_error = np.sum(np.absolute(np.array(yhat) - np.array(y)))
    maxes = findmaxes(yhat) + first_trough

    xpos = list(range(len(x)))
    nt_to_position = dict(zip(x,xpos))

    aup_list = [] #contains area under each peak
    height_list = []
    area_under_peaks = 0 # total area under all peaks for this curve
    intervals = []
    for MAX in maxes: #iterate through each peak and calculate its area
        # peaks are filtered
        area,left,right,height = single_peak(MAX,mins,yhat,x,nt_to_position)
        area_under_peaks += area
        aup_list.append(area)
        height_list.append(height)

        if left != 0:
            intervals.append([left,right])

    try:
        first_second_aup = sum(nlargest(2,aup_list)) # find two largest peaks and normalize by them
        if first_second_aup != 0:
            aup_normed = area_under_peaks / first_second_aup
        else:
            aup_normed = 0
    except:
        aup_normed = 0

    return area_under_peaks,aup_normed,smooth_error
