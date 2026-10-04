import { api } from './client';
export const saveProgress = (bookId: number, chapterId: number, position: number) => api(`/player/${bookId}/progress`, { method: 'PUT', body: JSON.stringify({ chapter_id: chapterId, position_seconds: position }) });
export type ProgressRow = { book_id: number; chapter_id: number | null; position_seconds: number; updated_at: string };
export const getProgress = (bookId: number) => api<ProgressRow | null>(`/player/${bookId}/progress`);
export type HistoryItem = { book_id: number; title: string; cover_url: string; chapter_id: number | null; chapter_title: string | null; position_seconds: number; completed_seconds: number; total_seconds: number; percentage: number; last_listened_at: string };
export const getHistory = () => api<HistoryItem[]>('/player/history');
export const getBookHistory = (bookId: number) => api<HistoryItem | null>(`/player/history/${bookId}`);
