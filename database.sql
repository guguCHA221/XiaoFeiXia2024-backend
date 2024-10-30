-- 创建数据库
CREATE DATABASE IF NOT EXISTS lost_and_found_db;
USE lost_and_found_db;

-- 创建用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建物品类型表
CREATE TABLE item_types (
    type_code CHAR(1) PRIMARY KEY,
    type_name VARCHAR(20) NOT NULL,
    current_sequence INT DEFAULT 0
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入物品类型数据
INSERT INTO item_types (type_code, type_name) VALUES
('Y', '衣帽眼镜'),
('U', '雨伞'),
('B', '书籍'),
('D', '电子产品'),
('S', '体育用品'),
('W', '水杯'),
('C', '证件'),
('G', '箱包'),
('Z', '其他');

-- 创建失物表
CREATE TABLE lost_items (
    id VARCHAR(20) PRIMARY KEY,
    item_type CHAR(1),
    type_id INT,
    name VARCHAR(100) NOT NULL,
    public_info TEXT,
    private_info TEXT,
    found_location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('未领取', '已领取', '过期处理') DEFAULT '未领取',
    claimer_name VARCHAR(50),
    claimer_student_id VARCHAR(20),
    claimer_phone VARCHAR(20),
    created_by INT,
    updated_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    FOREIGN KEY (item_type) REFERENCES item_types(type_code)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建西服租赁表
CREATE TABLE suit_rentals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    suit_number VARCHAR(50) NOT NULL,
    student_name VARCHAR(50) NOT NULL,
    student_id VARCHAR(20) NOT NULL,
    contact_info VARCHAR(50) NOT NULL,
    rental_time DATE NOT NULL,
    expected_return_time DATE NOT NULL,
    status ENUM('已预约', '未归还', '已归还') DEFAULT '已预约',
    notes TEXT,
    created_by INT,
    updated_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET time_zone = '+08:00';
