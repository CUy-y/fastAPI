# 今日头条项目

后端使用 FastAPI、SQLAlchemy Async 和 MySQL；前端为参考项目中的 Vue 3、Vite 应用。当前不依赖 Redis。

## 首次运行

1. 确认本机 MySQL 服务运行，并创建 `news_app` 数据库。
2. 复制 `.env.example` 为 `.env`，填写本机数据库账户和密码。
3. 在项目目录 `toutiao_` 打开 PowerShell，执行：

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

   服务启动时会创建缺少的数据表，并补齐默认新闻分类；已有数据不会被删除。
4. 另开终端进入 `news-headline-frontend`，执行：

   ```powershell
   npm ci
   npm run dev
   ```

前端默认请求 `http://127.0.0.1:8000`。接口文档地址为 `http://127.0.0.1:8000/docs`。

## 导入本地演示数据

应用首次启动并建好表、默认分类后，可在 MySQL Workbench 中打开并执行 `db/seed.sql`，或在 MySQL 客户端中运行：

```sql
SOURCE E:/fastAPI/toutiao_/db/seed.sql;
```

脚本从参考项目整理了 403 条示例新闻，并创建一个普通测试用户：`admin` / `admin123456`。新闻内容是演示数据，不代表实时新闻。**只在空的本地开发库执行一次**；再次执行会重复插入新闻。

## AI 问答

AI 问答需要单独配置 DashScope API Key。在前端目录创建本地 `.env` 并设置 `VITE_DASHSCOPE_API_KEY`；不要把真实密钥提交到代码仓库。其余新闻、用户、收藏和历史功能不需要 AI 密钥。
