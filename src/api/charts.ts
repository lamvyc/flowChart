import axios, { AxiosResponse } from 'axios';

// Base URL of the Flask backend
const BASE_URL = 'http://localhost:5000/api/charts';

export interface ChartMeta {
  id: number;
  name: string;
  created_at: string;
}

export interface Chart extends ChartMeta {
  data: any;
}

export function getCharts() {
  return axios
    .get<ChartMeta[]>(BASE_URL)
    .then((res: AxiosResponse<ChartMeta[]>) => res.data);
}

export function getChart(id: number) {
  return axios
    .get<Chart>(`${BASE_URL}/${id}`)
    .then((res: AxiosResponse<Chart>) => res.data);
}

export function createChart(payload: { name: string; data: any }) {
  return axios
    .post<{ id: number }>(BASE_URL, payload)
    .then((res: AxiosResponse<{ id: number }>) => res.data);
}

export function updateChart(id: number, payload: { name?: string; data: any }) {
  return axios
    .put(`${BASE_URL}/${id}`, payload)
    .then((res: AxiosResponse<any>) => res.data);
}

export function deleteChart(id: number) {
  return axios
    .delete(`${BASE_URL}/${id}`)
    .then((res: AxiosResponse<any>) => res.data);
} 