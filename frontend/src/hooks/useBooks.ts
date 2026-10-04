import { useQuery } from '@tanstack/react-query';
import { getBooks, type BookFilters } from '../api/books';
export const useBooks = (filters: BookFilters = {}) => useQuery({ queryKey: ['books', filters], queryFn: () => getBooks(filters), enabled: Boolean(localStorage.getItem('bookpilot_token')) });
