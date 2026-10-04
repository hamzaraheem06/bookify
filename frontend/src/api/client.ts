const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
export const apiRoot = API;
export async function api<T,>(path: string, options?: RequestInit): Promise<T> {
  const headers = new Headers(options?.headers);
  if (!(options?.body instanceof FormData)) headers.set('Content-Type', 'application/json');
  const token = localStorage.getItem('bookpilot_token');
  if (token) headers.set('Authorization', `Bearer ${token}`);
  const response = await fetch(`${API}${path}`, { ...options, headers });
  if (!response.ok) throw new Error((await response.text()) || `Request failed (${response.status})`);
  return response.status === 204 ? undefined as T : response.json();
}
