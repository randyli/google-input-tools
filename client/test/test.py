import ipc_pb2
import time
import sys
import win32pipe, win32file, pywintypes


import mmap
import struct
def GetPipeName():
	shm = mmap.mmap(0, 4,'Local\\GoopyIPCSharedMemory', access=mmap.ACCESS_READ)
	sid = shm.read(4)
	sid = struct.unpack("I", sid)
	print(sid)
#GetPipeName()
#quit()

handle = win32file.CreateFile(
                    r'\\.\\pipe\\com_google_ime_goopy_2ipc_server',
                    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                    0,
                    None,
                    win32file.OPEN_EXISTING,
                    0,
                    None)


def Send(msg):
	pack = msg.SerializeToString()
	data = struct.pack('I', len(pack)+4)
	win32file.WriteFile(handle, data+pack)
	if msg.reply_mode == 1:
		rc,resp = win32file.ReadFile(handle, 1024)
		res = ipc_pb2.Message()
		res.ParseFromString(resp[4:])
		return res

class MyComponet:
	def reg(self):
		### register componet message
		msg = ipc_pb2.Message()
		msg.type = 1#0x0204
		msg.reply_mode = 1
		component_info = ipc_pb2.ComponentInfo()
		component_info.string_id = 'input_in_python'
		component_info.produce_message.append(0x0020)
		component_info.produce_message.append(0x0200)
		component_info.produce_message.append(0x0201)
		component_info.produce_message.append(0x0204)
		component_info.produce_message.append(0x0205)
		msg.payload.component_info.append(component_info)

		rep = Send(msg)
		print(rep)
		self.source = rep.payload.component_info[0].id
	
	def showToolBar(self):
		### show tool bar
		msg = ipc_pb2.Message()
		msg.type = 0x0204
		msg.reply_mode = 1
		msg.source = self.source
		print(msg)
		rep = Send(msg)
		print(rep)



	def hideToolBar(self):
		### hide tool bar
		msg = ipc_pb2.Message()
		msg.type = 0x0205
		msg.reply_mode = 1
		msg.source = self.source
		print(msg)
		rep = Send(msg)
		print(rep)

	def createContext(self):
		msg = ipc_pb2.Message()
		msg.type = 0x0020
		msg.reply_mode = 1
		msg.source = self.source
		print(msg)
		rep = Send(msg)
		print(rep)
		self.icid = rep.icid
	def attachContext(self):
		pass

comp = MyComponet()
comp.reg()
comp.showToolBar()
quit()
comp.createContext()
time.sleep(3)
quit()
### show composition ui
msg = ipc_pb2.Message()
msg.type = 0x0200
msg.reply_mode = 1
msg.source = source
print(msg)
rep = Send(msg)
print(rep)

#while True:

handle.close()
