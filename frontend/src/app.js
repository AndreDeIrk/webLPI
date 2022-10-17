import { Route, Routes } from 'react-router-dom'
import React from 'react'
import Home from './components/Home';
import About from './components/About';
import Messages from './components/Messages';
import Login from './components/Login';
import useToken from './components/useToken';

function App() {
    const { token, setToken } = useToken();

    function element(elem) {
        if (!token) {
            return (<Login setToken={setToken}/>)
        }
        else {
            return (elem)
        }
    }

    return (
        <>
            <Routes>
                <Route path="/" element={element(<Home />)}/>
                {/*<Route path="/login" element={<Login setToken={setToken}/>}/>*/}
                <Route path="/messages" element={element(<Messages />)}/>
                <Route path="/about" element={element(<About />)}/>
            </Routes>
        </>
    );
}

export default App;