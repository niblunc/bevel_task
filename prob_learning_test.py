# taste task. 2/9/2018
#this is TEST TRIAL of the probabilistic learning task for side piece (a substudy of bevbits, formerly juice)
#this is done OUT OF SCANNER
#TR 2 sec
#the pkl file contains all study data as a back up including what files were used, useful for sanity checks
#the csv file is easier to read
#the log file also has onsets, but it has the time from when the .py file was initalized more accurate should be used for analysis
from psychopy import visual, core, data, gui, event, data, logging
import csv
import time
import serial
import numpy as N
import sys,os,pickle
import datetime
import exptutils
from exptutils import *
import random
from random import shuffle
from itertools import cycle
#import pdb

monSize = [800, 600]
info = {}
info['fullscr'] = False
info['participant'] = ''
info['computer']=(os.getcwd()).split('/')[2]
dlg = gui.DlgFromDict(info)
if not dlg.OK:
    core.quit()
########################################
subdata={}

subdata['completed']=0
subdata['cwd']=os.getcwd()

clock=core.Clock()
datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
subdata['datestamp']=datestamp
subdata['expt_title']='sidepiece_prob'

subdata['response']={}
subdata['score']={}
subdata['rt']={}
subdata['stim_onset_time']={}
subdata['stim_log']={}
subdata['is_this_SS_trial']={}
subdata['SS']={}
subdata['broke_on_trial']={}
subdata['simulated_response']=False

subdata['onset']='/Users/'+info['computer']+'/Documents/2019_bevel_pilot/test_onset_files/onsets'
subdata['conds']='/Users/'+info['computer']+'/Documents/2019_bevel_pilot/test_onset_files/conds'
subdata['quit_key']='q'

#######################################
dataFileName='/Users/'+info['computer']+'/Documents/2019_bevel_pilot/output/%s_%s_posttest_subdata.log'%(info['participant'],subdata['datestamp'])
logging.console.setLevel(logging.INFO)
logfile=logging.LogFile(dataFileName,level=logging.DATA)
ratings_and_onsets = []
key_responses=[]
correct_response=[]
flip=[]
#######################################
# Serial connection and commands setup
#ser = serial.Serial(
#                    port=info['port'],
#                    baudrate=19200,
#                    parity=serial.PARITY_NONE,
#                    stopbits=serial.STOPBITS_ONE,
#                    bytesize=serial.EIGHTBITS
#                   )
#if not ser.isOpen():
#    ser.open()
#
time.sleep(1)

#global settings aka Input parameters, make sure these match with the effciciency calculation
delivery_time=0.5
cue_time=2.0
wait_time=1.0
fix=int(2)

# HELPER FUNCTIONS. These are pulled from Russ. We don't change these usually. 
def show_instruction(instrStim):
    # shows an instruction until a key is hit.
    while True:
        instrStim.draw()
        win.flip()
        if len(event.getKeys()) > 0:
            break
        event.clearEvents()


def show_stim(stim, seconds):
    # shows a stim for a given number of seconds
    for frame in range(60 * seconds):
        stim.draw()
        win.flip()
        
def check_for_quit(subdata,win):
    k=event.getKeys()
    print 'checking for quit key %s'%subdata['quit_key']
    print 'found:',k
    if k.count(subdata['quit_key']) >0:# if subdata['quit_key'] is pressed...
        print 'quit key pressed'
        return True
    else:
        return False



# MONITOR set up
# set the window size as win 
win = visual.Window(monSize, fullscr=info['fullscr'],
                    monitor='testMonitor', units='deg')


# STIMS
fixation_text = visual.TextStim(win, text='+', pos=(0, 0), height=2)

scan_trigger_text = visual.TextStim(win, text='Waiting for task to begin', pos=(0, 0))
#Direction text (from Doll, Jacobs, Sanfey Frank (2009))
example_images=['a.jpg','b.jpg']
example_stim1=visual.ImageStim(win, image=N.zeros((300,300)),pos=(0.25,0.25), size=(0.25,0.25),units='height')
example_stim2=visual.ImageStim(win, image=N.zeros((300,300)),pos=(-0.25,0.25), size=(0.25,0.25),units='height')
example_stim1.setImage(example_images[0])#set which image appears
example_stim2.setImage(example_images[1])#set which image appears
scan_trigger_text = visual.TextStim(win, text='In this part, we will test what you learning from the MRI task. Two symbols will appear on the screen. Use the arrow keys to indicate which symbol is "correct". You will have 2 seconds to choose (left or right arrow key). You will not receive any feedback. Remember, try to pick the symbol with the highest CHANCE of being correct', pos=(0, -0.6), height=0.75)

#tastes(pump_phases)

onsets=[]
f=open(subdata['onset'],'r')
x = f.readlines()
for i in x:
    onsets.append(i.strip())
print(onsets)
onsets=[float(i) for i in onsets]
print(onsets, 'onsets')

#jitter=[]
#g=open(subdata['jitter'],'r')
#y = g.readlines()
#for i in y:
#    jitter.append(i.strip())
#    
#jitter=[float(i) for i in jitter]
#print(jitter, 'jitter')

#for this the trial conditions are created randomly each time so it doesn't really matter, the length is what matters
trialcond=N.loadtxt(subdata['conds'], dtype='int')
print(trialcond,'trial conditions')

ntrials=len(trialcond)
#pump=N.zeros(ntrials)

# specify lists of stimulus positions and their corresponding responses:
positions = [(0.25,0), (-0.25,0)]
positions_eng = ['right','left']
pos_ind = [0,1]

