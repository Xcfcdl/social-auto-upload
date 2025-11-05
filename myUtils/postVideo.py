import asyncio
import time
from pathlib import Path

from conf import BASE_DIR
from uploader.douyin_uploader.main import DouYinVideo
from uploader.ks_uploader.main import KSVideo
from uploader.tencent_uploader.main import TencentVideo
from uploader.xiaohongshu_uploader.main import XiaoHongShuVideo
from utils.constant import TencentZoneTypes
from utils.files_times import generate_schedule_time_next_day

# 发布间隔时间（秒），避免同一账号发布过快
PUBLISH_DELAY = 3


def post_video_tencent(title,files,tags,account_file,category=TencentZoneTypes.LIFESTYLE.value,enableTimer=False,videos_per_day = 1, daily_times=None,start_days = 0):
    # 生成文件的完整路径
    account_file = [Path(BASE_DIR / "cookiesFile" / file) for file in account_file]
    files = [Path(BASE_DIR / "videoFile" / file) for file in files]
    if enableTimer:
        publish_datetimes = generate_schedule_time_next_day(len(files), videos_per_day, daily_times,start_days)
    else:
        publish_datetimes = [0 for i in range(len(files))]

    total_tasks = len(files) * len(account_file)
    current_task = 0
    success_count = 0
    fail_count = 0

    for index, file in enumerate(files):
        print(f"\n{'='*60}")
        print(f"[视频 {index+1}/{len(files)}] {file.name}")
        print(f"{'='*60}")

        for cookie_index, cookie in enumerate(account_file):
            current_task += 1
            try:
                print(f"\n[任务 {current_task}/{total_tasks}] 正在使用账号 {cookie.name} 发布...")
                print(f"标题：{title}")
                print(f"标签：{tags}")

                app = TencentVideo(title, str(file), tags, publish_datetimes[index], cookie, category)
                asyncio.run(app.main(), debug=False)
                success_count += 1
                print(f"✅ 发布成功！")

                # 非最后一个账号时添加延迟
                if cookie_index < len(account_file) - 1:
                    print(f"等待 {PUBLISH_DELAY} 秒后切换下一个账号...")
                    time.sleep(PUBLISH_DELAY)
            except Exception as e:
                fail_count += 1
                print(f"❌ 发布失败 - 账号: {cookie.name}, 错误: {str(e)}")
                continue

    print(f"\n{'='*60}")
    print(f"视频号发布完成！成功: {success_count}, 失败: {fail_count}")
    print(f"{'='*60}\n")


def post_video_DouYin(title,files,tags,account_file,category=TencentZoneTypes.LIFESTYLE.value,enableTimer=False,videos_per_day = 1, daily_times=None,start_days = 0,
                      thumbnail_path = '',
                      productLink = '', productTitle = ''):
    # 生成文件的完整路径
    account_file = [Path(BASE_DIR / "cookiesFile" / file) for file in account_file]
    files = [Path(BASE_DIR / "videoFile" / file) for file in files]
    if enableTimer:
        publish_datetimes = generate_schedule_time_next_day(len(files), videos_per_day, daily_times,start_days)
    else:
        publish_datetimes = [0 for i in range(len(files))]

    total_tasks = len(files) * len(account_file)
    current_task = 0
    success_count = 0
    fail_count = 0

    for index, file in enumerate(files):
        print(f"\n{'='*60}")
        print(f"[视频 {index+1}/{len(files)}] {file.name}")
        print(f"{'='*60}")

        for cookie_index, cookie in enumerate(account_file):
            current_task += 1
            try:
                print(f"\n[任务 {current_task}/{total_tasks}] 正在使用账号 {cookie.name} 发布...")
                print(f"标题：{title}")
                print(f"标签：{tags}")

                app = DouYinVideo(title, str(file), tags, publish_datetimes[index], cookie, thumbnail_path, productLink, productTitle)
                asyncio.run(app.main(), debug=False)
                success_count += 1
                print(f"✅ 发布成功！")

                # 非最后一个账号时添加延迟
                if cookie_index < len(account_file) - 1:
                    print(f"等待 {PUBLISH_DELAY} 秒后切换下一个账号...")
                    time.sleep(PUBLISH_DELAY)
            except Exception as e:
                fail_count += 1
                print(f"❌ 发布失败 - 账号: {cookie.name}, 错误: {str(e)}")
                continue

    print(f"\n{'='*60}")
    print(f"抖音发布完成！成功: {success_count}, 失败: {fail_count}")
    print(f"{'='*60}\n")


