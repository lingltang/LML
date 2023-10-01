def extract_with_index(values, start, end):
    """
    从values集合列表中提取对应索引范围的指
    :param values: values列表
    :param start: 起始下标(包含)
    :param end: 结束下标(包含)
    :return:
    """
    if end == -1:
        return values[start:]
    else:
        return values[start:end + 1]
