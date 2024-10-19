#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convert XMind fie to gitee testcase csv file
把xmind转换为 中华广场 特定格式 的csv
"""

import csv
import logging
import os
from webtool.xmind2case.utils import get_xmind_testcase_list, get_absolute_path
import re




def xmind_to_xhc_csv_file(xmind_file):
    """Convert XMind file to a gitee csv file"""
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to gitee file...', xmind_file)
    testcases = get_xmind_testcase_list(xmind_file)

    # fileheader = ["所属模块", "用例标题", "前置条件", "步骤", "预期", "关键词", "优先级", "用例类型", "适用阶段"]
    # fileheader = ["序号","功能模块*", "用例名称*", "维护人", "用例类型", "优先级", "前置条件", "备注", "步骤描述", "预期结果"]
    fileheader = ["用例类型", "用例目录", "功能点", "用例名称", "前置条件", "用例步骤", "预期结果", "执行结果",
                  "优先级", "备注"]

    gitee_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        gitee_testcase_rows.append(row)

    gitee_file = xmind_file[:-6] + '.csv'
    if os.path.exists(gitee_file):
        os.remove(gitee_file)
        # logging.info('The gitee csv file already exists, return it directly: %s', gitee_file)
        # return gitee_file

    with open(gitee_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(gitee_testcase_rows)
        logging.info('Convert XMind file(%s) to a gitee csv file(%s) successfully!', xmind_file, gitee_file)

    return gitee_file


def split_and_number_string(input_string, delimiter=',',endwith=''):
    """
    用于添加case前置条件的序号
    将输入的字符串按指定分隔符切割，并添加序号
    """

    # 使用指定的分隔符切割字符串
    elements = input_string.split(delimiter)

    # 初始化一个空列表来保存带序号的元素
    numbered_elements = []

    # 遍历切割后的元素并添加序号
    if len(elements) == 1:
        numbered_elements.append(f"1.{input_string}")
    else:
        for i, element in enumerate(elements):
            numbered_element = f"{i + 1}.{element}"
            numbered_elements.append(numbered_element)

    # 将带序号的元素组合成一个字符串
    result_string = '\n'.join(numbered_elements)

    return result_string
def gen_a_testcase_row(testcase_dict):
    case_module = gen_case_module(testcase_dict['suite'])
    case_point = re.findall(r'^\[.*\]', testcase_dict['name'])[0]
    case_title = testcase_dict['name'].replace(case_point, '')
    case_point = re.sub(r'\[|\]', '', case_point)
    case_precontion = split_and_number_string (testcase_dict['preconditions'], '\r\n')

    case_step, case_expected_result = gen_case_step_and_expected_result(testcase_dict['steps'])
    case_keyword = ''
    case_priority = gen_case_priority(testcase_dict['importance'])
    case_type = gen_case_type(testcase_dict['execution_type'])
    case_apply_phase = '功能测试'
    # row = [case_module, case_title, case_precontion, case_step, case_expected_result, case_keyword, case_priority, case_type, case_apply_phase]
    # row = ["",case_module,case_title,"Lucas 陈应东",case_apply_phase,case_priority,case_precontion,case_keyword,case_step,case_expected_result]
    row = [case_apply_phase, case_module, case_point, case_title, case_precontion, case_step, case_expected_result,
           "通过", case_priority, ""]
    return row


def gen_case_module(module_name):
    if module_name:
        module_name = module_name.replace('（', '(')
        module_name = module_name.replace('）', ')')
    else:
        module_name = '/'

    return module_name


def gen_case_step_and_expected_result(steps):
    case_step = ''
    case_expected_result = ''

    for step_dict in steps:
        case_step += str(step_dict['step_number']) + '. ' + step_dict['actions'].replace('\n', '').strip() + '\n'
        case_expected_result += str(step_dict['step_number']) + '. ' + \
                                step_dict['expectedresults'].replace('\n', '').strip() + '\n' \
            if step_dict.get('expectedresults', '') else ''

    return case_step, case_expected_result


def gen_case_priority(priority):
    mapping = {1: 'P0', 2: 'P1', 3: 'P2'}
    if priority in mapping.keys():
        return mapping[priority]
    else:
        return 'P1'


def gen_case_type(case_type):
    mapping = {1: '手动', 2: '自动'}
    if case_type in mapping.keys():
        return mapping[case_type]
    else:
        return '手动'


if __name__ == '__main__':
    # xmind_file = '../docs/gitee_testcase_template.xmind'
    from pathlib import Path

    xmind_file = Path('~') / "Desktop" / "用例" / "中华广场Portal用例.xmind"
    xhc_csv_file = xmind_to_xhc_csv_file(xmind_file)
    print('转换XHC用例成功: ', xhc_csv_file)
