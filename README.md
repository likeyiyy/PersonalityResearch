# PersonalityResearch

-- 创建表
CREATE TABLE IF NOT EXISTS word_classifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(10),
    is_human_descriptive BOOLEAN,
    created_at DATETIME,
    INDEX(word)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS word_classifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(10),
    is_human_descriptive BOOLEAN,
    main_category VARCHAR(20) COMMENT '主类别：外貌/性格品德/能力才智/情绪状态/社交特征/生理状态/非人物描述',
    sub_category VARCHAR(20) COMMENT '子类别',
    description TEXT COMMENT '详细解释，包括词义和使用场景',
    reason TEXT COMMENT '分类判断依据',
    confidence FLOAT COMMENT '判断的置信度 0-1',
    example VARCHAR(255) COMMENT '使用示例',
    created_at DATETIME,
    INDEX(word)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
