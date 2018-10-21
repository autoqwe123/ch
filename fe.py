# -*- coding: utf-8 -*-

from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
from gtts import gTTS
from googletrans import Translator
#==============================================================================#
botStart = time.time()

nadya = LINE()
#nadya = LINE("TOKEN KAMU")
#nadya = LINE("Email","Password")
nadya.log("Auth Token : " + str(nadya.authToken))
channelToken = nadya.getChannelResult()
nadya.log("Channel Token : " + str(channelToken))

nadyaMID = nadya.profile.mid
nadyaProfile = nadya.getProfile()
lineSettings = nadya.getSettings()
oepoll = OEPoll(nadya)
Rfu = [nadya]
RfuBot=[nadyaMID]
supperadmin=['ue9781edcd4eecd9abfd6e50fc3ea95b1',nadyaMID]
admin=['ue9781edcd4eecd9abfd6e50fc3ea95b1','u9cff30bb3b8bd344356702e0340ce793',nadyaMID]
Family=["ue9781edcd4eecd9abfd6e50fc3ea95b1","u9cff30bb3b8bd344356702e0340ce793",nadyaMID]
RfuFamily = RfuBot + Family
#==============================================================================#
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")

read = json.load(readOpen)
settings = json.load(settingsOpen)

wait = {
   'acommentOn':False,
   'bcommentOn':False,
   'comment1':False,
   'AutoJoin':False,
   'autoLeave':False,
   'AutoAdd':False,
   'AutoRead':False,
   'checkSticker':False,
   'message':"บัญชีถูกป้องกันโดยระบบ ระบบได้บล็อคอัตโนมัติ(。-`ω´-)"
}

RfuProtect = {
    "AutoAdd":False,
}

myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}

myProfile["displayName"] = nadyaProfile.displayName
myProfile["statusMessage"] = nadyaProfile.statusMessage
myProfile["pictureStatus"] = nadyaProfile.pictureStatus
#==============================================================================#
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
#    time.sleep(3)
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False    
    
def logError(text):
    nadya.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
        
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        nadya.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
        
def helpmessage():
    helpMessage =  "คำสั่งทั้งหมดพิม . ข้างหน้าคำสั่งแทน -" + "\n" + \
                  " " + "\n" + \
                  "คำสั่ง" + "\n" + \
                  "คำสั่ง2" + "\n" + \
                  " " + "\n" + \
                  "-สปีด" + "\n" + \
                  "-เชคค่า" + "\n" + \
                  "-ข้อมูล" + "\n" + \
                  "-เทส" + "\n" + \
                  "-รีบอท" + "\n" + \
                  "-ออน" + "\n" + \
                  "-พูด(ข้อความ)" + "\n" + \
                  "-ชื่อ: (ชื่อ)" + "\n" + \
                  "-ตัส: (ตัส)" + "\n" + \
                  "-ข้อมูล" + "\n" + \
                  "-โทร (จำนวนการเชิญ)" + "\n" + \
                  "-เชคแอด" + "\n" + \
                  "-สแปม「On/Off」(เลข)(ข้อความ)" + "\n" + \
                  "-คท" + "\n" + \
                  "-มิด" + "\n" + \
                  "-ชื่อ" + "\n" + \
                  "-ตัส" + "\n" + \
                  "-รูป" + "\n" + \
                  "-ปก" + "\n" + \
                  "-คท @" + "\n" + \
                  "-มิด @" + "\n" + \
                  "-ชื่อ @" + "\n" + \
                  "-ตัส @" + "\n" + \
                  "-ดิส @" + "\n" + \
                  "-เตะ @" + "\n" + \
                  "-เด้ง @" + "\n" + \
                  "-!แทค" + "\n" + \
                  "-!มิด" "\n" + \
                  "-!คท" + "\n" + \
                  "-แทค" + "\n" + \
                  "-ชื่อกลุ่ม" + "\n" + \
                  "-ไอดีกลุ่ม" + "\n" + \
                  "-รูปกลุ่ม" + "\n" + \
                  "-กลุ่มทั้งหมด" + "\n" + \
                  "-ข้อมูลกลุ่ม" + "\n" + \
                  "-สมาชิก" + "\n" + \
                  "-ลิ้งกลุ่ม" + "\n" + \
                  "-เพิ่มพิมตาม" + "\n" + \
                  "-ลบพิมตาม" + "\n" + \
                  "-อ่าน" + "\n" + \
                  "-ยกเลิก" + "\n" + \
                  "-เปลี่ยนรูป" + "\n" + \
                  "-ประกาศ: (ข้อความ)" + "\n" + \
                  " " + "\n" + \
                  "*คำสั่งเฉพาะบัญชีเท่านั้น*"
    return helpMessage
    
