from avp_stream import VisionProStreamer
#####################################################此文件用于测试遥操##################################

avp_ip = "10.100.4.155"   # example IP 
s = VisionProStreamer(ip = avp_ip, record = True)

while True:
    r = s.latest
    print(r['head'], r['right_wrist'], r['right_fingers'])