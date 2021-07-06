"""
main window form file
"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow

from generate_file.ui_main_window import Ui_MainWindow
from morphing import wrap_image

import cv2

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main window form
    """
    ori_img1 = cv2.imread('src/img/women.jpg')
    ori_img2 = cv2.imread('src/img/cheetah.jpg')

    showing_img1 = cv2.imread('src/img/women.jpg')
    showing_img2 = cv2.imread('src/img/cheetah.jpg')

    prePoint_1 = -1
    prePoint_2 = -1
    lines_1 = []
    lines_2 = []
    lines_wrap = []
    animate_imgs = []

    def __init__(self, parent=None):
        """Initialize function

        Args:
            parent (QWidget, optional): parent of this form. Defaults to None.
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.pushButton_2.clicked.connect(self.reset_btn)
        self.pushButton.clicked.connect(self.start_btn)
        self.pushButton_3.clicked.connect(self.animation_btn)
        

        cv2.namedWindow('im1', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('im1', self.click_img1)
        cv2.resizeWindow('im1', self.ori_img1.shape[1], self.ori_img1.shape[0])
        cv2.imshow('im1', self.ori_img1)

        cv2.namedWindow('im2', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('im2', self.click_img2)
        cv2.resizeWindow('im2', self.ori_img2.shape[1], self.ori_img2.shape[0])
        cv2.imshow('im2', self.ori_img2)

    def click_img1(self, event, x, y, flags, param):
        if event== cv2.EVENT_LBUTTONDOWN:
            if self.prePoint_1 == -1:
                self.prePoint_1 = (x,y)
        elif event==cv2.EVENT_MOUSEMOVE:
            if self.prePoint_1 != -1:
                self.draw_lines(1)
                cv2.arrowedLine(self.showing_img1, self.prePoint_1, (x,y), (255, 200, 200), 3)
                cv2.imshow('im1', self.showing_img1)
        elif event==cv2.EVENT_LBUTTONUP:
            if self.prePoint_1 != -1:
                self.lines_1.append((self.prePoint_1, (x,y)))
                self.prePoint_1 = -1
                #print('lines_1')
                #print(self.lines_1)
                self.draw_lines(1)
                cv2.imshow('im1', self.showing_img1)

    def click_img2(self, event, x, y, flags, param):
        if event== cv2.EVENT_LBUTTONDOWN:
            if self.prePoint_2 == -1:
                self.prePoint_2 = (x,y)
        elif event==cv2.EVENT_MOUSEMOVE:
            if self.prePoint_2 != -1:
                self.draw_lines(2)
                cv2.arrowedLine(self.showing_img2, self.prePoint_2, (x,y), (255, 200, 200), 3)
                cv2.imshow('im2', self.showing_img2)
        elif event==cv2.EVENT_LBUTTONUP:
            if self.prePoint_2 != -1:
                self.lines_2.append((self.prePoint_2, (x,y)))
                self.prePoint_2 = -1
                #print('lines_2')
                #print(self.lines_2)
                self.draw_lines(2)
                cv2.imshow('im2', self.showing_img2)

    def draw_lines(self, index):
        if index==1:
            self.showing_img1 = self.ori_img1.copy()
            for l in self.lines_1:
                start = l[0]
                end = l[1]
                cv2.arrowedLine(self.showing_img1, start, end, (255, 255, 255), 3)
            #cv2.imshow('im1', im)
        else:
            self.showing_img2 = self.ori_img2.copy()
            for l in self.lines_2:
                start = l[0]
                end = l[1]
                cv2.arrowedLine(self.showing_img2, start, end, (255, 255, 255), 3)
            #cv2.imshow('im2', im)

    def reset_btn(self):
        self.lines_1.clear()
        self.lines_2.clear()
        self.lines_wrap.clear()
        self.draw_lines(1)
        self.draw_lines(2)
        cv2.namedWindow('im1', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('im1', self.click_img1)
        cv2.resizeWindow('im1', self.ori_img1.shape[1], self.ori_img1.shape[0])
        cv2.imshow('im1', self.showing_img1)
        cv2.namedWindow('im2', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('im2', self.click_img2)
        cv2.resizeWindow('im2', self.ori_img2.shape[1], self.ori_img2.shape[0])
        cv2.imshow('im2', self.showing_img2)

    def start_btn(self):
        t = float(self.doubleSpinBox.value())
        if len(self.lines_1)!=len(self.lines_2) or len(self.lines_1)==0 or len(self.lines_2)==0:
            print('Number of feature lines in two images must be same and cannot be zero!')
            return
        elif t == 0:
            im1 = self.ori_img1.copy()
            im2 = wrap_image(self.ori_img2, self.lines_2, self.lines_1)
            im_add = cv2.addWeighted(im1, 1.0-t, im2, t, 0.0)
            for l in self.lines_1:
                start = l[0]
                end = l[1]
                cv2.arrowedLine(im1, start, end, (255, 255, 255), 3)
                cv2.arrowedLine(im2, start, end, (255, 255, 255), 3)
        elif t == 1:
            im1 = wrap_image(self.ori_img1, self.lines_1, self.lines_2)
            im2 = self.ori_img2.copy()
            im_add = cv2.addWeighted(im1, 1.0-t, im2, t, 0.0)
            for l in self.lines_2:
                start = l[0]
                end = l[1]
                cv2.arrowedLine(im1, start, end, (255, 255, 255), 3)
                cv2.arrowedLine(im2, start, end, (255, 255, 255), 3)
        else:
            self.lines_wrap.clear()
            for l1, l2 in zip(self.lines_1, self.lines_2):
                p0 = ((1.0-t)*l1[0][0] + (t)*l2[0][0], (1.0-t)*l1[0][1] + (t)*l2[0][1])
                p1 = ((1.0-t)*l1[1][0] + (t)*l2[1][0], (1.0-t)*l1[1][1] + (t)*l2[1][1])
                self.lines_wrap.append((p0, p1))
            #print('wrap lines')
            #print(self.lines_wrap)
            im1 = wrap_image(self.ori_img1, self.lines_1, self.lines_wrap)
            im2 = wrap_image(self.ori_img2, self.lines_2, self.lines_wrap)
            im_add = cv2.addWeighted(im1, 1.0-t, im2, t, 0.0)
            for l in self.lines_wrap:
                start = (int(l[0][0]), int(l[0][1]))
                end = (int(l[1][0]), int(l[1][1]))
                cv2.arrowedLine(im1, start, end, (255, 255, 255), 3)
                cv2.arrowedLine(im2, start, end, (255, 255, 255), 3)

        cv2.namedWindow('wrap1', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('wrap1', im1.shape[1], im1.shape[0])
        cv2.imshow('wrap1', im1)
        cv2.namedWindow('wrap2', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('wrap2', im2.shape[1], im2.shape[0])
        cv2.imshow('wrap2', im2)
        cv2.namedWindow('result', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('result', im1.shape[1], im1.shape[0])
        cv2.imshow('result', im_add)

    def animation_btn(self):
        if len(self.lines_1)!=len(self.lines_2) or len(self.lines_1)==0 or len(self.lines_2)==0:
            print('Number of feature lines in two images must be same and cannot be zero!')
            return
        self.animate_imgs.clear()
        self.animate_imgs.append(self.ori_img1.copy())
        for i in range(1, 10, 1):
            self.lines_wrap.clear()
            t = i/10.0
            for l1, l2 in zip(self.lines_1, self.lines_2):
                p0 = ((1.0-t)*l1[0][0] + (t)*l2[0][0], (1.0-t)*l1[0][1] + (t)*l2[0][1])
                p1 = ((1.0-t)*l1[1][0] + (t)*l2[1][0], (1.0-t)*l1[1][1] + (t)*l2[1][1])
                self.lines_wrap.append((p0, p1))
            im1 = wrap_image(self.ori_img1, self.lines_1, self.lines_wrap)
            im2 = wrap_image(self.ori_img2, self.lines_2, self.lines_wrap)
            self.animate_imgs.append(cv2.addWeighted(im1, 1.0-t, im2, t, 0.0))
        self.animate_imgs.append(self.ori_img2.copy())
        cv2.namedWindow('animation', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('animation', self.click_animation)
        cv2.resizeWindow('animation', self.ori_img1.shape[1], self.ori_img1.shape[0])
        cv2.imshow('animation', self.animate_imgs[0])

    def click_animation(self, event, x, y, flags, param):
        if event== cv2.EVENT_LBUTTONDBLCLK:
             for i in range(len(self.animate_imgs)):
                win_name = 'animation'
                cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(win_name, self.ori_img1.shape[1], self.ori_img1.shape[0])
                cv2.imshow(win_name, self.animate_imgs[i])
                key = cv2.waitKey(100)
