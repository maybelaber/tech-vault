import axios from 'axios'

const AUTH_TOKEN_KEY = 'techvault_access_token'

export const apiClient = axios.create({
	baseURL: import.meta.env.VITE_API_URL || '',
	withCredentials: true,
	headers: {
		'Content-Type': 'application/json',
	},
})

apiClient.interceptors.request.use((config) => {
	const token = localStorage.getItem(AUTH_TOKEN_KEY)
	if (token) {
		config.headers.Authorization = `Bearer ${token}`
	}
	return config
})
