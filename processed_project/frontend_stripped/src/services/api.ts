import axios,{AxiosError,AxiosInstance,AxiosRequestConfig,AxiosResponse}from 'axios';import router from '@/router';export interface ApiResponse<T>{data:T;success:boolean;message?:string;}export interface ApiError{detail:string;status:number;title?:string;type?:string;}const apiConfig:AxiosRequestConfig={baseURL:'/api/v1',headers:{'Content-Type':'application/json','Accept':'application/json',},timeout:30000,};const apiClient:AxiosInstance=axios.create(apiConfig);apiClient.interceptors.request.use((config)=>{const token=localStorage.getItem('access_token');if(token){config.headers=config.headers||{};config.headers.Authorization=`Bearer ${token}`;}return config;},(error)=>{console.error('API request error:',error);return Promise.reject(error);});apiClient.interceptors.response.use((response)=>{return response;},async(error:AxiosError)=>{const originalRequest=error.config;if(!originalRequest){return Promise.reject(error);}if(error.response?.status===401){if(router.currentRoute.value.path!=='/login'){localStorage.removeItem('access_token');localStorage.setItem('redirectPath',router.currentRoute.value.fullPath);router.push('/login');return Promise.reject(error);}}if(error.response?.status===403){console.error('Permission denied:',error.response.data);}if(error.response?.status===404){console.error('Resource not found:',error.response.data);}if(error.response?.status===422){console.error('Validation error:',error.response.data);}if(error.response?.status===500){console.error('Server error:',error.response.data);}return Promise.reject(error);});const api={async get<T>(url:string,config?:AxiosRequestConfig):Promise<T>{try{const response:AxiosResponse<T>=await apiClient.get(url,config);return response.data;}catch(error){handleApiError(error);throw error;}},async post<T>(url:string,data?:any,config?:AxiosRequestConfig):Promise<T>{try{const response:AxiosResponse<T>=await apiClient.post(url,data,config);return response.data;}catch(error){handleApiError(error);throw error;}},async put<T>(url:string,data?:any,config?:AxiosRequestConfig):Promise<T>{try{const response:AxiosResponse<T>=await apiClient.put(url,data,config);return response.data;}catch(error){handleApiError(error);throw error;}},async delete<T>(url:string,config?:AxiosRequestConfig):Promise<T>{try{const response:AxiosResponse<T>=await apiClient.delete(url,config);return response.data;}catch(error){handleApiError(error);throw error;}},async uploadFile<T>(url:string,formData:FormData,config?:AxiosRequestConfig):Promise<T>{try{const defaultConfig:AxiosRequestConfig={headers:{'Content-Type':'multipart/form-data',},};const mergedConfig={...defaultConfig,...config};const response:AxiosResponse<T>=await apiClient.post(url,formData,mergedConfig);return response.data;}catch(error){handleApiError(error);throw error;}},client:apiClient,};function handleApiError(error:any):void{const errorResponse=error.response?.data;console.error('API Error:',{status:error.response?.status,url:error.config?.url,method:error.config?.method,data:errorResponse,});}export default api;