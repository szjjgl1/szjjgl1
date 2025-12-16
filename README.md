# 数字化转型指数查询应用

📊 一个基于Streamlit的交互式数字化转型指数查询与分析工具，支持按行业、年份等维度筛选和分析数据。

## ✨ 功能特性

### 📋 数据查询
- **多维度筛选**：支持按年份范围、行业、企业名称进行数据筛选
- **实时数据展示**：以表格形式清晰展示筛选结果
- **数据质量指标**：显示总记录数、企业数量、行业数量等关键指标

### 📈 数据分析
- **行业分布分析**：展示各行业企业数量分布（前20名）
- **指数对比分析**：对比各行业平均数字化转型指数（前20名）
- **趋势分析**：可视化展示选定行业的数字化转型指数年度变化趋势

### 💾 数据导出
- **CSV导出**：支持将筛选后的数据导出为CSV文件，便于进一步分析

### 🎨 用户界面
- **响应式布局**：适配不同屏幕尺寸
- **友好交互**：直观的筛选器和标签页设计
- **中文支持**：完整的中文界面和图表显示

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Git (用于版本控制和GitHub上传)

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/xj-x-a/-.git
   cd -
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **初始化数据库**
   ```bash
   python -c "from database import init_database; init_database()"
   ```

4. **启动应用**
   ```bash
   streamlit run main_app.py
   ```

5. **访问应用**
   - 在浏览器中打开显示的本地URL（通常是 http://localhost:8501）

## 📊 数据结构

应用使用以下数据文件：

- `1999-2023年数字化转型指数结果表(含行业信息).csv`：包含数字化转型指数及行业信息
- `1999-2023年年报技术关键词统计.csv`：包含各技术关键词的统计数据

### 主要数据字段

| 字段名称 | 说明 |
|---------|------|
| 股票代码 | 企业股票代码 |
| 企业名称 | 企业全称 |
| 年份 | 数据统计年份 |
| 行业代码 | 行业分类代码 |
| 行业名称 | 行业分类名称 |
| 数字化转型指数 | 企业数字化转型综合指数（0-100分） |
| 人工智能词频数 | 人工智能相关关键词出现次数 |
| 大数据词频数 | 大数据相关关键词出现次数 |
| 云计算词频数 | 云计算相关关键词出现次数 |
| 区块链词频数 | 区块链相关关键词出现次数 |

## 🛠️ 技术栈

- **前端框架**：Streamlit 1.50.0
- **数据处理**：Pandas 2.3.3
- **数据可视化**：Matplotlib 3.7.5, Seaborn 0.13.2
- **数据库**：SQLite3
- **开发语言**：Python 3.8+

## 📁 项目结构

```
├── main_app.py           # 主应用程序文件
├── database.py           # 数据库操作模块
├── requirements.txt      # 项目依赖
├── .gitignore            # Git忽略文件
├── README.md             # 项目说明文档
├── GIT_DEPLOY_GUIDE.md   # Git部署指南
├── 1999-2023年数字化转型指数结果表(含行业信息).csv   # 主要数据文件
├── 1999-2023年年报技术关键词统计.csv                # 技术关键词数据
└── digital_transformation.db  # SQLite数据库文件
```

## 📝 使用指南

### 数据查询
1. 使用左侧边栏的**年份滑块**选择要查询的年份范围
2. 在**行业选择**下拉框中选择一个或多个行业
3. 使用**企业名称搜索**框输入关键词查找特定企业
4. 查看下方的筛选结果表格

### 数据分析
1. 切换到**数据分析**部分
2. 使用**行业分布**标签查看各行业企业数量
3. 使用**指数对比**标签比较各行业平均指数
4. 使用**趋势分析**标签查看选定行业的年度变化趋势

### 数据导出
1. 在**数据导出**部分点击**导出筛选后的数据**按钮
2. 选择保存位置，CSV文件将包含所有筛选后的数据

## 🔧 部署到GitHub

### 首次部署

1. **初始化Git仓库**
   ```bash
   git init
   git config user.name "你的GitHub用户名"
   git config user.email "你的GitHub邮箱"
   ```

2. **添加文件**
   ```bash
   git add .
   ```

3. **提交更改**
   ```bash
   git commit -m "Initial commit: 数字化转型指数查询应用"
   ```

4. **连接远程仓库**
   ```bash
   git remote add origin https://github.com/xj-x-a/-.git
   ```

5. **推送代码**
   ```bash
   git push -u origin main
   ```

### 后续更新

```bash
# 查看修改状态
git status

# 添加修改的文件
git add .

# 提交更改
git commit -m "更新说明"

# 推送到GitHub
git push
```

## 📦 部署到Streamlit Cloud

1. 登录 [Streamlit Cloud](https://share.streamlit.io/)
2. 点击"New app"按钮
3. 选择你的GitHub仓库
4. 选择分支（通常是main）
5. 指定主文件为`main_app.py`
6. 点击"Deploy"按钮

## 🔍 故障排除

### 数据库连接失败
- 确保`digital_transformation.db`文件存在
- 重新运行数据库初始化命令：`python -c "from database import init_database; init_database()"`

### 数据加载为空
- 检查数据文件是否存在且格式正确
- 确保数据文件与应用在同一目录下

### 中文显示异常
- 确保已安装中文字体（SimHei或Microsoft YaHei）
- 重启应用后尝试

## 📄 许可证

MIT License - 详见LICENSE文件

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📞 联系方式

如有问题或建议，请通过GitHub Issues反馈。

---

**更新时间**：2023年
**版本**：v1.0.0