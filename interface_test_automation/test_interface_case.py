#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'zuozhijun'

import  unittest
import json
import base64
import Special_char_process
# 测试用例(组)类
class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', test_data=None, http=None, db1_cursor=None, db2_cursor=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.test_data = test_data
        self.http = http
        self.db1_cursor = db1_cursor
        self.db2_cursor = db2_cursor


class TestInterfaceCase(ParametrizedTestCase):
   def setUp(self):
       pass

   # 测试接口1
   def EWMS(self):
       # 根据被测接口的实际情况，合理的添加HTTP头
       header = {'Accept':'*/*','Accept-Encoding': 'gzip, deflate','Accept-Language':'zh-CN',
         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
          }
       self.http.set_header(header)
       response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
       print("response1",response)
       if {} == response[0]:         #请求失败
            self.test_data.result = 'Error'  #self.erro_msg(erro_msg) #
            #Lresponse=str(response[1])
            Lresponse = Special_char_process.SpCharReplace(str(response[1]))
            print("response2", Lresponse)
            print("response21", type(Lresponse))
            #Lresponsew = base64.b64encode(bytes(Lresponse,'utf-8'))
            #Lresponsew = base64.b64encode(bytearray(Lresponse,'utf-8'))
            #Lresponsew = base64.b64encode(Lresponse,'utf-8')
            #Lresponsew = base64.encodestring(Lresponse)
            #Lresponsew = base64.encode(Lresponse)
            #Lresponsew = base64.encodestring(Lresponse)
            #self.test_data.reason =Lresponsew  #str(response[1])
            self.test_data.reason = Lresponse
            print("response31", Lresponse)
            #print("response32", str(base64.b64decode(Lresponse),'utf-8'))
            try:
                # 更新结果表中的用例运行结果
                self.db1_cursor.execute('UPDATE test_result SET result = %s,reason = %s  WHERE case_id = %s', (self.test_data.result,self.test_data.reason, self.test_data.case_id))
                self.db1_cursor.execute('commit')
                print("response33", response)
            except Exception as e:
                print('%s' % e)
                self.db1_cursor.execute('rollback')
            #return
       else:
            self.db1_cursor.execute('SELECT expectedresults FROM test_data WHERE case_id = %s',(self.test_data.case_id,))  # 查出预期结果用来与响应结果做对比
            expectedresults_list = self.db1_cursor.fetchone()[0]
            print("response4", response)
            try:
                self.db1_cursor.execute('SELECT expectedresults FROM test_data WHERE case_id = %s',(self.test_data.case_id,))    #查出预期结果用来与响应结果做对比
                expectedresults_list=self.db1_cursor.fetchone()[0]
                print("response4", response)
           #print("expectedresults_list:",json.loads(expectedresults_list))
           #self.db1_cursor.close()
           #print("expectedresults_list2:", expectedresults_list)
                if expectedresults_list==None:
                  print("response5", response)
                  self.test_data.result="Fail"
                  self.test_data.reason ="预期结果为空，请填写预期结果"
               #print("expectedresults_list3:", expectedresults_list)
                else:
               #print("expectedresults_list:", json.loads(expectedresults_list))
               #print(len(json.loads(expectedresults_list)))
               #print(len( response))
                  print("response6", response)
                  if json.loads(expectedresults_list) ==response: #len(json.loads(expectedresults_list))==len( response):
                     print("response7", response)
                     self.test_data.result = 'Pass'
                  #print("pass")
                  else:
                     self.test_data.result = 'Fail'
                     self.test_data.reason = '预期结果与接口返回值不匹配'
                     print("response8", response)
                  #print("Fail")
                  #return
            except AssertionError as e:
               print('%s' % e)
               self.test_data.result = 'Fail'
               self.test_data.reason = '%s' % e # 记录失败原因
       #return
       # 更新结果表中的用例运行结果
       try:
          self.db1_cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s', (self.test_data.result, self.test_data.case_id))
          self.db1_cursor.execute('UPDATE test_result SET reason = %s WHERE case_id = %s', (self.test_data.reason, self.test_data.case_id))
          self.db1_cursor.execute('commit')
       except Exception as e:
           print('%s' % e)
           self.db1_cursor.execute('rollback')
       self.db1_cursor.close()
       #return
#2017-12-08从尾端复制过来
   def tearDown(self):
       pass