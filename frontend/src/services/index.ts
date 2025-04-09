// src/services/index.ts
/**
 * Export all services
 */

export { default as apiClient } from './api';
export { ApiService } from './api';

export { default as chatService, ChatService } from './chat';
export { default as fitmentService, FitmentService } from './fitment';
export { default as fitmentProcessingService, FitmentProcessingService } from './fitmentProcessing';
export { default as mediaService, MediaService } from './media';
export { default as modelMappingService, ModelMappingService } from './modelMapping';
export { default as productService, ProductService } from './product';
export { default as userService, UserService } from './user';
export { default as vcdbService, VCdbService } from './autocare/vcdb.service';
export { default as pcdbService, PCdbService } from './autocare/pcdb.service';
export { default as padbService, PAdbService } from './autocare/padb.service';
export { default as qdbService, QdbService } from './autocare/qdb.service';
