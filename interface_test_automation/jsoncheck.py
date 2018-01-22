#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018/1/12 0012 下午 11:34
# @Author  : bree
# @Site    : 
# @File    : jsoncheck.py
# @Software: PyCharm
# 1.jsons是要匹配的json，statement是匹配规则，传入字符串格式
# 2.statement若是json格式（被{}包含），则完全匹配
# 3.statement若是json格式去掉两侧{}，则通过正则匹配，例如'"key1":"value1","key2":"value2"'
# 4.部分匹配时，key匹配忽略大小写，statement.value只能是字符串（正则表达式）、数字、布尔（true/false）、None 其中一种
# 5.key可指定键的层级关系，用逗号隔开，正常逗号用{空格}+","表示。eg:"a,b,c"表示匹配a键下的b键下的c键()
# 6.使用时要注意json特殊值转换到python字典时会发生变化，例如：null-->None
import json
import re

class JsonCheck():
    #匹配成功返回1,失败0，参数异常2
    def check(self,jsons ,statement):
        try:
            js=json.loads(jsons)
        except Exception as e:
            return 2,'传入的json格式出错'
        if statement[0]+statement[-1]=='{}':            #用‘{}’包含表示完全匹配
            try:
                sta=json.loads(statement)
            except Exception as e:
                return 2,'传入的statement格式出错'
            if js==sta: return 1,'match'
            return 0,'不完全匹配'
        else:                   #用"key":"value",格式表示部分匹配（支持正则）
            try:
                sta= json.loads('{'+statement+'}')
            except Exception as e:
                return 2,'传入的statement格式出错'
            for key in sta:
                rs,msg=self.json_reg(key, sta[key], js)
                if rs != 1:return rs,msg
            return 1,'match'

    def json_reg(self,keyreg,valuereg,dic_json):          #支持指定键的层级关系,但是只会找到按顺序第一个匹配的
        json=dic_json
        keys=re.split("(?<!\s),",keyreg)                #根据逗号（前面没有空格）分割
        while '' in keys:
            keys.remove('')
        for key in keys:
            key =re.sub('\s,',',',key)
            if key==keys[-1]:return self.json_regmatch(key,valuereg,json)
            rs,json=self.json_regmatch(key,'.*',json)
            if rs !=1:return rs,json

    def json_regmatch(self,keyreg,valuereg,dic_json):
        if  isinstance(dic_json,list):              #传入的可能是dict list
            for json in dic_json:
                if isinstance(json,dict):
                    mrs, msg = self.json_regmatch(keyreg, valuereg, json)
                    if mrs != 0: return mrs, msg
        elif  isinstance(dic_json,dict):
                for key in dic_json:
                    if re.fullmatch(keyreg,key,re.I) != None:         #key值只进行字符串匹配（忽略大小写）
                        if isinstance(valuereg,(float,int,bool)) or valuereg == None:          #匹配value是布尔、数字、None(null)
                            if valuereg==dic_json[key]: return 1,{key:dic_json[key]}
                        elif re.fullmatch(valuereg, str(dic_json[key])): return 1,{key:dic_json[key]}
                        # return -1,'%s:%s的value不匹配%s:%s'%(keyreg,valuereg,key,dic_json[key])                                       #不注释则只返回第一次key匹配成功的value匹配结果
                    elif isinstance(dic_json[key],dict):                  #如果dic_json[key]依旧是字典类型,递归
                        mrs,msg=self.json_regmatch(keyreg, valuereg, dic_json[key])
                        if mrs!=0: return mrs,msg
                    elif isinstance(dic_json[key],list):                     #如果dic_json[key]是list,递归
                        for i in dic_json[key]:
                            if isinstance(i,dict):
                                mrs,msg = self.json_regmatch(keyreg, valuereg, i)
                                if mrs != 0: return mrs,msg
                return 0,'%s:%s--没有匹配的数据'%(keyreg,valuereg)
        else:
            return 2,'传入的json格式不正确'

