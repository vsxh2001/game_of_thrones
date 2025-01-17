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
import { MatchStatus } from './match-status';

/**
 *
 * @export
 * @interface MatchResponse
 */
export interface MatchResponse {
    /**
     *
     * @type {number}
     * @memberof MatchResponse
     */
    'season_id': number;
    /**
     *
     * @type {number}
     * @memberof MatchResponse
     */
    'id': number;
    /**
     *
     * @type {string}
     * @memberof MatchResponse
     */
    'name': string;
    /**
     *
     * @type {MatchStatus}
     * @memberof MatchResponse
     */
    'status': MatchStatus;
    /**
     *
     * @type {string}
     * @memberof MatchResponse
     */
    'start_time'?: string | null;
    /**
     *
     * @type {string}
     * @memberof MatchResponse
     */
    'end_time'?: string | null;
    /**
     *
     * @type {string}
     * @memberof MatchResponse
     */
    'created_at': string;
}
