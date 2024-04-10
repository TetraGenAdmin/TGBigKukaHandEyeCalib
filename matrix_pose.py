
import numpy as np

from scipy.spatial.transform import Rotation as R


class MatrixPose:
    @staticmethod
    def pose_to_matrix(startpose):
        rot_mat = R.from_euler('ZYX', [startpose[3], startpose[4], startpose[5]], degrees=True)
        homogeneous_mat = np.array(
            [[rot_mat.as_matrix()[0][0], rot_mat.as_matrix()[0][1], rot_mat.as_matrix()[0][2], startpose[0]],
             [rot_mat.as_matrix()[1][0], rot_mat.as_matrix()[1][1], rot_mat.as_matrix()[1][2], startpose[1]],
             [rot_mat.as_matrix()[2][0], rot_mat.as_matrix()[2][1], rot_mat.as_matrix()[2][2], startpose[2]],
             [0, 0, 0, 1]])
        return homogeneous_mat

    @staticmethod
    def matrix_to_pose(matrix):
        rot_mat = R.from_matrix([[matrix[0][0], matrix[0][1], matrix[0][2]],
                                 [matrix[1][0], matrix[1][1], matrix[1][2]],
                                 [matrix[2][0], matrix[2][1], matrix[2][2]]])

        eulerang = rot_mat.as_euler('ZYX', degrees=True)

        pose = [matrix[0][3], matrix[1][3], matrix[2][3], eulerang[0], eulerang[1], eulerang[2]]
        return pose