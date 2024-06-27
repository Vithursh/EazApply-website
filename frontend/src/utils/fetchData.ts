import { supabase } from './supabaseClient';

export const fetchData = async (tableName: string): Promise<any[] | null> => {
  const { data, error } = await supabase
    .from(tableName)
    .select('*');

  if (error) {
    console.error('Error fetching data:', error);
    return null;
  }

  return data;
};