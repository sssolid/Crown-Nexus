// src/types/user.ts
export enum UserRole {
  ADMIN = 'admin',
  MANAGER = 'manager',
  CLIENT = 'client',
  DISTRIBUTOR = 'distributor',
  READ_ONLY = 'read_only'
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_admin: boolean;
  role: UserRole;
  created_at: string;
  company?: {
    id: string;
    name: string;
    account_number: string;
    account_type: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
  };
}
