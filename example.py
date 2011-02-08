import ch
import random

class Test(ch.RoomConnection):
	def onConnect(self):
		print("Connected")
		self.enableBg()
		self.enableRecording()
		self.setNameColor("F9F")
		self.setFontColor("F33")
		self.setFontFace("1")
		self.setFontSize(10)
	
	def onReconnect(self):
		print("Reconnected")
	
	def onDisconnect(self):
		print("Disconnected")
	
	def onHistoryMessage(self, user, message):
		print(user.name, message.body)
	
	def onMessage(self, user, message):
		print(user.name, message.body)
		if self.user == user: return
		if message.body == "spam":
			for i in range(2):
				self.message("blehh")
		elif message.body == "mods":
			self.message(", ".join(self.modnames))
		elif message.body == "mimic":
			self.rawMessage(message.raw)
		elif message.body == "randomuser":
			self.message(random.choice(self.usernames))
		elif message.body[:5] == "nick ":
			user.nick = message.body[5:]
			self.message("your nick was set to " + message.body[5:])
		elif message.body == "hi":
			nick = user.nick
			if not nick: nick = user.name
			self.message("hi, " + nick)
	
	def onFloodWarning(self):
		self.reconnect()
	
	def onJoin(self, user):
		self.message("hello, " + user.name + "!")
	
	def onLeave(self, user):
		self.message("bye, " + user.name + "!")
	
	def onUserCountChange(self):
		print("users: " + str(self.usercount))
	
	def onMessageDelete(self, user, msg):
		self.message("a message got deleted! " + user.name + ": " + msg.body)

Test.easy_start()
