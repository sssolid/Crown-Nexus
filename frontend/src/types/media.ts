// src/types/media.ts
export interface Media {
  id: string;
  filename: string;
  url: string;
  thumbnail_url?: string;
  file_type: string;
  size: number;
  media_type: string;
  alt_text?: string;
  description?: string;
  product?: any;
  created_at: string;
  updated_at: string;
}
