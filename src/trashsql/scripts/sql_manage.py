#!/usr/bin/python3
#coding:utf-8
import pymysql
import datetime
import cv2
import rospy
import numpy as np
from trashsql.msg import sqlres
class filter_sql_cmd:
    def create_sql(self):
        pass


class sql_manage:
    def __init__(self,host,user,password,db_name,port = 3306,charset = 'utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.port = int(port)
        self.charset = charset

        self.db = pymysql.connect(host=self.host,
                    port=self.port,
                    user=self.user, 
                    password=self.password, 
                    db=self.db_name, 
                    charset=self.charset)
        self.cursor = self.db.cursor()
    
    def add_data(self,src_img,detect_img,detect_res,detect_res_string):
        _time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        sql="INSERT INTO trash (src_img,detect_img,detect_res,detect_res_string,create_time) VALUES  (%s,%s,%s,%s,%s)"
        param = (src_img,detect_img,detect_res,detect_res_string,_time)
        self.cursor.execute(sql , param)
        self.db.commit()
        return 1

    def handle_get_image(self,img):
        img= np.fromstring(img,np.uint8)
        img = img.flatten()
        return img

    def get_data(self,new_data_manage):
        sql= "SELECT * FROM trash"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for result in results:
            new_sqlres = sqlres()
            new_sqlres.id = result[0]
            new_sqlres.src_img = self.handle_get_image(result[1])
            new_sqlres.detect_img = self.handle_get_image(result[2])
            new_sqlres.create_time = str(result[3])
            new_sqlres.detect_res = result[4]
            new_sqlres.detect_res_string = result[5]
            new_data_manage.res.append(new_sqlres)
        new_data_manage.status = 1
        return new_data_manage
        # f = open("res.mp4","wb")
        # f.write(image)
        # f.close()

    def delete_data(self,select_id):
        sql = "DELETE FROM trash WHERE id='{}'".format(select_id)
        sta = self.cursor.execute(sql) 
        self.db.commit()
        return sta

if __name__ == '__main__':
    test = trashsql(
        host = "rm-2zeda02kh06843ewrwo.mysql.rds.aliyuncs.com",
        user = "ucwxb",
        password = "XYcstp123",
        db_name = "trash_sort",
    )
    f = open("1.mp4","rb")
    image = f.read()

    # cap = cv2.VideoCapture(1)
    # _,frame = cap.read()
    # success, encoded_image = cv2.imencode(".jpg", frame)
    # image = encoded_image.tostring()

    test.add_data(image,image,11,"中文")
    test.get_data()
    # cv2.imshow("123",frame)
    # cv2.waitKey(0)