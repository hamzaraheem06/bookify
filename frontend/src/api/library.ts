import { api } from './client';
import type { Book } from '../types';
export const getLibrary = () => api<Book[]>('/library');
export const addToLibrary = (id: number) => api<Book>(`/library/${id}`, { method: 'POST' });
export const removeFromLibrary = (id: number) => api<void>(`/library/${id}`, { method: 'DELETE' });
