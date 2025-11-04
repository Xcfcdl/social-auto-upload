import sqlite3
from pathlib import Path

# 数据库文件路径
db_file = './database.db'

# 连接到SQLite数据库
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 检查列是否存在的函数
def column_exists(table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return column_name in columns

# 添加title列
if not column_exists('file_records', 'title'):
    cursor.execute('ALTER TABLE file_records ADD COLUMN title TEXT')
    print("Added 'title' column to file_records table")
else:
    print("'title' column already exists")

# 添加description列
if not column_exists('file_records', 'description'):
    cursor.execute('ALTER TABLE file_records ADD COLUMN description TEXT')
    print("Added 'description' column to file_records table")
else:
    print("'description' column already exists")

# 添加tags列
if not column_exists('file_records', 'tags'):
    cursor.execute('ALTER TABLE file_records ADD COLUMN tags TEXT')
    print("Added 'tags' column to file_records table")
else:
    print("'tags' column already exists")

# 提交更改
conn.commit()
print("Migration completed successfully")

# 关闭连接
conn.close()
