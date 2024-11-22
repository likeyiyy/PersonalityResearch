# PersonalityResearch

-- 创建表
CREATE TABLE IF NOT EXISTS word_classifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(10),
    is_human_descriptive BOOLEAN,
    created_at DATETIME,
    INDEX(word)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
