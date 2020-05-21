import requests
import re
from PIL import Image, ImageDraw, ImageFont

#  作者不承担任何法律责任！The author assumes no legal liability！
#  仅供学习交流使用，严禁用于其他用途！
#  For learning and communication only, other use is strictly prohibited！


def get_url():  # 获取最新一期大学习的url
    html = requests.get('http://news.cyol.com/node_67071.htm').text
    url = re.findall('href="(.*?)" target', html)[0]
    return url


def get_id(url):  # 从url中提取本期的id
    the_id = url.split('/')[-2]
    return the_id


def get_icon(the_id):  # 根据id获取本期的分享缩略图
    addr = 'http://h5.cyol.com/special/daxuexi/%s/images/icon.jpg' % the_id
    icon = requests.get(addr).content
    with open('icon.jpg', 'wb') as f:
        f.write(icon)


def get_end(the_id):  # 根据id获取本期的完成图片
    addr = 'http://h5.cyol.com/special/daxuexi/%s/images/end.jpg' % the_id
    end = requests.get(addr).content
    with open('end.jpg', 'wb') as f:
        f.write(end)


def get_info(file='info.txt'):  # 从info文本中提取文字信息
    with open(file, 'r', encoding='utf-8') as f:
        info = []
        for line in f.readlines():
            line = line.strip('\n')
            i = line.split(':')
            info.append(i)
        info = dict(info)
    return info


def change(raw='raw.png', icon='icon.jpg', touxiang='touxiang.jpg'):  # 以raw为底图制作图片result
    result = Image.open(raw)
    icon = (Image.open(icon)).resize((80, 80), resample=0)
    touxiang = (Image.open(touxiang)).resize((80, 80), resample=0)
    result.paste(icon, (123, 330))
    result.paste(touxiang, (13, 132))

    '''========================以下为加文字部分==========================='''
    info = get_info()
    font = ImageFont.truetype('C:/windows/fonts/Simhei.ttf', size=32)
    draw = ImageDraw.Draw(result)
    draw.text((215, 355), info['share'], fill='black', font=font)  # 期数
    draw.text((116, 135), info['nickname'], fill=(87, 107, 149), font=font)  # 昵称
    draw.text((116, 190), info['school'], fill='black', font=font)  # 学院
    draw.text((116, 230), info['name'], fill='black', font=font)  # 姓名
    draw.text((116, 270), info['stu_num'], fill=(87, 107, 149), font=font)  # 学号
    result.save('result.png')


def run():
    url = get_url()
    Id = get_id(url)
    get_icon(Id)
    get_end(Id)
    change()


if __name__ == '__main__':
    run()
