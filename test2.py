import re


def reg_search(text, regex_list):
    # 预处理：只去掉换行，保留空格避免影响格式
    processed_text = text.replace('\n', '')
    result = []

    for field_regex in regex_list:
        item = {}
        for field, regex in field_regex.items():
            # 匹配时忽略大小写，兼容更多情况
            matches = re.findall(regex, processed_text, re.IGNORECASE)

            if not matches:
                # 换股期限默认空列表，其他字段默认None
                item[field] = [] if field == '换股期限' else None
                continue

            # 处理换股期限，格式化日期
            if field == '换股期限':
                date_list = []
                for match in matches:
                    # 确保是(年,月,日)的元组
                    if isinstance(match, tuple) and len(match) == 3:
                        year, month, day = match
                        # 清洗掉非数字字符
                        year = re.sub(r'\D', '', year)
                        month = re.sub(r'\D', '', month)
                        day = re.sub(r'\D', '', day)
                        # 补全位数并拼接
                        if year and month and day:
                            date_str = f"{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}"
                            date_list.append(date_str)
                item[field] = date_list

            # 处理其他字段
            else:
                first_match = matches[0]
                # 从分组中取有效部分
                if isinstance(first_match, tuple):
                    valid_part = max(first_match, key=lambda x: len(x.strip()), default='')
                else:
                    valid_part = first_match.strip()
                # 去掉首尾多余字符
                item[field] = re.sub(r'^[^a-zA-Z0-9.]+|[^a-zA-Z0-9.]+$', '', valid_part)

        result.append(item)

    return result


# 示例用法
if __name__ == "__main__":
    # 测试文本：包含各种格式情况
    text = '''
标的证券：本期证券为可交换债券，对应股票代码:  600900.SH！（简称：长江电力）。
换股期限：自发行结束后12个月起，即 2023年 06月 2日 至 2027 年6月01日止；
另附：可能存在的其他日期格式 2023-6-2 或 2027.06.1（但优先匹配年/月/日格式）。
'''
    # 正则表达式，兼容多种格式
    regex_list = [
        {
            '标的证券': r'股票代码[:：\s]*(\d+\.\s*[A-Za-z]{2})',  # 容忍代码前后的空格、符号
            '换股期限': r'(\d{4})\s*[年/-]\s*(\d{1,2})\s*[月/-]\s*(\d{1,2})\s*[日.]?'  # 兼容多种分隔符
        }
    ]

    print(reg_search(text, regex_list))
