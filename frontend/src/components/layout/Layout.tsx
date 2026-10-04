import type { ReactNode } from 'react';
import { Compass, Home as HomeIcon, Library } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { Player } from '../player/Player';
export function Layout({ children }: { children: ReactNode }) { return <div className="app-shell"><Sidebar /><main className="main"><Header /><div className="content">{children}</div></main><Player /><div className="mobile-nav"><NavLink to="/"><HomeIcon size={18} />Home</NavLink><NavLink to="/discover"><Compass size={18} />Discover</NavLink><NavLink to="/library"><Library size={18} />Library</NavLink></div></div>; }
