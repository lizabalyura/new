import React, {useEffect, useState} from "react";
import api from "../shared/api";


const BooksList = () => {
    const [books, setBooks] = useState([]);
    const [genreMap, setGenreMap] = useState({});
    const [genre, setGenre] = useState('');
    const [author, setAuthor] = useState('');

const loadBooks = async () => {
    try {
        const params = {};
        if (genre) params.genre = genre;
        if (author) params.author = author;

        const res = await api.get('lb/filter/', { params });
        setBooks(res.data);

        // Загружаем названия жанров по id из книг
        const ids = [...new Set(res.data.map(b => b.genre))];
        const genreNames = {};
        await Promise.all(ids.map(async (id) => {
            try {
                const g = await api.get(`lb/genre/${id}/`);
                genreNames[id] = g.data.name;
            } catch {
                genreNames[id] = 'Неизвестно';
            }
        }));
        setGenreMap(genreNames);

    } catch (err) {
        console.error("Ошибка загрузки книг:", err);
    }
};

    useEffect(() => {
        loadBooks();

        const socket = new WebSocket('ws://localhost:8000/ws/books/');

        socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (data.type === 'book_update' && ['delete', 'add'].includes(data.action)) {
            loadBooks(); // перезагружаем список книг
        }
    };

    return () => socket.close();
    }, []); // при первой загрузке

    const handleFilter = (e) => {
        e.preventDefault();
        loadBooks(); // повторно загрузим с фильтрами
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Удалить эту книгу?")) return;
        try {
            await api.delete(`lb/delete_book/${id}/`)
        } catch (err) {
            console.error("Ошибка при удалении книги:", err);
        }
    };

    return (
        <>
            <form onSubmit={handleFilter} style={styles.filterForm}>
                <input
                    type="text"
                    placeholder="Автор"
                    value={author}
                    onChange={(e) => setAuthor(e.target.value)}
                    style={styles.input}
                />
                <input
                    type="number"
                    placeholder="Жанр (id)"
                    value={genre}
                    onChange={(e) => setGenre(e.target.value)}
                    style={styles.input}
                />
                <button type="submit" style={styles.button}>Фильтровать</button>
            </form>

            <ul className="book-grid">
                {books.map((p) => (
                    <li key={p.id} className="book-card">
                        <p>
                            <strong>{p.title}</strong> - {p.author}
                        </p>
                        <p>{p.description}</p>
                        <p>Жанр: <strong>{genreMap[p.genre] || p.genre}</strong></p>
                        <button onClick={() => handleDelete(p.id)}>🗑 Удалить</button>
                    </li>
                ))}
            </ul>
        </>
    );
};

const styles = {
    filterForm: {
        display: 'flex',
        gap: '10px',
        marginBottom: '20px',
    },
    input: {
        padding: '8px',
        fontSize: '14px',
    },
    button: {
        padding: '8px 12px',
        backgroundColor: '#4CAF50',
        color: 'white',
        border: 'none',
        cursor: 'pointer',
    },
};

export default BooksList;