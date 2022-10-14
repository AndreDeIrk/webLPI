import { Link, Route, Routes } from 'react-router-dom'
import Home from './components/Home';
import About from './components/About';
import Messages from './components/Messages';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/*<img src={logo} className="App-logo" alt="logo" />*/}
        <h1 className="App-title">Welcome to React</h1>
      </header>
      <div className="menu">
        <ul>
          <li> <Link to="/">Home</Link> </li>
          <li> <Link to="/messages">Messages</Link> </li>
          <li> <Link to="/about">About</Link> </li>
        </ul>
      </div>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/messages" element={<Messages />}/>
        <Route path="/about" element={<About />}/>
      </Routes>
    </div>
  );
}

export default App;