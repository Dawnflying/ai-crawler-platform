// User types
export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  avatar_url?: string;
  role_id?: number;
  status: string;
  created_at: string;
  updated_at: string;
  last_login_at?: string;
  role_name?: string;
  role_display_name?: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

// Crawler types
export interface Crawler {
  id: number;
  name: string;
  description?: string;
  type: 'http' | 'api' | 'browser';
  status: 'active' | 'inactive' | 'error';
  config: Record<string, any>;
  tags?: string[];
  created_by?: number;
  created_at: string;
  updated_at: string;
  version: number;
  is_template: boolean;
  template_category?: string;
  creator_name?: string;
  task_count?: number;
  last_execution?: string;
}

export interface CrawlerCreate {
  name: string;
  description?: string;
  type: 'http' | 'api' | 'browser';
  config: Record<string, any>;
  tags?: string[];
  is_template?: boolean;
  template_category?: string;
}

export interface CrawlerUpdate {
  name?: string;
  description?: string;
  status?: 'active' | 'inactive' | 'error';
  config?: Record<string, any>;
  tags?: string[];
  change_note?: string;
}

// Task types
export interface Task {
  id: number;
  crawler_id: number;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  schedule_type: 'manual' | 'cron' | 'once';
  cron_expression?: string;
  execute_at?: string;
  started_at?: string;
  completed_at?: string;
  duration?: number;
  total_items: number;
  success_items: number;
  failed_items: number;
  error_message?: string;
  config_overrides?: Record<string, any>;
  created_by?: number;
  created_at: string;
  updated_at: string;
  crawler_name?: string;
  creator_name?: string;
}

export interface TaskCreate {
  crawler_id: number;
  name: string;
  schedule_type?: 'manual' | 'cron' | 'once';
  cron_expression?: string;
  execute_at?: string;
  config_overrides?: Record<string, any>;
}

export interface TaskLog {
  id: number;
  task_id: number;
  level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR';
  message: string;
  details?: Record<string, any>;
  created_at: string;
}

// API response types
export interface ApiResponse<T = any> {
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

// Query params
export interface ListQuery {
  page?: number;
  page_size?: number;
  search?: string;
}

export interface CrawlerListQuery extends ListQuery {
  type?: string;
  status?: string;
  is_template?: boolean;
}

export interface TaskListQuery extends ListQuery {
  crawler_id?: number;
  status?: string;
  schedule_type?: string;
}
