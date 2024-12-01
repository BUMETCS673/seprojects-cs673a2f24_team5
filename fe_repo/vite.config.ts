import {defineConfig} from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig(({command}) => {
  return {
    server: {
      port: 3001,
      open: true,
    },
    preview: {
      port: 8081,
      open: false,
    },
    plugins: [react()],
    define: {
      __CURRENT_URI__: JSON.stringify(command == 'serve' ? 'http://cvcoach.site' : 'http://localhost')
    }
  };
})
