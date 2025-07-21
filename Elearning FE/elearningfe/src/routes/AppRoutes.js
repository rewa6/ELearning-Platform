import React from 'react'
import { Routes, Route } from 'react-router-dom'
 
import Home from '../pages/Home'
import About from '../pages/About'
//import Product from '../pages/Product'
import Pricing from '../pages/Pricing'
import Contact from '../pages/Contact'
import Login from '../pages/Login'
import UserDashboard from '../pages/UserDashboard'
import EndUserDashboard from '../pages/EndUserDashboard'
import AdminDashboard from '../pages/AdminDashboard'
 
function AppRoutes() {
  return (
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='/about' element={<About />} />
      {/* <Route path='/product' element={<Product />} /> */}
      <Route path='/pricing' element={<Pricing />} />
      <Route path='/contact' element={<Contact />} />
      <Route path='/login' element={<Login />} />
      <Route path='/dashboard/user' element={<UserDashboard />} />
      <Route path='/dashboard/end-user' element={<EndUserDashboard />} />
      <Route path='/dashboard/admin' element={<AdminDashboard />} />
    </Routes>
  )
}
 
export default AppRoutes