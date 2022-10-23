import { Route, Routes, Link } from 'react-router-dom'
import React, { useState } from 'react'
import Home from './components/Home';
import About from './components/About';
import Settings from './components/Settings';
import Login from './components/Login';
import useToken from './components/useToken';
import HeaderSwitcher from "./components/elements/HeaderSwitcher";

function App(props) {
    const { token, setToken } = useToken();
    const [ page, setPage ] = useState(window.location.pathname);
    
    if (!token) {
        return <Login setToken={setToken}/>
    }

    return (
        <div className={"body text " + props.className}>
                <div className={"header-bar"}>
                    <Link to="/" onClick={() => {setPage('/')}}>
                        <button className={"header-btn" + (page === '/' ? " active" : "")}>
                            Home
                        </button>
                    </Link>
                    <HeaderSwitcher to={'Settings'} onClick={setPage} page={page}/>
                    <HeaderSwitcher to={'About'} onClick={setPage} page={page}/>
                </div>
                <div className={'content'}>
                    <Routes>
                        <Route path="/" element={<Home />}/>
                        {/*<Route path="/login" element={<Login setToken={setToken}/>}/>*/}
                        <Route path="/settings" element={<Settings />}/>
                        <Route path="/about" element={<About />}/>
                    </Routes>
                </div>
            </div>
    );
}

export default App;