import api,{ApiService}from '@/services/api';import{Brand,BrandCreateDTO,BrandUpdateDTO,Product,ProductCreateDTO,ProductDescriptionCreateDTO,ProductDescriptionUpdateDTO,ProductFilters,ProductListResponse,ProductMarketingCreateDTO,ProductMarketingUpdateDTO,ProductMeasurementCreateDTO,ProductStockCreateDTO,ProductStockUpdateDTO,ProductSupersessionCreateDTO,ProductUpdateDTO}from '@/types/product';export class ProductService extends ApiService{async getProducts(filters?:ProductFilters):Promise<ProductListResponse>{return api.get<ProductListResponse>('/products/',{params:filters});}async getProduct(id:string):Promise<Product>{return api.get<Product>(`/products/${id}`);}async createProduct(product:ProductCreateDTO):Promise<Product>{return api.post<Product>('/products',product);}async updateProduct(id:string,product:ProductUpdateDTO):Promise<Product>{return api.put<Product>(`/products/${id}`,product);}async deleteProduct(id:string):Promise<{message:string}>{return api.delete<{message:string}>(`/products/${id}`);}async addProductDescription(productId:string,description:ProductDescriptionCreateDTO):Promise<any>{return api.post<any>(`/products/${productId}/descriptions`,description);}async updateProductDescription(productId:string,descriptionId:string,description:ProductDescriptionUpdateDTO):Promise<any>{return api.put<any>(`/products/${productId}/descriptions/${descriptionId}`,description);}async deleteProductDescription(productId:string,descriptionId:string):Promise<{message:string}>{return api.delete<{message:string}>(`/products/${productId}/descriptions/${descriptionId}`);}async addProductMarketing(productId:string,marketing:ProductMarketingCreateDTO):Promise<any>{return api.post<any>(`/products/${productId}/marketing`,marketing);}async updateProductMarketing(productId:string,marketingId:string,marketing:ProductMarketingUpdateDTO):Promise<any>{return api.put<any>(`/products/${productId}/marketing/${marketingId}`,marketing);}async deleteProductMarketing(productId:string,marketingId:string):Promise<{message:string}>{return api.delete<{message:string}>(`/products/${productId}/marketing/${marketingId}`);}async addProductMeasurement(productId:string,measurement:ProductMeasurementCreateDTO):Promise<any>{return api.post<any>(`/products/${productId}/measurements`,measurement);}async addProductStock(productId:string,stock:ProductStockCreateDTO):Promise<any>{return api.post<any>(`/products/${productId}/stock`,stock);}async updateProductStock(productId:string,stockId:string,stock:ProductStockUpdateDTO):Promise<any>{return api.put<any>(`/products/${productId}/stock/${stockId}`,stock);}async createProductSupersession(productId:string,supersession:ProductSupersessionCreateDTO):Promise<any>{return api.post<any>(`/products/${productId}/supersessions`,supersession);}async deleteProductSupersession(productId:string,supersessionId:string):Promise<{message:string}>{return api.delete<{message:string}>(`/products/${productId}/supersessions/${supersessionId}`);}async getBrands():Promise<Brand[]>{return api.get<Brand[]>('/products/brands/');}async getBrand(id:string):Promise<Brand>{return api.get<Brand>(`/products/brands/${id}`);}async createBrand(brand:BrandCreateDTO):Promise<Brand>{return api.post<Brand>('/products/brands/',brand);}async updateBrand(id:string,brand:BrandUpdateDTO):Promise<Brand>{return api.put<Brand>(`/products/brands/${id}`,brand);}async deleteBrand(id:string):Promise<{message:string}>{return api.delete<{message:string}>(`/products/brands/${id}`);}}export const productService=new ProductService();export default productService;