import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { useTheme } from './ThemeProvider';
import { Moon, Sun, FlaskConical } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface LoginPageProps {
  onLogin: () => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { theme, toggleTheme } = useTheme();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onLogin();
  };

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-blue-50 to-teal-50 dark:from-slate-900 dark:to-slate-800">
      {/* Left Side - Login Form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <div className="bg-white dark:bg-slate-800 rounded-3xl shadow-2xl p-8 space-y-8">
            {/* Logo and Header */}
            <div className="text-center space-y-3">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-teal-500 mb-4">
                <FlaskConical className="w-8 h-8 text-white" />
              </div>
              <h1 className="text-slate-900 dark:text-white">
                Chemical Equipment Monitor
              </h1>
              <p className="text-slate-600 dark:text-slate-400">
                Sign in to access your dashboard
              </p>
            </div>

            {/* Login Form */}
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="email" className="text-slate-700 dark:text-slate-300">
                  Email Address
                </Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="engineer@chemlab.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="h-12 bg-slate-50 dark:bg-slate-700 border-slate-200 dark:border-slate-600"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password" className="text-slate-700 dark:text-slate-300">
                  Password
                </Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="h-12 bg-slate-50 dark:bg-slate-700 border-slate-200 dark:border-slate-600"
                  required
                />
              </div>

              <Button 
                type="submit" 
                className="w-full h-12 bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white"
              >
                Sign In
              </Button>
            </form>

            {/* Footer */}
            <p className="text-center text-slate-500 dark:text-slate-400">
              Demo credentials: Any email/password
            </p>
          </div>
        </div>
      </div>

      {/* Right Side - Illustration */}
      <div className="hidden lg:flex flex-1 items-center justify-center p-8 bg-gradient-to-br from-blue-500 to-teal-500 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-20 w-64 h-64 rounded-full bg-white blur-3xl"></div>
          <div className="absolute bottom-20 right-20 w-96 h-96 rounded-full bg-white blur-3xl"></div>
        </div>
        
        <div className="relative z-10 text-center text-white space-y-6 max-w-lg">
          <div className="inline-flex items-center justify-center w-32 h-32 rounded-3xl bg-white/20 backdrop-blur-lg mb-6">
            <FlaskConical className="w-16 h-16 text-white" />
          </div>
          <h2 className="text-white">
            Advanced Process Monitoring
          </h2>
          <p className="text-white/90">
            Real-time visualization and analysis of chemical equipment parameters. 
            Monitor flowrate, pressure, temperature, and performance metrics across your facility.
          </p>
          <div className="flex justify-center gap-8 pt-6">
            <div className="text-center">
              <div className="text-white/90">Equipment Tracked</div>
              <div className="text-white">500+</div>
            </div>
            <div className="text-center">
              <div className="text-white/90">Data Points/Day</div>
              <div className="text-white">10K+</div>
            </div>
            <div className="text-center">
              <div className="text-white/90">Facilities</div>
              <div className="text-white">15</div>
            </div>
          </div>
        </div>
      </div>

      {/* Theme Toggle */}
      <button
        onClick={toggleTheme}
        className="fixed top-6 right-6 p-3 rounded-full bg-white dark:bg-slate-800 shadow-lg hover:shadow-xl transition-shadow"
      >
        {theme === 'light' ? (
          <Moon className="w-5 h-5 text-slate-700" />
        ) : (
          <Sun className="w-5 h-5 text-amber-400" />
        )}
      </button>
    </div>
  );
}
