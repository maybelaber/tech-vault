import { ArrowLeft, ExternalLink, Heart } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { toggleFavorite } from '../api/favorites'
import {
	fetchSkillLevels,
	fetchTechnologies,
	type SkillLevel,
	type Technology,
} from '../api/reference'
import {
	fetchResource,
	rateResource,
	type MentorNested,
	type Resource,
} from '../api/resources'
import { Badge } from '../components/ui/Badge'
import { Button } from '../components/ui/Button'
import { StarRating } from '../components/resources/StarRating'

function mentorAvatarUrl(mentor: MentorNested): string {
	const url = mentor.avatar_url ?? null
	if (url) return url
	const name = `${mentor.first_name} ${mentor.last_name}`.trim() || 'Mentor'
	return `https://ui-avatars.com/api/?name=${encodeURIComponent(
		name
	)}&background=random&size=128`
}

function mentorDisplayName(mentor: MentorNested): string {
	return `${mentor.first_name} ${mentor.last_name}`.trim() || 'Mentor'
}

export default function ResourceDetails() {
	const { id } = useParams<{ id: string }>()
	const navigate = useNavigate()
	const [resource, setResource] = useState<Resource | null>(null)
	const [technologyName, setTechnologyName] = useState<string>('—')
	const [skillLevelName, setSkillLevelName] = useState<string>('—')
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState<string | null>(null)
	const [liked, setLiked] = useState(false)

	useEffect(() => {
		if (!id) {
			setError('Missing resource id')
			setLoading(false)
			return
		}
		let cancelled = false
		;(async () => {
			try {
				setLoading(true)
				setError(null)
				const [res, techs, levels] = await Promise.all([
					fetchResource(id),
					fetchTechnologies(),
					fetchSkillLevels(),
				])
				if (cancelled) return
				setResource(res)
				setLiked(Boolean(res.is_favorite))
				if (res.technology_id) {
					const t = techs.find((x: Technology) => x.id === res.technology_id)
					if (t) setTechnologyName(t.name)
				}
				if (res.skill_level_id) {
					const s = levels.find((x: SkillLevel) => x.id === res.skill_level_id)
					if (s) setSkillLevelName(s.name)
				}
			} catch (e) {
				if (!cancelled) {
					setError(e instanceof Error ? e.message : 'Failed to load resource')
					setResource(null)
				}
			} finally {
				if (!cancelled) setLoading(false)
			}
		})()

		return () => {
			cancelled = true
		}
	}, [id])

	if (loading) {
		return (
			<div className='py-6 flex items-center justify-center min-h-[40vh]'>
				<div className='text-slate-400'>Loading…</div>
			</div>
		)
	}

	if (error || !resource) {
		return (
			<div className='py-6'>
				<p className='text-red-400'>{error ?? 'Resource not found'}</p>
				<Button variant='ghost' className='mt-4' onClick={() => navigate(-1)}>
					<ArrowLeft className='h-4 w-4 mr-2' />
					Back
				</Button>
			</div>
		)
	}

	const typeLabel =
		resource.resource_type === 'blueprint'
			? 'Blueprint'
			: resource.resource_type === 'snippet'
			? 'Snippet'
			: 'Doc'

	// Backend origin for static files (e.g. /demo/file.md); avoid using frontend origin (port 3000)
	const backendOrigin = (() => {
		const url = import.meta.env.VITE_API_URL
		if (url) return url.replace(/\/api\/?$/, '')
		return 'http://localhost:8000'
	})()

	const fileUrl =
		resource.file_path.startsWith('http') || resource.file_path.startsWith('//')
			? resource.file_path
			: resource.file_path.startsWith('/')
			? `${backendOrigin}${resource.file_path}`
			: resource.file_path

	return (
		<div className='py-6'>
			<header className='flex items-start justify-between gap-4 mb-6'>
				<Button
					variant='ghost'
					size='icon'
					className='shrink-0 -ml-1'
					onClick={() => navigate(-1)}
					aria-label='Back'
				>
					<ArrowLeft className='h-5 w-5' />
				</Button>
				<h1 className='text-xl font-semibold text-slate-100 flex-1 min-w-0 line-clamp-2'>
					{resource.title}
				</h1>
				<a
					href={fileUrl}
					target='_blank'
					rel='noopener noreferrer'
					className='shrink-0'
				>
					<Button variant='secondary' size='sm'>
						<ExternalLink className='h-4 w-4 mr-1.5' />
						Open link
					</Button>
				</a>
			</header>

			<div className='flex flex-wrap gap-2 mb-6'>
				<Badge variant='tech'>{technologyName}</Badge>
				<Badge variant='level'>{skillLevelName}</Badge>
				<Badge variant='outline' className='capitalize'>
					{typeLabel}
				</Badge>
			</div>

			<section className='mb-6 rounded-xl border border-white/10 bg-slate-800/40 p-4 shadow-lg'>
				<p className='text-xs text-slate-500 uppercase tracking-wider mb-3'>
					Recommended by
				</p>
				{resource.mentor ? (
					<div className='flex flex-col sm:flex-row sm:items-center gap-4'>
						<div className='flex items-center gap-4 flex-1 min-w-0'>
							<img
								src={mentorAvatarUrl(resource.mentor)}
								alt=''
								className='h-14 w-14 rounded-full border-2 border-slate-600/50 object-cover shrink-0'
							/>
							<div className='min-w-0'>
								<p className='font-semibold text-slate-100 truncate'>
									{mentorDisplayName(resource.mentor)}
								</p>
								<p className='text-sm text-slate-400 mt-0.5'>
									{resource.mentor.role}
								</p>
							</div>
						</div>
					</div>
				) : (
					<p className='text-slate-500 text-sm'>—</p>
				)}
			</section>

			{resource.description && (
				<section className='mb-6'>
					<h2 className='text-sm font-semibold text-slate-200 mb-2'>
						Description
					</h2>
					<p className='text-sm text-slate-400 leading-relaxed whitespace-pre-wrap'>
						{resource.description}
					</p>
				</section>
			)}

			<div className='mb-6'>
				<StarRating
					value={resource.user_rating ?? null}
					average={Number(resource.average_rating)}
					ratingsCount={resource.ratings_count}
					onRate={async (star) => {
						if (!id || !resource) return
						const prevRating = resource.user_rating ?? null
						setResource((r: Resource | null) => (r ? { ...r, user_rating: star } : null))
						try {
							const res = await rateResource(id, star)
							setResource((r: Resource | null) =>
								r
									? {
											...r,
											user_rating: res.user_rating,
											average_rating: res.average_rating,
											ratings_count: res.ratings_count,
										}
									: null
							)
						} catch (err) {
							setResource((r: Resource | null) =>
								r ? { ...r, user_rating: prevRating ?? undefined } : null
							)
							console.error('Failed to rate', err)
						}
					}}
				/>
			</div>

			<div className='flex flex-col sm:flex-row gap-3'>
				<a
					href={fileUrl}
					target='_blank'
					rel='noopener noreferrer'
					className='flex-1'
				>
					<Button variant='primary' className='w-full' size='lg'>
						<ExternalLink className='h-4 w-4 mr-2' />
						Open Resource
					</Button>
				</a>
				<Button
					variant={liked ? 'primary' : 'outline'}
					size='lg'
					className='shrink-0'
					onClick={async () => {
						if (!id) return
						const previousLiked = liked
						setLiked(!liked)
						try {
							const res = await toggleFavorite(id)
							if (res.is_favorite !== !previousLiked) {
								setLiked(res.is_favorite)
							}
						} catch (error) {
							setLiked(previousLiked)
							console.error('Failed to toggle like', error)
						}
					}}
					aria-pressed={liked}
				>
					<Heart
						className={`h-4 w-4 mr-2 ${liked ? 'fill-current' : ''}`}
						aria-hidden
					/>
					{liked ? 'Liked' : 'Like'}
				</Button>
			</div>
		</div>
	)
}
