def get_GiteeMission(PJ_name, needs: list):
    """
    把gitee需求 转为 自己的gitee任务
    """
    print(get_GiteeMission.__doc__.strip().center(60, '*'))
    missions = []
    missions.append('【测试】' + f'【{PJ_name}】 功能测试')
    missions.append('【测试】' + f'【{PJ_name}】 回归测试')
    missions.append('【测试】' + f'【{PJ_name}】 用例设计')
    missions += ['【测试】' + f"""【{PJ_name}】 #{i} 功能测试""" for i in needs]

    print('\n'.join(missions))


def get_XmindMission(Model, needs: list):
    """
    把gitee需求 转为 xmind8标题
    """
    print(get_XmindMission.__doc__.strip().center(60, '*'))

    missions = [f"""{Model}#{i}""" for i in needs]
    print('\n'.join(missions))


if __name__ == '__main__':
    needs = """IL1O	工作流—流转详情receive task节点兼容
ILOD	工作流—前端：会签配置默认选中并行
ILOB	工作流—前端：流转详情页面子任务支持展示多个
ILOA	工作流—流转详情页面数据接口调整（支持重复委派）
ILO9	工作流—前端：手动委派备注必填
ILO7	工作流—手动委派支持重复委派
ILIY	工作流—流程功能说明文档补充
ILFA	工作流—前端：指定人审批支持审批人为空自动跳过且支持配置会签
ILF8	工作流—指定人审批支持审批人为空自动跳过且支持会签功能
IKC3	工作流—1.8版本迭代工作项梳理
IL0E	工作流—receive task功能和配置设计
IKYR	工作流—前端：receive task功能节点相关配置
IKYQ	工作流—receive task后端功能开发
IKYP	工作流—receive task实现技术调研
IKYO	工作流—receive task实现
IKO3	工作流—同一待办支持多次重复委派和回收
IKNM	工作流—新、旧权限映射关系梳理
IKNL	工作流—管理端权限项梳理
IKNK	工作流—管理端权限项控制重构
IKNH	工作流—前端：管理端权限项控制重构
""".strip().replace('	', ' ').split('\n')
    get_GiteeMission('wf.1.8', needs)
    get_XmindMission('Workflow/1.8/', needs)
