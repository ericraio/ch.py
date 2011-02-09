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

if __name__ == "__main__": Test.easy_start()
