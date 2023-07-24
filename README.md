#SCF-ihoneyBakFileScan_Modify

##一、起因

​       之前其实一直不怎么想用扫描器这种工具，因为一扫就被封，换ip又很烦。最近几个月各种攻防一大堆，很多目标存在备份文件的可能性其实挺大的。github存在这么一款工具ihoneyBakFileScan_Modify，这个玩意其实很不错，会自动生成一些字典然后去跑。最近用cs也比较多，也会用到云函数来进行隐匿，所以最后就出现了这个想法，将工具上云函数。

##二、操作详情

创建云函数

![image-20230724164302947](/Users/linlu/Library/Application Support/typora-user-images/image-20230724164302947.png)

输入代码

```
import requests
import logging
import json
from copy import deepcopy
import time
from hurry.filesize import size
from fake_headers import Headers
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.WARNING, format="%(message)s")


def vlun(urltarget):
    try:
        header = Headers(
            # generate any browser & os headeers
            headers=False  # don`t generate misc headers
        )
        r = requests.get(url=urltarget, headers=header.generate(), timeout=timeout, allow_redirects=False, stream=True, verify=False)
        if (r.status_code == 200) & ('html' not in r.headers.get('Content-Type')) & (
                'image' not in r.headers.get('Content-Type')) & ('xml' not in r.headers.get('Content-Type')) & (
                'text' not in r.headers.get('Content-Type')) & ('json' not in r.headers.get('Content-Type')) & (
                'javascript' not in r.headers.get('Content-Type')):
            tmp_rarsize = int(r.headers.get('Content-Length'))
            rarsize = str(size(tmp_rarsize))
            if (int(rarsize[0:-1]) > 0):
                result_dict = {
                    "status": "success",
                    "url": urltarget,
                    "size": rarsize
                }
                
                return result_dict
            else:
                result_dict = {
                    "status": "fail",
                    "url": urltarget
                }
                return result_dict
        else:
            result_dict = {
                "status": "fail",
                "url": urltarget
            }
            
            return result_dict
    except Exception as e:
        result_dict = {
            "status": "fail",
            "url": urltarget
        }
        
        return result_dict


def urlcheck(target=None, ulist=None):
    if target is not None and ulist is not None:
        if target.startswith('http://') or target.startswith('https://'):
            if target.endswith('/'):
                ulist.append(target)
            else:
                ulist.append(target + '/')
        else:
            line = 'https://' + target
            if line.endswith('/'):
                ulist.append(line)
            else:
                ulist.append(line + '/')
        return ulist


def dispatcher(url_file=None, url=None, max_thread=1, dic=None):
    urllist = []
    check_urllist = []
    if url_file is not None and url is None:
        with open(str(url_file)) as f:
            while True:
                line = str(f.readline()).strip()
                if line:
                    urllist = urlcheck(line, urllist)
                else:
                    break
    elif url is not None and url_file is None:
        url = str(url.strip())
        urllist = urlcheck(url, urllist)
    else:
        pass

    for u in urllist:
        cport = None
        if u.startswith('http://'):
            ucp = u.lstrip('http://')
        elif u.startswith('https://'):
            ucp = u.lstrip('https://')
        if '/' in ucp:
            ucp = ucp.split('/')[0]
        if ':' in ucp:
            cport = ucp.split(':')[1]
            ucp = ucp.split(':')[0]
            www1 = ucp.split('.')
        else:
            www1 = ucp.split('.')
        wwwlen = len(www1)
        wwwhost = ''
        for i in range(1, wwwlen):
            wwwhost += www1[i]

        current_info_dic = deepcopy(dic)  # deep copy
        suffixFormat = ['.zip', '.rar', '.tar.gz', '.tgz', '.tar.bz2', '.tar', '.jar', '.war', '.7z', '.bak', '.sql',
                        '.gz', '.sql.gz', '.tar.tgz']
        domainDic = [ucp, ucp.replace('.', ''), ucp.replace('.', '_'), wwwhost, ucp.split('.', 1)[-1],
                     (ucp.split('.', 1)[1]).replace('.', '_'), www1[0], www1[1]]

        for s in suffixFormat:
            for d in domainDic:
                current_info_dic.extend([d + s])

        for info in current_info_dic:
            url = str(u) + str(info)
            check_urllist.append(url)

    results = []
    with ThreadPoolExecutor(max_thread) as p:
        futures = [p.submit(vlun, url) for url in check_urllist]
        for future in futures:
            result = future.result()
            results.append(result)

    return results


