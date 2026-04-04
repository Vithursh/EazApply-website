import React from 'react';

const LoadingScreen: React.FC = () => {
  return (
    <div className="fixed inset-0 bg-gray-900 flex items-center justify-center z-50">
      <div className="flex flex-col items-center gap-6">
        {/* Spinning Loading Wheel */}
        <div className="relative w-16 h-16">
          <div className="absolute inset-0 border-4 border-gray-700 rounded-full"></div>
          <div className="absolute inset-0 border-4 border-blue-600 rounded-full border-t-transparent border-r-transparent animate-spin"></div>
        </div>
        
        {/* Loading Text */}
        <p className="text-white text-xl font-semibold">Loading...</p>
      </div>
    </div>
  );
};

export default LoadingScreen;
