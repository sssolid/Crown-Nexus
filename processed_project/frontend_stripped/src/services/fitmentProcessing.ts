import api,{ApiService}from '@/services/api';export interface FitmentValidationResult{status:string;message:string;original_text:string;suggestions:string[];fitment?:{vehicle:{year:number;make:string;model:string;submodel?:string;engine?:string;transmission?:string;attributes:Record<string,any>;};positions:{front_rear:string;left_right:string;upper_lower:string;inner_outer:string;};vcdb_vehicle_id?:number;pcdb_position_ids?:number[];};}export interface ProcessFitmentResponse{results:Record<string,FitmentValidationResult[]>;valid_count:number;warning_count:number;error_count:number;}export class FitmentProcessingService extends ApiService{async processApplications(applicationTexts:string[],partTerminologyId:number,productId?:string):Promise<ProcessFitmentResponse>{return api.post<ProcessFitmentResponse>('/fitment/process',{application_texts:applicationTexts,part_terminology_id:partTerminologyId,product_id:productId});}async parseApplication(applicationText:string):Promise<{raw_text:string;year_range?:[number,number];vehicle_text?:string;position_text?:string;additional_notes?:string;}>{return api.post<any>('/fitment/parse-application',{application_text:applicationText});}async getPcdbPositions(terminologyId:number):Promise<Array<{id:number;name:string;front_rear?:string;left_right?:string;upper_lower?:string;inner_outer?:string;}>>{return api.get<any[]>(`/fitment/pcdb-positions/${terminologyId}`);}}export const fitmentProcessingService=new FitmentProcessingService();export default fitmentProcessingService;