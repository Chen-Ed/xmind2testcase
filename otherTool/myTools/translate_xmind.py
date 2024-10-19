import xmind
from opencc import OpenCC
from common.comm import logger

def translation_xmind(input_xmind: str, output_xmind: str, config='s2t'):
    """
    翻译XMind文件
    s2t 表示从简体到繁体，t2s 则是从繁体到简体
    """
    # 创建转换器实例
    cc = OpenCC(config)

    def traverse_topics(old_topics, new_topoic):
        if title := old_topics.get('title'):
            new_title = cc.convert(title)
            new_topoic.setTitle(new_title)

        if note := old_topics.get('note'):
            new_note = cc.convert(note)
            new_topoic.setPlainNotes(new_note)

        markers = old_topics.get('markers')
        if markers and len(markers) > 0:
            for marker in markers:
                new_topoic.addMarker(marker)

        if old_topics.get('topics') is not None and len(old_topics.get('topics')):
            for sub_topic in old_topics.get('topics'):
                new_sub_topic = new_topoic.addSubTopic()
                traverse_topics(sub_topic, new_sub_topic)

    # 加载XMind文件
    workbook = xmind.load(input_xmind)
    new_workbook = xmind.load('new.xmind')
    # 遍历工作簿中的所有工作表
    for i, old_sheet in enumerate(workbook.getSheets()):
        sheet_title = old_sheet.getTitle()
        # 设置画布
        if i == 0:
            new_sheet = new_workbook.getPrimarySheet()
        else:
            new_sheet = new_workbook.createSheet()
        new_sheet.setTitle(cc.convert(sheet_title))
        old_topics = old_sheet.getData().get('topic')
        new_root_topic = new_sheet.getRootTopic()
        new_root_topic.setTitle(cc.convert(old_topics.get('title')))
        traverse_topics(old_topics, new_root_topic)

    xmind.save(new_workbook,output_xmind)
    logger.info(f'翻译完成，保存路径为：{output_xmind}')


if __name__ == '__main__':
    input_xmind = r'D:\pythonProject\xmind2testcase\webtool\uploads\测试翻译.xmind'
    output_xmind = r'D:\pythonProject\xmind2testcase\webtool\uploads\new_测试翻译.xmind'
    translation_xmind(input_xmind, output_xmind)
