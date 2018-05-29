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
                client.inviteIntoGroup(op.param1, ["u653b0286edecac66ae69e8a71067d881", "ud2eff6e0613cacf1618fb2f2a4bc5a0b", "ue91bf08b799cceda8c02caabd3297073"])
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
                    print("\n")
                    print("Private Chat Message Received")
                    print("Sender's Name : " + client.getContact(msg._from).displayName)
                    print("Sender's MID : " + msg._from)
                    print("Received Message : " + msg.text)
                    print("\n")
                    if msg._from in whiteListedMid:
                        if msg.text.startswith("/contact"):
                            str1 = find_between_r(msg.text, "/contact ", "")
                            client.sendContact(msg._from, str1)
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
                            client.sendMessage("u653b0286edecac66ae69e8a71067d881",
                                               "/jgurl gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                            client.sendMessage("ud2eff6e0613cacf1618fb2f2a4bc5a0b",
                                               "/jgurl gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                            client.sendMessage("ue91bf08b799cceda8c02caabd3297073",
                                               "/jgurlx gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                        if msg.text == "/help":
                            client.sendMessage(msg._from,
                                        "用戶指令:\n\n/help\n/contact <MID>\n/mid\n/jgurl <gid: GID gid> <url: gurl url>\n/send chat <mid: MID mid> <text: TEXT text>\n/send group <gid: GID gid> <text: TEXT text>\n/send chat contact <mid: MID mid> <cmid: CONTACT MID cmid>\n/send group contact <gid: GID gid> <cmid: CONTACT MID cmid>\n/kick <gid: GID gid> <mid: MID mid>\n\n群組指令:\n\n/gid\n/ginfo\n/kick <MID>\n/gurl on\n/gurl off\n/bye")
                        if msg.text == "/mid":
                            client.sendMessage(msg._from, "Name : " + client.getContact(msg._from).displayName + "\nMID : " + msg._from + "\nPermission Level : 5")
                        if msg.text == "/speed":
                            time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                            str1 = str(time0)
                            client.sendMessage(msg._from, str1)
                        if msg.text.startswith("/send chat"):
                            str1 = find_between_r(msg.text, "mid: ", " mid")
                            str2 = find_between_r(msg.text, "text: ", " text")
                            client.sendMessage(str1, str2)
                        if msg.text.startswith("/send group"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "text: ", " text")
                            client.sendMessage(str1, str2)
                        if msg.text.startswith("/send chat contact"):
                            str1 = find_between_r(msg.text, "mid: ", " mid")
                            str2 = find_between_r(msg.text, "cmid: ", " cmid")
                            client.sendContact(str1, str2)
                        if msg.text.startswith("/send group contact"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "cmid: ", " cmid")
                            client.sendContact(str1, str2)
                        if msg.text.startswith("/kick"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "mid: ", " mid")
                            try:
                                client.kickoutFromGroup(str1, [str2])
                            except Exception as e:
                                print(e)
                    elif msg._from in whiteListedMid:
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
                elif msg.toType == 1:
                    pass
                elif msg.toType == 2:
                    if msg._from in whiteListedMid:
                        if msg.text == "/gid":
                            client.sendMessage(msg.to, msg.to)
                        if msg.text == "/ginfo":
                            group = client.getGroup(msg.to)
                            md = "[群組名稱]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[群組圖片]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                            if group.preventedJoinByTicket is False:
                                md += "\n\n行動網址: 開啟\n"
                            else:
                                md += "\n\n行動網址: 關閉\n"
                            if group.invitee is None:
                                md += "\n成員數: " + str(len(group.members)) + "人\n\n邀請中: 0人"
                            else:
                                md += "\n成員數: " + str(len(group.members)) + "人\n邀請中: " + str(
                                    len(group.invitee)) + "人"
                                client.sendMessage(msg.to, md)
                        if msg.text == "/speed":
                            time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                            str1 = str(time0)
                            client.sendMessage(msg.to, str1)
                        if msg.text.startswith("/contact"):
                            str1 = find_between_r(msg.text, "/contact ", "")
                            client.sendContact(msg.to, str1)
                        if msg.text == "/mid":
                            client.sendMessage(msg.to, "名字 : " + client.getContact(msg._from).displayName + "\nMID : " + msg._from + "\n權限等級 : 5")
                        if msg.text == "/bye":
                            client.leaveGroup(msg.to)
                            JoinedGroups.remove(msg.to)
                        if msg.text == "/gurl on":
                            group = client.getGroup(msg.to)
                            try:
                                group.preventedJoinByTicket = False
                                str1 = client.reissueGroupTicket(msg.to)
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                            client.sendMessage(msg.to, "http://line.me/R/ti/g/" + str1)
                        if msg.text == "/gurl off":
                            group = client.getGroup(msg.to)
                            try:
                                client.reissueGroupTicket(msg.to)
                                group.preventedJoinByTicket = True
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                        if msg.text.startswith("/kick"):
                            str1 = find_between_r(msg.text, "/kick ", "")
                            if str1 not in whiteListedMid:
                                try:
                                    client.kickoutFromGroup(msg.to, [str1])
                                except Exception as e:
                                    print(e)
                                return
                else:
                    pass
            except:
                pass
        elif msg.contentType == 13:
            if msg.toType == 0:
                if msg._from in whiteListedMid:
                    x = op.message.contentMetadata
                    str1 = str(x)
                    str2 = find_between_r(str1, "'mid': '", "'")
                    str3 = find_between_r(str1, "'mid': '", "', '")
                    if "displayName" in str2:
                        strx = str(str3)
                        client.sendMessage(msg._from, strx)
                    else:
                        strx2 = str(str2)
                        client.sendMessage(msg._from, strx2)
                    print("\n")
                    print("Private Chat Contact Received")
                    print("Sender's Name : " + client.getContact(msg._from).displayName)
                    print("Sender's MID : " + msg._from)
                    print("Received Contact MID : " + str2)
                    print("Received Contact Display Name : " + client.getContact(str2).displayName)
                    print("\n")
                else:
                    x = op.message.contentMetadata
                    str1 = str(x)
                    str2 = find_between_r(str1, "'mid': '", "'")
                    str3 = find_between_r(str1, "'mid': '", "', '")
                    if "displayName" in str2 and str3 not in whiteListedMid:
                        strx = str(str3)
                        client.sendMessage(msg._from, strx)
                    elif str2 not in whiteListedMid:
                        strx2 = str(str2)
                        client.sendMessage(msg._from, strx2)
                    print("\n")
                    print("Private Chat Contact Received")
                    print("Sender's Name : " + client.getContact(msg._from).displayName)
                    print("Sender's MID : " + msg._from)
                    print("Received Contact MID : " + str2)
                    print("Received Contact Display Name : " + client.getContact(str2).displayName)
                    print("\n")
            elif msg.toType == 1:
                pass
            elif msg.toType == 2:
                x = op.message.contentMetadata
                str1 = str(x)
                str2 = find_between_r(str1, "'mid': '", "'")
                str3 = find_between_r(str1, "'mid': '", "', '")
                if "displayName" in str2 and str3 not in whiteListedMid:
                    strx = str(str3)
                    client.sendMessage(msg.to, strx)
                elif str2 not in whiteListedMid:
                    strx2 = str(str3)
                    client.sendMessage(msg.to, strx2)
                    print("Contact Received, MID : " + str2)
        else:
            pass
    except Exception as error:
        print(error)
        print ("\n\nRECEIVE_MESSAGE\n\n")
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
