# 多语言支持使用示例

## 基本用法

在需要多语言支持的文件中添加导入：

```python
from utils.i18n import get_message as _
```

## 使用示例

### 基本消息

```python
# 显示检查依赖消息
print(_("checking_dependencies"))

# 根据当前环境语言自动显示：
# 中文环境：正在检查依赖...
# 英文环境：Checking dependencies...
```

### 带参数的消息

```python
# 显示Docker Compose命令
docker_cmd = "docker-compose"
print(_("using_docker_compose_cmd", docker_cmd))

# 中文：使用 'docker-compose' 作为 docker-compose 命令。
# 英文：Using 'docker-compose' as docker-compose command.
```

### 错误消息

```python
# 显示目录不存在错误
directory = "/path/to/missing"
print(_("error_directory_not_exist", directory), file=sys.stderr)

# 中文：目录 '/path/to/missing' 不存在。
# 英文：Directory '/path/to/missing' does not exist.
```

## 环境语言控制

### 通过环境变量

```bash
# 使用中文
LANG=zh_CN.UTF-8 python3 app.py --help

# 使用英文
LANG=en_US.UTF-8 python3 app.py --help
```

### 程序内切换

```python
from utils.i18n import set_language, get_message as _

# 切换到英文
set_language("en_US")
print(_("checking_dependencies"))  # Checking dependencies...

# 切换到中文
set_language("zh_CN")
print(_("checking_dependencies"))  # 正在检查依赖...
```

## 语言检测优先级

1. 环境变量 `LANG`
2. 系统默认locale
3. 默认语言（zh_CN）

## 支持的语言

- `zh_CN` - 中文简体（默认）
- `en_US` - 英文

## 消息分类

- **通用信息**: checking_dependencies, dependencies_check_passed 等
- **错误信息**: error_* 开头的消息
- **警告信息**: warning_* 开头的消息  
- **成功信息**: *_success, *_complete 等
- **操作进度**: starting_*, creating_*, restoring_* 等
- **确认操作**: confirm_*, use_* 等
- **帮助说明**: *_description 等

## 错误处理

- 如果消息键不存在，返回键本身
- 如果格式化参数不匹配，返回原消息
- 如果语言文件加载失败，自动回退到默认语言