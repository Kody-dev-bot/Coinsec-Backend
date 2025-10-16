/* =========================================================
   个人记账数据库 · PostgresSQL ≥12
   作者： kody
   目标：单用户→多用户可扩展；支持多币种、预算、分账、自动余额
   ========================================================= */

-- 0. 插件 & 编码
-- 预留 UUID 主键扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- 预算排重 Exclusion Constraint 需要
CREATE EXTENSION IF NOT EXISTS "btree_gist";
-- 统一日期格式 yyyy-mm-dd
SET datestyle = 'ISO, YMD';

-- 1. 用户
CREATE TABLE users
(
    id         SERIAL PRIMARY KEY,
    user_name  VARCHAR(50) UNIQUE NOT NULL, -- 登录名，全局唯一
    pwd_hash   CHAR(60)           NOT NULL, -- bcrypt 哈希，固定 60 字符
    created_at TIMESTAMPTZ DEFAULT NOW()    -- 注册时间
);
COMMENT ON TABLE users IS '用户主表';
COMMENT ON COLUMN users.user_name IS '登录用户名，区分大小写';
COMMENT ON COLUMN users.pwd_hash IS 'bcrypt 加密后的密码';