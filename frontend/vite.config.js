import react from '@vitejs/plugin-react'
import path from 'path'
import { defineConfig, loadEnv } from 'vite'
export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, process.cwd(), '')

	const target =
		env.VITE_API_URL && env.VITE_API_URL.startsWith('http')
			? env.VITE_API_URL
			: 'http://backend:8000'

	return {
		plugins: [react()],
		resolve: {
			alias: {
				'@': path.resolve(__dirname, './src'),
			},
		},
		server: {
			host: true,
			port: 3000,
			strictPort: true,
			watch: {
				usePolling: true,
			},
			allowedHosts: true,
			proxy: {
				'/api': {
					target: target,
					changeOrigin: true,
					secure: false,
				},
				'/demo': {
					target: target,
					changeOrigin: true,
					secure: false,
				},
			},
		},
		build: {
			outDir: 'dist',
		},
	}
})
