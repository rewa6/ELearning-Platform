import React from 'react'
 
function UserDashboard() {
  return (
    <div className='p-10'>
      <h2 className='text-2xl font-bold'>User Dashboard</h2>
      <ul className='mt-4 list-disc pl-5'>
        <li>Enrolled IDs</li>
        <li>In Progress</li>
        <li>Certifications</li>
      </ul>
    </div>
  )
}
 
export default UserDashboard