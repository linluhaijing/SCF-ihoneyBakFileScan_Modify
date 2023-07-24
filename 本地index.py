import datetime
import json
import requests
import argparse

def request(url, params=None):
    try:
        response = requests.get(url, params=params)

        # 确保请求成功（状态码200表示成功）
        if response.status_code == 200:
            return response.json()  # 解析JSON字符串为字典列表
        else:
            return []

    except requests.RequestException as e:
        print(f"发生异常：{e}")
        return []

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, help='url')
    parser.add_argument('--thread', type=str, help='thread')
    parser.add_argument('--file', type=str, help='file')
    args = parser.parse_args()

    success_records = []  # 用于存储包含"success"的记录

    if args.url is not None:
        url = "xxxxxxxxxxxxxxxxxxxxxx.gz.apigw.tencentcs.com/index?domain=" + args.url + "&thread=" + args.thread
        response_data = request(url)
        response_json = json.loads(response_data)  # 解析返回的JSON字符串为字典列表
        for resource 在 response_json:
            if resource.get("status") == "success":
                success_records.append(resource)
    elif args.file is not None:
        with open(args.file， 'r') as f:
            for line 在 f.readlines():
                url = "xxxxxxxxxxxxxxxxxxxx.tencentcs.com/index?domain=" + line.strip() + "&thread=" + args.thread
                response_data = request(url)
                response_json = json.loads(response_data)  # 解析返回的JSON字符串为字典列表
                for resource 在 response_json:
                    if resource.get("status") == "success":
                        success_records.append(resource)

    if success_records:
        domain = url.split('//')[-1]。split('/')[0]
        timestamp = datetime.datetime。当前()。strftime("%Y%m%d%H%M%S")
        filename = f"{domain}_{timestamp}_success_records.txt"
        with open(filename, 'w') as f:
            json.dump(success_records, f, indent=2)

        print(f"成功记录已保存到文件：{filename}")
    else:
        print("未找到包含\"success\"的记录。")
