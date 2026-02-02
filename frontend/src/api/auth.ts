import { apiClient } from "./client.js";

export interface TelegramWidgetUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  photo_url?: string;
  auth_date: number;
  hash: string;
}

export interface TelegramAuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    telegram_id: number;
    username: string | null;
    first_name: string | null;
    last_name: string | null;
    team_id: string | null;
    skill_level_id: string | null;
    created_at: string;
    updated_at: string;
  };
}

export async function loginWithTelegram(
  telegramUser: TelegramWidgetUser
): Promise<TelegramAuthResponse> {
  const { data } = await apiClient.post<TelegramAuthResponse>(
    "/auth/telegram",
    telegramUser
  );
  return data;
}

/** Local dev only: login without Telegram widget. Backend must have ALLOW_DEV_LOGIN=true. */
export async function devLogin(payload: {
  telegram_id: number;
  first_name?: string;
  username?: string | null;
}): Promise<TelegramAuthResponse> {
  const { data } = await apiClient.post<TelegramAuthResponse>(
    "/auth/dev-login",
    payload
  );
  return data;
}
