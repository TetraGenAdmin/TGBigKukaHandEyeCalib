import time

from matrix_pose import MatrixPose
from kuka import Kuka
import zivid
import numpy as np

app = zivid.Application()

#logging.info("Zivid object initialised")
print("Connecting to camera...")
camera = app.connect_camera()
settings = zivid.Settings.load("big_kuka_settings.yml")
frame = camera.capture(settings)
#logging.info("Connecting to camera...")

# kuka = Kuka('192.168.1.147', 54600)
kuka = Kuka('172.31.1.147', 54600)
# kuka.set_tcp([0,0,0,0,0,0])

# hm = [146.214157, 146.214157, 801.594, -135.000, -1.54562918E-12, 180.000]
# hj = [0.000000, -90.000000, 90.000000, 0.000000, 90.000000, 0.000000]
# p1 = [   395.014000,    14.256000,   770.718000,   -81.290000,     0.000000,  -180.000000 ]
# p2 = [   267.445643,    14.256220,   770.717516,   -81.411217,    -1.450826,  -170.483648 ]
# p3 = [   247.754808,   -87.505530,   779.991294,   -76.333030,    -1.450784,  -170.483975 ]
# p4 = [   240.120979,    19.805084,   779.991236,   -76.333012,    -1.450710,  -170.484484 ]
# p5 = [   275.876798,   133.770582,   755.830052,   -83.307071,   -16.287075,  -174.204853 ]
# p6 = [   255.084111,    62.752662,   755.829388,   -83.551229,    -5.078164,  -172.893248 ]
# p7 = [   261.554349,    42.292845,   741.268954,   -76.033547,    -5.078027,  -172.893455 ]
# p8 = [   261.554538,   -14.185482,   741.268955,   -91.753921,    -5.078023,  -172.893466 ]
# p9 = [   272.886477,   145.982155,   741.272081,   -89.977636,    -5.077595,  -172.894077 ]
# p10 = [   242.552885,    97.523271,   741.272095,   -75.561109,    -5.077595,  -172.894077 ]
# p11 = [   274.923127,    85.412791,   741.266505,   -75.261285,   -14.052064,  -174.681035 ]
# p12 = [   303.131405,    85.412264,   741.292804,   -89.533222,   -14.051546,  -174.676696 ]
# p13 = [   346.631272,   169.178996,   745.626020,   -87.664386,   -13.920671,  -178.895028 ]
# p14 = [   299.574949,   169.179009,   745.626041,   -88.720694,   -14.054491,  -174.526897 ]
# p15 = [   296.264809,   109.659902,   718.548336,   -88.720691,   -14.054475,  -174.526904 ]


hj = [-5.441560, -83.242645, 93.466843, -0.288266, 82.780800, -5.398295]
p1 = [  1667.433329,   159.917220,  1468.933082,   179.999534,    -3.018472,  -179.999844 ]
p2 = [  1732.663907,   159.917215,  1468.932896,   179.999529,    -8.419345,  -179.999799 ]
p3 = [  1737.300701,     8.303557,  1468.932862,  -177.984632,    -8.176264,   166.099369 ]
p4 = [  1737.300663,   206.806960,  1468.933127,   179.350050,    -9.434148,  -175.560360 ]
p5 = [  1624.639673,   206.807016,  1468.933341,   179.357853,     3.179108,  -175.702513 ]
p6 = [  1624.639698,   206.807019,  1500.338955,  -175.352383,     1.434511,  -175.682956 ]
p7 = [  1582.146713,   206.776755,  1457.116407,  -170.309401,     3.530340,  -175.324039 ]
p8 = [  1582.146797,   143.377974,  1457.116362,  -170.309401,     3.530338,  -175.324038 ]
p9 = [  1611.205847,   225.286447,  1457.116350,   166.236248,     3.530332,  -175.324038 ]
p10 = [  1657.247054,   284.137243,  1457.116461,   168.861440,     3.530341,  -175.324042 ]
p11 = [  1617.601734,   284.137255,  1457.116229,  -177.787866,     3.530331,  -175.324038 ]
p12 = [  1678.884485,   284.137242,  1512.939297,  -177.784087,    -4.862251,  -175.648237 ]
p13 = [  1722.537176,   211.727174,  1507.632574,  -171.437468,    -4.863146,  -175.648020 ]
p14 = [  1669.647408,   194.486063,  1507.632503,  -162.853005,    -3.726150,   177.028301 ]
p15 = [  1669.647435,   302.601409,  1507.632608,  -168.557966,    -3.726143,   177.028301 ]

