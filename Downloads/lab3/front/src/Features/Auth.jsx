import {useState} from 'react'
import api from "../shared/api.jsx"
import { useNavigate } from 'react-router-dom';

export default function AuthForm() {
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const endpoint = isLogin ? 'lb/login/' : 'lb/register/';
        try {
            const response = await api.post(endpoint, { username, password });
            if (isLogin) {
                const { access, refresh } = response.data;
                localStorage.setItem('accessToken', access);
                localStorage.setItem('refreshToken', refresh);
                api.setTokenAuth();  // обновим заголовок Authorization
                navigate('/books')
            } else {
                setMessage('Регистрация успешна. Теперь войдите.');
                setIsLogin(true);
            }
        } catch (err) {
            setMessage('Ошибка: ' + err.response?.data?.detail || 'Проверьте данные');
        }
    };

    return (
        <div>
            <h2>{isLogin ? 'Вход' : 'Регистрация'}</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Имя пользователя"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                /><br />
                <input
                    type="password"
                    placeholder="Пароль"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                /><br />
                <button type="submit">{isLogin ? 'Войти' : 'Зарегистрироваться'}</button>
            </form>
            <button onClick={() => setIsLogin(!isLogin)}>
                {isLogin ? 'Нет аккаунта? Зарегистрироваться' : 'Уже есть аккаунт? Войти'}
            </button>
            <p>{message}</p>
        </div>
    );
}