def helptexttospeech():
    helpTextToSpeech =   "คำสั่งทั้งหมดพิม \ ข้างหน้าคำสั่งแทน -" + "\n" +\
                         " " + "\n" \
                         "-หาคนอ่าน 「On/Off/Reset」" + "\n" + \
                         "-ลิ้ง 「On/Off」" + "\n" + \
                         "-พิมตาม 「On/Off」" + "\n" + \
                         "-เข้ากลุ่ม「On/Off」" + "\n" + \
                         "-อ่านออโต้「On/Off」" + "\n" + \
                         "-ออโต้บล็อค 「On/Off」" + "\n" + \
                         "-เช็คสติ้กเกอร์「On/Off」" + "\n" + \
                         "-ออกกลุ่ม 「On/Off」" + "\n" + \
                         "-แทค 「On/Off」" + "\n" + \
                         "-แทค2 「On/Off」" + "\n" + \
                         "-ตอนรับ 「On/Off」" + "\n" + \
                         "-ตอนรับออก 「On/Off」" + "\n" + \
                         "-ไลค์「On/Off」" + "\n" + \
                         " " + "\n" + \
                         "-ตั้งแทค:" + "\n" + \
                         "-ตั้งออก:" + "\n" + \
                         "-ตั้งเข้า:" + "\n" + \
                         "-ตั้งไลค์:" + "\n" + \
                         "-เชคแทค" + "\n" + \
                         "-เชคออก" + "\n" + \
                         "-เชคเข้า" + "\n" + \
                         " " + "\n " \
                         "**คำสั่งเฉพาะบัญขีเท่านั้น**"
    return helpTextToSpeech
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] END OF OPERATION")
            return

        if op.type == 5:
            print ("[ 5 ] NOTIFIED AUTOBLOCK")
            if settings["autoAdd"] == True:
            	nadya.blockContact(op.param1)
                #nadya.sendMessage(op.param1, "Halo {} terimakasih telah menambahkan saya sebagai teman :D".format(str(nadya.getContact(op.param1).displayName)))

        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            group = nadya.getGroup(op.param1)
            if settings["autoJoin"] == True:
                nadya.acceptGroupInvitation(op.param1)

        if op.type == 15:
            if wait["bcommentOn"] and "bcomment" in wait:
                nadya.sendMessage(op.param1,nadya.getContact(op.param2).displayName + "\n\n" + str(wait["bcomment"]))
           
        if msg.contentType == 16:
               url = msg.contentMetadata['postEndUrl']
               nadya.like(url[25:58], url[66:], likeType=1001)
               nadya.comment(url[25:58], url[66:], wait["comment1"])

        if op.type == 17:
            if wait["acommentOn"] and "acomment" in wait:
                cnt = nadya. getContact(op.param2)
                nadya.sendMessage(op.param1,cnt.displayName + "\n\n" + str(wait["acomment"]))

        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                nadya.leaveRoom(op.param1)

        if op.type == 25:
            print ("[ 25 ] SEND MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != nadya.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
#==============================================================================#
                if text.lower() == 'คำสั่ง':
                    helpMessage = helpmessage()
                    nadya.sendMessage(to, str(helpMessage))
                elif text.lower() == 'คำสั่ง2':
                    helpTextToSpeech = helptexttospeech()
                    nadya.sendMessage(to, str(helpTextToSpeech))
#==============================================================================#
                elif ".ประกาศ:" in msg.text:
                      bctxt = text.replace(".ประกาศ:","")
                      n = nadya.getGroupIdsJoined()
                      for manusia in n:
                          nadya.sendMessage(manusia,(bctxt))
                elif ".สแปม " in msg.text:
                    txt = msg.text.split(" ")
                    jmlh = int(txt[2])
                    teks = msg.text.replace(".สแปม "+str(txt[1])+" "+str(jmlh)+" ","")
                    tulisan = jmlh * (teks+"\n")
                    if txt[1] == "on":
                        if jmlh <= 100000:
                           for x in range(jmlh):
                               nadya.sendMessage(msg.to, teks)
                        else:
                           nadya.sendMessage(msg.to, "Out of Range!")
                    elif txt[1] == "off":
                        if jmlh <= 100000:
                            nadya.sendMessage(msg.to, tulisan)
                        else:
                            nadya.sendMessage(msg.to, "Out Of Range!")
                elif ".โทร" in msg.text.lower():
                     if msg.toType == 2:
                            sep = text.split(" ")
                            strnum = text.replace(sep[0] + " ","")
                            num = int(strnum)
                            nadya.sendMessage(to, "เชิญเข้าร่วมการโทร(。-`ω´-)")
                            for var in range(0,num):
                                group = nadya.getGroup(to)
                                members = [mem.mid for mem in group.members]
                                nadya.acquireGroupCallRoute(to)
                                nadya.inviteIntoGroupCall(to, contactIds=members)
                elif ".ทีมงาน" == msg.text.lower():
                    msg.contentType = 13
                    nadya.sendMessage(to, "「 BOT TEAM 」 • H0ck")
                    nadya.sendContact(to, "ue9781edcd4eecd9abfd6e50fc3ea95b1")
                elif ".เทส" == msg.text.lower():
                    nadya.sendMessage(to,"LOADING:▒...0%")
                    nadya.sendMessage(to,"█▒... 10.0%")
                    nadya.sendMessage(to,"██▒... 20.0%")
                    nadya.sendMessage(to,"███▒... 30.0%")
                    nadya.sendMessage(to,"████▒... 40.0%")
                    nadya.sendMessage(to,"█████▒... 50.0%")
                    nadya.sendMessage(to,"██████▒... 60.0%")
                    nadya.sendMessage(to,"███████▒... 70.0%")
                    nadya.sendMessage(to,"████████▒... 80.0%")
                    nadya.sendMessage(to,"█████████▒... 90.0%")
                    nadya.sendMessage(to,"███████████..100.0%")
                    nadya.sendMessage(to,"บอทปกติดี(。-`ω´-)")

                elif ".ชื่อ: " in text.lower():
                    if msg._from in admin:
                           proses = text.split(": ")
                           string = text.replace(proses[0] + ": ","")
                           profile_A = nadya.getProfile()
                           profile_A.displayName = string
                           nadya.updateProfile(profile_A)
                           nadya.sendMessage(msg.to,"เปลี่ยนชื่อเป็น(。-`ω´-) " + string)
                elif ".ตัส: " in msg.text.lower():
                	if msg._from in admin:
                           proses = text.split(": ")
                           string = text.replace(proses[0] + ": ","")
                           profile_A = nadya.getProfile()
                           profile_A.statusMessage = string
                           nadya.updateProfile(profile_A)
                           nadya.sendMessage(msg.to,"เปลี่ยนตัสเสร็จสิ้น(。-`ω´-)  " + string)

                if "!ชื่อ: " in msg.text.lower():
                 if msg._from in supperadmin:
                     spl = re.split("!ชื่อ: ",msg.text,flags=re.IGNORECASE)
                     if spl[0] == "":
                        prof = nadya.getProfile()
                        prof.displayName = spl[1]
                        nadya.updateProfile(prof)
                        nadya.sendMessage(msg.to,"เปลี่ยนชื่อสำเร็จแล้ว(。-`ω´-)")

                if "!ตัส: " in msg.text.lower():
                 if msg._from in supperadmin:
                     spl = re.split("!ตัส: ",msg.text,flags=re.IGNORECASE)
                     if spl[0] == "":
                        prof = nadya.getProfile()
                        prof.statusMessage = spl[1]
                        nadya.updateProfile(prof)
                        nadya.sendMessage(msg.to,"เปลี่ยนตัสสำเร็จแล้ว(。-`ω´-)")

                if text.lower() == '!ออก':
                  if msg._from in supperadmin:
                      if msg.toType == 2:
                          ginfo = nadya.getGroup(to)
                          try:
                              nadya.sendMessage(msg.to,"「 Leave 」\n• Success ")
                              nadya.leaveGroup(to)
                          except:
                             pass

                if text.lower() == "!เปลี่ยนรูป":
                  if msg._from in supperadmin:
                      settings["changePictureProfile"] = True
                      nadya.sendMessage(msg.to,"ส่งรูปมา(。-`ω´-)")

                elif ".ยกเลิก" == msg.text.lower():
                    if msg.toType == 2:
                        group = nadya.getGroup(msg.to)
                        gMembMids = [contact.mid for contact in group.invitee]
                        for _mid in gMembMids:
                            nadya.cancelGroupInvitation(msg.to,[_mid])
                        nadya.sendMessage(to,"ยกเลิกค้างเชิญเสร็จสิ้น(。-`ω´-)")
                elif text.lower() == '.ลบรัน':
                    gid = nadya.getGroupIdsInvited()
                    start = time.time()
                    for i in gid:
                        nadya.rejectGroupInvitation(i)
                    elapsed_time = time.time() - start
                    nadya.sendMessage(to, "กำลังดำเนินการ(。-`ω´-)")
                    nadya.sendMessage(to, "เวลาที่ใช้: %sวินาที(。-`ω´-)" % (elapsed_time))
                elif msg.text in [".speed",".sp",".สปีด",".Speed",".Sp"]:
                    start = time.time()
                    nadya.sendMessage(to, "การตอบสนองของบอท(。-`ω´-)")
                    elapsed_time = time.time() - start
                    nadya.sendMessage(msg.to, "[ %s Seconds ]\n[ " % (elapsed_time) + str(int(round((time.time() - start) * 1000)))+" ms ]")
                elif text.lower() == '.รีบอท':
                    nadya.sendMessage(to, "กำลังรีบอท กรุณารอสักครู่.....(。-`ω´-)")
                    time.sleep(5)
                    nadya.sendMessage(to, "รีบอทสำเร็จแล้ว\n✍️  ᴛ⃢​ᴇ⃢​ᴀ⃢​ᴍ⃢   🔝ͲᎻᎬᖴ͙͛Ꮮ͙͛ᗩ͙͛ᔑ͙͛Ꮋ͙  ̾⚡")
                    restartBot()
                elif text.lower() == '.ออน':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    nadya.sendMessage(to, "ระยะเวลาการทำงานของบอท(。-`ω´-)\n{}".format(str(runtime)))
                elif text.lower() == '.ข้อมูล':
                    try:
                        arr = []
                        owner = "ude3230559bf63a55b9c28aa20ea194e3"
                        creator = nadya.getContact(owner)
                        contact = nadya.getContact(nadyaMID)
                        grouplist = nadya.getGroupIdsJoined()
                        contactlist = nadya.getAllContactIds()
                        blockedlist = nadya.getBlockedContactIds()
                        ret_ = "╔══[ ข้อมูลไอดีคุณ ]"
                        ret_ += "\n╠ ชื่อ : {}".format(contact.displayName)
                        ret_ += "\n╠ กลุ่ม : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ เพื่อน : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ บล็อค : {}".format(str(len(blockedlist)))
                        ret_ += "\n╚══[ ข้อมูลไอดีคุณ ]"
                        nadya.sendMessage(to, str(ret_))
                    except Exception as e:
                        nadya.sendMessage(msg.to, str(e))
#==============================================================================#
                elif text.lower() == '.เชคค่า':
                    try:
                        ret_ = "╔════════════"
                        if settings["autoAdd"] == True: ret_ += "\n║ ระบบออโต้บล็อค ✔"
                        else: ret_ += "\n║ ระบบออโต้บล็อค ✘"
                        if settings["autoJoin"] == True: ret_ += "\n║ ระบบเข้ากลุ่มออโต้ ✔"
                        else: ret_ += "\n║ ระบบเข้ากลุ่มออโต้ ✘"
                        if settings["autoLeave"] == True: ret_ += "\n║ ระบบออกกลุ่มออโต้  ✔"
                        else: ret_ += "\n║ ระบบออกกลุ่มออโต้ ✘"
                        if settings["autoRead"] == True: ret_ += "\n║ ระบบอ่านข้อความออโต้  ✔"
                        else: ret_ += "\n║ ระบบอ่านข้อความออโต้ ✘"
                        if settings["checkSticker"] == True: ret_ += "\n║ ระบบเช็คสติ้กเกอร์ ✔"
                        else: ret_ += "\n║ ระบบเช็คสติ้กเกอร์ ✘"
                        if settings["detectMention"] == True: ret_ += "\n║ ระบบข้อความแทค ✔"
                        else: ret_ += "\n║ ระบบข้อความแทค ✘"
                        if settings["detectMention"] == True: ret_ += "\n║ ระบบแทคส่งรูป ✔"
                        else: ret_ += "\n║ ระบบแทคส่งรูป ✘"
                        if wait["acommentOn"] == True: ret_ += "\n║ ระบบตอนรับคนเข้ากลุ่ม ✔"
                        else: ret_ += "\n║ ระบบตอนรับคนเข้ากลุ่ม ✘"
                        if wait["bcommentOn"] == True: ret_ += "\n║ ระบบตอนรับคนออกกลุ่ม ✔"
                        else: ret_ += "\n║ ระบบตอนรับคนออกกลุ่ม ✘"
                        ret_ += "\n╚════════════"
                        nadya.sendMessage(to, str(ret_))
                    except Exception as e:
                        nadya.sendMessage(msg.to, str(e))
                elif text.lower() == '\ออโต้บล็อค on':
                    settings["autoAdd"] = True
                    nadya.sendMessage(to, "เปิดระบบออโต้บล็อค(。-`ω´-)")
                elif text.lower() == '\ออโต้บล็อค off':
                    settings["autoAdd"] = False
                    nadya.sendMessage(to, "ปิดระบบออโต้บล็อค(。-`ω´-)")
                elif text.lower() == '\เข้ากลุ่ม on':
                    settings["autoJoin"] = True
                    nadya.sendMessage(to, "เปิดระบบเข้ากลุ่มออโต้(。-`ω´-)")
                elif text.lower() == '\เข้ากลุ่ม off':
                    settings["autoJoin"] = False
                    nadya.sendMessage(to, "ปิดระบบเข้ากลุ่มออโต้(。-`ω´-)")
                elif text.lower() == '\ออกกลุ่ม on':
                    settings["autoLeave"] = True
                    nadya.sendMessage(to, "เปิดระบบออกกลุ่มออโต้(。-`ω´-)")
                elif text.lower() == '\ออกกลุ่ม off':
                    settings["autoLeave"] = False
                    nadya.sendMessage(to, "ปิดระบบออกกลุ่มออโต้(。-`ω´-)")
                elif text.lower() == '\อ่านออโต้ on':
                    settings["autoRead"] = True
                    nadya.sendMessage(to, "เปิดระบบอ่านออโต้(。-`ω´-)")
                elif text.lower() == '\อ่านออโต้ off':
                    settings["autoRead"] = False
                    nadya.sendMessage(to, "ปิดระบบอ่านออโต้(。-`ω´-)")
                elif text.lower() == '\เช็คสติ้กเกอร์ on':
                    settings["checkSticker"] = True
                    nadya.sendMessage(to, "เปิดระบบเช็คสติ้กเกอร์(。-`ω´-)")
                elif text.lower() == '\เช็คสติ้กเกอร์ off':
                    settings["checkSticker"] = False
                    nadya.sendMessage(to, "ปิดระบบเช็คสติ้กเกอร์(。-`ω´-)")
                elif text.lower() == '\แทค on':
                    settings["datectMention"] = True
                    nadya.sendMessage(to, "เปิดระบบการกล่าวถึง(。-`ω´-)")
                elif text.lower() == '\แทค off':
                    settings["datectMention"] = False
                    nadya.sendMessage(to, "ปิดระบบการกล่าวถึง(。-`ω´-)")
                elif text.lower() == '\แทค2 on':
                    settings['potoMention'] = True
                    nadya.sendMessage(msg.to,"เปิดระบบส่งแทคส่งรูป(。-`ω´-)")
                elif text.lower() == '\แทค2 off':
                    settings['potoMention'] = False
                    nadya.sendMessage(msg.to,"ปิดระบบส่งแทคส่งรูป(。-`ω´-)")
#==============================================================================#
                elif msg.text.lower() ==  '\ตอนรับ on':
                    wait['acommentOn'] = True
                    nadya.sendMessage(msg.to,"เปิดระบบตอนรับสมาชิกเข้ากลุ่ม(。-`ω´-)")
                elif msg.text.lower() ==  '\ตอนรับ off':
                    wait['acommentOn'] = False
                    nadya.sendMessage(msg.to,"ปิดระบบตอนรับสมาชิกเข้ากลุ่ม(。-`ω´-)")
                elif msg.text.lower() == '\ตอนรับออก on':
                    wait["bcommentOn"] = True
                    nadya.sendMessage(msg.to,"เปิดระบบตอนรับสมาชิกออกกลุ่ม(。-`ω´-)")
                elif msg.text.lower() == '\ตอนรับออก off':
                    wait['bcommentOn'] = False
                    nadya.sendMessage(msg.to,"ปิดระบบตอนรับสมาชิกออกกลุ่ม(。-`ω´-)")
#==============================================================================#
                elif "\ตั้งแทค: " in msg.text:
                    settings["Tag"] = msg.text.replace("\ตั้งแทค: ","")
                    nadya.sendMessage(msg.to,"ตั้งค่าตอบกลับคนแทคเสร็จสิ้น(。-`ω´-)")
                    
                elif "\ตั้งเข้า:" in msg.text.lower():
                    c = msg.text.replace("\ตั้งเข้า:","")
                    if c in [""," ","\n",None]:
                        nadya.sendMessage(msg.to,"เกิดข้อผิดพลาด(。-`ω´-)")
                    else:
                        wait["acomment"] = c
                        nadya.sendMessage(msg.to,"ตั้งค่าข้อความตอนรับเสร็จสิ้น(。-`ω´-)")

                elif "\ตั้งออก:" in msg.text.lower():
                    c = msg.text.replace("\ตั้งออก:","")
                    if c in [""," ","\n",None]:
                        nadya.sendMessage(msg.to,"เกิดข้อผิดพลาด(。-`ω´-)")
                    else:
                        wait["bcomment"] = c
                        nadya.sendMessage(msg.to,"ตั้งค่าข้อความตอนรับออกเสร็จสิ้น(。-`ω´-)")
#==============================================================================#
                elif msg.text in ["\เชคแทค"]:
                	nadya.sendMessage(msg.to,"เช็คข้อความแทคล่าสุด(。-`ω´-)" + "\n\n➤" + settings["Tag"])
                elif msg.text in ["\เชคเข้า"]:
                	nadya.sendMessage(msg.to,"เช็คข้อความตอนรับล่าสุด(。-`ω´-)" + "\n\n➤" + str(wait["acomment"]))
                elif msg.text in ["\เชคออก"]:
                	nadya.sendMessage(msg.to,"เช็คข้อความตอนรับออกล่าสุด(。-`ω´-)" + "\n\n➤" + str(wait["bcomment"]))
#==============================================================================#
                elif text.lower() == ".เปลี่ยนรูป":
                    settings["changePictureProfile"] = True
                    nadya.sendMessage(to, "ส่งรูปมา(。-`ω´-)")
                elif text.lower() == '.!แทค':
                    gs = nadya.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        nadya.sendMessage(to, "ไม่มีคนใส่ชื่อร่องหน(。-`ω´-)")
                    else:
                        mc = ""
                        for target in targets:
                            mc += sendMessageWithMention(to,target) + "\n"
                        nadya.sendMessage(to, mc)
                elif text.lower() == '.!มิด':
                    gs = nadya.getGroup(to)
                    lists = []
                    for g in gs.members:
                        if g.displayName in "":
                            lists.append(g.mid)
                    if lists == []:
                        nadya.sendMessage(to, "ไม่มีคนใส่ชื่อร่องหน(。-`ω´-)")
                    else:
                        mc = ""
                        for mi_d in lists:
                            mc += "->" + mi_d + "\n"
                        nadya.sendMessage(to,mc)
                elif text.lower() == '.!คท':
                    gs = nadya.getGroup(to)
                    lists = []
                    for g in gs.members:
                        if g.displayName in "":
                            lists.append(g.mid)
                    if lists == []:
                        nadya.sendMessage(to, "ไม่มีคนใส่ชื่อร่องหน(。-`ω´-)")
                    else:
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            mi_d = contact.mid
                            nadya.sendContact(to, mi_d)
                elif text.lower() == '.คท':
                    sendMessageWithMention(to, nadyaMID)
                    nadya.sendContact(to, nadyaMID)
                elif text.lower() == '.มิด':
                    nadya.sendMessage(msg.to, nadyaMID)
                elif text.lower() == '.ชื่อ':
                    me = nadya.getContact(nadyaMID)
                    nadya.sendMessage(msg.to, me.displayName)
                elif text.lower() == '.ตัส':
                    me = nadya.getContact(nadyaMID)
                    nadya.sendMessage(msg.to, me.statusMessage)
                elif text.lower() == '.ดิส':
                    me = nadya.getContact(nadyaMID)
                    nadya.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == '.ดิสวีดีโอ':
                    me = nadya.getContact(nadyaMID)
                    nadya.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == '.ดิสปก':
                    me = nadya.getContact(nadyaMID)
                    cover = nadya.getProfileCoverURL(nadyaMID)    
                    nadya.sendImageWithURL(msg.to, cover)
                elif msg.text.lower().startswith(".คท "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            mi_d = contact.mid
                            nadya.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith(".มิด "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = ""
                        for ls in lists:
                            ret_ += ls
                        nadya.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith(".ชื่อ "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            nadya.sendMessage(msg.to, contact.displayName)
                elif msg.text.lower().startswith(".ตัส "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            nadya.sendMessage(msg.to, contact.statusMessage)
                elif msg.text.lower().startswith(".ดิส "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + nadya.getContact(ls).pictureStatus
                            nadya.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith(".ดิสวีดีโอ "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + nadya.getContact(ls).pictureStatus + "/vp"
                            nadya.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith(".ดิสปก "):
                    if line != None:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = nadya.getProfileCoverURL(ls)
                                nadya.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("ก็อปปี้ "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            contact = mention["M"]
                            break
                        try:
                            nadya.cloneContactProfile(contact)
                            nadya.sendMessage(msg.to, "ก็อปปี้เสร็จสิ้นกรุณารอโปรไฟล์เปลี่ยนสักครู่(。-`ω´-)")
                        except:
                            nadya.sendMessage(msg.to, "ก็อปปี้ล้มเหลวกรุณาลองใหม่อีกครั้ง(。-`ω´-)")
                            
                elif text.lower() == 'กลับร่าง':
                    try:
                        nadyaProfile.displayName = str(myProfile["displayName"])
                        nadyaProfile.statusMessage = str(myProfile["statusMessage"])
                        nadyaProfile.pictureStatus = str(myProfile["pictureStatus"])
                        nadya.updateProfileAttribute(8, nadyaProfile.pictureStatus)
                        nadya.updateProfile(nadyaProfile)
                        nadya.sendMessage(msg.to, "กู้คืนโปรไฟล์สำเร็จกรุณารอจนกว่าโปรไฟล์จะเปลี่ยน(。-`ω´-)")
                    except:
                        nadya.sendMessage(msg.to, "กู้คืนโปรไฟล์ล้มเหลว(。-`ω´-)")
                        
#==============================================================================#
                elif ".เด้ง " in msg.text:
                        vkick0 = msg.text.replace(".เด้ง ","")
                        vkick1 = vkick0.rstrip()
                        vkick2 = vkick1.replace("@","")
                        vkick3 = vkick2.rstrip()
                        _name = vkick3
                        gs = nadya.getGroup(msg.to)
                        targets = []
                        for s in gs.members:
                            if _name in s.displayName:
                                targets.append(s.mid)
                        if targets == []:
                            pass
                        else:
                            for target in targets:
                                try:
                                    nadya.kickoutFromGroup(msg.to,[target])
                                    nadya.findAndAddContactsByMid(target)
                                    nadya. inviteIntoGroup(msg.to,[target])
                                except:
                                    pass
                elif msg.text.lower().startswith(".เตะ "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            nadya.kickoutFromGroup(msg.to,[target])
                        except:
                            nadya.sendText(msg.to,"Error")
                elif msg.text.lower().startswith(".เพิ่มพิมตาม "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            settings["mimic"]["target"][target] = True
                            nadya.sendMessage(msg.to,"เพิ่มพิมตามเรียบร้อย(。-`ω´-)")
                            break
                        except:
                            nadya.sendMessage(msg.to,"เพิ่มพิมตามล้มเหลว(。-`ω´-)")
                            break
                elif msg.text.lower().startswith(".ลบพิมตาม "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del settings["mimic"]["target"][target]
                            nadya.sendMessage(msg.to,"ลบพิมตามเรียบร้อย(。-`ω´-)")
                            break
                        except:
                            nadya.sendMessage(msg.to,"ลบพิมตามล้มเหลว(。-`ω´-)")
                            break
                elif text.lower() == '.รายชื่อคนพิมตาม':
                    if settings["mimic"]["target"] == {}:
                        nadya.sendMessage(msg.to,"ไม่มีการเพิ่มก่อนหน้านี้(。-`ω´-)")
                    else:
                        mc = "╔══[ รายชื่อคนพิมตาม ]"
                        for mi_d in settings["mimic"]["target"]:
                            mc += "\n╠ "+nadya.getContact(mi_d).displayName
                        nadya.sendMessage(msg.to,mc + "\n╚══[ 🔝ƬΣΛM✍️ŦЂềƒÎάŠħ⚡]")
                    
                elif "\พิมตาม" in msg.text.lower():
                    sep = text.split(" ")
                    mic = text.replace(sep[0] + " ","")
                    if mic == "on":
                        if settings["mimic"]["status"] == False:
                            settings["mimic"]["status"] = True
                            nadya.sendMessage(msg.to,"เปิดระบบพิมตามเรียบร้อย(。-`ω´-)")
                    elif mic == "off":
                        if settings["mimic"]["status"] == True:
                            settings["mimic"]["status"] = False
                            nadya.sendMessage(msg.to,"ปิดระบบพิมตามเรียบร้อย(。-`ω´-)")
#==============================================================================#
                elif text.lower() == '.เชคแอด':
                    group = nadya.getGroup(to)
                    GS = group.creator.mid
                    nadya.sendContact(to, GS)
                elif text.lower() == '.ไอดีกลุ่ม':
                    gid = nadya.getGroup(to)
                    nadya.sendMessage(to, "\n" + gid.id)
                elif text.lower() == '.รูปกลุ่ม':
                    group = nadya.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    nadya.sendImageWithURL(to, path)
                elif text.lower() == '.ชื่อกลุ่ม':
                    gid = nadya.getGroup(to)
                    nadya.sendMessage(to, "\n" + gid.name)
                elif text.lower() == '.ลิ้งกลุ่ม':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = nadya.reissueGroupTicket(to)
                            nadya.sendMessage(to, "https://line.me/R/ti/g/{}".format(str(ticket)))
                        else:
                            nadya.sendMessage(to, "กรุณาเปิดลิ้งกลุ่มก่อน\nลงคำสั่งนี้ด้วยครับ(。-`ω´-)".format(str(settings["keyCommand"])))
                elif text.lower() == '\ลิ้งกลุ่ม on':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            nadya.sendMessage(to, "ลิ้งกลุ่มเปิดอยู่แล้ว(。-`ω´-)")
                        else:
                            group.preventedJoinByTicket = False
                            nadya.updateGroup(group)
                            nadya.sendMessage(to, "เปิดลิ้งกลุ่มเรียบร้อย(。-`ω´-)")
                elif text.lower() == '\ลิ้งกลุ่ม off':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            nadya.sendMessage(to, "ลิ้งกลุ่มปิดอยู่แล้ว(。-`ω´-)")
                        else:
                            group.preventedJoinByTicket = True
                            nadya.updateGroup(group)
                            nadya.sendMessage(to, "ลิ้งกลุ่มปิดเรียบร้อย(。-`ω´-)")
                elif text.lower() == '.ข้อมูลกลุ่ม':
                    group = nadya.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "ไม่พบผู้สร้าง"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "ปิด"
                        gTicket = "ลิ้งถูกปิดอยู่.."
                    else:
                        gQr = "เปิด"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(nadya.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ ข้อมูลกลุ่ม ]"
                    ret_ += "\n╠ ชื่อกลุ่ม : {}".format(str(group.name))
                    ret_ += "\n╠ ไอดีกลุ่ม:{}".format(group.id)
                    ret_ += "\n╠ ผู้สร้างกลุ่ม : {}".format(str(gCreator))
                    ret_ += "\n╠ สมาชิกกลุ่ม : {}".format(str(len(group.members)))
                    ret_ += "\n╠ ค้างเชิญ : {}".format(gPending)
                    ret_ += "\n╠ กลุ่มตั๋ว:{}".format(gQr)
                    ret_ += "\n╠ ลิ้งกลุ่ม : {}".format(gTicket)
                    ret_ += "\n╚══[ Finish ]"
                    nadya.sendMessage(to, str(ret_))
                    nadya.sendImageWithURL(to, path)
                elif text.lower() == 'รายชื่อสมาชิกกลุ่ม':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        ret_ = "╔══[ รายชื่อสมชิกกลุ่ม ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ จำนวนสมาชิก {} คน(。-`ω´-) ]".format(str(len(group.members)))
                        nadya.sendMessage(to, str(ret_))
                elif text.lower() == '.รายชื่อกลุ่ม':
                        groups = nadya.groups
                        ret_ = "╔══[ รายชื่อกลุ่ม ]"
                        no = 0 + 1
                        for gid in groups:
                            group = nadya.getGroup(gid)
                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n╚══[ จำนวนกลุ่ม {} กลุ่ม(。-`ω´-)]".format(str(len(groups)))
                        nadya.sendMessage(to, str(ret_))
#==============================================================================#          
                elif text.lower() == '.แทค':
                    group = nadya.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        nadya.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        nadya.sendMessage(to, "จำนวนสมาชิก {} คน(。-`ω´-)".format(str(len(nama))))          
                elif text.lower() == '\หาคนอ่าน on':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read['readPoint']:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                pass
                            read['readPoint'][msg.to] = msg.id
                            read['readMember'][msg.to] = ""
                            read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                            read['ROM'][msg.to] = {}
                            with open('read.json', 'w') as fp:
                                json.dump(read, fp, sort_keys=True, indent=4)
                                nadya.sendMessage(msg.to,"เปิดหาคนซุ่ม(。-`ω´-)")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open('read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            nadya.sendMessage(msg.to, "Set reading point:\n" + readTime)
                            
                elif text.lower() == '\หาคนอ่าน off':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to not in read['readPoint']:
                        nadya.sendMessage(msg.to,"ปิดหาคนซุ่ม(。-`ω´-)")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                              pass
                        nadya.sendMessage(msg.to, "Delete reading point:\n" + readTime)
    
                elif text.lower() == '\หาคนซุ่ม reset':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read["readPoint"]:
                        try:
                            del read["readPoint"][msg.to]
                            del read["readMember"][msg.to]
                            del read["readTime"][msg.to]
                        except:
                            pass
                        nadya.sendMessage(msg.to, "Reset reading point:\n" + readTime)
                    else:
                        nadya.sendMessage(msg.to, "Lurking belum diaktifkan ngapain di reset?")
                        
                elif text.lower() == '.อ่าน':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if receiver in read['readPoint']:
                        if read["ROM"][receiver].items() == []:
                            nadya.sendMessage(receiver,"[ Reader ]:\nNone")
                        else:
                            chiya = []
                            for rom in read["ROM"][receiver].items():
                                chiya.append(rom[1])
                            cmem = nadya.getContacts(chiya) 
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = '[ Reader ]:\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan+"@c\n"
                            xlen = str(len(zxc)+len(xpesan))
                            xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan+ zxc + "\n[ Lurking time ]: \n" + readTime
                        try:
                            nadya.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                        except Exception as error:
                            print (error)
                        pass
                    else:
                        nadya.sendMessage(receiver,"Lurking has not been set.")
#==============================================================================#
            elif msg.text.lower().startswith(".พูด "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'th'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    nadya.sendAudio(msg.to,"hasil.mp3")
#==============================================================================#
            elif msg.contentType == 7:
                if settings["checkSticker"] == True:
                    stk_id = msg.contentMetadata['STKID']
                    stk_ver = msg.contentMetadata['STKVER']
                    pkg_id = msg.contentMetadata['STKPKGID']
                    ret_ = "╔══( ข้อมูลสติกเกอร์ )"
                    ret_ += "\n╠ สติกเกอร์ id : {}".format(stk_id)
                    ret_ += "\n╠ แพคเกจสติกเกอร์ : {}".format(pkg_id)
                    ret_ += "\n╠ เวอร์ชั่นสติกเกอร: {}".format(stk_ver)
                    ret_ += "\n╠ ลิ้งสติกเกอร์ : line://shop/detail/{}".format(pkg_id)
                    ret_ += "\n╚══( ข้อมูลสติกเกอร์ )"
                    nadya.sendMessage(to, str(ret_))
            elif msg.contentType == 1:
                        if settings["changePictureProfile"] == True:
                            path = nadya.downloadObjectMsg(msg_id)
                            settings["changePictureProfile"] = False
                            nadya.updateProfilePicture(path)
                            nadya.sendMessage(to, "เปลี่ยนโปรไฟล์สำเร็จแล้ว(。-`ω´-)")
            elif msg.contentType == 13:
                if settings["copy"] == True:
                    _name = msg.contentMetadata["displayName"]
                    copy = msg.contentMetadata["mid"]
                    groups = nadya.getGroup(msg.to)
                    targets = []
                    for s in groups.members:
                        if _name in s.displayName:
                            print ("[Target] Copy")
                            break                             
                        else:
                            targets.append(copy)
                    if targets == []:
                        nadya.sendText(msg.to, "Not Found...")
                        pass
                    else:
                        for target in targets:
                            try:
                                nadya.cloneContactProfile(target)
                                nadya.sendMessage(msg.to, "Berhasil clone member tunggu beberapa saat sampai profile berubah")
                                settings['copy'] = False
                                break
                            except:
                                     msg.contentMetadata = {'mid': target}
                                     settings["copy"] = False
                                     break                     
                    

#==============================================================================#
        if op.type == 26:
            print ("[ 26 ] RECEIVE MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != nadya.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                
                if op.type == 5:
                    if RfuProtect["autoAdd"] == True:
                        if (settings["message"] in [""," ","\n",None]):
                            pass
                    else:
                        nadya.sendMessage(op.param1,str(settings["message"]))
                        
                if settings["autoRead"] == True:
                    nadya.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        nadya.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in nadyaMID and msg.toType == 2:
                    if "MENTION" in list(msg.contentMetadata.keys())!= None:
                        if settings['potoMention'] == True:
                             contact = nadya.getContact(msg._from)
                             cName = contact.pictureStatus
                             balas = ["http://dl.profile.line-cdn.net/" + cName]
                             ret_ = random.choice(balas)
                             mention = ast.literal_eval(msg.contentMetadata["MENTION"])
                             mentionees = mention["MENTIONEES"]
                             for mention in mentionees:
                                   if mention["M"] in nadyaMID:
                                          nadya.sendImageWithURL(to,ret_)
                                          break
                if msg.contentType == 0 and sender not in nadyaMID and msg.toType == 2:
                    if "MENTION" in list(msg.contentMetadata.keys()) != None:
                         if settings['detectMention'] == True:
                            contact = nadya.getContact(msg._from)
                            cName = contact.displayName
                            balas = [cName + "\n" + str(settings["Tag"])]
                            ret_ = "" + random.choice(balas)
                            name = re.findall(r'@(\w+)', msg.text)
                            mention = ast.literal_eval(msg.contentMetadata["MENTION"])
                            mentionees = mention['MENTIONEES']
                            for mention in mentionees:
                                  if mention['M'] in nadyaMID:
                                         nadya.sendMessage(to,ret_)
                                         sendMessageWithMention(to, contact.mid)
                                         break

                if msg.contentType == 16:
                   url = msg.contentMetadata['postEndUrl']
                   nadya.like(url[25:58], url[66:], likeType=1001)
                   nadya.comment(url[25:58], url[66:], wait["comment1"])

                if msg.text in ["Speed","speed","Sp","sp",".Sp",".sp",".Speed",".speed","\Sp","\sp","\speed","\Speed"]:
                    nadya.sendMessage(to, "แรงแล้วครับพี่😆")
                if msg.text in ["Me","me","คท","!me","!Me",".me",".Me"]:
            	    nadya.sendMessage(to, "เช็คจังหนังกระโปก😋")
                if msg.text in ["ออน",".ออน","\ออน",".uptime",".Uptime"]:
                	nadya.sendMessage(to, "ออนนานเกิ๊น😘")
                if msg.text in [".มอง","มอง"]:
                	nadya.sendMessage(to, "มองจังไอสัส😉")
                if msg.text in ["5","55","555","5555","55555","555555","5555555"]:
                	nadya.sendMessage(to, "ขำเหี้ยไรสัส😒")
                if msg.text in ["--","-.-","-..-","-,,-","-,-","+.+","*-*","-*-","=-=","=.=","=_=","._.",".__.","=="]:
                	nadya.sendMessage(to, "หน้าหีมากสัส😋")
                if msg.text in [".","..","...","....",".....","......",".......","........",".........","............","..................."]:
                	nadya.sendMessage(to, "จุดจบมึง?😎")
                if msg.text in ["Tag","tagall","แทค","แทก","Tagall","tag"]:
                	nadya.sendMessage(to,"แทคทำควยไร😃")
                if msg.text in ["กำ",".กำ"]:
                	nadya.sendMessage(to,"กำไรดีควยหรือหี😌")
                if msg.text in [".ขำ",".ขรรม","ขำ","ขรรม","ขำๆ"]:
                	nadya.sendMessage(to,"ขำทำเหี้ยไร😝")

#==============================================================================#
        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
