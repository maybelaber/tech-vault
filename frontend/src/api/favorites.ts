import { apiClient } from "./client";
import type { Resource } from "./recommendations";

export interface ToggleFavoriteResponse {
  is_favorite: boolean;
}

export async function toggleFavorite(resourceId: string): Promise<ToggleFavoriteResponse> {
  const { data } = await apiClient.post<ToggleFavoriteResponse>(
    `/resources/${resourceId}/favorite`
  );
  return data;
}

export async function fetchFavorites(): Promise<Resource[]> {
  const { data } = await apiClient.get<Resource[]>("/favorites");
  return data;
}
