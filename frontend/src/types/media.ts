// src/types/media.ts
export interface Media {
  id: string;
  filename: string;
  url: string;
  thumbnail_url?: string;
  mime_type: string;
  file_size: number;
  media_type: string;
  alt_text?: string;
  description?: string;
  product?: any;
  created_at: string;
  updated_at: string;
}
