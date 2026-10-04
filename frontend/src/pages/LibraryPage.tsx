import { Library } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getBooks } from '../api/books';
import { BookCard } from '../components/books/BookCard';
export function LibraryPage() { const { data = [], isLoading, error } = useQuery({ queryKey: ['library'], queryFn: () => getBooks() }); return <><div className="page-title"><div><div className="eyebrow">YOUR COLLECTION</div><h1>My library</h1></div><Link className="button primary" to="/upload">Upload PDF</Link></div>{isLoading ? <div className="state">Loading library...</div> : error ? <div className="state">Could not load your library. Check that the backend is running.</div> : data.length ? <div className="book-grid discover-grid">{data.map(book => <BookCard book={book} key={book.id} />)}</div> : <div className="empty"><Library size={32} /><h2>Your library is empty.</h2><p>Upload a PDF and make your first listening edition.</p><Link className="button primary" to="/upload">Upload a PDF</Link></div>}</>; }
