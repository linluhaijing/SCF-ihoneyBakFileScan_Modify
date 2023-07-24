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
        if (r.status_code == 200) & ('html' not 在 r.headers。get('Content-Type')) & (
                'image' not 在 r.headers。get('Content-Type')) & ('xml' not 在 r.headers。get('Content-Type')) & (
                'text' not 在 r.headers。get('Content-Type')) & ('json' not 在 r.headers。get('Content-Type')) & (
                'javascript' not 在 r.headers。get('Content-Type')):
            tmp_rarsize = int(r.headers。get('Content-Length'))
            rarsize = str(size(tmp_rarsize))
            if (int(rarsize[0:-1]) > 0):
                result_dict = {
                    "status": "success"，
                    "url": urltarget,
                    "size": rarsize
                }
                
                return result_dict
            else:
                result_dict = {
                    "status": "fail"，
                    "url": urltarget
                }
                return result_dict
        else:
            result_dict = {
                "status": "fail"，
                "url": urltarget
            }
            
            return result_dict
    except Exception as e:
        result_dict = {
            "status": "fail"，
            "url": urltarget
        }
        
        return result_dict


def urlcheck(target=None, ulist=None):
    if target is not None 和 ulist is not None:
        if target.startswith('http://') 或 target.startswith('https://'):
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
    if url_file is not None 和 url is None:
        with open(str(url_file)) as f:
            while True:
                line = str(f.readline())。strip()
                if line:
                    urllist = urlcheck(line, urllist)
                else:
                    break
    elif url is not None 和 url_file is None:
        url = str(url.strip())
        urllist = urlcheck(url, urllist)
    else:
        pass

    for u 在 urllist:
        cport = None
        if u.startswith('http://'):
            ucp = u.lstrip('http://')
        elif u.startswith('https://'):
            ucp = u.lstrip('https://')
        if '/' 在 ucp:
            ucp = ucp.split('/')[0]
        if ':' 在 ucp:
            cport = ucp.split(':')[1]
            ucp = ucp.split(':')[0]
            www1 = ucp.split('.')
        else:
            www1 = ucp.split('.')
        wwwlen = len(www1)
        wwwhost = ''
        for i 在 range(1, wwwlen):
            wwwhost += www1[i]

        current_info_dic = deepcopy(dic)  # deep copy
        suffixFormat = ['.zip'， '.rar'， '.tar.gz'， '.tgz'， '.tar.bz2'， '.tar'， '.jar'， '.war'， '.7z'， '.bak'， '.sql'，
                        '.gz'， '.sql.gz'， '.tar.tgz']
        domainDic = [ucp, ucp.replace('.'， ''), ucp.replace('.'， '_'), wwwhost, ucp.split('.'， 1)[-1]，
                     (ucp.split('.'， 1)[1])。replace('.'， '_'), www1[0], www1[1]]

        for s 在 suffixFormat:
            for d 在 domainDic:
                current_info_dic.extend([d + s])

        for info 在 current_info_dic:
            url = str(u) + str(info)
            check_urllist.append(url)

    results = []
    with ThreadPoolExecutor(max_thread) as p:
        futures = [p.submit(vlun, url) for url 在 check_urllist]
        for future 在 futures:
            result = future.result()
            results.append(result)

    return results


def main_handler(event, context):
    # domain = json.loads(event['body'])['domain']
    query_params = event.get('queryString'， {})
    domain = str(query_params.get('domain'))
    thread = int(query_params.get('thread'， 1))
    # thread = event.get('thread', {})
    print(domain)
    # thread = json.loads(event['body'])['thread']

        # 现在，request_body 是一个Python字典，其中包含传入的JSON数据
        # 你可以根据传入的JSON结构来处理数据
        # ...

        # 将处理后的结果转换为JSON格式的字符串并返回
    

    tmp_suffixFormat = ['.zip'， '.rar'， '.tar.gz'， '.tgz'， '.tar.bz2'， '.tar'， '.jar'， '.war'， '.7z'， '.bak'， '.sql'，
                        '.gz'， '.sql.gz'， '.tar.tgz']
    tmp_info_dic = ['1'， '127.0.0.1'， '2010'， '2011'， '2012'， '2013'， '2014'， '2015'， '2016'， '2017'， '2018'， '2019'，
                    '2020'， '2021'， '2022'， '2023'， '2024'， '2025'， 'admin'， 'archive'， 'asp'， 'aspx'， 'auth'， 'back'，
                    'backup'， 'backups'， 'bak'， 'bbs'， 'bin'， 'clients'， 'code'， 'com'， 'customers'， 'dat'， 'data'，
                    'database'， 'db'， 'dump'， 'engine'， 'error_log'， 'faisunzip'， 'files'， 'forum'， 'home'， 'html'，
                    'index'， 'joomla'， 'js'， 'jsp'， 'local'， 'localhost'， 'master'， 'media'， 'members'， 'my'， 'mysql'，
                    'new'， 'old'， 'orders'， 'php'， 'sales'， 'site'， 'sql'， 'store'， 'tar'， 'test'， 'user'， 'users'，
                    'vb'， 'web'， 'website'， 'wordpress'， 'wp'， 'www'， 'wwwroot'， 'root'， 'log']

    info_dic = []
    for a 在 tmp_info_dic:
        for b 在 tmp_suffixFormat:
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
