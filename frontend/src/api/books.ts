import { api } from './client';
import type { Book, Chapter } from '../types';
export type BookFilters = { search?: string; category?: string; language?: string; source?: string; author?: string };
export const getBooks = (filters: BookFilters = {}) => {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => { if (value) params.set(key, value); });
  const query = params.toString();
  return api<Book[]>(query ? `/books?${query}` : '/books');
};
export const getBook = (id: string) => api<Book>(`/books/${id}`);
export const getChapters = (id: string) => api<Chapter[]>(`/books/${id}/chapters`);
