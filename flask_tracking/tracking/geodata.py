from json import loads
from re import compile, VERBOSE
from urllib.request import urlopen

FREE_GEOIP_URL = "http://freegeoip.net/json/{}"

VALID_IP = compile(r"""
\b                                          # 边界
(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)     # 0到255
\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)   # 0到255
\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)   # 0到255
\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)   # 0到255
\b                                          # 边界
""", VERBOSE)  # ip的范围是 0.0.0.0 到 255.255.255.255 之间
# 指定VERBOSE可以去掉空白符(该空白符没有在字符之间或反斜杠之后)和注释(#号之后的内容)
# re.compile()得到一个正则表达式对象，该对象可以调用match等方法来匹配结果

def get_geodata(ip):
    """
    Search for geolocation information using http://freegeoip.net/
    """
    if not VALID_IP.match(ip):
        raise ValueError('Invalid IPv4 format')

    url = FREE_GEOIP_URL.format(ip)
    data = {}

    try:
        response = urlopen(url).read()  # 读到json字符串
        data = loads(response)  # json字符串到json对象
    except Exception:
        pass

    return data
