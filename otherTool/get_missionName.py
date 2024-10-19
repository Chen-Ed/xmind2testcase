def get_GiteeMission(PJ_name, needs: list):
    """
    把gitee需求 转为 自己的gitee任务
    """
    print(get_GiteeMission.__doc__.strip().center(60, '*'))
    missions = []
    missions.append('【测试】' + f'【{PJ_name}】 功能测试')
    missions.append('【测试】' + f'【{PJ_name}】 用例执行')
    missions.append('【测试】' + f'【{PJ_name}】 回归测试')
    missions.append('【测试】' + f'【{PJ_name}】 用例设计')
    missions += ['【测试】' + f"""【{PJ_name}】#{i} 功能测试""" for i in needs]

    print('\n'.join(missions))


def get_XmindMission(Model, needs: list):
    """
    把gitee需求 转为 xmind8标题
    """
    print(get_XmindMission.__doc__.strip().center(60, '*'))

    missions = [f"""{Model}#{i}""" for i in needs]
    print('\n'.join(missions))


if __name__ == '__main__':
    needs = """IOBQ	SOPI切换剩余模板前测试报告
IOBR	A.Connect系统跳转入口切换和字眼调整
IOBY	模板类型为空时，隐藏分类
IOE7	补充催促功能
IOH0	SOPI域名重定向处理和排查
IOIH	KTSP项目跳转迁移
IOIT	导出IHM本次迁移site人员名单，以便复核
IOPD	列表和项目标题调整
""".strip().replace('	', ' ').replace('/', ',').split('\n')
    get_GiteeMission('XC-SOPI 1.9.1', needs)
    get_XmindMission('XC-SOPI/1.9.1/', needs)
