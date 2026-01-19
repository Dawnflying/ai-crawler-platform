import request from '@/utils/request';
import { Task, TaskCreate, TaskLog, TaskListQuery } from '@/types';

export const taskApi = {
  // Get task list
  list: (params?: TaskListQuery) => {
    return request.get<any, Task[]>('/tasks', { params });
  },

  // Get task by id
  get: (id: number) => {
    return request.get<any, Task>(`/tasks/${id}`);
  },

  // Create task
  create: (data: TaskCreate) => {
    return request.post<any, Task>('/tasks', data);
  },

  // Update task
  update: (id: number, data: Partial<Task>) => {
    return request.put<any, Task>(`/tasks/${id}`, data);
  },

  // Delete task
  delete: (id: number) => {
    return request.delete<any, void>(`/tasks/${id}`);
  },

  // Get task logs
  getLogs: (id: number, params?: { level?: string; page?: number; page_size?: number }) => {
    return request.get<any, TaskLog[]>(`/tasks/${id}/logs`, { params });
  },

  // Cancel task
  cancel: (id: number) => {
    return request.post<any, { message: string }>(`/tasks/${id}/cancel`);
  },

  // Execute task
  execute: (id: number) => {
    return request.post<any, { message: string; total_items: number; success_items: number; failed_items: number }>(`/tasks/${id}/execute`);
  },
};
