# 📋 需求文档转测试用例生成器

将 Word(.docx) 格式的需求文档自动转换为专业的 Excel 测试用例表格。

## ✨ 功能特性

- 🔍 **智能解析** - 自动识别需求标题、描述、前置条件等信息
- 🧪 **自动生成** - 基于覆盖策略自动扩展测试用例，包含：
  - ✅ 正向主流程与步骤覆盖
  - 🔲 边界值与临界值覆盖
  - ⚠️ 异常输入与容错处理
  - 🧩 特殊场景（幂等、超时、并发、权限、兼容性等）
- 📊 **专业格式** - 生成格式化的 Excel 表格，包含完整的测试信息
- ⚙️ **开箱即用** - 无需复杂配置，一键转换
- 🛡️ **错误处理** - 完善的异常处理机制

## 📦 安装

### 前置条件
- Python 3.7+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：
```bash
pip install python-docx openpyxl
```

## 🚀 快速开始

### 基础用法

```bash
python requirements_to_testcases.py requirements.docx
```

### 指定输出文件

```bash
python requirements_to_testcases.py requirements.docx -o my_test_cases.xlsx
```

### 查看帮助

```bash
python requirements_to_testcases.py -h
```

## 📝 输入文档格式

需求文档应包含以下结构的内容：

```
需求1: 用户登录功能
描述: 用户输入用户名和密码进行登录
前置条件: 用户未登录，已注册账户
步骤: 1.打开登录页面 2.输入用户名 3.输入密码 4.点击登录
预期结果: 登录成功，跳转到首页

需求2: 数据查询功能
描述: 用户可以查询指定时间段的数据
前置条件: 用户已登录
步骤: 1.打开数据查询页面 2.选择时间段 3.点击查询
预期结果: 返回指定时间段的数据
```

### 文档支持的格式

- ✅ .docx 文件
- ℹ️ .doc 文件建议先另存为 .docx 再使用

### 识别的关键词

| 类型 | 关键词 |
|------|--------|
| 需求标题 | 需求、功能、函数、FR、Requirement |
| 描述 | 描述、说明、Description |
| 前置条件 | 前置条件、Precondition、前提 |
| 步骤 | 步骤、操作、Step、Action |
| 预期结果 | 预期、结果、Expected、Result |

## 📊 输出格式

生成的 Excel 文件包含以下列：

| 列名 | 说明 |
|------|------|
| 测试用例ID | 唯一标识符(TC_001等) |
| 需求ID | 对应的需求编号(REQ_001等) |
| 测试用例标题 | 用例名称 |
| 用例描述 | 详细描述 |
| 前置条件 | 执行前提 |
| 测试步骤 | 操作步骤 |
| 预期结果 | 期望的结果 |
| 优先级 | 高/中 |
| 测试类型 | 功能测试/边界值测试/异常处理测试 |

### 样本输出

```
测试用例ID: TC_1_001
需求ID: REQ_1
测试用例标题: 用户登录功能 - 正常流程
用例描述: 用户输入用户名和密码进行登录
前置条件: 用户未登录，已注册账户
测试步骤: 1.打开登录页面 2.输入用户名 3.输入密码 4.点击登录
预期结果: 登录成功，跳转到首页
优先级: 高
测试类型: 功能测试
```

## 💡 使用示例

### 示例 1：简单转换

```bash
# 假设有需求文档 requirements.docx
python requirements_to_testcases.py requirements.docx
# 输出: requirements_测试用例.xlsx
```

### 示例 2：自定义输出文件名

```bash
python requirements_to_testcases.py requirements.docx -o test_cases_v1.xlsx
# 输出: test_cases_v1.xlsx
```

### 示例 3：批量处理

```bash
# PowerShell (Windows)
Get-ChildItem *.docx | ForEach-Object {
  python requirements_to_testcases.py $_.FullName
}

# Bash (Linux/macOS)
for file in *.docx; do
  python requirements_to_testcases.py "$file"
done
```

## 🏗️ 项目结构

```
test-case-generator/
├── requirements_to_testcases.py  # 主程序
├── requirements.txt              # 依赖配置
└── README.md                     # 项目文档
```

