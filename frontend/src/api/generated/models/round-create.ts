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



/**
 *
 * @export
 * @interface RoundCreate
 */
export interface RoundCreate {
    /**
     *
     * @type {number}
     * @memberof RoundCreate
     */
    'match_id': number;
    /**
     *
     * @type {number}
     * @memberof RoundCreate
     */
    'round_number': number;
    /**
     *
     * @type {number}
     * @memberof RoundCreate
     */
    'duration': number;
    /**
     *
     * @type {number}
     * @memberof RoundCreate
     */
    'gong_timedelta': number;
}
