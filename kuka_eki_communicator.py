import time

from lib_py.imports import MatrixPose, ET, sys, socket

class KukaEKICommunicator:
    def __init__(self, host, port):
        self.port = port
        self.host = host
        # initializing the xml msg
        self.xml_msg = '<Sensor><Status Reset="true"></Status><Data NumberOfToolPaths="0"></Data><BaseFrame X="0" Y="0" Z="0" A="0" B="0" C="0"></BaseFrame></Sensor>'
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_data(self, NumberOfToolPaths=0, base_x = 0, base_y = 0, base_z = 0, base_a = 0, base_b = 0, base_c = 0,):
        xml = self.xml_msg
        sensor = ET.fromstring(xml)
        data = sensor.find('Data')
        data.set('NumberOfToolPaths', str(NumberOfToolPaths))
        base = sensor.find('BaseFrame')
        base.set('X', str(round(base_x,2)))
        base.set('Y', str(round(base_y,2)))
        base.set('Z', str(round(base_z,2)))
        base.set('A', str(round(base_a,2)))
        base.set('B', str(round(base_b,2)))
        base.set('C', str(round(base_c,2)))
        xmlstr = ET.tostring(sensor,encoding="utf-8",short_empty_elements=False)
        print(xmlstr)
        self.client_socket.send(xmlstr);
        data = self.client_socket.recv(1024)
        print('data:', data)

    def receive_data(self):
        tcp_pose = []
        flange_pose = []
        joints = []
        xml = self.xml_msg
        sensor = ET.fromstring(xml)
        xmlstr = ET.tostring(sensor)
        # self.client_socket.send(xmlstr);
        rec = self.client_socket.recv(1024)
        rec = rec.decode('UTF-8')
        # rec = '<Robot><PartID ID="0"></PartID><Data><ActPos X="10" Y="5" Z="6" A="7" B="8" C="9" /><FlangePos X="10" Y="5" Z="6" A="7" B="8" C="9" /><Joints A1="10" A2="5" A3="6" A4="7" A5="8" A6="9" /></Data></Robot>'
        # print('data:',rec)
        robot = ET.fromstring(rec)
        part_id = robot.find('PartID')
        data = robot.find('Data')
        actpos = data.find('ActPos')
        flangepos = data.find('FlangePos')
        jointss = data.find('Joints')

        part_id = part_id.attrib['ID']
        tcp_pose.append(actpos.attrib['X'])
        tcp_pose.append(actpos.attrib['Y'])
        tcp_pose.append(actpos.attrib['Z'])
        tcp_pose.append(actpos.attrib['A'])
        tcp_pose.append(actpos.attrib['B'])
        tcp_pose.append(actpos.attrib['C'])

        flange_pose.append(flangepos.attrib['X'])
        flange_pose.append(flangepos.attrib['Y'])
        flange_pose.append(flangepos.attrib['Z'])
        flange_pose.append(flangepos.attrib['A'])
        flange_pose.append(flangepos.attrib['B'])
        flange_pose.append(flangepos.attrib['C'])

        joints.append(jointss.attrib['A1'])
        joints.append(jointss.attrib['A2'])
        joints.append(jointss.attrib['A3'])
        joints.append(jointss.attrib['A4'])
        joints.append(jointss.attrib['A5'])
        joints.append(jointss.attrib['A6'])
        print(rec)
        # time.sleep(0.2)
        self.client_socket.send(xmlstr);

        return part_id,tcp_pose, flange_pose, joints