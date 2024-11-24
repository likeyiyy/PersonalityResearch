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


CREATE TABLE `chinese_words_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `word` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level_1_category` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level_2_category` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level_3_category` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` mediumtext COLLATE utf8mb4_unicode_ci,
  `confidence` float DEFAULT NULL,
  `classification_reason` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `example` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_reviewed` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_word` (`word`),
  KEY `level_1_category` (`level_1_category`),
  KEY `level_2_category` (`level_2_category`),
  KEY `level_3_category` (`level_3_category`)
) ENGINE=InnoDB AUTO_INCREMENT=15655 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `derogatory_terms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `word` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level_1_category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level_2_category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level_3_category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_word` (`word`),
  KEY `level_1_category` (`level_1_category`),
  KEY `level_2_category` (`level_2_category`),
  KEY `level_3_category` (`level_3_category`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `commendatory_terms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `word` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level_1_category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level_2_category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level_3_category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_word` (`word`),
  KEY `level_1_category` (`level_1_category`),
  KEY `level_2_category` (`level_2_category`),
  KEY `level_3_category` (`level_3_category`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
