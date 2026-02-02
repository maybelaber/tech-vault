import { apiClient } from "./client";

export interface Technology {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
}

export interface SkillLevel {
  id: string;
  name: string;
  sort_order: number;
  created_at: string;
}

export async function fetchTechnologies(): Promise<Technology[]> {
  const { data } = await apiClient.get<Technology[]>("/reference/technologies");
  return data;
}

export async function fetchSkillLevels(): Promise<SkillLevel[]> {
  const { data } = await apiClient.get<SkillLevel[]>("/reference/skill-levels");
  return data;
}
