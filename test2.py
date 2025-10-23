import re


def reg_search(text, regex_list):
    # 处理文本，去除换行符，确保匹配不受换行影响
    processed_text = text.replace('\n', '')
    result = []

    for regex_dict in regex_list:
        item = {}
        for key in regex_dict:
            if key == '标的证券':
                # 匹配股票代码，格式为 数字.SH
                pattern = r'(\d+\.SH)'
                match = re.search(pattern, processed_text)
                item[key] = match.group(1) if match else None

            elif key == '换股期限':
                # 匹配带空格的日期格式（如：2023 年 6 月 2 日）
                # 允许数字与"年/月/日"之间有空格，并用非贪婪模式匹配两个日期
                pattern = r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日.*?(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日'
                match = re.search(pattern, processed_text)
                if match:
                    # 提取并格式化日期（补全两位数）
                    start_date = f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
                    end_date = f"{match.group(4)}-{match.group(5).zfill(2)}-{match.group(6).zfill(2)}"
                    item[key] = [start_date, end_date]
                else:
                    item[key] = []

        result.append(item)

    return result


# 测试代码
if __name__ == "__main__":
    text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债
券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
日至 2027 年 6 月 1 日止。
'''
    regex_list = [{'标的证券': '*自定义*', '换股期限': '*自定义*'}]
    print(reg_search(text, regex_list))