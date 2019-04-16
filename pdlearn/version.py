import time
import requests


def up_info():
    __Version = "v2.5"
    __INFO = "熊猫学习唯一下载地址为 https://github.com/Alivon/Panda-Learning"

    try:
        try:
            version_check = float(open('./user/version_check').read())
        except Exception:
            version_check = 0
        if time.time() - version_check > 12 * 3600:
            print("正在联网获取更新信息...")
            updata_log = requests.get(
                "https://raw.githubusercontent.com/Alivon/Panda-Learning/master/Update%20log").content.decode(
                "utf8")
            with open('./user/version_info', 'w') as f:
                f.write(updata_log)
            with open('./user/version_check', 'w') as f:
                f.write(str(time.time()))
    except Exception:
        print("版本信息网络错误")

    print(__INFO)
    print("程序版本为：{}".format(__Version))
    try:
        version_info = open('./user/version_info').read().splitlines()
        if __Version < version_info[1].split("=")[1]:
            print("最新版本为：{}".format(version_info[1].split("=")[1]))
            print("=" * 120)
            print("当前不是最新版本，建议更新")
            print("=" * 120)
            print("更新提要：")
            for i in version_info[2:]:
                print(i)
            print("=" * 120)
    except Exception:
        print("读取版本信息错误")
    print()


if __name__ == '__main__':
    up_info()
