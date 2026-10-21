"use client";
/**
 * useUser() — the logged-in user (or null). Updates on login/logout.
 * "ready" is false until we've checked the browser, so pages don't flash the wrong thing.
 */
import { useEffect, useState } from "react";
import { getSavedUser, getToken } from "./auth";
import type { User } from "./types";

export function useUser() {
  const [user, setUser] = useState<User | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const update = () => {
      setUser(getToken() ? getSavedUser() : null);
      setReady(true);
    };
    update();
    window.addEventListener("auth-change", update);
    return () => window.removeEventListener("auth-change", update);
  }, []);

  return { user, ready };
}
