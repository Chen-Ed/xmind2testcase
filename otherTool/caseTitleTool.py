import itertools
import pyperclip
import re
"""
    生成用例标题文件
"""
def get_sorted_combinations(lists:list[list],orderList=None):
    """生成元素的组合结果，并按指定列表排序

    Args:
        lists (list[list]): 需要组合的元素列表
        orderList (_type_): 排序列表

    Returns:
        _type_: _description_
    """
    if orderList is None:
        orderList = lists[0] 
    combinations = list(itertools.product(*lists))

    combinations.sort(key=lambda x: [orderList.index(i) for i in x if i in orderList])

    # result_str = '\n'.join([''.join(i) for i in combinations])
    # result_str = '\n'.join([strTemplates.format(i) for i in combinations])
    # print(result_str)

    # pyperclip.copy(result_str)
    # print('已复制到剪贴板！')
    return combinations

def insertStr(templeStr:str,combinations:list):
    """在模板字符串中，按顺序插入列表中的元素，多余元素舍弃。最后复制结果到剪贴板。

    Args:
        templeStr (str): 模板字符串 
        my_list (list): 元素列表
    """
    resultList = []
    # 找到字符串中的标记位置
    pattern = r'\[\d\]'
    matches = re.findall(pattern, templeStr)

    for my_list in combinations:
        input_string = templeStr
        # 将列表中的元素按照标记位置依次插入到字符串中
        for match in matches:
            index = int(match[1])
            if index < len(my_list):
                input_string = input_string.replace(match, my_list[index],1)
        # 替换完毕后收集起来
        resultList.append(input_string)

    # 输出结果
    result_str = '\n'.join(resultList)
    print(result_str)
    pyperclip.copy(result_str)
    print('已复制到剪贴板！')


if __name__ == '__main__':
    # a = '【增加】,【删除】,【更改】,【查看】'.split(',')
    b = '【公司】,【部门】,【个人】'.split(',')
    c = '【模糊】,【精确】 '.split(',')
    a = '【查看】,【导出】'.split(',')
    d = '【操作方式一】,【操作方式二】'.split(',')
    e = '【部分】,【全部】'.split(',')
    f = '【增加】,【删除】,【更改】'.split(',')
    g = """Leave Balance
Attendance
K11 eFlagging
Billing
RM+
旧SOPI
iOA
BrandBook
Ctrip
One-ITS
AccessControl
iHM
Tezign
PMS
Signature
Leasing""".split('\n')
    h = """BA 2.0 应用
BA 2.0 手册
SA.Pad 应用
SA.Pad 手册
TalentPlus 应用
TalentPlus 手册
E-Learning
NWDrive
Sharepoint HK
MICE
CRM+SOP
KPOS
Sharepoint GZ
Sharepoint BJ
Sharepoint SH
CRM+ 应用
FZ CRM Backend
FZ CRM Frontend
Qlikview
SSRS Report
eForm Portal
DMS NB
Customer
CRM+ HK
DMS TJ
DMS 手册
Brand DB""".split("\n")
    j = """默认工具
Office-Tools 办公工具
Pre-opening 开业工具
Operation 操作应用
Back-end Office 内部办公工具
Others 其他
Handbook 手册""".strip().split('\n')

    templeStr = """在应用管理页面，把应用的应用类型从 默认工具 切换为 【[0]】。
	点击应用分类标识
		返回包含应用类型：【[0]】
	点击【[0]】
		成功
	查看应用列表页面
		应用在【[0]】类中展示"""
    inputList=[j]
    combinations = get_sorted_combinations(inputList)
    insertStr(templeStr,combinations)