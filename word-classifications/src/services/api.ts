// src/services/api.ts
import axios from "axios";
import { CategoryData, QueryParams, CategoryStats } from "../types";

const API_BASE_URL = "http://localhost:8000/api";

export const api = {
  async getCategories(): Promise<CategoryData> {
    const { data } = await axios.get(`${API_BASE_URL}/categories`);
    return data;
  },

  async getWords(params: QueryParams) {
    const { data } = await axios.get(`${API_BASE_URL}/words`, { params });
    return data;
  },
  async getCategoryStats(): Promise<CategoryStats[]> {
    const { data } = await axios.get(`${API_BASE_URL}/category-stats`);
    return data;
  },
};
