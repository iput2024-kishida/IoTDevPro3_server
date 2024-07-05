# Work08 (IoT Device Programming 3 Week 8)
# Group 3
# Created by Shotar Noda(TK220137) on 2024/07/05.

from datetime import timedelta, timezone, datetime
import socket, os, json
from dotenv import load_dotenv
from time import sleep
load_dotenv()

def get_current_date():
  return datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo'))

def save_csv(list_data):
  now = get_current_date
  with open(f'data/{now.strftime("%Y%m%d_%H%M%S")}.csv', mode="w") as f:
    for row in list_data:
      print(*row, sep=',', file=f)
  f.close()
  
def start_server():
  socket_w = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  socket_w.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
  socket_w.bind((os.getenv('SERVER_ADDR'), os.getenv('WAITING_PORT')))
  socket_w.listen(5)
  
  try:
    while True:
      socket_s_r, client_address = socket_w.accept()
      print(f"[{get_current_date}]Connection from {str(client_address)} has been established.")

      data_r = socket_s_r.recv(1024)
      data_r_j = data_r.decode('utf-8')
      data_r_list = json.loads(data_r_j)
      
      data_listed = []
      for i in range(len(data_r_list)):
          print(data_r_list[i])
          single_data = data_r_list[i]
          data_listed.append([single_data["temp_dht"], single_data["humid_dht"]])
          
      save_csv(data_listed)
      print(f"[{get_current_date}]CSV saved.")
      
      sleep(5)
      socket_s_r.close()
      
  except KeyboardInterrupt:
    socket_s_r.close()
    socket_w.close()
    print(f"[{get_current_date}]Server Stopped!")
    
