import socket
import sys
import subprocess
try:
    import xml.etree.ElementTree as ET
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'elementpath'])
finally:
    import xml.etree.ElementTree as ET


class Kuka:
    """
    A class used to represent the kuka robot

    ...

    Attributes
    ----------
    host : str
        The robot's IP address
    port : int
        The port of the robt
    xml_msg : str
        The initial XML message for EKI
    client_socket : socket
        Client for socket connection

    Methods
    -------
    set_base(base_frame)
        sets the robot's base frame for the program.

        Parameters:
        ---------
        base_frame: list that contains the new base frame. The elements of the list must be float/int. [X,Y,Z,A(Rz),B(Ry),C(Rx)]

    set_tcp(tcp_frame)
        sets the robot's tcp frame for the program.

        Parameters:
        --------
        tcp_frame: list that contains the new tcp frame. The elements of the list must be float/int. [X,Y,Z,A(Rz),B(Ry),C(Rx)]

    set_acc_speed(acceleration,speed)
        sets the robot's acceleration and speed

        Parameters:
        --------
        acceleration: float/int unit = mm/s^2
        speed: float/int unit mm/s

    move_j(joints_pose)
        performs the PTP motion

        Parameters:
        --------
        joints_pose: list that contains the joints angles. The elements of the list must be float/int. [A1,A2,A3,A4,A5,A6]

    move_lin(poses)
        performs the linear motion either for a single waypoint or multiple waypoints

        Parameters:
        --------
        poses: list of lists that contain the waypoints.
        [[X1,Y1,Z1,A1(Rz),B1(Ry),C1(Rx)], [X2,Y2,Z2,A2(Rz),B2(Ry),C2(Rx)], ...., [Xn,Yn,Zn,An(Rz),Bn(Ry),Cn(Rx)]]

    get_current_state()
        returns the current state of the robot:
        1) tcp_pose [X,Y,Z,A(Rz),B(Ry),C(Rx)]
        2) flange_pose [X,Y,Z,A(Rz),B(Ry),C(Rx)]
        3) joints [A1,A2,A3,A4,A5,A6]
    set_digout(number,value)
        sets the output of the robot.

        Parameters:
        --------
        number: The index of the robot's digital output that you want to change. Data type: INT
        value: True or false.  Data type: Bool

    set_digin(number,value)
        sets the output of the robot.

        Parameters:
        --------
        number: The index of the robot's digital input that you want to change. Data type: INT
        value: True or false.  Data type: Bool

    call_subroutine()
        calls a subroutine in the program
    """
    def __init__(self, host, port):
        self.port = port
        self.host = host
        #initializing the xml msg
        self.xml_msg = '<Sensor><Status Reset="false" Count="0"></Status><Command><Set base="false" tcp="false" joints="false" movement="false" digout="false" digin="false" callsubroute="false"></Set><Goto stop="false"></Goto></Command></Sensor>'
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host,self.port))


    def set_base(self,base_frame):
        assert all(isinstance(item, (float, int)) for item in base_frame), 'Argument of wrong type! Please use list of Float/Int.'
        assert len(base_frame) == 6, 'Please add all the values of xyzabc in the argument'
        xml = self.xml_msg
        sensor = ET.fromstring(xml)
        command = sensor.find('Command')
        sset = command.find('Set')
        sset.set('base','true')
        #base = sset.find('base')
        base = ET.SubElement(sset, 'base')
        base.set('X',str(base_frame[0]))
        base.set('Y',str(base_frame[1]))
        base.set('Z',str(base_frame[2]))
        base.set('A',str(base_frame[3]))
        base.set('B',str(base_frame[4]))
        base.set('C',str(base_frame[5]))
        xmlstr = ET.tostring(sensor)
        # print(xmlstr)
        self.client_socket.send(xmlstr);
        data = self.client_socket.recv(1024)
        print('data:',data)

    def set_tcp(self,tcp_frame):
        assert all(isinstance(item, (float, int)) for item in tcp_frame), 'Argument of wrong type! Please use list of Float/Int.'
        assert len(tcp_frame) == 6, 'Please add all the values of xyzabc in the argument'
        xml = self.xml_msg
        sensor = ET.fromstring(xml)
        command = sensor.find('Command')
        sset = command.find('Set')
        sset.set('tcp','true')
        #tcp = sset.find('tcp')
        tcp = ET.SubElement(sset, 'tcp')
        tcp.set('X',str(tcp_frame[0]))
        tcp.set('Y',str(tcp_frame[1]))
        tcp.set('Z',str(tcp_frame[2]))
        tcp.set('A',str(tcp_frame[3]))
        tcp.set('B',str(tcp_frame[4]))
        tcp.set('C',str(tcp_frame[5]))
        xmlstr = ET.tostring(sensor)
        #print(xmlstr)
        self.client_socket.send(xmlstr);
        data = self.client_socket.recv(1024)
        print('data:',data)

    def set_acc_speed(self,acceleration,speed):
        assert isinstance(acceleration, (float,int)), 'Argument of wrong type! Please use Float/Int.'
        assert isinstance(speed, (float,int)), 'Argument of wrong type! Please use Float/Int.'
        xml = self.xml_msg
        sensor = ET.fromstring(xml)
        command = sensor.find('Command')
        sset = command.find('Set')
        sset.set('movement','true')
        #movement = sset.find('movement')
        movement = ET.SubElement(sset, 'movement')
        movement.set('acceleration',str(acceleration))
        #movement.set('acceleration',str(acceleration))
        #new = ET.SubElement(movement, 'acceleration', link='1', pos='3.88888')
        #new.text = 'update'
        movement.set('speed',str(speed))
        xmlstr = ET.tostring(sensor)
        self.client_socket.send(xmlstr);
        data = self.client_socket.recv(1024)
        print('data:',data)

    def move_j(self,joints_pose):
        assert all(isinstance(item, (float, int)) for item in joints_pose), 'Argument of wrong type! Please use list of Float/Int.'
        assert len(joints_pose) == 6, 'Please add all the values of joints in the argument'
        xml = self.xml_msg
        sensor = ET.fromstring(xml)
        command = sensor.find('Command')
        sset = command.find('Set')
        sset.set('joints','true')
        #base = sset.find('base')
        joints = ET.SubElement(sset, 'joints')
        joints.set('A1',str(joints_pose[0]))
        joints.set('A2',str(joints_pose[1]))
        joints.set('A3',str(joints_pose[2]))
        joints.set('A4',str(joints_pose[3]))
        joints.set('A5',str(joints_pose[4]))
        joints.set('A6',str(joints_pose[5]))
        xmlstr = ET.tostring(sensor)
        #print(xmlstr)
        self.client_socket.send(xmlstr);
        data = self.client_socket.recv(1024)
        print('data:',data)

    def move_lin(self,poses):
        for pose in poses:
            assert all(isinstance(item, (float, int)) for item in pose), 'Argument of wrong type! Please use list of Float/Int.'
            assert len(pose) == 6, 'Please add all the values of xyzabc in each pose in the argument'
        xml = self.xml_msg
        sensor = ET.fromstring(xml)
        command = sensor.find('Command')
        goto = command.find('Goto')
        goto.set('stop','true')
        status = sensor.find('Status')
        status.set('Count',str(len(poses)))
        #print(len(poses))
        for pose in poses:
            xyzabc = ET.SubElement(goto, 'xyzabc', X=str(pose[0]), Y=str(pose[1]), Z=str(pose[2]), A=str(pose[3]), B=str(pose[4]), C=str(pose[5]))
        xmlstr = ET.tostring(sensor)
        #print(xmlstr)
        self.client_socket.send(xmlstr);
        data = self.client_socket.recv(1024)
        print('data:',data)

    def get_current_state(self):
        tcp_pose=[]
        flange_pose=[]
        joints=[]
        xml = self.xml_msg
        sensor = ET.fromstring(xml)
        xmlstr = ET.tostring(sensor)
        self.client_socket.send(xmlstr);
        rec = self.client_socket.recv(1024)
        rec = rec.decode('UTF-8')
        #rec = '<Robot><Data><ActPos X="10" Y="5" Z="6" A="7" B="8" C="9" /><FlangePos X="10" Y="5" Z="6" A="7" B="8" C="9" /><Joints A1="10" A2="5" A3="6" A4="7" A5="8" A6="9" /></Data></Robot>'
        #print('data:',rec)
        robot = ET.fromstring(rec)
        data = robot.find('Data')
        actpos = data.find('ActPos')
        flangepos = data.find('FlangePos')
        jointss = data.find('Joints')

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
        #print(tcp_pose,flange_pose,joints)
        return tcp_pose,flange_pose,joints


    def set_digout(self,number,value):
        assert isinstance(number, int), 'Argument of wrong type! Please use Float/Int.'
        assert isinstance(value, bool), 'Argument of wrong type! Please use Float/Int.'
        xml = self.xml_msg
        sensor = ET.fromstring(xml)
        command = sensor.find('Command')
        sset = command.find('Set')
        sset.set('digout','true')
        #base = sset.find('base')
        digout = ET.SubElement(sset, 'digout')
        digout.set('number',str(number))
        digout.set('value',str(value))
        xmlstr = ET.tostring(sensor)
        #print(xmlstr)
        self.client_socket.send(xmlstr);
        data = self.client_socket.recv(1024)
        #print('data:',data)

    def set_digin(self,number,value):
        assert isinstance(number, int), 'Argument of wrong type! Please use Float/Int.'
        assert isinstance(value, bool), 'Argument of wrong type! Please use Float/Int.'
        xml = self.xml_msg
        sensor = ET.fromstring(xml)
        command = sensor.find('Command')
        sset = command.find('Set')
        sset.set('digin','true')
        #base = sset.find('base')
        digin = ET.SubElement(sset, 'digin')
        digin.set('number',str(number))
        digin.set('value',str(value))
        xmlstr = ET.tostring(sensor)
        #print(xmlstr)
        self.client_socket.send(xmlstr);
        data = self.client_socket.recv(1024)
        #print('data:',data)

    def call_subroutine(self, number = 0):
        xml = self.xml_msg
        sensor = ET.fromstring(xml)
        command = sensor.find('Command')
        sset = command.find('Set')
        sset.set('callsubroute','true')
        subroute = ET.SubElement(sset, 'subroute')
        subroute.set('number', str(number))
        #base = sset.find('base')
        xmlstr = ET.tostring(sensor)
        print(xmlstr)
        self.client_socket.send(xmlstr);
        data = self.client_socket.recv(1024)
        print('data:',data)

