import sqlite3
import pandas as pd
import os

# 尝试导入Streamlit，但如果导入失败，使用普通打印函数
try:
    import streamlit as st
    has_streamlit = True
except ImportError:
    has_streamlit = False

# 打印函数，根据是否有Streamlit环境选择不同的输出方式
def log_message(message):
    """根据环境选择适当的日志输出方式"""
    if has_streamlit:
        st.write(message)
    else:
        print(message)

def log_error(message):
    """根据环境选择适当的错误输出方式"""
    if has_streamlit:
        st.error(message)
    else:
        print(f"ERROR: {message}")

def create_connection():
    """创建数据库连接"""
    conn = None
    try:
        conn = sqlite3.connect('digital_transformation.db')
        log_message("数据库连接成功")
        return conn
    except sqlite3.Error as e:
        log_error(f"连接数据库时出错: {e}")
    return conn

def create_tables(conn):
    """创建数据库表"""
    try:
        cursor = conn.cursor()
        
        # 创建数字化转型指数表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transformation_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code TEXT NOT NULL,
            company_name TEXT NOT NULL,
            year INTEGER NOT NULL,
            transformation_index REAL NOT NULL,
            ai_count INTEGER NOT NULL,
            big_data_count INTEGER NOT NULL,
            cloud_computing_count INTEGER NOT NULL,
            blockchain_count INTEGER NOT NULL,
            digital_tech_count INTEGER NOT NULL,
            total_count INTEGER NOT NULL,
            industry_code TEXT,
            industry_name TEXT,
            UNIQUE(stock_code, year)
        )
        ''')
        
        # 创建技术关键词统计表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tech_keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code TEXT NOT NULL,
            company_name TEXT NOT NULL,
            year INTEGER NOT NULL,
            ai_count INTEGER NOT NULL,
            big_data_count INTEGER NOT NULL,
            cloud_computing_count INTEGER NOT NULL,
            blockchain_count INTEGER NOT NULL,
            digital_tech_count INTEGER NOT NULL,
            UNIQUE(stock_code, year)
        )
        ''')
        
        conn.commit()
        log_message("数据库表创建成功")
    except sqlite3.Error as e:
        log_error(f"创建数据库表时出错: {e}")

def import_csv_to_db(conn, csv_file, table_name):
    """将CSV文件导入到数据库表中"""
    try:
        # 读取CSV文件
        df = pd.read_csv(csv_file)
        log_message(f"CSV文件读取成功，共{len(df)}行数据")
        
        # 数据预处理
        if '股票代码' in df.columns:
            df['股票代码'] = df['股票代码'].astype(str).str.strip()
        if '年份' in df.columns:
            df['年份'] = pd.to_numeric(df['年份'], errors='coerce').fillna(0).astype(int)
        
        # 根据表名确定导入逻辑
        if table_name == 'transformation_index':
            # 重命名列以匹配数据库表结构
            df.rename(columns={
                '股票代码': 'stock_code',
                '企业名称': 'company_name',
                '年份': 'year',
                '数字化转型指数(0-100分)': 'transformation_index',
                '人工智能词频数': 'ai_count',
                '大数据词频数': 'big_data_count',
                '云计算词频数': 'cloud_computing_count',
                '区块链词频数': 'blockchain_count',
                '数字技术运用词频数': 'digital_tech_count',
                '总词频数': 'total_count',
                '行业代码': 'industry_code',
                '行业名称': 'industry_name'
            }, inplace=True)
            
            # 导入数据
            cursor = conn.cursor()
            for _, row in df.iterrows():
                try:
                    cursor.execute('''
                    INSERT OR REPLACE INTO transformation_index 
                    (stock_code, company_name, year, transformation_index, 
                     ai_count, big_data_count, cloud_computing_count, 
                     blockchain_count, digital_tech_count, total_count,
                     industry_code, industry_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row['stock_code'], row['company_name'], row['year'],
                        row['transformation_index'], row['ai_count'],
                        row['big_data_count'], row['cloud_computing_count'],
                        row['blockchain_count'], row['digital_tech_count'],
                        row['total_count'],
                        row.get('industry_code', None),
                        row.get('industry_name', None)
                    ))
                except sqlite3.Error as e:
                    log_error(f"导入数据行时出错: {e}")
                    continue  # 跳过重复或有错误的行
        
        elif table_name == 'tech_keywords':
            # 重命名列以匹配数据库表结构
            df.rename(columns={
                '股票代码': 'stock_code',
                '企业名称': 'company_name',
                '年份': 'year',
                '人工智能词频数': 'ai_count',
                '大数据词频数': 'big_data_count',
                '云计算词频数': 'cloud_computing_count',
                '区块链词频数': 'blockchain_count',
                '数字技术运用词频数': 'digital_tech_count'
            }, inplace=True)
            
            # 导入数据
            cursor = conn.cursor()
            for _, row in df.iterrows():
                try:
                    cursor.execute('''
                    INSERT OR REPLACE INTO tech_keywords 
                    (stock_code, company_name, year, ai_count, 
                     big_data_count, cloud_computing_count, blockchain_count, digital_tech_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row['stock_code'], row['company_name'], row['year'],
                        row['ai_count'], row['big_data_count'],
                        row['cloud_computing_count'], row['blockchain_count'],
                        row['digital_tech_count']
                    ))
                except sqlite3.Error as e:
                    log_error(f"导入数据行时出错: {e}")
                    continue  # 跳过重复或有错误的行
        
        conn.commit()
        log_message(f"数据成功导入到{table_name}表")
    except Exception as e:
        log_error(f"导入数据时出错: {e}")

