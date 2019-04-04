import time
from sys import argv
import random
from pdlearn import version
from pdlearn import user
from pdlearn import dingding
from pdlearn import mydriver
from pdlearn import score
from pdlearn import threads
from pdlearn import get_links

ARTICLE_COUNT = 6
ARTICLE_TIME = 120
ARTICLE_SCORE = 6
ARTICLE_SCORE_MINUTE = 2
VIDEO_COUNT = 6
VIDEO_TIME = 180
VIDEO_SCORE = 6
VIDEO_SCORE_MINUTE = 3


def user_flag(dd_status, uname):
    if dd_status:
        cookies = dingding.dd_login_status(uname, has_dd=True)
    else:
        if (input("是否保存钉钉帐户密码，保存后可后免登陆学习(Y/N) ")) not in ["y", "Y"]:
            driver_login = mydriver.Mydriver(nohead=False)
            cookies = driver_login.login()
        else:
            cookies = dingding.dd_login_status(uname)
    a_log = user.get_a_log(uname)
    v_log = user.get_v_log(uname)

    return cookies, a_log, v_log


def get_argv():
    nohead = True
    lock = False
    stime = False
    if len(argv) > 2:
        if argv[2] == "hidden":
            nohead = True
        elif argv[2] == "show":
            nohead = False
    if len(argv) > 3:
        if argv[3] == "single":
            lock = True
        elif argv[3] == "multithread":
            lock = False
    if len(argv) > 4:
        if argv[4].isdigit():
            stime = argv[4]
    return nohead, lock, stime


def show_score(cookies):
    total, each = score.get_score(cookies)
    print("\n当前学习总积分：" + str(total))
    lst = ['阅读文章:{}/{}'.format(each[0], ARTICLE_COUNT),
           '观看视频:{}/{}'.format(each[1], VIDEO_COUNT),
           '登录:{}/1'.format(each[2]),
           '文章时长:{}/1'.format(each[3], ARTICLE_SCORE),
           '视频时长:{}/1'.format(each[4], VIDEO_SCORE),
           ]
    print(','.join(lst))
    return total, each


def article(cookies, a_log, each):
    if each[0] < ARTICLE_COUNT or each[3] < ARTICLE_SCORE:
        driver_article = mydriver.Mydriver(nohead=nohead)
        driver_article.get_url("https://www.xuexi.cn/notFound.html")
        driver_article.set_cookies(cookies)
        links = get_links.get_article_links()
        for _ in range(10):
            if each[0] >= ARTICLE_COUNT:
                print("检测到文章数量分数已满,退出学习")
                break

            driver_article.get_url(links[a_log])
            time.sleep(random.uniform(5, 10))
            for i in range(ARTICLE_TIME):
                driver_article.go_js('window.scrollTo(0, document.body.scrollHeight/30*{})'.format(i))
                print("\r文章学习中，文章剩余{}篇,本篇剩余时间{}秒....".format(ARTICLE_COUNT - each[0], ARTICLE_TIME - i), end="")
                time.sleep(1)
            time.sleep(random.uniform(2, 6))
            driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')

            a_log += 1
            with open("./user/{}/a_log".format(uname), "w", encoding="utf8") as fp:
                fp.write(str(a_log))

            total, each = show_score(cookies)
        else:
            print("文章学习(篇数)出现异常，请调整学习时间")

        if each[3] < ARTICLE_SCORE:
            driver_article.get_url(links[a_log - 1])
            time.sleep(random.uniform(2, 6))
            remaining = (6 - each[3]) * ARTICLE_SCORE_MINUTE * 60
            for i in range(remaining):
                driver_article.go_js(
                    'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                print("\r文章时长学习中，文章总时长剩余{}秒.....".format(remaining - i), end="")
                time.sleep(1)
            time.sleep(random.uniform(2, 6))
            total, each = show_score(cookies)
            if each[3] >= ARTICLE_SCORE:
                print("检测到文章时长分数已满,退出学习")
            else:
                print("文章学习(时长)出现异常")

        if each[0] >= ARTICLE_COUNT and each[3] >= ARTICLE_SCORE_MINUTE:
            print("文章学习完成")
        driver_article.quit()
    else:
        print("文章之前学完了")


def video(cookies, v_log, each):
    if each[1] < VIDEO_COUNT or each[4] < VIDEO_SCORE:
        driver_video = mydriver.Mydriver(nohead=nohead)
        driver_video.get_url("https://www.xuexi.cn/notFound.html")
        driver_video.set_cookies(cookies)
        links = get_links.get_video_links()
        video_open = False
        for _ in range(10):
            if each[1] >= VIDEO_COUNT:
                print("检测到视频数量分数已满,退出学习")
                break

            driver_video.get_url(links[v_log])
            video_open = True
            time.sleep(random.uniform(5, 10))
            for j in range(VIDEO_TIME):
                driver_video.go_js('window.scrollTo(0, document.body.scrollHeight/180*{})'.format(j))
                print("\r视频学习中，视频剩余{}个,本次剩余时间{}秒....".format(VIDEO_COUNT - each[1], VIDEO_TIME - j), end="")
                time.sleep(1)

            v_log += 1

            with open("./user/{}/v_log".format(uname), "w", encoding="utf8") as fp:
                fp.write(str(v_log))
            # driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
            total, each = show_score(cookies)
        else:
            print("视频学习(数量)出现异常，请调整学习时间")

        if each[4] < VIDEO_SCORE:
            remaining = (VIDEO_SCORE - each[4]) * VIDEO_SCORE_MINUTE * 60
            # max_time = remaining + 180

            # while time_count < max_time:
            if not video_open:
                driver_video.get_url(links[v_log - 1])
                video_open = True

            # random_time = random.randint(60, 180)
            for i in range(remaining + 60):
                driver_video.go_js(
                    'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                print("\r视频时长学习中，视频总时长剩余{}秒.....".format(remaining - i), end="")
                time.sleep(1)
                if remaining - i < VIDEO_SCORE_MINUTE * 60 and i % 43 == 0:
                    total, each = show_score(cookies)
                    if each[4] >= VIDEO_SCORE:
                        print("检测到视频时长分数已满,退出学习")
                        break
            else:
                print("视频学习(时长)出现异常")
            time.sleep(random.random())
            # driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')

            if each[1] > VIDEO_COUNT and each[4] >= VIDEO_SCORE:
                print("视频学习完成")
        driver_video.quit()
    else:
        print("视频之前学完了")


if __name__ == '__main__':
    #  0 读取版本信息
    version.up_info()
    #  1 创建用户标记，区分多个用户历史纪录
    dd_status, uname = user.get_user()
    cookies, a_log, v_log = user_flag(dd_status, uname)
    total, each = show_score(cookies)

    start_time = time.time()
    nohead, lock, stime = get_argv()
    article_thread = threads.MyThread("文章学习", article, cookies, a_log, each, lock=lock)
    video_thread = threads.MyThread("视频学习", video, cookies, v_log, each, lock=lock)
    article_thread.start()
    video_thread.start()
    article_thread.join()
    video_thread.join()
    print("总计用时" + str(int(time.time() - start_time) / 60) + "分钟")
    user.shutdown(stime)
