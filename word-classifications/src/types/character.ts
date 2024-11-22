export interface Character {
  id: number;
  character: string;
  level1Category: string;
  level2Category: string;
  level3Category: string;
  description: string;
  confidence: number;
  classificationReason: string;
  example: string;
  isReviewed: boolean;
}

export interface CharacterResponse {
  data: Character[];
  total: number;
  page: number;
  pageSize: number;
}

export interface CategoryStats {
  [key: string]: {
    count: number;
    children: {
      [key: string]: {
        count: number;
        children: {
          [key: string]: number;
        };
      };
    };
  };
} 