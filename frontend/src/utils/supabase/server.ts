import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export function createServerSupabase() {
  const cookieStore = cookies();
  return createServerClient(
    import.meta.env.VITE_SUPABASE_URL!,
    import.meta.env.VITE_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          // This may error in certain server contexts, but it's expected in middleware
          try {
            cookiesToSet.forEach(({ name, value, options }) => {
              cookieStore.set(name, value, options);
            });
          } catch (e) {
            // swallow or log
            console.error("Error setting auth cookies:", e);
          }
        },
      },
    }
  );
}