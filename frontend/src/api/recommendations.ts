import { apiClient } from "./client";

export interface TechnologyNested {
  id: string;
  name: string;
}

export interface SkillLevelNested {
  id: string;
  name: string;
}

export interface MentorNested {
  id: string;
  first_name: string;
  last_name: string;
  role: string;
  avatar_url: string | null;
}

export interface Resource {
  id: string;
  uploader_id: string;
  title: string;
  description: string | null;
  file_path: string;
  resource_type: "doc" | "blueprint" | "snippet";
  technology_id: string | null;
  mentor_id: string | null;
  team_id: string | null;
  skill_level_id: string | null;
  average_rating: string;
  ratings_count: number;
  created_at: string;
  updated_at: string;
  meta: Record<string, unknown> | null;
  technology?: TechnologyNested | null;
  skill_level?: SkillLevelNested | null;
  mentor?: MentorNested | null;
  is_favorite?: boolean;
  user_rating?: number | null;
}

export async function fetchRecommendations(): Promise<Resource[]> {
  const { data } = await apiClient.get<Resource[]>("/recommendations");
  return data;
}
