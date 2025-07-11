/**
 * DRES Client API
 *
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { ApiHint } from './apiHint';
import { ApiTarget } from './apiTarget';


export interface ApiTaskTemplate { 
    id?: string;
    name: string;
    taskGroup: string;
    taskType: string;
    duration: number;
    collectionId: string;
    targets: Array<ApiTarget>;
    hints: Array<ApiHint>;
    comment?: string;
}

