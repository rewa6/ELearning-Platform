import React, { useState } from 'react';
 
function Contact() {
  const [form, setForm] = useState({
    name: '',
    email: '',
    contact: '',
    message: '',
  });
 
  const handleChange = (e) => {
setForm({ ...form, [e.target.name]: e.target.value });
  };
 
  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Message sent! We will contact you soon.');
    setForm({ name: '', email: '', contact: '', message: '' });
  };
 
  return (
    <div className="container py-5">
      <h2 className="text-center mb-5 text-primary">Contact Us</h2>
      <form onSubmit={handleSubmit} className="mx-auto" style={{ maxWidth: '600px' }}>
        <div className="mb-3">
          <label className="form-label fw-bold">User Name</label>
          <input
            className="form-control"
            name="name"
value={form.name}
            onChange={handleChange}
            required
            placeholder="Enter your name"
          />
        </div>
        <div className="mb-3">
          <label className="form-label fw-bold">User Email ID</label>
          <input
            type="email"
            className="form-control"
            name="email"
value={form.email}
            onChange={handleChange}
            required
            placeholder="Enter your email"
          />
        </div>
        <div className="mb-3">
          <label className="form-label fw-bold">Contact Details</label>
          <input
            className="form-control"
            name="contact"
value={form.contact}
            onChange={handleChange}
            required
            placeholder="Phone or WhatsApp"
          />
        </div>
        <div className="mb-4">
          <label className="form-label fw-bold">Your Message</label>
          <textarea
            className="form-control"
            name="message"
            rows="4"
            value={form.message}
            onChange={handleChange}
            required
            placeholder="Type your message here"
          ></textarea>
        </div>
        <button type="submit" className="btn btn-primary w-100">
          Submit
        </button>
      </form>
    </div>
  );
}
 
export default Contact;