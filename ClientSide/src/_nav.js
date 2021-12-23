export default [
  {
    component: 'CNavItem',
    name: 'Dashboard',
    to: '/dashboard',
    icon: 'cil-speedometer',
  },
  {
    component: 'CNavGroup',
    name: 'Customers',
    to: '/Customers',
    icon: 'cil-user',
    items: [
      {
        component: 'CNavItem',
        name: 'Customer Lists',
        to: '/customers/customer',
      },
      {
        component: 'CNavItem',
        name: 'New Customer',
        to: '/customers/customer',
      },
    ],
  },
  {
    component: 'CNavGroup',
    name: 'Loans',
    to: '/Disbursements',
    icon: 'cil-money',
    items: [
      {
        component: 'CNavItem',
        name: 'Disbursed Lists',
        to: '/disbursements/disbursed',
      },
      {
        component: 'CNavItem',
        name: 'New Disbursement',
        to: '/disbursements/disbursed',
      },
    ],
  },
  {
    name: 'Authentications',
    to: '/Users',
    icon: 'cil-star',
    items: [
      {
        component: 'CNavItem',
        name: 'Users',
        to: '/Users/user',
      },
    ],
  },
]
