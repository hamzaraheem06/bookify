import type { ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { PlayerProvider } from '../components/player/PlayerContext';
const queryClient = new QueryClient();
export function AppProviders({ children }: { children: ReactNode }) { return <QueryClientProvider client={queryClient}><BrowserRouter><PlayerProvider>{children}</PlayerProvider></BrowserRouter></QueryClientProvider>; }
