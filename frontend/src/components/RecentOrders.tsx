import type { Order } from '../types';

interface RecentOrdersProps {
  orders: Order[];
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

const statusStyles: Record<string, string> = {
  completed: 'bg-emerald-100 text-emerald-800',
  pending: 'bg-amber-100 text-amber-800',
  cancelled: 'bg-red-100 text-red-800',
  refunded: 'bg-gray-100 text-gray-800',
};

export default function RecentOrders({ orders }: RecentOrdersProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100">
      <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
        <h3 className="font-semibold text-gray-900">Recent Orders</h3>
        <a href="/orders" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
          View all →
        </a>
      </div>

      <div className="divide-y divide-gray-50">
        {orders.map((order) => (
          <div key={order.id} className="px-6 py-3.5 flex items-center justify-between hover:bg-gray-50 transition-colors">
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center text-xs font-medium text-gray-600">
                #{order.id.slice(-4)}
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">{order.customerName}</p>
                <p className="text-xs text-gray-500">{order.id} · {order.items} item{order.items > 1 ? 's' : ''}</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${statusStyles[order.status] || ''}`}>
                {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
              </span>
              <span className="text-sm font-semibold text-gray-900 w-20 text-right">
                {formatCurrency(order.amount)}
              </span>
              <span className="text-xs text-gray-400 w-24 text-right">{order.date}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
