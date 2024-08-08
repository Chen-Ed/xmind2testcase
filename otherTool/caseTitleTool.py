# -*- coding: utf-8 -*-
import itertools
import pyperclip
import re

"""
    生成用例标题文件
"""


def get_result(combination, res_rules):
    """
    根据输入的元素，匹配结果
    """
    default_result = res_rules['default_result']

    rules = res_rules['rules'].keys()
    # 匹配结果
    combination_str = ','.join(combination)
    for rule in rules:
        if re.fullmatch(rule, combination_str):
            return res_rules['rules'][rule]
    return default_result


def get_sorted_combinations(lists: list[list], orderList=None, res_rules=None):
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

    if orderList is not None:
        combinations.sort(key=lambda x: [orderList.index(i) for i in x if i in orderList])

    # result_str = '\n'.join([''.join(i) for i in combinations])
    # result_str = '\n'.join([strTemplates.format(i) for i in combinations])
    # print(result_str)

    # pyperclip.copy(result_str)
    # print('已复制到剪贴板！')
    new_combinations = []
    for combination in combinations:
        new_combinations.append({'item': list(combination), 'res': get_result(combination, res_rules)})
    return new_combinations


def insertStr(templeStr: str, combinations: list):
    """在模板字符串中，按顺序插入列表中的元素，多余元素舍弃。最后复制结果到剪贴板。

    Args:
        templeStr (str): 模板字符串 
        my_list (list): 元素列表
    """
    resultList = []
    # 找到字符串中的标记位置
    pattern = r'\[\d\]'
    matches = re.findall(pattern, templeStr)

    for combination in combinations:
        my_list = combination.get('item')
        input_string = templeStr
        # 将列表中的元素按照标记位置依次插入到字符串中
        for match in matches:
            index = int(match[1])
            if index < len(my_list):
                input_string = input_string.replace(match, f'【{my_list[index]}】', 1)
                input_string = input_string.replace('[res]', combination.get('res'))
        # 替换完毕后收集起来
        resultList.append(input_string)

    # 输出结果
    result_str = '\n'.join(resultList)
    print(result_str)
    pyperclip.copy(result_str)
    print('已复制到剪贴板！')


if __name__ == '__main__':
    # a = '增加,删除,更改,查看'.split(',')
    b = '公司,部门,个人'.split(',')
    c = '模糊,精确'.split(',')
    a = '查看,导出'.split(',')
    d = '操作方式一,操作方式二'.split(',')
    e = '部分,全部'.split(',')
    f = '增加,删除,更改'.split(',')
    ff = '新增,修改,查看'.split(',')
    fff = '新增,删除'.split(',')
    g = '用户，角色，权限，部门，消息\公告，公司，项目，操作记录，岗位'.split('，')
    h = '新增，修改，查看，导出'.split('，')
    i = '项目列表,项目详情信息,项目成员,项目关联公司,项目关联公司详情信息,项目隐私协议,项目隐私协议-历史版本'.split(',')
    j = '角色,角色名称,角色权限配置,角色列表,角色详情,角色权限配置详情,个人页面，角色指派信息'.split(',')
    角色类型 = '通用，项目，公司'.split('，')
    k = '人员名称，邮箱'.split('，')
    不切换的页面 = '系统设置，应用中心，消息中心，我的应用，个人设定'.split('，')
    登录方式 = 'AAS，邮箱+密码，手机+密码，手机+验证码，免密登录'.split('，')
    职员管理页_搜索条件 = '人事状态,数据源,用户类型,职员信息,工号,业务主体,公司,部门'.split(',')
    职员详情页_可更改信息 = '基本信息,公司部门,人事信息'.split(',')
    应用管理页_搜索条件 = '应用分类,应用状态,应用名称,业务主体'.split(',')
    # worflow1.8.1
    回调类型 = '同步（实时），异步'.split('，')
    权限项 = """回调记录-入口
回调记录-查询
回调记录-手动重试回调""".split('\n')
    流程tab页 = "任务查询页，流程实例页".split('，')
    tab页条件 = "任务状态，流程分类".split('，')
    流程tab页2 = "回调记录页".split('，')
    tab页条件2 = """流程实例ID
回调方式
回调节点类型
回调方式
时间范围""".split('\n')
    流程回调结果 = "流程回调成功，流程回调失败".split('，')
    手动重试结果 = "手动重试成功，手动重试失败".split('，')

    # XC-Portal 2.2.1
    应用名称 = "E-Learning，E-Leasing，Billing，RM+".split('，')
    应用名称2 = "E-Learning，E-Leasing".split('，')

    ip围栏状态1 = "开启围栏".split('，')
    ip围栏开启范围 = "勾选pc端，取消勾选pc端".split('，')
    登录类型1 = "外部，企业".split('，')
    登录类型2 = "邮箱+密码，手机+密码".split('，')
    res_rules = {
        "rules": {
            '关闭围栏,[^,]+,[^,]+,[^,]+': '登录成功，不需要输入邮箱/手机验证码',
            '开启围栏,[^,]+,[^,]+,[^,]+': '登录成功，不需要输入邮箱/手机验证码',
            '开启围栏,勾选pc端,企业,手机': '登录成功，不需要输入邮箱/手机验证码',
            '开启围栏,取消勾选pc端,[^,]+,[^,]+': '登录成功，不需要输入邮箱/手机验证码',
            '开启围栏,勾选pc端,[^,]+,[^,]+': '登录成功，页面需要输入邮箱/手机验证码',
            # '勾选pc端,[^,]+,[^,]+': '登录成功，页面需要输入邮箱/手机验证码'
        },
        "default_result": "*****************"
    }

    templeStr = """系统管理员配置[0]并[1]后,【ip围栏内】使用[2][3]登录portal。预期[res]。
	系统管理员配置[0]并[1]
		成功
	系统管理员退出登录
		成功
	【ip围栏内】使用[2][3]登录portal
		[res]"""
    inputList = [ip围栏状态1, ip围栏开启范围, 登录类型1, 登录类型2]
    combinations = get_sorted_combinations(lists=inputList, orderList=ip围栏状态1, res_rules=res_rules)
    insertStr(templeStr, combinations)
