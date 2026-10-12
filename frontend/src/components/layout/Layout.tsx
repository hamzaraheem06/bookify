import type { ReactNode } from 'react';
import { Compass, Home as HomeIcon, Library } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { Player } from '../player/Player';
import { useState } from 'react';
export function Layout({ children }: { children: ReactNode }) { const [menuOpen,setMenuOpen]=useState(false); const closeMenu=()=>setMenuOpen(false); return <div className="app-shell"><Sidebar open={menuOpen} onNavigate={closeMenu}/>{menuOpen&&<button className="sidebar-backdrop" aria-label="Close navigation" onClick={closeMenu}/>}<main className="main"><Header onMenuClick={()=>setMenuOpen(open=>!open)}/><div className="content">{children}</div></main><Player /><div className="mobile-nav"><NavLink to="/"><HomeIcon size={18} />Home</NavLink><NavLink to="/discover"><Compass size={18} />Discover</NavLink><NavLink to="/library"><Library size={18} />Library</NavLink></div></div>; }
