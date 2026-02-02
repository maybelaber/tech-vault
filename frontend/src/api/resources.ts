import { apiClient } from "./client";
import type { Resource, MentorNested } from "./recommendations";

export type { Resource, MentorNested };

export async function fetchResources(params: { search?: string; limit?: number } = {}): Promise<Resource[]> {
  const query: Record<string, string | number> = {};
  if (params.search?.trim()) query.search = params.search.trim();
  if (params.limit != null) query.limit = params.limit;
  const { data } = await apiClient.get<Resource[]>("/resources", { params: query });
  return data;
}

export async function fetchResource(id: string): Promise<Resource> {
  const { data } = await apiClient.get<Resource>(`/resources/${id}`);
  return data;
}

export interface RateResponse {
  average_rating: string;
  ratings_count: number;
  user_rating: number;
}

export async function rateResource(resourceId: string, value: number): Promise<RateResponse> {
  const { data } = await apiClient.post<RateResponse>(`/resources/${resourceId}/rate`, {
    value,
  });
  return data;
}
