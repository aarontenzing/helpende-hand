from time import strftime
from write_json import write
from playsound import playsound

def add_queue(cid, pressed, user_list, time_list, vak):
    print("dit is het vak=",vak)
    if(cid not in user_list and pressed == 1):
        user_list.append(cid)
        time_list.append(strftime("%H:%M:%S"))
        #playsound("/home/tenzing/Documenten/git/helpende-hand/Flask-webserver/join.mp3")
        write({'cid':cid, 'time': strftime("%H:%M:%S"),'entry':'joined', 'subject': vak}, '/home/tenzing/Documenten/git/helpende-hand/Flask-webserver/log_prob.json')
        return user_list, time_list
    
    elif (cid in user_list and pressed == 0):
        for i in range(len(user_list)):
            if(cid == user_list[i]):
                del user_list[i], time_list[i]
                #playsound("/home/tenzing/Documenten/git/helpende-hand/Flask-webserver/leave.mp3")
                write({'cid':cid, 'time': strftime("%H:%M:%S"),'entry':'left', 'subject': vak}, '/home/tenzing/Documenten/git/helpende-hand/Flask-webserver/log_prob.json')
                return user_list, time_list
    else:
        return "queuelist error"
