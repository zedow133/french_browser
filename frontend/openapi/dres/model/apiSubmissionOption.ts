/**
 * DRES Client API
 *
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


export const ApiSubmissionOption = {
    NO_DUPLICATES: 'NO_DUPLICATES',
    LIMIT_CORRECT_PER_TEAM: 'LIMIT_CORRECT_PER_TEAM',
    LIMIT_WRONG_PER_TEAM: 'LIMIT_WRONG_PER_TEAM',
    LIMIT_TOTAL_PER_TEAM: 'LIMIT_TOTAL_PER_TEAM',
    LIMIT_CORRECT_PER_MEMBER: 'LIMIT_CORRECT_PER_MEMBER',
    TEMPORAL_SUBMISSION: 'TEMPORAL_SUBMISSION',
    TEXTUAL_SUBMISSION: 'TEXTUAL_SUBMISSION',
    ITEM_SUBMISSION: 'ITEM_SUBMISSION',
    MINIMUM_TIME_GAP: 'MINIMUM_TIME_GAP'
} as const;
export type ApiSubmissionOption = typeof ApiSubmissionOption[keyof typeof ApiSubmissionOption];

