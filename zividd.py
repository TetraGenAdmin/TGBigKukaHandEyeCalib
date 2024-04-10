from imports import zivid, datetime, np, o3d


class Zivid:

    def __init__(self, file,simulation = False):
        self.__simulation = simulation
        self.app = zivid.Application()
        if self.__simulation == False:
            #self.app = zivid.Application()

            #logging.info("Zivid object initialised")
            print("Connecting to camera...")
            #logging.info("Connecting to camera...")

            self.camera = self.app.connect_camera()
            self.settings = zivid.Settings.load(file)

            # self.Settings.Acquisition(aperture=fnum) for fnum in (11.31, 5.66, 2.83)]


    def edit_settings(self,engine = "phase", aperture = 5.66, exposure_time = datetime.timedelta(microseconds=6500), enable_outlier_removal = True, outlier_removal_threshold = 5.0):
        if self.__simulation == False:

            self.settings.experimental.engine = engine
            self.settings.acquisitions.append(zivid.Settings.Acquisition())
            self.settings.acquisitions[0].aperture = aperture
            self.settings.acquisitions[0].exposure_time = exposure_time
            self.settings.processing.filters.outlier.removal.enabled = enable_outlier_removal
            if enable_outlier_removal == True:
                self.settings.processing.filters.outlier.removal.threshold = outlier_removal_threshold

            print("Changed camera settings...")
            #logging.info("Changed camera settings...")


    def capture_organised_points(self):
        if self.__simulation == False:
            print("Capturing organised points")
            frame =  self.camera.capture(self.settings)
            point_cloud = frame.point_cloud()
            xyz = point_cloud.copy_data("xyz")

            print("Captured organised points")
            #logging.info("Captured organised points")

            return xyz


    def capture_o3d_point_cloud(self):
        if self.__simulation == False:
            frame = self.camera.capture(self.settings)
            point_cloud = frame.point_cloud()
            #xyz = point_cloud.copy_data("xyz")
            #xyz = np.nan_to_num(xyz).reshape(-1, 3)
            point_cloud_open3d = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.nan_to_num(point_cloud.copy_data("xyz")).reshape(-1, 3)))
            #point_cloud_open3d = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(xyz))

            print("Captured point cloud")
            #logging.info("Captured point cloud")

            return point_cloud_open3d
    def capture_o3d_point_cloud_color(self):
        if self.__simulation == False:
            frame = self.camera.capture(self.settings)
            #point_cloud = frame.point_cloud()
            #xyz = point_cloud.copy_data("xyz")
            #xyz = np.nan_to_num(xyz).reshape(-1, 3)
            #rgba = point_cloud.copy_data("rgba")
            #rgb = rgba[:, :, 0:3]
            #rgb = rgb.reshape(-1, 3)

            #point_cloud.copy_data("rgba")[:, :, 0:3].reshape(-1, 3)
            #point_cloud_open3d = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(xyz))
            point_cloud_open3d = o3d.geometry.PointCloud(
                o3d.utility.Vector3dVector(np.nan_to_num(frame.point_cloud().copy_data("xyz")).reshape(-1, 3)))
            point_cloud_open3d.colors = o3d.utility.Vector3dVector(frame.point_cloud().copy_data("rgba")[:, :, 0:3].reshape(-1, 3)/255)

            print("Captured point cloud")
            #logging.info("Captured point cloud")

            return point_cloud_open3d

    def capture_zivid_frame(self):
        if self.__simulation == False:
            frame = self.camera.capture(self.settings)
            return frame

    @staticmethod
    def convert_zivid_frame_to_o3d_colored_PC(frame):
        point_cloud_open3d = o3d.geometry.PointCloud(
            o3d.utility.Vector3dVector(np.nan_to_num(frame.point_cloud().copy_data("xyz")).reshape(-1, 3)))
        point_cloud_open3d.colors = o3d.utility.Vector3dVector(
            frame.point_cloud().copy_data("rgba")[:, :, 0:3].reshape(-1, 3) / 255)
        return point_cloud_open3d

    def disconnect_camera(self):
        if self.__simulation == False:
            self.camera.disconnect()

    def load_zdf(self, filename):
        print(filename)
        return zivid.Frame(filename)