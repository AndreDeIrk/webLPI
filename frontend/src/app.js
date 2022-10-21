import { Route, Routes, Link } from 'react-router-dom'
import React, { useState } from 'react'
import Home from './components/Home';
import About from './components/About';
import Messages from './components/Messages';
import Login from './components/Login';
import useToken from './components/useToken';

function App(props) {
    const { token, setToken } = useToken();
    const [ page, setPage ] = useState('home');
    
    if (!token) {
        return <Login setToken={setToken}/>
    }

    return (
        <div className={"body text " + props.className}>
                <div className={"header-bar"}>
                    <Link to="/" 
                          onClick={() => {setPage('home')}}>
                        <button className={"header-btn" + (page === 'home' ? " active" : "")}>
                            Home
                        </button>
                    </Link>
                    <Link to="/messages" 
                          onClick={() => {setPage('back')}}>
                        <button className={"header-btn" + (page === 'back' ? " active" : "")}>
                            Back to home
                        </button>
                    </Link>
                </div>
                <div style={{
                    height: '4000px',
                    background: "rgba(0, 0, 0, 0)",
                    marginTop: '50px',
                    display: 'flex',
                    justifyContent: 'center',
                }}>                    
                    <Routes>
                        <Route path="/" element={<Home />}/>
                        {/*<Route path="/login" element={<Login setToken={setToken}/>}/>*/}
                        <Route path="/messages" element={<Messages />}/>
                        <Route path="/about" element={<About />}/>
                    </Routes>
                </div>
            </div>
    );
}

export default App;