def init_database():
    """初始化数据库"""
    # 创建数据库连接
    conn = create_connection()
    if conn is None:
        return False
    
    try:
        # 创建表
        create_tables(conn)
        
        # 检查表是否为空
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM transformation_index")
        count = cursor.fetchone()[0]
        
        # 如果表为空，则导入数据
        if count == 0:
            log_message("数据库表为空，开始导入数据...")
            # 导入数字化转型指数数据
            if os.path.exists('1999-2023年数字化转型指数结果表(含行业信息).csv'):
                import_csv_to_db(conn, '1999-2023年数字化转型指数结果表(含行业信息).csv', 'transformation_index')
            else:
                log_error("找不到数字化转型指数数据文件")
            
            # 导入技术关键词统计数据
            if os.path.exists('1999-2023年年报技术关键词统计.csv'):
                import_csv_to_db(conn, '1999-2023年年报技术关键词统计.csv', 'tech_keywords')
            else:
                log_error("找不到技术关键词统计数据文件")
        else:
            log_message("数据库表已有数据，跳过导入")
        
        return True
    except Exception as e:
        log_error(f"初始化数据库时出错: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_data_from_db():
    """从数据库获取数据"""
    conn = create_connection()
    if conn is None:
        return None
    
    try:
        # 从数据库获取所有数据
        query = '''
        SELECT 
            stock_code AS 股票代码,
            company_name AS 企业名称,
            year AS 年份,
            industry_code AS 行业代码,
            industry_name AS 行业名称,
            transformation_index AS 数字化转型指数,
            ai_count AS 人工智能词频数,
            big_data_count AS 大数据词频数,
            cloud_computing_count AS 云计算词频数,
            blockchain_count AS 区块链词频数,
            digital_tech_count AS 数字技术运用词频数,
            total_count AS 总词频数
        FROM transformation_index
        ORDER BY stock_code, year
        '''
        
        df = pd.read_sql_query(query, conn)
        log_message(f"从数据库获取数据成功，共{len(df)}行")
        return df
    except Exception as e:
        log_error(f"从数据库获取数据时出错: {e}")
        # 打印详细的错误信息
        import traceback
        if not has_streamlit:
            print(traceback.format_exc())
        return None
    finally:
        if conn:
            conn.close()