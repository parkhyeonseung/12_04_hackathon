# ë³¸ í”„ë¡œê·¸ëž¨ì€ jetbot ë”¥ëŸ¬ë‹ í•™ìŠµëª¨ë¸ ìˆ˜ì§‘ì„ ìœ„í•´ 'ìž„ì¢…í•œ(reinforcehan@gmail.com)'ì´ ê°œë°œí•˜ì˜€ìŠµë‹ˆë‹¤.
# ì´ í”„ë¡œê·¸ëž¨ì˜ ì‹¤í–‰ì—ëŠ” 2ê°œì˜ ì¹´ë©”ë¼ê°€ ë‹¬ë¦° jetbotì— ê°ê°ì˜ ì£¼í–‰ ì˜ìƒì´ 1000ê°œ ë‹¬ì„±ì‹œ ì™„ë£Œê°€ ë˜ê²Œ ë˜ì–´ ìžˆìŠµë‹ˆë‹¤.
# ì´ ì˜ìƒì˜ ê°¯ìˆ˜ëŠ” tot_count ì—ì„œ ìˆ˜ì •í•˜ì‹œë©´ ë©ë‹ˆë‹¤.

# ì¡°ìž‘ : 'w'=ê°€ì†, 's'=ê°ì†, 'q'=ì¢ŒíšŒì „, 'e'=ìš°íšŒì „, 'a'=ì¢Œì„ íšŒ, 'd'=ìš°ì„ íšŒ, 'x'=ê¸´ê¸‰ì •ì§€
# ì„ íšŒëŠ” í•œìª½ ëª¨í„°ë§Œ êµ¬ë™ë˜ëŠ” ìƒí™©(ì—­íšŒì „ ì—†ìŒ)

# 2021/11/21 R.A.P.A. ë”°ë¼ì™€ë¼íŒŒ, ë”°ë¼ê°€ë¼íŒŒ

import os

# ì¹´ë©”ë¼ êµ¬ë™ë¶€
import cv2
from camera import gstreamer_pipeline

#ëª¨í„° ì œì–´ë¶€
from motor import Robot
from threading import Thread

#ìº¡ì³ ì´ë¯¸ì§€ íŒŒì¼ëª… ë¶€ì—¬ë¥¼ ìœ„í•œ
import datetime
import time




# ìˆ˜ì§‘ ìžë£Œ ê°¯ìˆ˜ ì •ì˜
tot_count = 1000




d_time=None

# ì €ìž¥ í´ë”
UP_CAMERA='./up_camera/'
DOWN_CAMERA='./down_camera/'

def makeDir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


p_dir = [UP_CAMERA, DOWN_CAMERA]

for a in p_dir:
    makeDir(a)

