import React, { useState } from 'react';
 
function Login() {
  const [userType, setUserType] = useState('user');
 
  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
      <div className="p-4 bg-white rounded shadow-sm" style={{ width: '100%', maxWidth: '400px' }}>
        <h2 className="mb-4 text-center text-primary">Login</h2>
 
        <div className="mb-3">
          <label className="form-label fw-bold">Select User Type</label>
          <select
            value={userType}
onChange={(e) => setUserType(e.target.value)}
            className="form-select"
          >
            <option value="user">User</option>
            <option value="end-user">End User</option>
            <option value="admin">Admin</option>
          </select>
        </div>
 
        <div className="mb-3">
          <label className="form-label fw-bold">User ID</label>
          <input className="form-control" placeholder="Enter User ID" />
        </div>
 
        <div className="mb-4">
          <label className="form-label fw-bold">Password</label>
          <input className="form-control" type="password" placeholder="Enter Password" />
        </div>
 
        <button className="btn btn-primary w-100">
          Login as {userType.charAt(0).toUpperCase() + userType.slice(1)}
        </button>
      </div>
    </div>
  );
}
 
export default Login;