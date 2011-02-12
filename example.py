import ch
import random
import sys
import re
if sys.version_info[0] > 2:
	import urllib.request as urlreq
else:
	import urllib2 as urlreq

dictionary = dict() #volatile... of course...

dancemoves = [
	"(>^.^)>",
	"(v^.^)v",
	"v(^.^v)",
	"<(^.^<)"
]

class TestBot(ch.RoomManager):
	def onInit(self):
		self.setNameColor("F9F")
		self.setFontColor("F33")
		self.setFontFace("1")
		self.setFontSize(10)
		self.enableBg()
		self.enableRecording()
	
	def onConnect(self, room):
		print("Connected")
	
	def onReconnect(self, room):
		print("Reconnected")
	
	def onDisconnect(self, room):
		print("Disconnected")
	
	def onMessage(self, room, user, message):
		if room.getLevel(self.user) > 0:
			print(user.name, message.ip, message.body)
		else:
			print(user.name, message.body)
		if self.user == user: return
		if message.body[0] == "!":
			data = message.body[1:].split(" ", 1)
			if len(data) > 1:
				cmd, args = data[0], data[1]
			else:
				cmd, args = data[0], ""
			if   cmd == "delay":
				self.setTimeout(int(args), room.message, ":D")
			elif cmd == "randomuser":
				room.message(random.choice(room.usernames))
			elif cmd == "ival":
				self.setInterval(int(args), room.message, ":D")
			elif cmd == "mylvl":
				room.message("Your mod level: %i" %(room.getLevel(user)))
			elif cmd == "mods":
				room.message(", ".join(room.modnames + [room.ownername]))
			elif cmd == "dance":
				for i, msg in enumerate(dancemoves):
					self.setTimeout(i / 2, room.message, msg)
			elif cmd == "td":
				word = args\
					.replace(" ", "%20")\
					.replace("&", "%26")\
					.replace("%", "%25")\
					.replace("<", "%3C")\
					.replace("=", "%3D")
				def rfinish(doc):
					doc = doc.read().decode()
					m = re.search("<h1>(.*?)</h1>\n(.*?)<BR><i>(.*)</i>", doc, re.DOTALL | re.IGNORECASE)
					if m:
						room.message(("<b>%s:</b> <i>%s</i> - %s" %(m.group(1), m.group(2), m.group(3))).replace("%20", " "), html = True)
					else:
						room.message("An error occured...")
				self.deferToThread(rfinish, urlreq.urlopen, "http://thesurrealist.co.uk/slang.cgi?ref=" + word)
			elif cmd == "ismod":
				user = ch.User(args)
				if room.getLevel(user) > 0:
					room.message("yes")
				else:
					room.message("no")
			elif cmd == "define":
				if args.find(":") != -1: #if there's a colon somewhere
					word, definition = args.split(":", 1)
					if word in dictionary:
						room.message(word + ": already defined")
					else:
						dictionary[word] = definition
						room.message(word + ": " + definition)
				else:
					word = args
					if word in dictionary:
						room.message(word + ": " + dictionary[word])
					else:
						room.message(word + ": not found")
	
	def onFloodWarning(self, room):
		room.reconnect()
	
	def onJoin(self, room, user):
		room.message("hello, " + user.name + "!")
	
	def onLeave(self, room, user):
		room.message("bye, " + user.name + "!")
	
	def onUserCountChange(self, room):
		print("users: " + str(room.usercount))
	
	def onMessageDelete(self, room, user, msg):
		room.message("a message got deleted! " + user.name + ": " + msg.body)

if __name__ == "__main__": TestBot.easy_start()
