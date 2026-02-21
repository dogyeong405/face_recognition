import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import RecognitionPage from './pages/RecognitionPage';
import RegisterPage from './pages/RegisterPage';
import PeoplePage from './pages/PeoplePage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>🔍 얼굴 인식 시스템</h1>
          <nav className="app-nav">
            <NavLink to="/" end>인식</NavLink>
            <NavLink to="/register">등록</NavLink>
            <NavLink to="/people">사용자 목록</NavLink>
          </nav>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<RecognitionPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/people" element={<PeoplePage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
