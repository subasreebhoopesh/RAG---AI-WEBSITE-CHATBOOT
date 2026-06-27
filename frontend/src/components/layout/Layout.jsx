import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';

const Layout = () => {
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const isMobile = window.innerWidth < 1024;

  return (
    <div className="min-h-screen flex">
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setSidebarOpen(false)}
        isMobile={isMobile}
      />
      
      <div className="flex-1 flex flex-col lg:ml-0">
        <Navbar
          onMenuClick={() => setSidebarOpen(!isSidebarOpen)}
          isMobile={isMobile}
        />
        
        <main className="flex-1 p-4 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