#these are indexed on img_index
stim_images1=['a.jpg','c.jpg']
stim_images2=['a.jpg','d.jpg']
stim_images3=['a.jpg','e.jpg']
stim_images4=['a.jpg','f.jpg']
stim_images5=['b.jpg','c.jpg']
stim_images6=['b.jpg','d.jpg']
stim_images7=['b.jpg','e.jpg']
stim_images8=['b.jpg','f.jpg']

img_index=[0,1]

#stim list is on the stim index
stim_list=[stim_images1, stim_images2, stim_images3, stim_images4, stim_images5, stim_images6, stim_images7, stim_images8]
stim_index=[0,1,2,3,4,5,6,7]

subdata['trialdata']={}

            
"""
    The main run block!
"""

def run_block(fix):

    # Await scan trigger
    while True:
        scan_trigger_text.draw()
        win.flip()
        if 'o' in event.waitKeys():
            logging.log(logging.DATA, "start key press")
            break
        event.clearEvents()
        
    clock=core.Clock()
    t = clock.getTime()
    
    
    #start the loop
    for trial in range(ntrials):
        #check for quit
        if check_for_quit(subdata,win):
            exptutils.shut_down_cleanly(subdata,win)
            sys.exit()
        #empty trial data 
        trialdata={}
        trialdata['onset']=onsets[trial]
        
        #shuffle the positions
        shuffle(pos_ind)
        visual_stim1=visual.ImageStim(win, image=N.zeros((300,300)),pos=positions[pos_ind[0]], size=(0.25,0.25),units='height')
        visual_stim2=visual.ImageStim(win, image=N.zeros((300,300)),pos=positions[pos_ind[1]], size=(0.25,0.25),units='height')
        
        #set which image is which
        x=int(N.random.choice(stim_index, 1, p=[0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]))
        print("here is the list")
        print(stim_list)
        print(x)
        stim_img_trial=stim_list[x]
        print(stim_img_trial)
        
        #set which image appears on what side
        visual_stim1.setImage(stim_img_trial[img_index[0]])
        visual_stim2.setImage(stim_img_trial[img_index[1]])
        
        
        shuffle(img_index)
        #creating a dictory which will store the image set and which image is at what postion
        mydict={}
        mydict[positions_eng[pos_ind[1]]] = [stim_img_trial[img_index[1]]]
        mydict[positions_eng[pos_ind[0]]] = [stim_img_trial[img_index[0]]]
        print(mydict)
        
        #which is sweet?
        message=visual.TextStim(win, text='Which is Correct?',pos=(0,5))
        print trial
        t = clock.getTime()
        
        #get the time of the image and log, this log is appending it to the csv file 
        visual_stim1.draw()#making image of the logo appear
        visual_stim2.draw()
        message.draw()
        RT = core.Clock()
        
        logging.log(logging.DATA, "%s at position=%s and %s at position=%s"%(stim_img_trial[img_index[0]],positions_eng[pos_ind[0]],stim_img_trial[img_index[1]],positions_eng[pos_ind[1]]))
        
        while clock.getTime()<trialdata['onset']:
            pass
        win.flip()
        
        RT.reset() # reaction time starts immediately after flip 
        
        while clock.getTime()<(trialdata['onset']+cue_time):#show the image, while clock is less than onset and cue, show cue
            pass
        
        keys = event.getKeys(timeStamped=RT)
        message=visual.TextStim(win, text='')
        message.draw()
        win.flip()
        
        # get the key press logged, and time stamped 
        
        if len(keys)>0:
            logging.log(logging.DATA, "keypress=%s at time= %f"%(keys[0][0],keys[0][1]))
            print("here are the keys:")
            print(keys)
            t = clock.getTime()
            #back up of the key press
            tempArray = [t, keys[0]]
            key_responses.append(tempArray)
            ratings_and_onsets.append(["keypress=%s"%keys[0][0],t])
        else:
            taste=0
            t = clock.getTime()
            logging.log(logging.DATA,"Key Press Missed!")
            keys=keys.append(['MISS',t])
            message=visual.TextStim(win, text='Please answer quicker', pos=(0, 0), height=2)#this lasts throught the taste
            message.draw()
            win.flip()

        while clock.getTime()<(trialdata['onset']+cue_time+delivery_time):
            pass
        
        message=visual.TextStim(win, text='+', pos=(0, 0), height=2)#this lasts throught the wait
        message.draw()
        win.flip()
        t = clock.getTime()
        ratings_and_onsets.append(["wait", t])

        #trialdata['dis']=[ser.write('0DIS\r'),ser.write('1DIS\r')]
        #print(trialdata['dis'])
        
        while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time):
            pass

      
        
        while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time):
            pass

        message=visual.TextStim(win, text='+', pos=(0, 0), height=2)#lasts through the jitter 
        message.draw()
        win.flip()
        t = clock.getTime()
        ratings_and_onsets.append(["jitter", t])

        while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time):
            pass
        
        t = clock.getTime()
        ratings_and_onsets.append(['end time', t])
        logging.log(logging.DATA,"finished")
        subdata['trialdata'][trial]=trialdata
        
      
        
        print(key_responses)
        
    win.close()


run_block(fix)

#subdata['key_responses']=keys_responses

subdata.update(info)
f=open('/Users/'+info['computer']+'/Documents/2019_bevel_pilot/output/%s_%s_posttest_subdata.log'%(info['participant'],subdata['datestamp']))
pickle.dump(subdata,f)
f.close()

myfile = open('/Users/'+info['computer']+'/Documents/2019_bevel_pilot/output/%s_%s_posttest_subdata.csv'%(info['participant'],subdata['datestamp'],'wb'))
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(['event','data'])
for row in ratings_and_onsets:
    wr.writerow(row)


core.quit()
