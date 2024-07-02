#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv
import logging
import os
from xmind2testcase.utils import get_xmind_testcase_list, get_absolute_path

"""
Convert XMind fie to gitee testcase csv file 
"""


def xmind_to_gitee_csv_file(xmind_file):
    """Convert XMind file to a gitee csv file"""
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to gitee file...', xmind_file)
    testcases = get_xmind_testcase_list(xmind_file)

    # fileheader = ["所属模块", "用例标题", "前置条件", "步骤", "预期", "关键词", "优先级", "用例类型", "适用阶段"]
    fileheader = ["序号","功能模块*", "用例名称*", "维护人", "用例类型", "优先级", "前置条件", "备注", "步骤描述", "预期结果"]

    gitee_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        gitee_testcase_rows.append(row)

    gitee_file = xmind_file[:-6] + '.csv'
    if os.path.exists(gitee_file):
        os.remove(gitee_file)
        # logging.info('The gitee csv file already exists, return it directly: %s', gitee_file)
        # return gitee_file

    with open(gitee_file, 'w', encoding='utf-8-sig',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(gitee_testcase_rows)
        logging.info('Convert XMind file(%s) to a gitee csv file(%s) successfully!', xmind_file, gitee_file)

    return gitee_file


def gen_a_testcase_row(testcase_dict):
    case_module = gen_case_module(testcase_dict['suite'])
    case_title = testcase_dict['name']
    case_precontion = testcase_dict['preconditions']
    case_step, case_expected_result = gen_case_step_and_expected_result(testcase_dict['steps'])
    case_keyword = ''
    case_priority = gen_case_priority(testcase_dict['importance'])
    case_type = gen_case_type(testcase_dict['execution_type'])
    case_apply_phase = '功能测试'
    # row = [case_module, case_title, case_precontion, case_step, case_expected_result, case_keyword, case_priority, case_type, case_apply_phase]
    row = ["",case_module,case_title,"Lucas 陈应东",case_apply_phase,case_priority,case_precontion,case_keyword,case_step,case_expected_result]
    return row


def gen_case_module(module_name):
    if module_name:
        module_name = module_name.replace('（', '(')
        module_name = module_name.replace('）', ')')
    else:
        module_name = '/'
    # gitee模块名只能15个字符
    nameList = module_name.split('/')
    if len(nameList[-1])>=14:
        nameList[-1] = nameList[-1][0:12]+'..'
    return '/'.join(nameList)


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
    xmind_file = "C:/Users/te_chenyingdong/Desktop/portal 2.1.5功能用例.xmind"
    gitee_csv_file = xmind_to_gitee_csv_file(xmind_file)
    print('Conver the xmind file to a gitee csv file succssfully: %s', gitee_csv_file)