import { AnimatePresence, motion } from 'framer-motion'
import { Heart, Home, Search, User } from 'lucide-react'
import { NavLink, useLocation, useNavigate, useOutlet } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Button } from './ui/Button'

const nav = [
	{ to: '/', label: 'Home', icon: Home },
	{ to: '/vault-search', label: 'Search', icon: Search },
	{ to: '/favorites', label: 'Favorites', icon: Heart },
	{ to: '/profile', label: 'Profile', icon: User },
]

const pageVariants = {
	initial: { opacity: 0, scale: 0.99 },
	in: { opacity: 1, y: 0, scale: 1 },
	out: { opacity: 0, scale: 1.01 },
}

const pageTransition = {
	type: 'tween',
	ease: 'circOut',
	duration: 0.17,
}

export default function Layout() {
	const { logout } = useAuth()
	const navigate = useNavigate()
	const location = useLocation()
	const currentOutlet = useOutlet()

	const handleLogout = () => {
		logout()
		navigate('/login', { replace: true })
	}

	return (
		<div className='flex min-h-screen flex-col bg-slate-900 text-white'>
			<main className='flex-1 overflow-x-hidden pb-20 pt-safe-area-inset-top'>
				<AnimatePresence mode='wait' initial={false}>
					<motion.div
						key={location.pathname}
						initial='initial'
						animate='in'
						exit='out'
						variants={pageVariants}
						transition={pageTransition}
						className='h-full py-4 page-container'
					>
						{currentOutlet}
					</motion.div>
				</AnimatePresence>
			</main>

			<nav
				className='fixed bottom-0 left-0 right-0 z-50 border-t border-slate-700/60 bg-slate-900/95 backdrop-blur-md pb-safe-area-inset-bottom'
				role='navigation'
			>
				<div className='flex justify-around py-2'>
					{nav.map(({ to, label, icon: Icon }) => (
						<NavLink
							key={to}
							to={to}
							end={to === '/'}
							className={({ isActive }) =>
								`flex min-h-[44px] min-w-[44px] touch-manipulation flex-col items-center justify-center gap-0.5 rounded-xl px-3 py-2 text-[10px] font-medium transition-all ${
									isActive
										? 'text-emerald-400 bg-emerald-500/10'
										: 'text-slate-500 hover:text-slate-300'
								}`
							}
						>
							<Icon className='h-5 w-5 mb-0.5' strokeWidth={2} />
							<span>{label}</span>
						</NavLink>
					))}
				</div>
			</nav>

			<div className='fixed right-4 top-4 z-40'>
				<Button
					variant='ghost'
					size='sm'
					onClick={handleLogout}
					className='text-slate-400 hover:text-white hover:bg-white/5'
				>
					Log out
				</Button>
			</div>
		</div>
	)
}
