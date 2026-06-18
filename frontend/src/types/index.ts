export interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string;
  company: string;
  status: 'active' | 'inactive' | 'lead' | 'vip';
  totalOrders: number;
  totalSpent: number;
  lastOrder: string;
  createdAt: string;
  tags: string[];
  avatar?: string;
}

export interface DashboardStats {
  totalCustomers: number;
  activeCustomers: number;
  totalRevenue: number;
  averageOrderValue: number;
  newCustomersThisMonth: number;
  customerGrowth: number;
  revenueGrowth: number;
  aovGrowth: number;
}

export interface Order {
  id: string;
  customerId: string;
  customerName: string;
  amount: number;
  status: 'completed' | 'pending' | 'cancelled' | 'refunded';
  date: string;
  items: number;
}

export interface NavItem {
  label: string;
  icon: string;
  path: string;
  badge?: number;
}
