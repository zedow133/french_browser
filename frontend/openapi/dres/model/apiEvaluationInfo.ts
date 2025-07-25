/**
 * DRES Client API
 *
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { ApiTeamInfo } from './apiTeamInfo';
import { ApiEvaluationStatus } from './apiEvaluationStatus';
import { ApiTaskTemplateInfo } from './apiTaskTemplateInfo';
import { ApiRunProperties } from './apiRunProperties';
import { ApiEvaluationType } from './apiEvaluationType';


export interface ApiEvaluationInfo { 
    id: string;
    name: string;
    type: ApiEvaluationType;
    status: ApiEvaluationStatus;
    properties: ApiRunProperties;
    templateId: string;
    templateDescription?: string;
    teams: Array<ApiTeamInfo>;
    taskTemplates: Array<ApiTaskTemplateInfo>;
}
export namespace ApiEvaluationInfo {
}


