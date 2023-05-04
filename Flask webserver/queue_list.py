from time import strftime
from write_json import write
from playsound import playsound

def add_queue(cid, pressed, user_list, time_list):

    if(cid not in user_list and pressed == 1):
        user_list.append(cid)
        time_list.append(strftime("%H:%M:%S"))
        playsound("join.mp3")
        write({'cid':cid, 'time': strftime("%H:%M:%S"),'entry':'joined'}, 'log.json')
        return user_list, time_list
    
    elif (cid in user_list and pressed == 0):
        for i in range(len(user_list)):
            if(cid == user_list[i]):
                del user_list[i], time_list[i]
                playsound("leave.mp3")
                write({'cid':cid, 'time': strftime("%H:%M:%S"),'entry':'left'}, 'log.json')
                return user_list, time_list

