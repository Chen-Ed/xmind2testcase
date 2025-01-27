#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import logging
from webtool.xmind2case import xmind_to_gitee_csv_file

logging.basicConfig(level=logging.INFO)


def main():
    xmind_file = 'docs/gitee_testcase_template.xmind'
    print('Start to convert XMind file: %s' % xmind_file)

    # 1、testcases import file
    # (1) zentao
    # zentao_csv_file = xmind_to_zentao_csv_file(xmind_file)
    # print('Convert XMind file to zentao csv file successfully: %s' % zentao_csv_file)
    gitee_csv_file = xmind_to_gitee_csv_file(xmind_file)
    print('Convert XMind file to gitee csv file successfully: %s' % gitee_csv_file)
    # (2) testlink
    # testlink_xml_file = xmind_to_testlink_xml_file(xmind_file)
    # print('Convert XMind file to testlink xml file successfully: %s' % testlink_xml_file)

    # # 2、 testcases json file
    # # (1) testsuite
    # testsuite_json_file = xmind_testsuite_to_json_file(xmind_file)
    # print('Convert XMind file to testsuite json file successfully: %s' % testsuite_json_file)
    # # (2) testcase
    # testcase_json_file = xmind_testcase_to_json_file(xmind_file)
    # print('Convert XMind file to testcase json file successfully: %s' % testcase_json_file)
    #
    # # 3、test dict/json data
    # # (1) testsuite
    # testsuites = get_xmind_testsuite_list(xmind_file)
    # print('Convert XMind to testsuits dict data:\n%s' %
    #       json.dumps(testsuites, indent=2, separators=(',', ': '), ensure_ascii=False))
    # # (2) testcase
    # testcases = get_xmind_testcase_list(xmind_file)
    # print('Convert Xmind to testcases dict data:\n%s' %
    #       json.dumps(testcases, indent=4, separators=(',', ': '), ensure_ascii=False))
    # # (3) xmind file
    # workbook = xmind.load(xmind_file)
    # print('Convert XMind to Json data:\n%s' %
    #       json.dumps(workbook.getData(), indent=2, separators=(',', ': '), ensure_ascii=False))
    #
    # print('Finished conversion, Congratulations!')


if __name__ == '__main__':
    main()