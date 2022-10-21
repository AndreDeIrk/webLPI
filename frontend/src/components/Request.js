// import useToken from './useToken';
// import { useState } from 'react';

export default async function Request(url, body, auth=false, token="", setToken=() => {}) {
    const header = {'Content-Type': 'application/json'};
    if (auth) {
        if (!token) {
            return {status: false, detail: "No JWT saved."}
        }
        console.log(token); header['Authorization'] = 'Bearer ' + token
    }

    return fetch(process.env.REACT_APP_BACKEND_URL + url, {
        method: 'POST',
        headers: header,
        body: body
    }).then(data => data.json()).catch((error) => {
        if (error === "Invalid token or expired token.") {
            const tokenString = localStorage.getItem('token');
            const userToken = JSON.parse(tokenString);
            const refresh_token = userToken?.['refreshToken'];
            return fetch(process.env.REACT_APP_BACKEND_URL + '/auth/refresh', {
                method: 'POST',
                headers: header,
                body: {token: refresh_token}
            }).then(data => data.json()).catch((error) => {

            });
        }
        return {status: false, detail: error};
    })
}