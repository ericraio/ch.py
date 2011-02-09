import ch
from example import Test

class TestManager(ch.RoomManager):
	_RoomConnection = Test

TestManager().easy_start()
