import axios from 'axios';
import { Character, CharacterResponse, CategoryStats } from '../types/character';

const API_BASE_URL = '/api';

export const getCharacters = async (
  page: number,
  pageSize: number,
  category?: string
): Promise<CharacterResponse> => {
  const response = await axios.get(`${API_BASE_URL}/characters`, {
    params: {
      page,
      pageSize,
      category,
    },
  });
  return response.data;
};

export const getCharacterCategories = async (): Promise<CategoryStats> => {
  const response = await axios.get(`${API_BASE_URL}/characters/categories`);
  return response.data;
}; 