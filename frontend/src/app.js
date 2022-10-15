import { Link, Route, Routes } from 'react-router-dom'
import React from 'react'
import Home from './components/Home';
import About from './components/About';
import Messages from './components/Messages';
import LogIn from './components/LogIn';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />}/>
      <Route path="/login" element={<LogIn />}/>
      <Route path="/messages" element={<Messages />}/>
      <Route path="/about" element={<About />}/>
    </Routes>
  );
}

export default App;