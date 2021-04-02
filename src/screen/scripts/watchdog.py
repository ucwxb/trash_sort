#!/usr/bin/python3
#coding:utf-8

import time
import threading

class WatchDog:
    def __init__(self,bite,bowl=1):
        self.bite = bite
        self.Kill()
    
    def Check(self):
        if self.food>0:
            self.food-=1
        elif self.food==0:
            self.food=-1
            self.bite()

    def Feed(self):
        if self.bowl>0:
            self.bowl-=1
            self.food = self.each_time_food
            return True
        return False
    
    def AutoCheck(self,timeout_s,frequency_hz,cmd_queue_max_len=3):
        self.interval = 1/frequency_hz
        self.each_time_food = int(timeout_s*frequency_hz)
        self.bowl = cmd_queue_max_len
        self.watching = True
        self.thread = threading.Thread(target=self.AutoCheckFunc)
        self.thread.start()

    def AutoCheckFunc(self):
        while self.watching:
            time.sleep(self.interval)
            self.Check()
    
    def Kill(self):
        self.watching = False
        self.food = -1
