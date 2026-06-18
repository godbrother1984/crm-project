import { useState } from 'react';
import type { Customer } from '../types';

interface CustomerTableProps {
  customers: Customer[];
  onSelectCustomer: (customer: Customer) => void;
}

const statusBadge: Record<string, string> = {
  active: 'badge-active',
  inactive: 'badge-inactive',
  lead: 'badge-lead',
  vip: 'badge-vip',
};

type SortKey = 'name' | 'company' | 'totalSpent' | 'lastOrder' | 'status';

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export default function CustomerTable({ customers, onSelectCustomer }: CustomerTableProps) {
  const [search, setSearch] = useState('');
  const [sortKey, setSortKey] = useState<SortKey>('lastOrder');
  const [sortAsc, setSortAsc] = useState(false);

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortAsc(!sortAsc);
    } else {
      setSortKey(key);
      setSortAsc(false);
    }
  };

  const sortIcon = (key: SortKey) => {
    if (sortKey !== key) return '↕';
    return sortAsc ? '↑' : '↓';
  };

  const filtered = customers
    .filter((c) =>
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.company.toLowerCase().includes(search.toLowerCase()) ||
      c.email.toLowerCase().includes(search.toLowerCase())
    )
    .sort((a, b) => {
      let cmp = 0;
      switch (sortKey) {
        case 'name': cmp = a.name.localeCompare(b.name); break;
        case 'company': cmp = a.company.localeCompare(b.company); break;
        case 'totalSpent': cmp = a.totalSpent - b.totalSpent; break;
        case 'lastOrder': cmp = a.lastOrder.localeCompare(b.lastOrder); break;
        case 'status': cmp = a.status.localeCompare(b.status); break;
      }
      return sortAsc ? cmp : -cmp;
    });

  const initials = (name: string) =>
    name.split(' ').map((n) => n[0]).join('').toUpperCase().slice(0, 2);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      {/* Header with search */}
      <div className="p-4 border-b border-gray-100 flex items-center justify-between gap-4">
        <div className="relative flex-1 max-w-sm">
          <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            placeholder="Search customers..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">{filtered.length} customers</span>
          <button className="btn-secondary text-xs px-3 py-1.5">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            Filter
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50">
              <th className="table-header cursor-pointer select-none" onClick={() => handleSort('name')}>
                Customer {sortIcon('name')}
              </th>
              <th className="table-header cursor-pointer select-none" onClick={() => handleSort('company')}>
                Company {sortIcon('company')}
              </th>
              <th className="table-header">Contact</th>
              <th className="table-header cursor-pointer select-none" onClick={() => handleSort('status')}>
                Status {sortIcon('status')}
              </th>
              <th className="table-header cursor-pointer select-none" onClick={() => handleSort('totalSpent')}>
                Total Spent {sortIcon('totalSpent')}
              </th>
              <th className="table-header">Orders</th>
              <th className="table-header cursor-pointer select-none" onClick={() => handleSort('lastOrder')}>
                Last Order {sortIcon('lastOrder')}
              </th>
              <th className="table-header">Tags</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filtered.map((customer) => (
              <tr
                key={customer.id}
                className="hover:bg-gray-50 cursor-pointer transition-colors"
                onClick={() => onSelectCustomer(customer)}
              >
                <td className="table-cell">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full flex items-center justify-center text-white font-semibold text-xs">
                      {initials(customer.name)}
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{customer.name}</p>
                      <p className="text-xs text-gray-500">{customer.id}</p>
                    </div>
                  </div>
                </td>
                <td className="table-cell text-gray-700">{customer.company}</td>
                <td className="table-cell">
                  <div className="text-sm text-gray-700">{customer.email}</div>
                  <div className="text-xs text-gray-400">{customer.phone}</div>
                </td>
                <td className="table-cell">
                  <span className={statusBadge[customer.status] || 'badge'}>
                    {customer.status.charAt(0).toUpperCase() + customer.status.slice(1)}
                  </span>
                </td>
                <td className="table-cell font-medium text-gray-900">
                  {formatCurrency(customer.totalSpent)}
                </td>
                <td className="table-cell text-gray-700">{customer.totalOrders}</td>
                <td className="table-cell text-gray-500">{customer.lastOrder}</td>
                <td className="table-cell">
                  <div className="flex flex-wrap gap-1">
                    {customer.tags.map((tag) => (
                      <span
                        key={tag}
                        className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-700"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Empty state */}
      {filtered.length === 0 && (
        <div className="text-center py-16">
          <span className="text-4xl">🔍</span>
          <p className="mt-3 text-gray-500 text-sm">No customers found matching "{search}"</p>
          <button
            onClick={() => setSearch('')}
            className="mt-2 text-sm text-primary-600 hover:text-primary-700"
          >
            Clear search
          </button>
        </div>
      )}
    </div>
  );
}
