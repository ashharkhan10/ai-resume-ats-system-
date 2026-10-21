/**
 * Keeps the login token (and the user's name) in the browser.
 * Other components listen for the "auth-change" event to update themselves.
 */
import type { User } from "./types";

const TOKEN_KEY = "ats_token";
const USER_KEY = "ats_user";

export function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

export function getSavedUser(): User | null {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? (JSON.parse(raw) as User) : null;
  } catch {
    return null;
  }
}

export function saveLogin(token: string, user: User) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
  window.dispatchEvent(new Event("auth-change"));
}

export function logout() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  window.dispatchEvent(new Event("auth-change"));
}
