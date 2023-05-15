import { Route, Routes, Link } from 'react-router-dom'
import React, { useState } from 'react'
import Home from './components/Home';
import About from './components/About';
import Settings from './components/Settings';
import Login from './components/Login';
import useToken from './components/useToken';
import HeaderSwitcher from "./components/elements/HeaderSwitcher";

import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';

function App(props) {
    const { token, setToken } = useToken();
    const [ page, setPage ] = useState(window.location.pathname);
    
    if (!token) {
        return <Login setToken={setToken}/>
    }

    const tabs = [
        {href: '/', name: 'Home'},
        {href: '/settings', name: 'Settings'},
        {href: '/about', name: 'About'},
        {href: '/login', name: 'Login'},
    ]

    return (
        <div className={`body ${props.className}`}>
            <Navbar sticky='top' bg='dark' variant="dark" expand='sm'>
                <Container>
                    <Navbar.Brand>Navbar</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className='me-auto'>
                        {tabs.map((tab) => 
                            <Nav.Link as={Link} to={tab.href} onClick={() => {setPage(tab.href)}}>
                                {tab.name}
                            </Nav.Link>
                        )}
                            
                            {/* <HeaderSwitcher to={'Settings'} onClick={setPage} page={page}/>
                            <HeaderSwitcher to={'About'} onClick={setPage} page={page}/>                    
                            <HeaderSwitcher to={'Login'} onClick={setPage} page={page}/> */}
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
            <div className={'content'}>
                <Routes>
                    <Route path="/" element={<Home />}/>
                    {/*<Route path="/login" element={<Login setToken={setToken}/>}/>*/}
                    <Route path="/settings" element={<Settings />}/>
                    <Route path="/about" element={<About />}/>
                    <Route path="/login" element={<Login setToken={setToken}/>}/>
                </Routes>
            </div>
        </div>
    );
}

export default App;