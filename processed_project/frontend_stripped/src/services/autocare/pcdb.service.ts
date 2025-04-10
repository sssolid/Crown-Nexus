import{ApiService}from '../api';import{Category,SubCategory,Part,PartDetail,PartSearchParams,PartSearchResponse,Position,PCdbStats}from '@/types';export class PCdbService extends ApiService{private readonly baseUrl='/autocare/pcdb';async getVersion():Promise<string>{return this.get<string>(`${this.baseUrl}/version`);}async getStats():Promise<PCdbStats>{return this.get<PCdbStats>(`${this.baseUrl}/stats`);}async getCategories():Promise<Category[]>{return this.get<Category[]>(`${this.baseUrl}/categories`);}async getSubcategoriesByCategory(categoryId:number):Promise<SubCategory[]>{return this.get<SubCategory[]>(`${this.baseUrl}/categories/${categoryId}/subcategories`);}async searchParts(params:PartSearchParams):Promise<PartSearchResponse>{return this.get<PartSearchResponse>(`${this.baseUrl}/parts/search${this.buildQueryParams(params)}`);}async getPartDetails(partTerminologyId:number):Promise<PartDetail>{return this.get<PartDetail>(`${this.baseUrl}/parts/${partTerminologyId}`);}async getPartsByCategory(categoryId:number,page:number=1,pageSize:number=20):Promise<PartSearchResponse>{return this.get<PartSearchResponse>(`${this.baseUrl}/categories/${categoryId}/parts${this.buildQueryParams({ page, page_size: pageSize })}`);}async searchCategories(searchTerm:string):Promise<Category[]>{return this.get<Category[]>(`${this.baseUrl}/categories/search${this.buildQueryParams({ search_term: searchTerm })}`);}async getPositions():Promise<Position[]>{return this.get<Position[]>(`${this.baseUrl}/positions`);}async getPositionsByPart(partTerminologyId:number):Promise<Position[]>{return this.get<Position[]>(`${this.baseUrl}/parts/${partTerminologyId}/positions`);}async getPartSupersessions(partTerminologyId:number):Promise<{superseded_by:Part[];supersedes:Part[]}>{return this.get<{superseded_by:Part[];supersedes:Part[]}>(`${this.baseUrl}/parts/${partTerminologyId}/supersessions`);}}export const pcdbService=new PCdbService();export default pcdbService;