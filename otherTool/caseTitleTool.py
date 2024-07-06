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
    ff = '【新增】,【修改】,【查看】'.split(',')
    g = '【用户】，【角色】，【权限】，【部门】，【消息\公告】，【公司】，【项目】，【操作记录】，【岗位】'.split('，')
    h = '新增，修改，查看，导出'.split('，')
    i = '【项目列表】,【项目详情信息】,【项目成员】,【项目关联公司】,【项目关联公司详情信息】,【项目隐私协议】,【项目隐私协议-历史版本】'.split(',')
    j = '【角色】,【角色名称】,【角色权限配置】,【角色列表】,【角色详情】,【角色权限配置详情】,【个人页面，角色指派信息】'.split(',')

    templeStr = """在NWCS BU中，[0] [1]数据，预期成功
	[0] [1]数据
		成功"""
    inputList=[ff,g]
    combinations = get_sorted_combinations(inputList,ff)
    insertStr(templeStr,combinations)