if __name__ == '__main__':
    js=JsonCheck()
    jsl='{' \
    '"IsSuccess": true,'\
    '"Data": {' \
        '"VolumenWidth": 11.00000, ' \
        '"VolumenHeight": 5.00000,' \
        '"VolumenLength": 26.00000,' \
        '"productWeight": 153.00000},' \
    '"ResponseError": null,' \
    '"CheckedKey": null,' \
    '"Message": null,\
    "data2": ' \
        '{"feedbacks": ' \
            '{"feedbacklist": ' \
                '[{"comment": "5分",' \
                '"createtime": "2016.09.07 12:38",' \
                '"score": 5,' \
                '"username": "1331##11"}],' \
            '"totalcount": 1,'\
            '"totalscore": 5},' \
        '"liketeamlist": ' \
            '[{"limage": "http://baidu.com.465.jpg",' \
            '"lmarketprice": 199,' \
            '"lteamId": 386,' \
            '"lteamprice": 38,' \
            '"ltitle": "我才是测试文本哦,用于测试此次验证。"},'\
            '{"limage": "http://baidu.com/37.jpg",' \
            '"lmarketprice": 3380,' \
            '"lteamId": 57133,' \
            '"lteamprice": 580,' \
            '"ltitle": "测试文本,15级软件开发！"}],' \
        '"partnerteamlist":\
            [{"pteamId": 35,"pteamprice": 228,"ptitle": "计算机应用专业。"},' \
            '{"pteamId": 72598,"pteamprice": 2888,"ptitle": "潍坊职业学院。"},' \
            '{"pteamId": 3613,"pteamprice": 499,  "ptitle": "2015级！"},'\
            '{"pteamId": 72638,"pteamprice": 4299,"ptitle": "本次测试于16年9月7日。"},' \
            '{"pteamId": 716,"pteamprice": 38,"ptitle": "后期持续更新！"}]},' \
        '"state": 1 ,' \
        '"err":null}'
    sd1='"CheckedKey":null,"issuccess":true,"VolumenWidth":11,"pteamId":"726.*","data2,username":"1331##11","err":"None","err":null,"liketeam.*,lteam.*":"\\\\d*"'
    sd='"data2,.*team.*,lteam.*":"\\\\d*"'
    jsl2='{"IsSuccess":true,"Data":{"sNeedQuantity":52651,"mNeedQuantity":21316,"sAllocatedQuantity":53022,"nonCompleteBatch":["P1201801227002","P0201801227003","P0201801227004","P0201801227005","MP0201801227006","MP0201801227007","MP0201801227009","P0201801227011","P5201801227012","MP0201801227014","MP0201801227016","MP0201801227018","MP0201801227019","MP0201801227020","MP0201801227022","MP0201801227023","MP0201801227024","MP0201801227025","P2201801227027","P0201801227028","P0201801227029","P0201801227030","MP0201801227033","MP0201801227035","MP0201801227036","MP0201801227040","MP0201801227043","MP0201801227044","MP0201801227046","MP0201801227047","MP0201801227049","MP0201801227050","MP0201801227051","MP0201801227052","MP0201801227054","MP0201801227055","MP0201801227056","MP0201801227058","MP9201801227061","MP9201801227062","MP0201801227065","P1201801227067","P0201801227068","MP0201801227070","MP0201801227071","MP0201801227072","MP0201801227073","MP0201801227074","MP0201801227075","MP0201801227077","MP0201801227079","P0201801227080","P0201801227083","MP0201801227084","MP0201801227086","MP0201801227089","P5201801227090","P2201801227092","P0201801227093","MP0201801227094","MP0201801227096","MP0201801227097","MP0201801227098","P0201801227101","MP0201801227102","MP0201801227103","MP0201801227104","MP0201801227105","P0201801227107","MP9201801227108","MP0201801227113","MP0201801227117","P0201801227118","P0201801227119","P0201801227120","MP0201801227121","P0201801227123","MP0201801227125","MP0201801227127","MP0201801227128","P0201801227131","P0201801227133","P0201801227134"],"allocatorQuantity":{"吴海雄":2605,"马楚亮":2028,"廖腾":430,"赵志伟":2859,"张超A":1159,"舒彩迪3":4175,"周雪芳":4061,"农荣稳":3499,"刘灿辉":3220,"肖葵芳":5952,"卢柳焕":781,"黄经伟":1121,"甘金华":2468,"刘丽欣":1903,"李先亮A":2489,"罗梓明":3127,"罗海宁":3710,"杨大明":2771,"谢新华1":2953,"黎佩福":131,"梁国艺":3773,"冼穗锋":1472,"陆金伟1":920,"王金矿":410,"肖伟1":3032,"肖志祥":1,"吴宏雁":70,"陈伟耀":12,"蒋羽宾":177,"徐敏1":200,"韦京日":1040,"唐旭":2257,"黄健宁":166,"欧阳慷有":334,"谢宝文":2317,"何海源":31,"林康":3333,"欧阳育平":3532},"completeBatch":["P2201801227001","MP0201801227008","MP0201801227010","MP0201801227013","MP0201801227015","MP0201801227017","MP0201801227021","MP0201801227026","P0201801227031","MP0201801227032","MP0201801227034","MP0201801227037","MP0201801227038","MP0201801227039","MP0201801227041","MP0201801227042","MP0201801227045","MP0201801227048","MP0201801227053","MP0201801227057","MP0201801227059","MP0201801227060","MP9201801227063","MP0201801227064","P2201801227066","MP0201801227069","MP0201801227076","MP0201801227078","P2201801227081","P1201801227082","MP0201801227085","MP0201801227087","MP0201801227088","P1201801227091","MP0201801227095","P0201801227099","MP0201801227100","P0201801227106","MP9201801227109","P3201801227111","MP3201801227112","P2201801227114","P1201801227115","MP0201801227116","MP0201801227122","SP0201801227126","P0201801227129","P0201801227130","P0201801227132"],"sNonAllocateQuantity":-371,"NonAllocateQuantity":-552,"mNonAllocateQuantity":-181,"mAllocatedQuantity":21497,"batchCount":132,"AllocatedQuantity":74519,"allocatorCount":38},"ResponseError":null,"CheckedKey":null,"Message":null}'
    ss=js.check(jsl2,'"issuccess":true,"ResponseError":null')
    print (ss)

    # jsl2=json.loads(jsl)
    # a,b=js.json_regmatch("partnerteamlist,123",'.*',jsl2)
    # print(a,b)
    #
    # keys=js.json_reg('data\d ,partnerteamlist ,pteamprice','\d{3}',jsl2)
    # print(keys)