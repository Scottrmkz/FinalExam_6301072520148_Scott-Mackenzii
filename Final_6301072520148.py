import cv2
import argparse

# Construct the argument parser.
parser = argparse.ArgumentParser()
parser.add_argument('--input',default='Final_Exam\left_output.avi')
parser.add_argument('--template', default='Final_Exam\Template-1.png')
args = vars(parser.parse_args())


#####################################################################
# Read the video input.
cap = cv2.VideoCapture(args['input'])
if (cap.isOpened() == False):
    print('Error')
# Get the frame width and height
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# Read the template in grayscale format.
template = cv2.imread(args['template'], 0)
resize = cv2.resize(template,(92,125))
w, h = resize.shape[::-1]



##############################################################

# Read until end of video.
while(cap.isOpened()):
    # Capture each frame from the video.
    ret, frame = cap.read()
    if ret:
        image = frame.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(image, resize, cv2.TM_CCOEFF_NORMED)
    
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        #  x and y coordinates.
        x, y = max_loc
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        cv2.putText(frame,"X =", (x,y-15),cv2.FONT_HERSHEY_COMPLEX,0.55,(0,255,0),2)
        cv2.putText(frame,str(int(x)), (x+50,y-15),cv2.FONT_HERSHEY_COMPLEX,0.55,(0,255,0),2)
        cv2.putText(frame,"Y =", (x+110,y-15),cv2.FONT_HERSHEY_COMPLEX,0.55,(0,255,0),2)
        cv2.putText(frame,str(int(y)), (x+160,y-15),cv2.FONT_HERSHEY_COMPLEX,0.55,(0,255,0),2)

        cv2.imshow('Result', frame)
        
        
        # cancel with q
        if cv2.waitKey(15) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()