import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Hero from './components/Hero';
import Features from './components/Features';
import Languages from './components/Languages';
import Review from './pages/Review';
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <Header />
        <main style={{ flex: '1' }}>
          <Routes>
            <Route path="/" element={
              <>
                <Hero />
                <Features />
                <Languages />
                <section id="upload" style={{ padding: '2rem 0' }}>
                  <Review />
                </section>
              </>
            } />
            <Route path="/review" element={<Review />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
