-- 1. 系统信息表
CREATE TABLE system_info (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    system_name VARCHAR(100) NOT NULL COMMENT '系统名称',
    system_code VARCHAR(50) UNIQUE NOT NULL COMMENT '系统编码',
    description TEXT COMMENT '系统描述',
    status TINYINT DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. 服务器信息表
CREATE TABLE server_info (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    server_name VARCHAR(100) NOT NULL COMMENT '服务器名称',
    server_ip VARCHAR(50) NOT NULL COMMENT '服务器IP',
    server_type VARCHAR(50) COMMENT '服务器类型',
    cpu_cores INT COMMENT 'CPU核心数',
    cpu_model VARCHAR(200) COMMENT 'CPU型号',
    total_memory BIGINT COMMENT '总内存(MB)',
    total_storage BIGINT COMMENT '总存储(GB)',
    total_shared_storage BIGINT COMMENT '总共享存储(GB)',
    system_id BIGINT COMMENT '所属系统ID',
    status TINYINT DEFAULT 1 COMMENT '状态：1-在线，0-离线',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES system_info(id)
);

-- 3. 计费规则表
CREATE TABLE billing_rule (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    rule_name VARCHAR(100) NOT NULL COMMENT '规则名称',
    resource_type VARCHAR(50) NOT NULL COMMENT '资源类型：CPU,MEMORY,STORAGE,SHARED_STORAGE',
    unit_price DECIMAL(10,4) NOT NULL COMMENT '单价',
    unit VARCHAR(20) NOT NULL COMMENT '单位：核/天,GB/天等',
    effective_date DATE NOT NULL COMMENT '生效日期',
    expiry_date DATE COMMENT '失效日期',
    status TINYINT DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 4. 资源使用监控表（按小时记录）
CREATE TABLE resource_monitor (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    server_id BIGINT NOT NULL COMMENT '服务器ID',
    monitor_time TIMESTAMP NOT NULL COMMENT '监控时间',
    cpu_usage_percent DECIMAL(5,2) COMMENT 'CPU使用率%',
    memory_usage_mb BIGINT COMMENT '内存使用量MB',
    storage_usage_gb BIGINT COMMENT '存储使用量GB',
    shared_storage_usage_gb BIGINT COMMENT '共享存储使用量GB',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (server_id) REFERENCES server_info(id),
    INDEX idx_server_time (server_id, monitor_time),
    INDEX idx_monitor_time (monitor_time)
);

-- 5. 日计费统计表
CREATE TABLE daily_billing (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    server_id BIGINT NOT NULL COMMENT '服务器ID',
    billing_date DATE NOT NULL COMMENT '计费日期',
    cpu_hours DECIMAL(10,2) COMMENT 'CPU小时数',
    cpu_cost DECIMAL(10,4) COMMENT 'CPU费用',
    memory_avg_gb DECIMAL(10,2) COMMENT '平均内存使用GB',
    memory_cost DECIMAL(10,4) COMMENT '内存费用',
    storage_avg_gb DECIMAL(10,2) COMMENT '平均存储使用GB',
    storage_cost DECIMAL(10,4) COMMENT '存储费用',
    shared_storage_avg_gb DECIMAL(10,2) COMMENT '平均共享存储使用GB',
    shared_storage_cost DECIMAL(10,4) COMMENT '共享存储费用',
    total_cost DECIMAL(10,4) COMMENT '总费用',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (server_id) REFERENCES server_info(id),
    UNIQUE KEY uk_server_date (server_id, billing_date)
);

-- 6. 月计费统计表
CREATE TABLE monthly_billing (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    server_id BIGINT NOT NULL COMMENT '服务器ID',
    billing_month VARCHAR(7) NOT NULL COMMENT '计费月份 YYYY-MM',
    total_cpu_cost DECIMAL(10,4) COMMENT '总CPU费用',
    total_memory_cost DECIMAL(10,4) COMMENT '总内存费用',
    total_storage_cost DECIMAL(10,4) COMMENT '总存储费用',
    total_shared_storage_cost DECIMAL(10,4) COMMENT '总共享存储费用',
    total_cost DECIMAL(10,4) COMMENT '月总费用',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (server_id) REFERENCES server_info(id),
    UNIQUE KEY uk_server_month (server_id, billing_month)
);

-- 7. 年计费统计表
CREATE TABLE yearly_billing (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    server_id BIGINT NOT NULL COMMENT '服务器ID',
    billing_year INT NOT NULL COMMENT '计费年份',
    total_cpu_cost DECIMAL(10,4) COMMENT '总CPU费用',
    total_memory_cost DECIMAL(10,4) COMMENT '总内存费用',
    total_storage_cost DECIMAL(10,4) COMMENT '总存储费用',
    total_shared_storage_cost DECIMAL(10,4) COMMENT '总共享存储费用',
    total_cost DECIMAL(10,4) COMMENT '年总费用',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (server_id) REFERENCES server_info(id),
    UNIQUE KEY uk_server_year (server_id, billing_year)
);

-- 8. 系统计费汇总表
CREATE TABLE system_billing_summary (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    system_id BIGINT NOT NULL COMMENT '系统ID',
    billing_period VARCHAR(10) NOT NULL COMMENT '计费周期：daily/monthly/yearly',
    billing_date VARCHAR(10) NOT NULL COMMENT '计费日期：YYYY-MM-DD/YYYY-MM/YYYY',
    server_count INT COMMENT '服务器数量',
    total_cpu_cost DECIMAL(10,4) COMMENT '总CPU费用',
    total_memory_cost DECIMAL(10,4) COMMENT '总内存费用',
    total_storage_cost DECIMAL(10,4) COMMENT '总存储费用',
    total_shared_storage_cost DECIMAL(10,4) COMMENT '总共享存储费用',
    total_cost DECIMAL(10,4) COMMENT '总费用',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES system_info(id),
    UNIQUE KEY uk_system_period_date (system_id, billing_period, billing_date)
);

-- 插入示例数据
INSERT INTO billing_rule (rule_name, resource_type, unit_price, unit, effective_date) VALUES
('CPU计费规则', 'CPU', 10.0000, '核/天', '2025-01-01'),
('内存计费规则', 'MEMORY', 5.0000, 'GB/天', '2025-01-01'),
('存储计费规则', 'STORAGE', 2.0000, 'GB/天', '2025-01-01'),
('共享存储计费规则', 'SHARED_STORAGE', 3.0000, 'GB/天', '2025-01-01');


-- 1. 环境配置表
CREATE TABLE environment_config (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    env_code VARCHAR(50) NOT NULL UNIQUE COMMENT '环境编码',
    env_name VARCHAR(100) NOT NULL COMMENT '环境名称',
    description TEXT COMMENT '环境描述',
    status TINYINT DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. 计费配置表（当前生效的配置）
CREATE TABLE billing_config (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    env_id BIGINT NOT NULL COMMENT '环境ID',
    resource_type VARCHAR(50) NOT NULL COMMENT '资源类型：CPU,MEMORY,STORAGE,SHARED_STORAGE',
    unit_price DECIMAL(10,4) NOT NULL COMMENT '单价',
    unit VARCHAR(20) NOT NULL COMMENT '单位',
    effective_date DATE NOT NULL COMMENT '生效日期',
    status TINYINT DEFAULT 1 COMMENT '状态：1-生效，0-失效',
    created_by VARCHAR(50) COMMENT '创建人',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (env_id) REFERENCES environment_config(id),
    UNIQUE KEY uk_env_resource_date (env_id, resource_type, effective_date)
);

-- 3. 计费配置历史表（每日记录）
CREATE TABLE billing_config_history (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    config_id BIGINT COMMENT '配置ID',
    env_id BIGINT NOT NULL COMMENT '环境ID',
    resource_type VARCHAR(50) NOT NULL COMMENT '资源类型',
    unit_price DECIMAL(10,4) NOT NULL COMMENT '单价',
    unit VARCHAR(20) NOT NULL COMMENT '单位',
    record_date DATE NOT NULL COMMENT '记录日期',
    operation_type VARCHAR(20) NOT NULL COMMENT '操作类型：CREATE,UPDATE,DELETE',
    created_by VARCHAR(50) COMMENT '操作人',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_env_resource_date (env_id, resource_type, record_date),
    INDEX idx_record_date (record_date)
);

-- 4. 计费配置审批表（可选，用于重要环境的审批流程）
CREATE TABLE billing_config_approval (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    config_id BIGINT NOT NULL COMMENT '配置ID',
    env_id BIGINT NOT NULL COMMENT '环境ID',
    resource_type VARCHAR(50) NOT NULL COMMENT '资源类型',
    old_price DECIMAL(10,4) COMMENT '原单价',
    new_price DECIMAL(10,4) NOT NULL COMMENT '新单价',
    unit VARCHAR(20) NOT NULL COMMENT '单位',
    effective_date DATE NOT NULL COMMENT '生效日期',
    approval_status VARCHAR(20) DEFAULT 'PENDING' COMMENT '审批状态：PENDING,APPROVED,REJECTED',
    applicant VARCHAR(50) NOT NULL COMMENT '申请人',
    approver VARCHAR(50) COMMENT '审批人',
    approval_time TIMESTAMP NULL COMMENT '审批时间',
    approval_comment TEXT COMMENT '审批意见',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (config_id) REFERENCES billing_config(id)
);

-- 插入环境基础数据
INSERT INTO environment_config (env_code, env_name, description) VALUES
('TEST_INTRANET', '测试内网', '内网测试环境'),
('TEST_DZ', '测试DZ', 'DZ测试环境'),
('PRE_PROD', '永久准生产', '准生产环境'),
('PROD_COMPILE', '生产编译', '生产编译环境');

-- 插入默认计费配置
INSERT INTO billing_config (env_id, resource_type, unit_price, unit, effective_date, created_by) VALUES
-- 测试内网环境
(1, 'CPU', 5.0000, '核/天', CURDATE(), 'system'),
(1, 'MEMORY', 2.0000, 'GB/天', CURDATE(), 'system'),
(1, 'STORAGE', 1.0000, 'GB/天', CURDATE(), 'system'),
(1, 'SHARED_STORAGE', 1.5000, 'GB/天', CURDATE(), 'system'),
-- 测试DZ环境
(2, 'CPU', 6.0000, '核/天', CURDATE(), 'system'),
(2, 'MEMORY', 3.0000, 'GB/天', CURDATE(), 'system'),
(2, 'STORAGE', 1.2000, 'GB/天', CURDATE(), 'system'),
(2, 'SHARED_STORAGE', 1.8000, 'GB/天', CURDATE(), 'system'),
-- 准生产环境
(3, 'CPU', 8.0000, '核/天', CURDATE(), 'system'),
(3, 'MEMORY', 4.0000, 'GB/天', CURDATE(), 'system'),
(3, 'STORAGE', 1.5000, 'GB/天', CURDATE(), 'system'),
(3, 'SHARED_STORAGE', 2.0000, 'GB/天', CURDATE(), 'system'),
-- 生产编译环境
(4, 'CPU', 10.0000, '核/天', CURDATE(), 'system'),
(4, 'MEMORY', 5.0000, 'GB/天', CURDATE(), 'system'),
(4, 'STORAGE', 2.0000, 'GB/天', CURDATE(), 'system'),
(4, 'SHARED_STORAGE', 2.5000, 'GB/天', CURDATE(), 'system');
