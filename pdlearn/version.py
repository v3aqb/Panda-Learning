import time
import requests


def up_info():
    __Version = "v2.3 preview"
    __INFO = "熊猫学习唯一下载地址为 https://github.com/Alivon/Panda-Learning"

    try:
        version_info = open('./user/version_info').read().splitlines()
        if __Version < version_info[1].split("=")[1]:
            print(__INFO)
            print("程序版本为：{}，\n最新版本为：{}".format(__Version, version_info[1].split("=")[1]))
            print("=" * 120)
            print("当前不是最新版本，建议更新")
            print("=" * 120)
            print("更新提要：")
            for i in version_info[2:]:
                print(i)
            print("=" * 120)
            return
    except Exception:
        pass

    try:
        version_check = float(open('./user/version_check').read())
        if time.time() - version_check < 12 * 3600:
            # skip version check
            return
    except Exception:
        pass

    try:
        print("正在联网获取跟新信息...")
        updata_log = requests.get(
            "https://raw.githubusercontent.com/Alivon/Panda-Learning/master/Update%20log").content.decode(
            "utf8")
        updata_log = updata_log.split("\n")
        print(__INFO)
        print("程序版本为：{}，\n最新版本为：{}".format(__Version, updata_log[1].split("=")[1]))
        print("=" * 120)
        if __Version != updata_log[1].split("=")[1]:
            print("当前不是最新版本，建议更新")
            print("=" * 120)
            print("更新提要：")
            for i in updata_log[2:]:
                print(i)
            print("=" * 120)
            with open('./user/version_info', 'w') as f:
                for line in updata_log:
                    f.write(line + '\n')
        else:
            with open('./user/version_check', 'w') as f:
                f.write(str(time.time()))
        print()

    except Exception:
        print("版本信息网络错误")
        print()


if __name__ == '__main__':
    up_info()
