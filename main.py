import time

from matrix_pose import MatrixPose
from kuka import Kuka
import zivid
import numpy as np

app = zivid.Application()

#logging.info("Zivid object initialised")
print("Connecting to camera...")
camera = app.connect_camera()
settings = zivid.Settings.load("1_by_4_settings.yml")
frame = camera.capture(settings)
#logging.info("Connecting to camera...")

kuka = Kuka('172.31.1.147', 54600)
# kuka.set_tcp([0,0,0,0,0,0])

hm = [146.214157, 146.214157, 801.594, -135.000, -1.54562918E-12, 180.000]
hj = [-45,-120,110,0,100,0]
p1 = [   122.512706,   137.252647,   658.144109,  -132.454505,    30.874380,  -176.862760 ]
p2 = [   159.907715,   105.692644,   659.056857,  -132.454518,    30.873023,  -176.862939 ]
p3 = [   202.883204,    44.511435,   662.170986,  -144.154342,    33.638005,  -176.986258 ]
p4 = [   197.225433,    37.712055,   644.044071,  -144.154341,    33.638009,  -176.986256 ]
p5 = [   155.836283,    74.550686,   643.011858,  -157.080371,    33.836897,  -177.149825 ]
p6 = [   165.238061,    84.928739,   639.921456,  -156.107231,    30.187039,  -175.174762 ]
p7 = [   201.114978,    98.003612,   624.684203,  -158.659066,    27.980902,   179.527808 ]
p8 = [   201.114978,    98.003612,   624.684203,  -158.659066,    27.980902,   179.527808 ]
p9 = [   119.690778,   186.384089,   623.358986,  -148.540002,    32.308568,  -168.947522 ]
p10 = [    92.543859,   181.972561,   622.934174,  -127.117908,    31.928332,  -168.777527 ]
p11 = [   142.231948,   124.753845,   624.612638,  -149.005444,    31.626720,   167.840334 ]
p12 = [   173.053990,   156.750833,   541.437961,  -149.005445,    31.626719,   167.840299 ]
p13 = [   173.053990,   156.750833,   541.437961,  -149.005445,    31.626719,   167.840299 ]
p14 = [    75.467684,   306.890052,   536.068659,  -142.826128,    31.519454,   167.908945 ]
p15 = [    61.051060,   320.031916,   507.804130,  -142.826316,    31.519712,   167.909334 ]



poses = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15]
correct_poses = []
frames = []
kuka.move_lin([hm])
calibration_inputs = []
kuka.move_j(hj)
for p in poses:


    kuka.move_lin([p])
    time.sleep(5)
    frame = camera.capture(settings)
    result = zivid.calibration.detect_feature_points(frame.point_cloud())
    robot_pose = zivid.calibration.Pose(MatrixPose.pose_to_matrix(p))
    if result:
        print("OK")
        res = zivid.calibration.HandEyeInput(robot_pose, result)
        calibration_inputs.append(res)

    else:
        print("FAILED")


kuka.move_j(hj)
calibration_result = zivid.calibration.calibrate_eye_to_hand(calibration_inputs)
if calibration_result:
    print("OK")
    print("Result:\n{}".format(calibration_result))

    np.savetxt(
        'bTz.csv',
        calibration_result.transform(), delimiter=",")
else:
    print("FAILED")



# camera = Zivid("C:/Users/BhavinDharia/OneDrive - TetraGen Robotics Inc/Deploy/sync_software_eki/ProgramData/settings.yml")
# robot = KukaEKICommunicator('172.31.1.147', 54600,camera)
#
# for i in range(12):
#     robot.receive_data()
#
# robot.calibrate_eye_to_hand()


