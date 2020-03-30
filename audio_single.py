"""
This is file which when the sound effect occured in the file
"""

#loading the necessary libraries
import librosa
import numpy as np

"""
To identify the given sound inside the given sounds I will use template matching approach, for this I will sample the clip being tested 
every 0.1 second and each sample would be of same length as the one its being compared to and the result of comparison will tell if the taken 
sample consists of the given sound or not.
"""

def template_matching(y_compare, y_test, sr): 
  leap = sr//10 #sr is the sampling rate of y, so sr//10, represents the number of samples in 0.1 seconds
  length = 15*leap # specifying the length of the template, replace 15 by (length of given sample file in seconds) * 10, Should be Integer
  run = False #boolean to tell if the current sample contains the given sound
  for i in range(length, len(y_test), leap):
    '''
    since the leap is the number of samples taken in 0.1 second we will move 0.1
    second ahead in each iteration and take last 1.5 seconds as a sample to be
    compared against the template sound.
    The sample is taken is 1.5 seconds in past if i represents the current time,
    this is done so that unnessary latency of sample duration isnt noticed if
    used in real time scenario
    '''
    sample = y_test[i-length:i] 
    cor = np.correlate(y_compare, sample)  #finding the correlation between the given sound and the sample taken
    '''
      Now we'll compare the maximum correlation with some hardcoded numbers
      that might change according to the sound being detected and other factors
    '''
    if run == False and cor.max() > 550: #this conditions tell that the sample wasnt running yet and now it is running
      print('Started at {}'.format(i/sr, cor.max()))
      run = True
    if run and cor.max() < 300: 
      # print('closed at {}'.format(i/sr, cor.max())) #if you need to tell the closing time of the single occurance
      run = False

def main():
  y_compare, sr = librosa.load('single50.wav') #loading the sound to identified
  y_test, sr = librosa.load('tring tring.wav') #loading file in which sound is to be identified

  #since the cut was imperfect i will adjust it to make it of exactly 1.5 seconds
  #if your file doesnt need any trimming delete this
  y_compare = y_compare[350:] 
  y_compare = y_compare[:len(y_compare)-350]

  template_matching(y_compare, y_test, sr)


if __name__ == '__main__':
  main()