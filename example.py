import ch
import random

class TestBot(ch.RoomManager):
	def onConnect(self, room):
		print("Connected")
		room.enableBg()
		room.enableRecording()
		room.setNameColor("F9F")
		room.setFontColor("F33")
		room.setFontFace("1")
		room.setFontSize(10)
	
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
			elif cmd == "ismod":
				user = ch.User(args)
				if room.getLevel(user) > 0:
					room.message("yes")
				else:
					room.message("no")
	
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
