import { useState } from 'react';

export default function useToken() {
    const getToken = () => {
        const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString);
        return userToken?.token;
    };

    const [token, setToken] = useState(getToken());

    const saveToken = (userToken) => {
        if (userToken?.token === ""){
            localStorage.clear();
            setToken("");
        }
        else {
            localStorage.setItem('token', JSON.stringify(userToken));
            setToken(userToken.token);
        }
    };

    return {
        setToken: saveToken,
        token
    }
}
