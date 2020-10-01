# import socket
# import multiprocessing
# import json
# import threading


# class TcpClient:
#     def __init__(self, ip, port, buffer_size=1024):
#         self.ip = ip
#         self.port = port
#         self.buffer_size = buffer_size
#         self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.send_queue = multiprocessing.Queue()
#         self.recv_json_queue = multiprocessing.Queue()
#         self.recv_string_queue = multiprocessing.Queue()

#     def run(self):
#         self.connect()
#         send_thread = threading.Thread(target=self.send)
#         send_thread.start()
#         recv_thread = threading.Thread(target=self.recv)
#         recv_thread.start()

#     def connect(self):
#         print("connect called")
#         self.client_socket.connect((self.ip, self.port))
#         self.connected = True
#         print("TcpClient - Connected on {}:{}".format(self.ip, self.port))

#     def recv(self):
#         while self.connected:
#             try:
#                 data = self.client_socket.recv(self.buffer_size)
#             except:
#                 print("Error Receiving")
#                 # self.close_conn()
#                 break
#             if not data:
#                 print("Error: Not data")
#                 # self.close_conn()
#                 break
#             data_s = data.decode("utf-8")
#             data_arr = data_s.splitlines()
#             for data_str in data_arr:
#                 print("TcpClient - Received data: {}".format(data_str))
#                 if data_str[0] == "{":
#                     self.recv_json_queue.put(data_str)
#                 else:
#                     self.recv_string_queue.put(data_str)

#     def send(self):
#         # while self.connected:
#         if not self.send_queue.empty():
#             try:
#                 data = self.send_queue.get()
#                 self.client_socket.send((data + "\n").encode("utf-8"))
#                 print("TcpClient - Sent data: {}".format(data))
#             except:
#                 print("TcpClient - Error sending data: {}".format(data))
#                 # self.close_conn()
#                 # break

#     def get_json(self):
#         while self.recv_json_queue.empty() and self.connected:
#             pass
#         return self.recv_json_queue.get()

#     def get_string(self):
#         while self.recv_string_queue.empty():
#             pass
#         return self.recv_string_queue.get()

#     def send_command(self, command):
#         # self.send_queue.put(convertString.stringToList(command))
#         self.send_queue.put(command)

#     def send_status(self, status):
#         self.send_queue.put(json.dumps({"status": status}))

#     def send_event(self, event):
#         self.send_queue.put(json.dumps({"event": event}))

#     def send_robot_pos(self, pos):
#         self.send_queue.put(json.dumps({"robotPos": pos}))

#     def send_arena(self, arena):
#         self.send_queue.put(
#             json.dumps({"gridP1": arena.to_mdf_part1(), "gridP2": arena.to_mdf_part2()})
#         )

#     def close_conn(self):
#         try:
#             self.client_socket.close()
#             self.connected = False
#             print("TcpClient - Disconnected")
#         except:
#             pass

#     def send_movement(self, movement, multiplemovement):
#         try:
#             if not multiplemovement:
#                 string = "MDATA:" + movement
#                 self.send_command(string)
#                 self.send()
#                 print("-")
#             else:
#                 string = "MDATA"
#                 for index in range(len(movement)):
#                     string = string + ":" + movement[index]
#                 self.send_command(string)
#                 self.send()
#                 print("+")
#         except:
#             print("Something gone wrong")

#     def get_sensor_value(self):
#         # while(True):
#         try:
#             self.recv()
#             data = self.get_string()
#             sensorVal = data.split(":")  # 1:SRFL,2:SRFC,3:SRFR,4:SRTR,5:SRBR,6:SRL
#             """
#                 if(sensorVal[0] == "SDATA"):
#                 break
#             """
#         except:
#             print("No more sensor value")
#         return sensorVal



from configurations import *
import socket
import multiprocessing
import json
import threading


