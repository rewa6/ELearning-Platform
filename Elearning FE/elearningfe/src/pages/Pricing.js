import React from 'react';

function Pricing() {
  const plans = [
    {
      name: 'Starter Pack',
      price: '₹199',
      details: 'Includes 10 End User IDs valid for 30 days.',
    },
    {
      name: 'Pro Pack',
      price: '₹499',
      details: '30 End User IDs, Email reminders, extended support.',
    },
    {
      name: 'Enterprise Pack',
      price: '₹999',
      details: 'Unlimited End Users with admin control and priority support.',
    },
  ];

  return (
    <div className="container py-5">
      <h2 className="text-center text-primary mb-5">Pricing</h2>
      <div className="row">
        {plans.map((plan, index) => (
          <div className="col-md-4 mb-4" key={index}>
            <div className="card border-primary shadow-sm h-100">
              <div className="card-body text-center">
                <h5 className="card-title">{plan.name}</h5> {/* Corrected here */}
                <h6 className="card-subtitle text-muted mb-3">{plan.price}</h6>
                <p className="card-text">{plan.details}</p>
                <button className="btn btn-outline-primary mt-3">Subscribe</button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="text-center mt-5">
        <h5 className="mb-3">We accept UPI QR payments via</h5>
        <div className="d-flex justify-content-center gap-3">
          <span className="badge bg-primary">GPay</span>
          <span className="badge bg-success">PhonePe</span>
          <span className="badge bg-info text-dark">Paytm</span>
        </div>
      </div>
    </div>
  );
}

export default Pricing;
