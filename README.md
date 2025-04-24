# WallpaperMCP

## 简介

自己写的一个用于壁纸管理的MCP server。

目前是从Unsplash获取壁纸，支持的平台是Windows10. 用uv来管理环境，所使用的库见uv.lock

制作MCP Server的[教程](https://modelcontextprotocol.io/quickstart/server#windows)，来自Claude Desktop。

## 使用方法

1. 创建环境

```bash
cd /path/to/project
uv venv
uv pip install -r uv.lock
```

或者`uv venv`以后手动`uv add mcp[cli] httpx requests`以及其他需要的库，我也记不得具体有哪些了，看情况补充吧

1. 配置API

在项目目录下创建文件.env，在里面写入UNSPLASH_API='xxx'。如何申请Unsplash的API参见[这里](https://unsplash.com/documentation#getting-started)。

1. 导入MCP Host (比如cursor)

导入所需的指令如下，我就不格式化成json了

```bash
uv --directory ABSOLUTE-PATH-TO-PARENT-FOLDER/WallpaperMCP run Unsplash.py
```

可能需要将uv替换成其可执行文件的绝对路径才行，比如对我来说就是C:\\Users\\{Username}\\.local\\bin\\uv.exe。运行which uv（MacOS/Linux）或者where uv（Windows）可以看到该路径。
