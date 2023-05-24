import json
import os

def tijden(vak):

    #if os.stat('/home/tenzing/Documenten/git/helpende-hand/Flask-webserver/log_prob.json').st_size == 0:
    if os.stat('./Flask-webserver/log_prob.json').st_size == 0:

        return
    
    #json_data=open('/home/tenzing/Documenten/git/helpende-hand/Flask-webserver/log_prob.json')
    json_data=open('./Flask-webserver/log_prob.json')


    # EERST DE LIJST ORDENEN

    data=json.load(json_data)
    data=sorted(data, key=lambda item : item["cid"])
    #data=sorted(data, key=lambda item : item["subject"])
    #print("dit is de data:",data)

    #print(data)
    joinlist=[]
    leftlist=[]
    timelist=[]

    #TIJD IN SECONDEN OMZETTEN
    for i in range(len(data)):

        timelist=data[i]['time'].split(":")
        #timelist=map(int,timelist)
        seconden=int(timelist[0])*3600+int(timelist[1])*60+int(timelist[2])
        #print(seconden)
        data[i]['time']=seconden

    for i in range(len(data)):
        
        #print(data[i]['cid'],data[i]['time'])
        if(data[i]['entry']=='joined'):

            #print("Joined:",data[i]['time'])
            newitem = { "cid": data[i]['cid'], "time": data[i]['time'], "subject": data[i]['subject'] }
            joinlist.append(newitem)

        if(data[i]['entry']=='left'):

            #print("Left:",data[i]['time'])
            newitem = { "cid": data[i]['cid'], "time": data[i]['time'], "subject": data[i]['subject'] }
            leftlist.append(newitem)

    waitlist=[]

    #print("Joinlist: ", len(joinlist))
    #print("Leftlist :", len(leftlist))

    if(len(joinlist)!=len(leftlist)):
         return waitlist

    for i in range(len(joinlist)):
        j=0
        if(joinlist[i]['cid']==leftlist[j]['cid']):
            #print(joinlist[i]['cid'])
            time = (leftlist[j]['time'] - joinlist[i]['time'])

            newitem = { "cid": joinlist[i]['cid'], "time": time, "subject": joinlist[i]['subject'] }
            waitlist.append(newitem)
            

            del leftlist[j]

        else:

            while(j<len(leftlist)):
                if(joinlist[i]['cid']==leftlist[j]['cid'] and joinlist[i]['subject']==leftlist[j]['subject']):
                    time = (leftlist[j]['time']-joinlist[i]['time'])
                    newitem = { "cid": joinlist[i]['cid'], "time": time, "subject" : joinlist[i]['subject'] }
                    waitlist.append(newitem)

                    del leftlist[j]
                j+=1



    tmp = []
    # Wanneer vak geselecteerd is filter op vak
    for x in range(len(waitlist)):
         if (waitlist[x]['subject'] == vak):
            tmp.append(waitlist[x])
    return tmp
    
 
