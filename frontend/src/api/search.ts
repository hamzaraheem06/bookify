import { api } from './client';
import type { Book } from '../types';
export const searchBooks = (query: string) => api<Book[]>(`/search?q=${encodeURIComponent(query)}`);
