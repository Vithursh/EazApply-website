import { createBrowserClient } from '@supabase/ssr';

export function createBrowserSupabase() {
  return createBrowserClient(
    import.meta.env.VITE_SUPABASE_URL!,
    import.meta.env.VITE_SUPABASE_ANON_KEY!,
  );
}