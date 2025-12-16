# 数字化转型指数查询应用 - 简化版
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 应用程序标题
st.title("📊 数字化转型指数查询应用")

# 数据库操作类
class DatabaseManager:
    def __init__(self, db_file='digital_transformation.db'):
        self.db_file = db_file
        self.conn = None
    
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            return True
        except sqlite3.Error as e:
            st.error(f"数据库连接失败: {e}")
            return False
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def get_all_data(self):
        if not self.connect():
            return None
        
        try:
            query = '''
            SELECT 
                stock_code AS 股票代码,
                company_name AS 企业名称,
                year AS 年份,
                industry_name AS 行业名称,
                transformation_index AS 数字化转型指数
            FROM transformation_index
            ORDER BY stock_code, year
            '''
            
            df = pd.read_sql_query(query, self.conn)
            return df
        except Exception as e:
            st.error(f"数据查询失败: {e}")
            return None
        finally:
            self.disconnect()

# 数据加载
@st.cache_data
def load_data():
    db_manager = DatabaseManager()
    df = db_manager.get_all_data()
    
    if df is not None:
        df['年份'] = pd.to_numeric(df['年份'], errors='coerce')
        df['数字化转型指数'] = pd.to_numeric(df['数字化转型指数'], errors='coerce')
    
    return df

# 加载数据
df = load_data()

if df is None or df.empty:
    st.error("无法加载数据，请确保数据库已正确初始化。")
    st.stop()

# 侧边栏筛选
st.sidebar.header("🔍 筛选条件")

# 年份筛选
year_range = st.sidebar.slider(
    "选择年份范围",
    min_value=int(df['年份'].min()),
    max_value=int(df['年份'].max()),
    value=(int(df['年份'].min()), int(df['年份'].max()))
)

# 行业筛选
all_industries = sorted(df['行业名称'].dropna().unique().tolist())
selected_industries = st.sidebar.multiselect(
    "选择行业",
    options=all_industries,
    default=[],
    help="选择一个或多个行业进行筛选"
)

# 企业搜索
company_search = st.sidebar.text_input(
    "搜索企业名称",
    placeholder="输入企业名称关键词..."
)

# 数据筛选
filtered_df = df.copy()
filtered_df = filtered_df[(filtered_df['年份'] >= year_range[0]) & (filtered_df['年份'] <= year_range[1])]

if selected_industries:
    filtered_df = filtered_df[filtered_df['行业名称'].isin(selected_industries)]

if company_search:
    filtered_df = filtered_df[filtered_df['企业名称'].str.contains(company_search, case=False, na=False)]

# 数据展示
st.header("数据展示")
st.info(f"筛选后数据量: {len(filtered_df):,} 条记录")

if not filtered_df.empty:
    st.dataframe(
        filtered_df[['股票代码', '企业名称', '年份', '行业名称', '数字化转型指数']],
        hide_index=True,
        use_container_width=True,
        column_config={
            '股票代码': st.column_config.NumberColumn('股票代码', format='%d'),
            '数字化转型指数': st.column_config.NumberColumn('数字化转型指数', format='%.4f')
        }
    )
else:
    st.warning("没有符合筛选条件的数据")

# 数据分析
st.header("数据分析")
tab1, tab2 = st.tabs(["行业企业数量分布", "行业数字化转型指数对比"])

with tab1:
    st.subheader("行业企业数量分布")
    if not filtered_df.empty:
        industry_dist = filtered_df.groupby('行业名称')['股票代码'].nunique().reset_index()
        industry_dist = industry_dist.rename(columns={'股票代码': '企业数量'})
        industry_dist = industry_dist.sort_values('企业数量', ascending=False).head(20)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(industry_dist['行业名称'], industry_dist['企业数量'], color='skyblue')
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 5, bar.get_y() + bar.get_height()/2, f'{int(width)}', 
                    va='center', ha='left', fontweight='bold')
        
        ax.set_xlabel('企业数量')
        ax.set_ylabel('行业名称')
        ax.set_title('行业企业数量分布 (前20名)')
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)

with tab2:
    st.subheader("行业数字化转型指数对比")
    if not filtered_df.empty:
        industry_avg = filtered_df.groupby('行业名称')['数字化转型指数'].mean().reset_index()
        industry_avg = industry_avg.rename(columns={'数字化转型指数': '平均数字化转型指数'})
        industry_avg = industry_avg.sort_values('平均数字化转型指数', ascending=False).head(20)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(industry_avg['行业名称'], industry_avg['平均数字化转型指数'], color='lightgreen')
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.2f}', 
                    va='center', ha='left', fontweight='bold')
        
        ax.set_xlabel('平均数字化转型指数')
        ax.set_ylabel('行业名称')
        ax.set_title('各行业平均数字化转型指数对比 (前20名)')
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)

# 数据导出
if not filtered_df.empty:
    st.header("数据导出")
    csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 导出筛选后的数据 (CSV)",
        data=csv,
        file_name=f"数字化转型指数_{year_range[0]}-{year_range[1]}.csv",
        mime="text/csv"
    )

# 页脚信息
st.markdown("---")
st.markdown("📅 数据更新时间: 2023年")
st.markdown("💡 提示: 可使用左侧筛选器查看特定行业和年份的数据")