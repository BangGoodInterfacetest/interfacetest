import base64
import io
a = "<urlopen error [WinError 10061] 由于目标计算机积极拒绝，无法连接。>"
b = base64.b64encode(bytes(a,'gb2312')) # 对字符串编码  URLError(ConnectionRefusedError(10061, '由于目标计算机积极拒绝，无法连接。', None, 10061),) this is a test   <urlopen error [WinError 10061] 由于目标计算机积极拒绝，无法连接。>
print ('b11:',b)
print ('b12:',base64.b64decode(b) )# 对字符串解码
c = io.StringIO()
c.write(a)
d = io.StringIO()
e = io.StringIO()
c.seek(0)
print(c, d)
#s1=str(c)
print(type(c))
base64.b64encode(bytes(str(c),'gb2312'))# 对StringIO内的数据进行编码
print (d.getvalue())
d.seek(0)
base64.decode(d, e) # 对StringIO内的数据进行解码
print (e.getvalue())
a = "this is a +test"
b = base64.urlsafe_b64encode(bytes(a,'gb2312')) # 进行url的字符串编码
print (b)
print (base64.urlsafe_b64decode(b))

a="qwert"
temp = a[:]
for i in temp:
    if 'q' in i:
        print(i)
        str(i)
        li=i.replace('q','a')
        print(li)
        li +=li
        #i.
        #a[2]=""
print(a)

char="<te'e\\e\"e&e||e%r*t（y-u)3>"
temp=str(char)
for i in  temp:
        if '<'==i:
            char= char.replace('<','《')
        if '>' == i:
            char = char.replace('>', '》')
        if '\'' == i:
            char = char.replace('\'', '') #处理单引号
        if '\\' == i:
            char = char.replace('\\', '') #处理反斜杠 \
        if '\"' == i:
            char = char.replace('\"', '_')  # 处理双引号"
        if '&' == i:
            char = char.replace('&', '_')  # 处理双引号&
        if '|' == i:
            char = char.replace('|', '')
        if '@' == i:
            char = char.replace('@', '.')
        if '%' == i:
            char = char.replace('%', "`")  # 处理单引号
        if '*' == i:
            char = char.replace('*', '`')  # 处理反斜杠\
        if '("' == i:
            char = char.replace('\"', '`')  # 处理双引号"
        if ')"' == i:
            char = char.replace(')"', '`')
        if '-' == i:
            char = char.replace('-', '`')  # 处理&号"
            print(char)
print(char)