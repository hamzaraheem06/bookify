import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './app/router';
import { AppProviders } from './app/providers';
import './styles.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AppProviders><App /></AppProviders>
  </StrictMode>,
);
