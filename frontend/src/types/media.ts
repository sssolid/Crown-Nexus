// src/types/media.ts
export interface Media {
  id: string;
  filename: string;
  url: string;
  thumbnail_url?: string;
  file_type: string;
  size: number;
  product_id?: string;
  created_at: string;
  updated_at: string;
}
