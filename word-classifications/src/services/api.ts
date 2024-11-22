// src/services/api.ts
import axios from "axios";
import { CategoryData, QueryParams, CategoryStats } from "../types";

const API_BASE_URL = "http://localhost:8001/api";

// 词语相关的 API
const wordApi = {

  async getWords(params: {
    page: number;
    pageSize: number;
    category?: string;
  }) {
    const { data } = await axios.get(`${API_BASE_URL}/words`, { params });
    return data;
  },

  async getCategories() {
    const { data } = await axios.get(`${API_BASE_URL}/words/categories`);
    return data;
  },

};

// 汉字相关的 API
const characterApi = {
  async getCharacters(params: {
    page: number;
    pageSize: number;
    category?: string;
  }) {
    const { data } = await axios.get(`${API_BASE_URL}/characters`, { params });
    return data;
  },

  async getCategories() {
    const { data } = await axios.get(`${API_BASE_URL}/characters/categories`);
    return data;
  },

};


// 导出所有 API
export const api = {
  word: wordApi,
  character: characterApi
};
