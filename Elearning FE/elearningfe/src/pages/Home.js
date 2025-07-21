import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

function Home() {
  return (
    <>
      <Navbar />
      <div className='container text-center p-5 py-5'>
        <h1 className='display-4 mb-4'>Welcome to the Portal</h1>
        <p className='lead'>Your gateway to eLearning and content access.</p>
      </div>
      <Footer />
    </>
  );
}

export default Home;