# ë©”ì¸í•¨ìˆ˜
def main():
    cap_down = cv2.VideoCapture(gstreamer_pipeline(sensor_id = 0, flip_method = 0), cv2.CAP_GSTREAMER)
    cap_up = cv2.VideoCapture(gstreamer_pipeline(sensor_id = 1, flip_method = 0), cv2.CAP_GSTREAMER)
    # Robot Control
    robot = Robot()
    forward_val = 0

    # png count
    f_count = 0
    l_count = 0
    r_count = 0
    s_count = 0
    lt_count = 0
    rt_count = 0
    
    try:
        while True:
                ret_down,image_down = cap_down.read()
                ret_up,image_up = cap_up.read()
                if not ret_down : 
                    print('down camera')
                    break
                if not ret_up:
                    print('up camera')
                    break
                
                elif ret_down and ret_up:
                    d_time = datetime.datetime.now().strftime(r"%Y%m%d%H%M%S.%f")

                    cv2.imshow('image_down', image_down)
                    cv2.imshow('image_up', image_up)
                    
                    keyco = cv2.waitKey(30) & 0xFF
                                   
                    # ê¸´ê¸‰ ì¤‘ë‹¨ 'esc'
                    if keyco == 27:
                        break

                    # ì „ì§„
                    elif keyco == ord('w'): 

                        if f_count >= tot_count:
                            print("ì „ì§„ ìžë£Œ ìˆ˜ì§‘ ì™„ë£Œ")

                        else:
                            cv2.imwrite(UP_CAMERA+d_time+'.png', image_up)
                            cv2.imwrite(DOWN_CAMERA+d_time+'.png', image_down)
                            f_count += 1

                        #ì´ë™ ì†ë„ ì¡°ì ˆë¶€    
                        forward_val += 0.1

                        if forward_val>1:
                            forward_val=1.

                        # robot.forward(forward_val)
                    
                    # ì¢ŒíšŒì „
                    elif keyco == ord('q') or keyco == ord('a'):
                        if l_count >= tot_count:
                            print("ì¢ŒíšŒì „ ìžë£Œ ìˆ˜ì§‘ ì™„ë£Œ")

                        else:
                            cv2.imwrite(UP_CAMERA+d_time+'.png', image_up)
                            cv2.imwrite(DOWN_CAMERA+d_time+'.png', image_down)
                            l_count += 1
                                                
                        #ì´ë™ ì†ë„ ì¡°ì ˆë¶€
                        if forward_val<0:
                            forward_val=0
                        forward_val+=0.05
                        
                        if forward_val>1:
                            forward_val=1.
                        
                        robot.left(forward_val)
                        time.sleep(0.5)
                        if keyco == ord('a'):
                            robot.left(forward_val)
                            time.sleep(0.5)
                        forward_val-=0.05
                        
                        robot.forward(forward_val)

                    # ìš°íšŒì „
                    elif keyco == ord('e') or keyco == ord('d'):
                        if r_count >= tot_count:
                            print("ìš°íšŒì „ ìžë£Œ ìˆ˜ì§‘ ì™„ë£Œ")

                        else:                                
                            cv2.imwrite(UP_CAMERA+d_time+'.png', image_up)
                            cv2.imwrite(DOWN_CAMERA+d_time+'.png', image_down)
                            r_count += 1
                        
                        #ì´ë™ ì†ë„ ì¡°ì ˆë¶€
                        if forward_val<0:
                            forward_val=0
                        forward_val+=0.05

                        if forward_val>1:
                            forward_val=1.
                        
                        robot.right(forward_val)
                        time.sleep(0.5)
                        if keyco == ord('d'):
                            robot.right(forward_val)
                            time.sleep(0.5)
                        forward_val -= 0.05

                        robot.forward(forward_val)
                    
                    # # ì¢Œì„ íšŒ
                    # elif keyco == ord('a'):
                        
                    #     if lt_count >= tot_count-500:
                    #         print("ì¢Œì„ íšŒ ìžë£Œ ìˆ˜ì§‘ ì™„ë£Œ")

                    #     else:
                    #         cv2.imwrite(UP_CAMERA+L_TURN_FOLDER+d_time+'.png', image_up)
                    #         cv2.imwrite(DOWN_CAMERA+L_TURN_FOLDER+d_time+'.png', image_down)
                    #         lt_count += 1
                                                
                    #     #ì´ë™ ì†ë„ ì¡°ì ˆë¶€
                    #     forward_val+=0.05
                        
                    #     if forward_val>1:
                    #         forward_val=1.
                        
                    #     robot.motors2(0,forward_val)
                    #     # robot.left_motor.value = 0
                    #     # robot.right_motor.value = forward_val
                        
                    #     time.sleep(0.24)
                    #     forward_val-=0.05
                        
                    #     robot.stop()
                    
                    # # ìš°ì„ íšŒ
                    # elif keyco == ord('d'):
                    #     if rt_count >= tot_count-500:
                    #         print("ìš°ì„ íšŒ ìžë£Œ ìˆ˜ì§‘ ì™„ë£Œ")

                    #     else:
                    #         cv2.imwrite(UP_CAMERA+R_TURN_FOLDER+d_time+'.png', image_up)
                    #         cv2.imwrite(DOWN_CAMERA+R_TURN_FOLDER+d_time+'.png', image_down)
                    #         rt_count += 1
                                                
                    #     #ì´ë™ ì†ë„ ì¡°ì ˆë¶€
                    #     forward_val += 0.05
                        
                    #     if forward_val>1:
                    #         forward_val=1.
                    #     robot.motors2(forward_val,0)
                    #     # robot.left_motor.value = forward_val
                    #     # robot.right_motor.value = 0

                    #     time.sleep(0.24)
                    #     forward_val-=0.05
                        
                    #     robot.stop()

                    # # ê°ì†/í›„ì§„
                    elif keyco == ord('s'):
                        if f_count >= tot_count:
                            print("ìš°íšŒì „ ìžë£Œ ìˆ˜ì§‘ ì™„ë£Œ")
                        else:
                            cv2.imwrite(UP_CAMERA+d_time+'.png',image_up)
                            cv2.imwrite(DOWN_CAMERA+d_time+'.png',image_down)
                            s_count += 1

                        #ì´ë™ ì†ë„ ì¡°ì ˆë¶€
                        if forward_val >= 0:
                            forward_val -= 0.1
                            robot.forward(forward_val)

                        elif forward_val < 0:
                            forward_val -= 0.1
                            # robot.backward(forward_val)
                            robot.forward(forward_val)
                        
                        if forward_val > 1:
                            forward_val = 1.
                        
                        if forward_val < -1:
                            forward_val = -1.

                    # ì •ì§€
                    elif keyco == ord('x'):
                        print("ê¸´ê¸‰ì •ì§€")
                        robot.stop()                 


    except cv2.error:
        print(cv2.error)
        pass


    finally:
        robot.stop()
        robot.init()
        cap_down.release()
        cap_up.release()
        cv2.destroyAllWindows()
    return

if __name__ == "__main__":
    th_main = Thread(target=main, args=())
    th_main.start()
    th_main.join()
