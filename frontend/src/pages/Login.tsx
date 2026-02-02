import { motion } from 'framer-motion'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import type { TelegramUser } from 'react-telegram-login'
import TelegramLoginButton from 'react-telegram-login'
import { loginWithTelegram } from '../api/auth'
import { useAuth } from '../contexts/AuthContext'

const TELEGRAM_BOT_USERNAME = import.meta.env.VITE_TELEGRAM_BOT_USERNAME

export default function Login() {
	const navigate = useNavigate()
	const { login } = useAuth()
	const [error, setError] = useState<string | null>(null)
	const [loading, setLoading] = useState(false)

	const handleTelegramAuth = async (tgUser: TelegramUser) => {
		setError(null)
		setLoading(true)
		try {
			const res = await loginWithTelegram(tgUser)
			login(res.access_token, res.user)
			navigate('/', { replace: true })
		} catch (e: unknown) {
			const message =
				e && typeof e === 'object' && 'response' in e
					? (e as { response?: { data?: { detail?: string } } }).response?.data
							?.detail ?? 'Login failed'
					: 'Login failed'
			setError(message)
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className='min-h-screen flex flex-col items-center justify-center bg-slate-900 px-4 pt-safe-area-inset-top pb-safe-area-inset-bottom'>
			<motion.div
				initial={{ opacity: 0, y: 16 }}
				animate={{ opacity: 1, y: 0 }}
				transition={{ duration: 0.4 }}
				className='flex flex-col items-center max-w-xs w-full'
			>
				<div className='mb-8 flex h-16 w-16 items-center justify-center rounded-2xl bg-slate-800/80 border border-slate-600/40 shadow-xl'>
					<span className='text-2xl font-bold text-emerald-400'>TV</span>
				</div>
				<h1 className='text-xl font-semibold text-slate-100 mb-1'>TechVault</h1>
				<p className='text-slate-400 text-sm text-center mb-8'>
					Corporate Knowledge Sharing
				</p>

				{error && (
					<motion.p
						initial={{ opacity: 0 }}
						animate={{ opacity: 1 }}
						className='mb-4 w-full rounded-xl border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-300'
						role='alert'
					>
						{error}
					</motion.p>
				)}

				{loading ? (
					<p className='text-slate-400 text-sm'>Logging in…</p>
				) : (
					<div className='[&_.telegram-login]:!block w-full flex justify-center'>
						<TelegramLoginButton
							dataOnauth={handleTelegramAuth}
							botName={TELEGRAM_BOT_USERNAME}
						/>
					</div>
				)}

				<p className='mt-6 text-slate-500 text-xs text-center'>
					Use your Telegram account to access the vault.
				</p>
			</motion.div>
		</div>
	)
}
