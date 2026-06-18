import type { NavItem } from '../types';

interface SidebarProps {
  activePath: string;
}

const navItems: NavItem[] = [
  { label: 'Dashboard', icon: '📊', path: '/' },
  { label: 'Customers', icon: '👥', path: '/customers', badge: 12 },
  { label: 'Orders', icon: '📦', path: '/orders' },
  { label: 'Analytics', icon: '📈', path: '/analytics' },
  { label: 'Reports', icon: '📄', path: '/reports' },
  { label: 'Settings', icon: '⚙️', path: '/settings' },
];

export default function Sidebar({ activePath }: SidebarProps) {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col h-screen">
      {/* Logo */}
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center text-white font-bold text-lg">
            C
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900">CRM Hub</h1>
            <p className="text-xs text-gray-500">Customer Dashboard</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        <p className="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
          Main Menu
        </p>
        {navItems.map((item) => {
          const isActive = item.path === activePath;
          return (
            <a
              key={item.path}
              href={item.path}
              className={`sidebar-link ${
                isActive ? 'sidebar-link-active' : 'sidebar-link-inactive'
              }`}
            >
              <span className="text-lg">{item.icon}</span>
              <span className="flex-1">{item.label}</span>
              {item.badge && (
                <span className="inline-flex items-center justify-center w-5 h-5 text-xs font-semibold text-white bg-primary-600 rounded-full">
                  {item.badge}
                </span>
              )}
            </a>
          );
        })}

        <p className="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3 mt-6">
          Support
        </p>
        <a
          href="/help"
          className="sidebar-link sidebar-link-inactive"
        >
          <span className="text-lg">❓</span>
          <span>Help Center</span>
        </a>
        <a
          href="/docs"
          className="sidebar-link sidebar-link-inactive"
        >
          <span className="text-lg">📖</span>
          <span>Documentation</span>
        </a>
      </nav>

      {/* User Profile */}
      <div className="p-4 border-t border-gray-100">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
            AD
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">Alex Demos</p>
            <p className="text-xs text-gray-500 truncate">alex@crmhub.com</p>
          </div>
          <button className="text-gray-400 hover:text-gray-600 transition-colors" aria-label="Logout">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>
      </div>
    </aside>
  );
}
