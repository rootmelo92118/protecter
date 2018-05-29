from linepy import *
import timeit
from time import strftime
import time


client = LINE()
client.log("Auth Token : " + str(client.authToken))
#client = LINE('email', 'password')

oepoll = OEPoll(client)

MySelf = client.getProfile()
JoinedGroups = client.getGroupIdsJoined()
print("My MID : " + MySelf.mid)

whiteListedMid = ["u2ee4fe577cac70ba27136ebe72e2835c", "ua0131a1d94b182df6e00415dfc0781bf", "u653b0286edecac66ae69e8a71067d881", "ud2eff6e0613cacf1618fb2f2a4bc5a0b", "ue91bf08b799cceda8c02caabd3297073"]

#mymid : ""


def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        if op.param1 not in JoinedGroups:
            if op.param2 in whiteListedMid:
                client.acceptGroupInvitation(op.param1)
                JoinedGroups.append(op.param1)
            else:
                client.acceptGroupInvitation(op.param1)
                JoinedGroups.append(op.param1)
                client.leaveGroup(op.param1)
                JoinedGroups.remove(op.param1)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_INVITE_INTO_GROUP\n\n")
        return


def NOTIFIED_UPDATE_GROUP(op):
    group = client.getGroup(op.param1)
    if op.param2 not in whiteListedMid:
        if op.param3 == "4":
            if group.preventedJoinByTicket == False:
                try:
                    client.reissueGroupTicket(op.param1)
                    group.preventedJoinByTicket = True
                    client.updateGroup(group)
                    client.kickoutFromGroup(op.param1, [op.param2])
                except Exception as e:
                    print(e)


def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    # print op
    try:
        b = open("b.txt", "r")
        blackListedMid = b.readline()
        b.close()
        if op.param2 in blackListedMid:
            try:
                client.kickoutFromGroup(op.param1, [op.param2])
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return


def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        if op.param3 == MySelf.mid:
            hb = open("hb.txt", "r")
            b = open("b.txt", "r")
            halfBlackListedMid = hb.readline()
            blackListedMid = b.readline()
            hb.close()
            b.close()
            if op.param2 not in halfBlackListedMid and op.param3 not in blackListedMid:
                hb = open("hb.txt", "w")
                hb.write(op.param2)
                hb.close()
            elif op.param2 in halfBlackListedMid:
                b = open("b.txt", "w")
                b.write(op.param2)
                b.close()
            JoinedGroups.remove(op.param1)
        else:
            if op.param3 in whiteListedMid:
                client.kickoutFromGroup(op.param1, [op.param2])
                group = client.getGroup(op.param1)
                if group.preventedJoinByTicket == True:
                    try:
                        group.preventedJoinByTicket = False
                        str1 = client.reissueGroupTicket(op.param1)
                        client.updateGroup(group)
                        client.sendMessage(op.param3,
                                           "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    except Exception as e:
                        print(e)
                else:
                    try:
                        str1 = client.reissueGroupTicket(op.param1)
                        client.updateGroup(group)
                        client.sendMessage(op.param3,
                                           "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    except Exception as e:
                        print(e)
            if op.param2 not in whiteListedMid:
                try:
                    client.kickoutFromGroup(op.param1, [op.param2])
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return


def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.toType == 0:
                    if msg._from in whiteListedMid:
                        if msg.text.startswith("/jgurlx"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                            client.acceptGroupInvitationByTicket(str1, str2)
                            JoinedGroups.append(str1)
                            group = client.getGroup(str1)
                            try:
                                client.reissueGroupTicket(str1)
                                group.preventedJoinByTicket = True
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                        elif msg.text.startswith("/jgurl"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                            client.acceptGroupInvitationByTicket(str1, str2)
                            JoinedGroups.append(str1)
                            client.sendMessage("ue91bf08b799cceda8c02caabd3297073",
                                               "/jgurlx gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                elif msg.toType == 2:
                      if msg._from in whiteListedMid:
                          if msg.text == "/bye":
                              client.leaveGroup(msg.to)
                              JoinedGroups.remove(msg.to)
                else:
                    pass
            except:
                pass
        else:
            pass
    except Exception as error:
        print(error)
        print("\n\nRECEIVE_MESSAGE\n\n")
        return


oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.NOTIFIED_KICKOUT_FROM_GROUP: NOTIFIED_KICKOUT_FROM_GROUP,
    OpType.NOTIFIED_ACCEPT_GROUP_INVITATION: NOTIFIED_ACCEPT_GROUP_INVITATION,
    OpType.NOTIFIED_UPDATE_GROUP: NOTIFIED_UPDATE_GROUP,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""


while True:
    oepoll.trace()
