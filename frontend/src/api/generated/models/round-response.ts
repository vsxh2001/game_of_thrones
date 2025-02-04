/* tslint:disable */
/* eslint-disable */
/**
 * Game of Thrones Championship API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


// May contain unused imports in some cases
// @ts-ignore
import { RoundStatus } from './round-status';

/**
 *
 * @export
 * @interface RoundResponse
 */
export interface RoundResponse {
    /**
     *
     * @type {number}
     * @memberof RoundResponse
     */
    'match_id': number;
    /**
     *
     * @type {number}
     * @memberof RoundResponse
     */
    'round_number': number;
    /**
     *
     * @type {number}
     * @memberof RoundResponse
     */
    'duration': number;
    /**
     *
     * @type {number}
     * @memberof RoundResponse
     */
    'gong_timedelta': number;
    /**
     *
     * @type {number}
     * @memberof RoundResponse
     */
    'id': number;
    /**
     *
     * @type {RoundStatus}
     * @memberof RoundResponse
     */
    'status': RoundStatus;
    /**
     *
     * @type {string}
     * @memberof RoundResponse
     */
    'start_time'?: string | null;
    /**
     *
     * @type {string}
     * @memberof RoundResponse
     */
    'created_at': string;
}
