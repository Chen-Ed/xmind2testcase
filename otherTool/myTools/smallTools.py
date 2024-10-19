import pyperclip
import re


def apifox_to_ATX(jsonTEXT):
    """
    请求体{{变量}} 转为 ${变量}
    """
    a = jsonTEXT.strip()
    a = a.replace("{{", "${").replace("}}", "}")
    # 复制到剪贴板
    pyperclip.copy(a)
    return a


def ATX_to_apifox(jsonTEXT):
    """
    ${变量} 转为 {{变量}}
    """
    a = jsonTEXT.strip()
    a = re.sub(r'\$\{(\w+)\}', r'{{\1}}', a)
    # 复制到剪贴板
    pyperclip.copy(a)
    return a

if __name__ == '__main__':
    print(apifox_to_ATX('{"a": "{{a}}", "b": "{{b}}", "c": "{{c}}"}'))
    print(ATX_to_apifox('{"a": "${a}", "b": "${b}", "c": "${c}"}'))