class TcpClient():
    def __init__(self, ip, port, buffer_size=1024):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_queue = multiprocessing.Queue()
        self.recv_json_queue = multiprocessing.Queue()
        self.recv_string_queue = multiprocessing.Queue()

    def run(self):
        self.connect()
        send_thread = threading.Thread(target=self.send)
        send_thread.start()
        recv_thread = threading.Thread(target=self.recv)
        recv_thread.start()

    def connect(self):
        print('connect called')
        self.client_socket.connect((self.ip, self.port))
        self.connected = True
        print("TcpClient - Connected on {}:{}".format(self.ip, self.port))

    def recv(self):
        while self.connected:
            try:
                data = self.client_socket.recv(self.buffer_size)
            except:
                self.close_conn()
                break
            if not data:
                self.close_conn()
                break
            data_s = data.decode('utf-8')
            data_arr = data_s.splitlines()
            for data_str in data_arr:
                print("TcpClient - Received data: {}".format(data_str))
                if data_str[0] == "{":
                    self.recv_json_queue.put(data_str)
                else:
                    self.recv_string_queue.put(data_str)

    def send(self):
        #while self.connected:
        if not self.send_queue.empty():
            try:
                data = self.send_queue.get()
                self.client_socket.send((data+"\n").encode('utf-8'))
                print("TcpClient - Sent data: {}".format(data))
            except:
                print("TcpClient - Error sending data: {}".format(data))
                self.close_conn()
                #break

    def get_json(self):
        while self.recv_json_queue.empty() and self.connected:
            pass
        return self.recv_json_queue.get()

    def get_string(self):
        while self.recv_string_queue.empty():
            pass
        return self.recv_string_queue.get()

    def send_command(self, command):
        #self.send_queue.put(convertString.stringToList(command))
        self.send_queue.put(command)

    def send_status(self, status):
        self.send_queue.put(json.dumps({"status": status}))

    def send_event(self, event):
        self.send_queue.put(json.dumps({"event": event}))

    def send_robot_pos(self, pos):
        self.send_queue.put(json.dumps({"robotPos": pos}))

    def send_arena(self, arena):
        self.send_queue.put(json.dumps(
            {"gridP1": arena.to_mdf_part1(), "gridP2": arena.to_mdf_part2()}))

    def close_conn(self):
        try:
            self.client_socket.close()
            self.connected = False
            print("TcpClient - Disconnected")
        except:
            pass



    def send_movement(self,type,movement,multiplemovement):
        try:
            if(not multiplemovement):
                if(type == Movement.FORWARD):
                    string = "A481"
                    self.send_command(string)
                    self.send()
                    print("Sending 1 moving forward command")
                elif(type == Movement.RIGHT or type == Movement.LEFT or type == Movement.CALIBRATE):
                    string = "A66" + movement
                    self.send_command(string)
                    self.send()
                    print("Sending Command:",movement)
            else:
                #This block is only for sending multiple forward commands
                string = "A48" + str(multiplemovement)
                self.send_command(string)
                self.send()
                print("Sending Multiple Forward Movement")
        except Exception as inst:
            print("Error sending movement commands", inst)



    def get_sensor_value(self):
        print("Getting sensor value.....")
        try:
            string = "A66"+Movement.READ_SENSOR.value
            self.send_command(string)
            self.send()
            self.recv()
            data = self.get_string()
            sensorVal = data.split(":") #1:SRFL,2:SRFC,3:SRFR,4:SRTR,5:SRBR,6:SRL
        except:
            print("Error reading sensor value. Might need to call while loop to continue waiting for input....")
        return sensorVal


    def take_picture(self,coordinate):
        print("Taking Picture.....")
        try:
            string = "XP"
            self.send_command(string)
            self.send()
        except:
            print("Error sending take picture commands to RPI")

    def get_android_command(self):
        print("Listening for Android command...")
        try:
            self.recv()
            data = self.get_string()
            command = data.strip()
            print("Receive Android command:"+command)
        except:
            print("Error receiving Android command")
        return command