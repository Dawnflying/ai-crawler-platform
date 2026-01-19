import request from '@/utils/request';
import { Crawler, CrawlerCreate, CrawlerUpdate, CrawlerListQuery } from '@/types';

export const crawlerApi = {
  // Get crawler list
  list: (params?: CrawlerListQuery) => {
    return request.get<any, Crawler[]>('/crawlers', { params });
  },

  // Get crawler by id
  get: (id: number) => {
    return request.get<any, Crawler>(`/crawlers/${id}`);
  },

  // Create crawler
  create: (data: CrawlerCreate) => {
    return request.post<any, Crawler>('/crawlers', data);
  },

  // Update crawler
  update: (id: number, data: CrawlerUpdate) => {
    return request.put<any, Crawler>(`/crawlers/${id}`, data);
  },

  // Delete crawler
  delete: (id: number) => {
    return request.delete<any, void>(`/crawlers/${id}`);
  },

  // Get crawler config history
  getHistory: (id: number) => {
    return request.get<any, any[]>(`/crawlers/${id}/history`);
  },
};