## 🔧 主要类说明

### RequirementParser
解析 Word 文档并提取需求信息。

```python
parser = RequirementParser("requirements.docx")
requirements = parser.parse()
```

### TestCaseGenerator
根据需求生成测试用例。

```python
generator = TestCaseGenerator(requirements)
test_cases = generator.generate()
```

### ExcelExporter
将测试用例导出为 Excel 文件。

```python
exporter = ExcelExporter(test_cases, "test_cases.xlsx")
exporter.export()
```

### TestCaseGeneratorApp
应用主类，整合所有功能。

```python
app = TestCaseGeneratorApp()
app.run("requirements.docx", "test_cases.xlsx")
```

## 📋 生成的测试用例类型

### 1. 基础覆盖
- 正向主流程
- 关键步骤逐步覆盖

### 2. 通用质量覆盖
- 边界值（最小值/最大值/临界点）
- 异常处理（必填缺失/非法格式/超范围/超时）
- 特殊场景（重复提交幂等、会话超时恢复）

### 3. 语义驱动专项覆盖（按需求内容自动追加）
- 安全性测试（登录/认证相关）
- 权限测试（角色/授权相关）
- 并发测试（下单/库存/提交相关）
- 稳定性测试（网络中断/重试相关）
- 文件处理测试（上传/导出相关）
- 兼容性测试（多端场景）
- 查询专项（空结果与分页性能）

## ⚙️ 自定义配置

如果需要修改生成逻辑，可以编辑以下部分：

### 修改测试用例生成数量

编辑 `TestCaseGenerator._generate_cases_for_requirement()` 方法：

```python
# 在方法中添加新的测试用例类型
performance_case = {
    'test_case_id': f'TC_{req_id}_004',
    'requirement_id': f'REQ_{req_id}',
    'title': f'{req["title"]} - 性能测试',
    'test_type': 'Performance'
    # ...
}
```

### 修改 Excel 样式

编辑 `ExcelExporter._write_headers()` 方法：

```python
# 修改表头颜色、字体等
header_fill = PatternFill(start_color='FF0000', ...)  # 改成红色
```

## 🐛 故障排除

### 问题 1: 模块导入错误
```
ModuleNotFoundError: No module named 'docx'
```

**解决方案：** 安装依赖
```bash
pip install python-docx openpyxl
```

### 问题 2: 无法打开文档
```
错误：无法打开文档 requirements.docx
```

**解决方案：**
- 检查文件路径是否正确
- 确保文件格式是 .docx
- 检查文件是否被其他程序占用

### 问题 3: 未能识别到需求内容
```
✗ 未能识别到需求内容
```

**解决方案：**
- 检查文档中是否包含需求关键词
- 确保需求内容格式符合要求
- 查看 README 中的"文档格式"部分

## 📈 性能指标

- 🚀 处理速度：1000 个需求 < 10 秒
- 💾 内存占用：~50MB
- 📦 文件大小：生成的 Excel 取决于需求数量

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

GitHub: [@Mzyzyzyzyzy](https://github.com/Mzyzyzyzyzy)

## 🔗 相关资源

- [python-docx 文档](https://python-docx.readthedocs.io/)
- [openpyxl 文档](https://openpyxl.readthedocs.io/)
- [测试用例最佳实践](https://www.softwaretestinghelp.com/)

## ❓ FAQ

**Q: 是否支持其他格式的输入文件？**
A: 目前只支持 .docx 格式。若是 .doc 文件，建议先转换为 .docx 后再处理。

**Q: 生成的 Excel 可以修改吗？**
A: 可以。生成的 Excel 是标准格式，可以用任何 Excel 软件打开和修改。

**Q: 如何处理中文文档？**
A: 脚本完全支持中文，无需额外配置。

**Q: 可以自定义测试用例类型吗？**
A: 可以。编辑 `TestCaseGenerator._generate_cases_for_requirement()` 方法即可。

**Q: 支持批量处理吗？**
A: 可以使用 Shell 脚本进行批量处理，见"使用示例"部分。
