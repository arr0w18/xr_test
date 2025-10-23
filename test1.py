import requests
import csv
import json
from urllib3.exceptions import InsecureRequestWarning

# 禁用不安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def fetch_2023_treasury_bonds():
    search_api = "https://www.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Referer": "https://www.chinamoney.com.cn/english/bdInfo/",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "_ulta_id.ECM-Prod.e9dc=7904c88b114cfb6b; _ulta_ses.ECM-Prod.e9dc=59e5a9eee90f5709; AlteonP10=CWk9RSw/F6zbp3Rs0tUTdQ$$",
        "Origin": "https://www.chinamoney.com.cn"
    }

    # 筛选参数：国债(100001) + 2023年
    form_data = {
        "pageNo": "1",
        "pageSize": "15",
        "bondType": "100001",
        "issueYear": "2023",
        "isin": "",
        "bondCode": "",
        "issueEnty": "",
        "couponType": "",
        "rtngShrt": "",
        "bondSpclPrjctVrty": ""
    }

    # 字段映射关系
    field_mapping = {
        'ISIN': 'isin',
        'Bond Code': 'bondCode',
        'Issuer': 'entyFullName',
        'Bond Type': 'bondType',
        'Issue Date': 'issueStartDate',
        'Latest Rating': 'debtRtng'
    }
    target_cols = list(field_mapping.keys())
    all_data = [target_cols]
    current_page = 1
    has_more = True

    try:
        print("开始获取2023年国债数据...")
        while has_more:
            form_data["pageNo"] = str(current_page)
            print(f"处理第{current_page}页...")

            # 发送请求
            response = requests.post(
                search_api,
                headers=headers,
                data=form_data,
                timeout=30,
                verify=False
            )
            response.encoding = response.apparent_encoding

            # 解析响应
            json_result = json.loads(response.text.strip().rstrip(';'))
            data_dict = json_result.get("data", {})
            total_count = data_dict.get("total", 0)
            bond_list = data_dict.get("resultList", [])

            if not bond_list:
                print("无更多数据")
                break

            # 提取数据
            for item in bond_list:
                if not isinstance(item, dict):
                    continue

                row = [
                    str(item.get(field_mapping[col], "")).strip()
                    for col in target_cols
                ]
                # 处理评级字段的特殊标记
                row[-1] = row[-1].replace("---", "")
                all_data.append(row)

            # 分页控制
            next_page = data_dict.get("nextpg", 0)
            if next_page == 0 or len(all_data) - 1 >= total_count:
                has_more = False
            else:
                current_page = next_page

        # 保存数据
        csv_filename = "2023_treasury_bonds.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
            csv.writer(f).writerows(all_data)

        total = len(all_data) - 1
        print(f"完成！共获取{total}条数据，已保存至{csv_filename}")

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except json.JSONDecodeError:
        print("响应格式错误，无法解析JSON")
    except Exception as e:
        print(f"处理错误: {e}")


if __name__ == "__main__":
    fetch_2023_treasury_bonds()