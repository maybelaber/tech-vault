import { apiClient } from "./client";

export interface Mentor {
  id: string;
  name: string;
  email: string | null;
  created_at: string;
}

export async function fetchMentors(): Promise<Mentor[]> {
  const { data } = await apiClient.get<Mentor[]>("/reference/mentors");
  return data;
}
