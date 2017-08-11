# coding=utf-8

import cv2
import filters
from managers import WindowsManager, CaptureManager


class Cameo(object):
    def __init__(self):
        self._windowManager = WindowsManager('Cameo', self.onkeypress)
        self._capturemanager = CaptureManager(
            cv2.VideoCapture(0), self._windowManager, True)

        # 此处滤波器声明
        self._BlurFilter = filters.BlurFilter()
        self._FindEdgesFilter = filters.FindEdgesFilter()

    def run(self):
        """run the main loop"""
        self._windowManager.create_window()
        while self._windowManager.is_window_created:
            self._capturemanager.enterframe()
            frame = self._capturemanager.frame

            # 这里插入滤波代码
            filters.strokeEdges(frame, frame)
            self._FindEdgesFilter.apply(frame, frame)

            self._capturemanager.exitframe()
            self._windowManager.process_events()

    def onkeypress(self, keycode):
        """处理按键操作
        空格 表示 截图
        tab 表示 开始/停止 记录 screencast
        escape 表示退出
        """
        if keycode == 32:  # 空格
            self._capturemanager.writeimage('Screenshot.png')
            print("已截图")
        elif keycode == 9:  # Tab键
            if not self._capturemanager.is_writingvideo:
                self._capturemanager.start_writinvideo('screenshot.avi')
                print("开始录制视频")
            else:
                self._capturemanager.stop_writingvideo()
                print("停止录制视频")
        elif keycode == 27:  # escape 键
            self._windowManager.destroy_window()
            print("正在退出")


if __name__ == "__main__":
    Cameo().run()