def post_video_ks(title,files,tags,account_file,category=TencentZoneTypes.LIFESTYLE.value,enableTimer=False,videos_per_day = 1, daily_times=None,start_days = 0):
    # 生成文件的完整路径
    account_file = [Path(BASE_DIR / "cookiesFile" / file) for file in account_file]
    files = [Path(BASE_DIR / "videoFile" / file) for file in files]
    if enableTimer:
        publish_datetimes = generate_schedule_time_next_day(len(files), videos_per_day, daily_times,start_days)
    else:
        publish_datetimes = [0 for i in range(len(files))]

    total_tasks = len(files) * len(account_file)
    current_task = 0
    success_count = 0
    fail_count = 0

    for index, file in enumerate(files):
        print(f"\n{'='*60}")
        print(f"[视频 {index+1}/{len(files)}] {file.name}")
        print(f"{'='*60}")

        for cookie_index, cookie in enumerate(account_file):
            current_task += 1
            try:
                print(f"\n[任务 {current_task}/{total_tasks}] 正在使用账号 {cookie.name} 发布...")
                print(f"标题：{title}")
                print(f"标签：{tags}")

                app = KSVideo(title, str(file), tags, publish_datetimes[index], cookie)
                asyncio.run(app.main(), debug=False)
                success_count += 1
                print(f"✅ 发布成功！")

                # 非最后一个账号时添加延迟
                if cookie_index < len(account_file) - 1:
                    print(f"等待 {PUBLISH_DELAY} 秒后切换下一个账号...")
                    time.sleep(PUBLISH_DELAY)
            except Exception as e:
                fail_count += 1
                print(f"❌ 发布失败 - 账号: {cookie.name}, 错误: {str(e)}")
                continue

    print(f"\n{'='*60}")
    print(f"快手发布完成！成功: {success_count}, 失败: {fail_count}")
    print(f"{'='*60}\n")

def post_video_xhs(title,files,tags,account_file,category=TencentZoneTypes.LIFESTYLE.value,enableTimer=False,videos_per_day = 1, daily_times=None,start_days = 0):
    # 生成文件的完整路径
    account_file = [Path(BASE_DIR / "cookiesFile" / file) for file in account_file]
    files = [Path(BASE_DIR / "videoFile" / file) for file in files]
    file_num = len(files)
    if enableTimer:
        publish_datetimes = generate_schedule_time_next_day(file_num, videos_per_day, daily_times,start_days)
    else:
        publish_datetimes = [0 for i in range(file_num)]

    total_tasks = len(files) * len(account_file)
    current_task = 0
    success_count = 0
    fail_count = 0

    for index, file in enumerate(files):
        print(f"\n{'='*60}")
        print(f"[视频 {index+1}/{len(files)}] {file.name}")
        print(f"{'='*60}")

        for cookie_index, cookie in enumerate(account_file):
            current_task += 1
            try:
                print(f"\n[任务 {current_task}/{total_tasks}] 正在使用账号 {cookie.name} 发布...")
                print(f"标题：{title}")
                print(f"标签：{tags}")

                app = XiaoHongShuVideo(title, file, tags, publish_datetimes[index], cookie)
                asyncio.run(app.main(), debug=False)
                success_count += 1
                print(f"✅ 发布成功！")

                # 非最后一个账号时添加延迟
                if cookie_index < len(account_file) - 1:
                    print(f"等待 {PUBLISH_DELAY} 秒后切换下一个账号...")
                    time.sleep(PUBLISH_DELAY)
            except Exception as e:
                fail_count += 1
                print(f"❌ 发布失败 - 账号: {cookie.name}, 错误: {str(e)}")
                continue

    print(f"\n{'='*60}")
    print(f"小红书发布完成！成功: {success_count}, 失败: {fail_count}")
    print(f"{'='*60}\n")



# post_video("333",["demo.mp4"],"d","d")
# post_video_DouYin("333",["demo.mp4"],"d","d")