import { Menu, Search } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
export function Header() { const navigate = useNavigate(); const [query, setQuery] = useState(''); const logout = () => { localStorage.removeItem('bookpilot_token'); navigate('/'); }; return <header className="header"><button className="mobile-menu" aria-label="Open menu"><Menu /></button><div className="search-box"><Search size={17} /><input value={query} onChange={e => setQuery(e.target.value)} onKeyDown={e => e.key === 'Enter' && query.trim() && navigate(`/search?q=${encodeURIComponent(query)}`)} placeholder="Search titles, authors, stories..." /><kbd>⌘ K</kbd></div><button className="avatar" aria-label="Log out" onClick={logout}>AL</button></header>; }
