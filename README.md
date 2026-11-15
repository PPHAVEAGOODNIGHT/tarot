---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 7d2a95b442ff029d099c51d0510d2f27_56e00a17e0cf11f1913b525400393706
    ReservedCode1: jsksl+iln+qTn2K60V1Cg3K+JEDlJmcmF7BtTiJmLlYFW+hDjMDF82hEV58p3yH0uDTP1Aa/3horZHtuE2nqJum8uQT+xOYjL9CywEDRGvJ72hBMtvNW8CdGPmjZEjKaf2YRJF+Rk0nYydsQhb3JpD37cQ6MJNBPwa6KjCkMmeFJygS0vSX+iKd8gmA=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 7d2a95b442ff029d099c51d0510d2f27_56e00a17e0cf11f1913b525400393706
    ReservedCode2: jsksl+iln+qTn2K60V1Cg3K+JEDlJmcmF7BtTiJmLlYFW+hDjMDF82hEV58p3yH0uDTP1Aa/3horZHtuE2nqJum8uQT+xOYjL9CywEDRGvJ72hBMtvNW8CdGPmjZEjKaf2YRJF+Rk0nYydsQhb3JpD37cQ6MJNBPwa6KjCkMmeFJygS0vSX+iKd8gmA=
---

# PPTAROT 🔮 塔罗占星工作台

一个本地运行的塔罗占卜 / 占星工具站：前台给来问者抽牌问事，后台给占卜师管客户档案、生成解读提示词与成品图。

- 后端：Python 标准库 `http.server`，零 Web 框架依赖
- 前台：单页 H5（PC / 手机自适应），内置在 `front_page.py`
- 出图：Pillow + numpy 手绘分享海报，qrcode 生成二维码
- 星盘：pyswisseph + 瑞士星历（`ephe/`）

## 功能

| 模块 | 说明 |
| --- | --- |
| 抽牌台 | 78 张牌面、正逆位、单牌/多牌阵，手机端支持拖拽滑牌 |
| 占卜问答 | 按分类问事，返回牌面组合解读 |
| 运势 / 星盘 | 太阳星座运势、本命盘与合盘（含婚神星） |
| 分享海报 | 水晶球 / 蝴蝶 / 月亮 / 星球四种版式，带站点二维码 |
| 图文生成器 | 长图 / 单图两套独立流程，可分段导出 |
| 管理后台 | 客户档案、占卜记录、访问统计、站点 banner 配置 |

## 目录结构

```
.
├── web_tarot_workbench.py   主入口：HTTP 服务（默认 8765）与全部 API
├── front_page.py            前台单页 HTML/CSS/JS（后端拼接后输出）
├── share_poster.py          分享海报生成
├── astro_engine.py          星盘计算（pyswisseph）
├── astro_words.py           星象文案库
├── fortune_engine.py        运势引擎
├── tarot_workbench.py       legacy：最早的命令行版 MVP，仅存档参考
├── config.example.py        配置模板（复制为 config.py 使用）
├── requirements.txt
├── cards/                   78 张塔罗牌面
├── assets/                  横幅、蝴蝶素材、默认封面、联系卡
├── ephe/                    瑞士星历 seas_18.se1（婚神星需要）
└── guide_screenshots/       引导页截图
```

运行时自动生成、**不进仓库**的目录：`longimage/`（长图成品）、`groupimage/`（拼图成品）、`_tmp/`（临时文件）。

## 环境要求

- Python 3.9+
- Windows / macOS / Linux 均可运行（字体自动查找系统字体）

## 安装与启动

```bash
pip install -r requirements.txt
python web_tarot_workbench.py
```

浏览器打开 `http://127.0.0.1:8765`。

后端入口 `web_tarot_workbench.py`，端口 8765。**修改 `front_page.py` 后必须重启进程才生效**，因为前台页面是启动时读取并缓存的。

## 后台配置

```bash
copy config.example.py config.py     # Windows
cp config.example.py config.py       # macOS / Linux
```

在 `config.py` 里设置 `ADMIN_USER` / `ADMIN_PASS`，或用环境变量 `PPTAROT_ADMIN_USER` / `PPTAROT_ADMIN_PASS` 覆盖。

`config.py` 与 `tarot_workbench.db` 都已被 `.gitignore` 排除，不会进仓库。若未配置密码，服务启动时会随机生成一个并打印在控制台。

后台入口：`http://127.0.0.1:8765/admin`

## 数据说明

- `tarot_workbench.db`：SQLite，存客户档案、占卜记录、访问日志、站点配置。**首次启动自动建表**，克隆仓库后无需手动初始化。
- `prompts_log.txt`：解读提示词存档。
- 这两项都属于个人业务数据，禁止提交到仓库。

## 素材版权

`cards/` 牌面图与 `assets/` 内的素材仅用于本项目自身展示，若来自第三方素材站需自行确认授权范围，公开仓库前请留意版权。
*（内容由AI生成，仅供参考）*