def main_handler(event, context):
    # domain = json.loads(event['body'])['domain']
    query_params = event.get('queryString', {})
    domain = str(query_params.get('domain'))
    thread = int(query_params.get('thread', 1))
    # thread = event.get('thread', {})
    print(domain)
    # thread = json.loads(event['body'])['thread']

        # 现在，request_body 是一个Python字典，其中包含传入的JSON数据
        # 你可以根据传入的JSON结构来处理数据
        # ...

        # 将处理后的结果转换为JSON格式的字符串并返回
    

    tmp_suffixFormat = ['.zip', '.rar', '.tar.gz', '.tgz', '.tar.bz2', '.tar', '.jar', '.war', '.7z', '.bak', '.sql',
                        '.gz', '.sql.gz', '.tar.tgz']
    tmp_info_dic = ['1', '127.0.0.1', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
                    '2020', '2021', '2022', '2023', '2024', '2025', 'admin', 'archive', 'asp', 'aspx', 'auth', 'back',
                    'backup', 'backups', 'bak', 'bbs', 'bin', 'clients', 'code', 'com', 'customers', 'dat', 'data',
                    'database', 'db', 'dump', 'engine', 'error_log', 'faisunzip', 'files', 'forum', 'home', 'html',
                    'index', 'joomla', 'js', 'jsp', 'local', 'localhost', 'master', 'media', 'members', 'my', 'mysql',
                    'new', 'old', 'orders', 'php', 'sales', 'site', 'sql', 'store', 'tar', 'test', 'user', 'users',
                    'vb', 'web', 'website', 'wordpress', 'wp', 'www', 'wwwroot', 'root', 'log']

    info_dic = []
    for a in tmp_info_dic:
        for b in tmp_suffixFormat:
            info_dic.extend([a + b])

    global timeout
    timeout = 3

    try:
        if domain:
            results = dispatcher(url=domain, max_thread=thread, dic=info_dic)

            # 将列表转换为JSON格式的字符串
            response_data = json.dumps(results)
            return response_data
        else:
            return json.dumps({"error": "[!] Please specify a URL."})
    except Exception as e:
        return {"error": str(e)}
```

部署可能测试会提示缺少模块，可以将原模版的requirements.txt导入然后进行安装

我建议是cd src然后python3.7 -m pip intsall -r requirements.txt -t . 这样子安装。

点击测试一下，如果出现这样就说明函数没啥问题了。

![image-20230724164338801](/Users/linlu/Library/Application Support/typora-user-images/image-20230724164338801.png)

然后创建触发器

![image-20230724164346988](/Users/linlu/Library/Application Support/typora-user-images/image-20230724164346988.png)

超时时间最好长一点，有的时候会出现扫描时间过长这种情况

![image-20230724164355927](/Users/linlu/Library/Application Support/typora-user-images/image-20230724164355927.png)

然后修改路径为根路径就好了，用其他的也行。

![image-20230724164403453](/Users/linlu/Library/Application Support/typora-user-images/image-20230724164403453.png)

我这边是把集成响应关了，没具体确定要不要开。

![image-20230724164411728](/Users/linlu/Library/Application Support/typora-user-images/image-20230724164411728.png)

然后api测试一下，这样就可以了。

这样可以直接在网站上进行敏感目录扫描，但是这样还是好麻烦，索性写了个本地调用的脚本进行尝试

```
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
        url = "https://xxxxxxxxxx.gz.apigw.tencentcs.com/index?domain=" + args.url + "&thread=" + args.thread
        response_data = request(url)
        response_json = json.loads(response_data)  # 解析返回的JSON字符串为字典列表
        for resource in response_json:
            if resource.get("status") == "success":
                success_records.append(resource)
    elif args.file is not None:
        with open(args.file, 'r') as f:
            for line in f.readlines():
                url = "https://xxxxxxxxxx.gz.apigw.tencentcs.com/index?domain=" + line.strip() + "&thread=" + args.thread
                response_data = request(url)
                response_json = json.loads(response_data)  # 解析返回的JSON字符串为字典列表
                for resource in response_json:
                    if resource.get("status") == "success":
                        success_records.append(resource)

    if success_records:
        domain = url.split('//')[-1].split('/')[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{domain}_{timestamp}_success_records.txt"
        with open(filename, 'w') as f:
            json.dump(success_records, f, indent=2)

        print(f"成功记录已保存到文件：{filename}")
    else:
        print("未找到包含\"success\"的记录。")

```



运行方式的话就是

python3 index.py --file url.txt --thread 10

python3 index.py --url http://baidu.com --thread 10

如果存在的话就会创建一个文件

![image-20230724164435490](/Users/linlu/Library/Application Support/typora-user-images/image-20230724164435490.png)

![image-20230724164438390](/Users/linlu/Library/Application Support/typora-user-images/image-20230724164438390.png)
