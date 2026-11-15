# -*- coding: utf-8 -*-
"""本地私有配置模板。

使用方法：
    1. 复制本文件为 config.py（config.py 已被 .gitignore 排除，不会进仓库）
    2. 修改下面的账号密码
    3. 若不想用 config.py，也可用环境变量覆盖：PPTAROT_ADMIN_USER / PPTAROT_ADMIN_PASS
"""

# 后台登录账号
ADMIN_USER = "admin"

# 后台登录密码（留空则每次启动随机生成，并在控制台打印）
ADMIN_PASS = ""
