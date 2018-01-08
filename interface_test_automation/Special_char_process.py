__author__ = 'zuozhijun'
def SpCharReplace(char):
        #char=char
    temp=str(char)
    for i in  temp:
        if '<'==i:
            char= char.replace('<','《')
        if '>' == i:
            char = char.replace('>', '》')
        if '\'' == i:
            char = char.replace('\'', '')#处理单引号
        if '\\' == i:
            char = char.replace('\\', '')#处理反斜杠\
        if '\"' == i:
            char = char.replace('\"', '`')  # 处理双引号"
        if '&' == i:
            char = char.replace('&', '-')  # 处理&号"
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
        #在后面扩展其他特殊字符
    return char