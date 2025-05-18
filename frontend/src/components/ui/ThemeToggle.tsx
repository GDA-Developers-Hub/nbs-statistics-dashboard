import { Moon, Sun } from "lucide-react";
import { motion } from "framer-motion";
import { useTheme } from "@/lib/themeContext";
import { Button } from "./button";

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={toggleTheme}
      className="relative h-8 w-8 rounded-full"
      aria-label="Toggle theme"
    >
      <motion.div
        initial={{ opacity: 0, rotate: -90 }}
        animate={{ 
          opacity: theme === 'dark' ? 1 : 0,
          rotate: theme === 'dark' ? 0 : 90,
          scale: theme === 'dark' ? 1 : 0.5,
        }}
        transition={{ duration: 0.3 }}
        className="absolute"
      >
        <Moon className="h-4 w-4 text-yellow-300" />
      </motion.div>
      
      <motion.div
        initial={{ opacity: 0, rotate: 90 }}
        animate={{ 
          opacity: theme === 'light' ? 1 : 0,
          rotate: theme === 'light' ? 0 : -90,
          scale: theme === 'light' ? 1 : 0.5,
        }}
        transition={{ duration: 0.3 }}
        className="absolute"
      >
        <Sun className="h-4 w-4 text-yellow-500" />
      </motion.div>
    </Button>
  );
} 