p16 = [  1749.324526,   -33.212856,  1482.376881,  -169.968098,    -6.000878,   156.521589 ]
p17 = [  1779.933281,   -63.608571,  1482.376818,  -153.250028,    -6.000879,   156.521590 ]
p18 = [  1712.544024,   -63.608560,  1482.376891,   152.720676,    -6.000876,   156.521596 ]
p19 = [  1646.360966,   350.331835,  1482.376887,   152.524920,    10.757950,  -171.220144 ]
p20 = [  1646.360997,   408.124672,  1482.376908,   164.307739,     8.938856,  -163.508718 ]
p21 = [  1368.603394,   395.751120,  1439.688728,  -157.890668,     8.938855,  -163.508718 ]
p22 = [  1301.680376,   159.917208,  1443.066427,  -150.653259,    15.528048,  -169.821309 ]
p23 = [  1301.680396,   159.917217,  1443.066228,  -148.676585,    10.532552,  -161.078723 ]
p24 = [  1689.687815,   490.750655,  1443.066287,   149.021512,    10.532557,  -161.078718 ]
p25 = [  1777.608115,   490.809766,  1443.234648,   139.091732,    10.536022,  -161.083289 ]
p26 = [  1777.608211,   490.809795,  1443.234476,  -169.944986,   -14.845997,  -165.509496 ]
p27 = [  1777.608144,   259.147181,  1443.234569,  -169.944985,   -14.845992,  -165.509497 ]






poses = [p1,p16,p2,p3,p17,p4,p5,p6,p18,p7,p8,p19,p9,p20,p10,p11,p12,p21,p13,p14,p15,p22,p23,p24,p25,p26,p27]

poses = [p1,p16,p2,p3,p17,p4,p5,p6,p18,p7,p8,p19,p9,p20,p10]

correct_poses = []
frames = []
# kuka.move_lin([hm])
calibration_inputs = []
kuka.move_j(hj)
for p in poses:


    kuka.move_lin([p])
    time.sleep(3)
    frame = camera.capture(settings)
    result = zivid.calibration.detect_feature_points(frame.point_cloud())
    _,r_p,_ = kuka.get_current_state()
    robot_pose = zivid.calibration.Pose(MatrixPose.pose_to_matrix(r_p))
    # robot_pose = zivid.calibration.Pose(MatrixPose.pose_to_matrix(p))
    if result:
        print("OK")
        res = zivid.calibration.HandEyeInput(robot_pose, result)
        calibration_inputs.append(res)

    else:
        print("FAILED")


kuka.move_j(hj)
calibration_result = zivid.calibration.calibrate_eye_in_hand(calibration_inputs)
if calibration_result:
    print("OK")
    print("Result:\n{}".format(calibration_result))

    # np.savetxt(
    #     'bTz.csv',
    #     calibration_result.transform(), delimiter=",")
    print(calibration_result.transform())
    print(MatrixPose.matrix_to_pose(calibration_result.transform()))
else:
    print("FAILED")



# camera = Zivid("C:/Users/BhavinDharia/OneDrive - TetraGen Robotics Inc/Deploy/sync_software_eki/ProgramData/settings.yml")
# robot = KukaEKICommunicator('172.31.1.147', 54600,camera)
#
# for i in range(12):
#     robot.receive_data()
#
# robot.calibrate_eye_to_hand()

