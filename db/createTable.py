import sqlite3
import json
import os

# 数据库文件路径（如果不存在会自动创建）
db_file = './database.db'

# 如果数据库已存在，则删除旧的表（可选）
# if os.path.exists(db_file):
#     os.remove(db_file)

# 连接到SQLite数据库（如果文件不存在则会自动创建）
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 创建账号记录表
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type INTEGER NOT NULL,
    filePath TEXT NOT NULL,  -- 存储文件路径
    userName TEXT NOT NULL,
    status INTEGER DEFAULT 0
)
''')

# 创建文件记录表
cursor.execute('''CREATE TABLE IF NOT EXISTS file_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 唯一标识每条记录
    filename TEXT NOT NULL,               -- 文件名
    filesize REAL,                     -- 文件大小（单位：MB）
    upload_time DATETIME DEFAULT CURRENT_TIMESTAMP, -- 上传时间，默认当前时间
    file_path TEXT,                       -- 文件路径
    title TEXT,                           -- 视频标题（用于AI生成视频）
    description TEXT,                     -- 视频描述/简介
    tags TEXT                             -- 标签（逗号分隔）
)
''')

# 创建任务记录表
cursor.execute('''CREATE TABLE IF NOT EXISTS task_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 唯一标识每条记录
    title TEXT NOT NULL,                  -- 任务标题
    platform INTEGER NOT NULL,            -- 平台类型 (1=小红书, 2=视频号, 3=抖音, 4=快手)
    account_id INTEGER,                   -- 关联的账号ID
    account_name TEXT,                    -- 账号名称
    status TEXT DEFAULT '待执行',          -- 任务状态 (待执行, 进行中, 已完成, 已失败, 已取消)
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP, -- 创建时间
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP, -- 更新时间
    file_list TEXT,                       -- 文件列表（JSON格式）
    tags TEXT,                            -- 标签
    category INTEGER,                     -- 分类
    error_msg TEXT                        -- 错误信息（如果失败）
)
''')

# 提交更改
conn.commit()
print("Table created successfully")
# 关闭连接
conn.close()