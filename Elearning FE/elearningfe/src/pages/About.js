import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
function About() {
  return (
    <>
      <Navbar />
      <div className='container p-5'>
        <h2 className='h2 mb-4'>About Us</h2>
        <p>We are an eLearning platform empowering learners.</p>
      </div>
      <Footer />
    </>
  );
}
export default About;