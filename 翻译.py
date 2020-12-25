from gevent import monkey
import gevent
import requests
import re
import json
import random
import execjs
import urllib.parse as parse
from queue import Queue
monkey.patch_all()

in_dir = '反击式破碎机板锤的维修保养.xml'
out_dir = in_dir
# out_dir = '文章\\9.制砂机的成砂率如何提高？.xml'
ip_dir = 'translate\国外高匿ip(清洗).txt'
proxy_sw = False  #是否使用代理
moreover = 1     #并发量
lines = 1        #多条合并发送 谷歌翻译接口规定：单词请求不能超过5000字符
un_trans = False  #跳过非中文行
recon = 3        #重连次数
sl = 'auto'      #原始语种
tl = 'en'        #目标语种  

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'
]

get_tk = execjs.compile("""
    function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;

        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";

        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };

    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
""")

def request():
    while True:
        content = ''
        for i in range(lines):
            try:
                word = word_que.get(block=False)
            except:
                print('列表为空，等待最后的翻译结果。')
                break
            content += word
        if len(content) == 0:
            return
        # 生成url
        tk = get_tk.call('TL',content)
        content = parse.quote(content)
        url = "http://translate.google.cn/translate_a/single?client=t"\
            "&sl=%s&tl=%s&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca"\
            "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8"\
            "&source=btn&ssel=3&tsel=3&kc=0&tk=%s&q=%s"%(sl,tl,tk,content)

        headers['user-agent'] = random.choice(user_agent_list)
        for i in range(recon):
            if proxy_sw:
                ip = random.choice(ip_list)
                proxy = {
                    'http':'http://'+ip,
                    'https':'https://'+ip
                }
                print(proxy)
                try:
                    response = requests.get(url,headers=headers,proxies=proxy,timeout=3)
                except:
                    ip_list.remove(ip)
            else:
                try:
                    response = requests.get(url,headers=headers,timeout=3)
                except:
                    # print('正在重连（%s/%s）'%(i+1,recon))
                    pass
        try:
            response
        except:
            print('请求发送失败')
            break
        response = json.loads(response.text)
        out_file.write('<p>')
        for i in range(len(response[0])-1):
            print(response[0][i][0])
            out_file.write(response[0][i][0].rstrip())
        out_file.write('</p>')
        out_file.write('\n')
        print('正在翻译，%s/%s'%(total-word_que.qsize(),total),end='\r')
    

def get_word():
    print('正在加载翻译列表')
    with open(in_dir,'r',encoding='utf-8') as f:
        words = f.readlines()
    global word_que
    for word in words:
        if not word.strip():
            continue
        if un_trans:
            try:
                match_obj = re.match(r'[0-9\u4E00-\u9FA5]+',word).group()
            except:
                print('跳过内容：')
                print(word)
                continue
        word_que.put(word)
    global total
    total = word_que.qsize()
    print('列表加载完毕，共%s个'%(total))

def get_proxy():
    print('正在加载代理池')
    with open(ip_dir,'r',encoding='utf-8') as f:
        global ip_list
        ip_list = f.readlines()
    # for ip in ip_list:
    #     ip = re.match(r'[^@]+',ip).group()
    for i in range(len(ip_list)):
        ip_list[i] = re.match(r'[^@]+',ip_list[i]).group()
    print('代理池加载完毕，共%s个'%(len(ip_list)))

if __name__ == "__main__":
    if in_dir == out_dir:
        out_file = open(out_dir,'a',encoding='utf-8')
        out_file.write('\n\n')
    else:
        out_file = open(out_dir,'w',encoding='utf-8')
    word_que = Queue()
    get_word()
    if proxy_sw:
        get_proxy()
    tasks = [gevent.spawn(request) for i in range(moreover)]
    gevent.joinall(tasks)
    out_file.close()
    print('翻译结束')