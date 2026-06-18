import { useState } from 'react';
import Sidebar from '../components/Sidebar';
import StatsCard from '../components/StatsCard';
import CustomerTable from '../components/CustomerTable';
import CustomerDetailModal from '../components/CustomerDetailModal';
import RecentOrders from '../components/RecentOrders';
import { mockStats, mockCustomers, mockOrders } from '../data/mockData';
import type { Customer } from '../types';

export default function Dashboard() {
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar activePath="/" />

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        {/* Top Bar */}
        <header className="bg-white border-b border-gray-200 px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-sm text-gray-500 mt-0.5">
                Welcome back, Alex. Here's what's happening today.
              </p>
            </div>
            <div className="flex items-center gap-3">
              <button className="btn-secondary relative">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                  3
                </span>
              </button>
              <button className="btn-primary">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Add Customer
              </button>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="p-8 space-y-8">
          {/* Stats Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatsCard
              title="Total Customers"
              value={mockStats.totalCustomers.toLocaleString()}
              trend={mockStats.customerGrowth}
              icon="👥"
            />
            <StatsCard
              title="Active Customers"
              value={mockStats.activeCustomers.toLocaleString()}
              trend={8.4}
              icon="✅"
            />
            <StatsCard
              title="Total Revenue"
              value={(mockStats.totalRevenue / 1000000).toFixed(1) + 'M'}
              trend={mockStats.revenueGrowth}
              icon="💰"
              prefix="$"
            />
            <StatsCard
              title="Avg Order Value"
              value={mockStats.averageOrderValue.toFixed(0)}
              trend={mockStats.aovGrowth}
              icon="📊"
              prefix="$"
            />
          </div>

          {/* Customer Table */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-gray-900">Customers</h2>
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded">
                  {mockStats.newCustomersThisMonth} new this month
                </span>
              </div>
            </div>
            <CustomerTable
              customers={mockCustomers}
              onSelectCustomer={setSelectedCustomer}
            />
          </div>

          {/* Recent Orders */}
          <div>
            <h2 className="text-lg font-bold text-gray-900 mb-4">Recent Orders</h2>
            <RecentOrders orders={mockOrders} />
          </div>
        </div>
      </div>

      {/* Customer Detail Modal */}
      {selectedCustomer && (
        <CustomerDetailModal
          customer={selectedCustomer}
          onClose={() => setSelectedCustomer(null)}
        />
      )}
    </div>
  );
}
