export interface WordClassification {
    word: string;
    is_human_descriptive: boolean;
    main_category: string | null;
    sub_category: string | null;
    description: string | null;
    reason: string | null;
    confidence: number | null;
    example: string | null;
    created_at: string;
}

export interface CategoryData {
    [key: string]: string[];
}

export interface QueryParams {
    main_category?: string;
    sub_category?: string;
    is_human_descriptive?: boolean;
    confidence_min?: number;
    page: number;
    page_size: number;
}

export interface CategoryStats {
    main_category: string;
    sub_categories: {
      name: string;
      count: number;
    }[];
    total_count: number;
  }

export interface CharacterQueryParams {
    page: number;
    pageSize: number;
    category?: string;
}

export interface Character {
    id: number;
    character: string;
    level_1_category: string;
    level_2_category: string;
    level_3_category: string;
    description: string;
    confidence: number;
    classification_reason: string;
    example: string;
    is_reviewed: boolean;
    created_at: string;
    updated_at: string;
}

export interface CharacterResponse {
    total: number;
    items: Character[];
    page: number;
    page_size: number;
}

export interface CharacterCategoryStats {
    level_1_category: string;
    total_count: number;
    sub_categories: {
      [key: string]: {
        count: number;
        children: {
          [key: string]: number;
        };
      };
    };
}
