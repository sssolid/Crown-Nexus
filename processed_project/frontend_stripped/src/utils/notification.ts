import{reactive}from 'vue';export enum NotificationType{SUCCESS='success',ERROR='error',WARNING='warning',INFO='info',}export interface Notification{id:number;type:NotificationType;message:string;timeout?:number;closeable?:boolean;position?:'top'|'bottom';}const DEFAULT_TIMEOUT=5000;const DEFAULT_POSITION='bottom';const notifications=reactive<Notification[]>([]);let nextId=1;function createNotification(type:NotificationType,message:string,timeout:number=DEFAULT_TIMEOUT,closeable:boolean=true,position:'top'|'bottom'=DEFAULT_POSITION):number{const id=nextId++;const notification:Notification={id,type,message,timeout,closeable,position,};notifications.push(notification);if(timeout>0){setTimeout(()=>removeNotification(id),timeout);}return id;}function removeNotification(id:number):void{const index=notifications.findIndex(notification=>notification.id===id);if(index!==-1){notifications.splice(index,1);}}function getNotifications():Notification[]{return notifications;}function success(message:string,timeout?:number):number{return createNotification(NotificationType.SUCCESS,message,timeout);}function error(message:string,timeout?:number):number{return createNotification(NotificationType.ERROR,message,timeout);}function warning(message:string,timeout?:number):number{return createNotification(NotificationType.WARNING,message,timeout);}function info(message:string,timeout?:number):number{return createNotification(NotificationType.INFO,message,timeout);}export const notificationService={success,error,warning,info,remove:removeNotification,getAll:getNotifications,};