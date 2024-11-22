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
