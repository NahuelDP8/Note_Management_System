export interface Note {
  id: number;
  title: string;
  content: string;
  is_archived: boolean;
  created_at?: string;
  updated_at?: string;
}
