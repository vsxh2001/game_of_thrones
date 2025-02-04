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


import type { Configuration } from '../configuration';
import type { AxiosPromise, AxiosInstance, RawAxiosRequestConfig } from 'axios';
import globalAxios from 'axios';
// Some imports not used depending on template conditions
// @ts-ignore
import { DUMMY_BASE_URL, assertParamExists, setApiKeyToObject, setBasicAuthToObject, setBearerAuthToObject, setOAuthToObject, setSearchParams, serializeDataIfNeeded, toPathString, createRequestFunction } from '../common';
// @ts-ignore
import { BASE_PATH, COLLECTION_FORMATS, RequestArgs, BaseAPI, RequiredError, operationServerMap } from '../base';
// @ts-ignore
import { HTTPValidationError } from '../models';
// @ts-ignore
import { RoundCreate } from '../models';
// @ts-ignore
import { RoundResponse } from '../models';
// @ts-ignore
import { RoundUpdate } from '../models';
/**
 * RoundsApi - axios parameter creator
 * @export
 */
export const RoundsApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * Create a new round
         * @summary Create Round
         * @param {RoundCreate} roundCreate
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createRoundApiV1RoundsPost: async (roundCreate: RoundCreate, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'roundCreate' is not null or undefined
            assertParamExists('createRoundApiV1RoundsPost', 'roundCreate', roundCreate)
            const localVarPath = `/api/v1/rounds/`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;



            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(roundCreate, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Get a specific round by ID
         * @summary Get Round
         * @param {number} roundId
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getRoundApiV1RoundsRoundIdGet: async (roundId: number, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'roundId' is not null or undefined
            assertParamExists('getRoundApiV1RoundsRoundIdGet', 'roundId', roundId)
            const localVarPath = `/api/v1/rounds/{round_id}`
                .replace(`{${"round_id"}}`, encodeURIComponent(String(roundId)));
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;



            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * List all rounds
         * @summary List Rounds
         * @param {number} [matchId]
         * @param {number} [skip]
         * @param {number} [limit]
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        listRoundsApiV1RoundsGet: async (matchId?: number, skip?: number, limit?: number, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/rounds/`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            if (matchId !== undefined) {
                localVarQueryParameter['match_id'] = matchId;
            }

            if (skip !== undefined) {
                localVarQueryParameter['skip'] = skip;
            }

            if (limit !== undefined) {
                localVarQueryParameter['limit'] = limit;
            }



            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Update a round
         * @summary Update Round
         * @param {number} roundId
         * @param {RoundUpdate} roundUpdate
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updateRoundApiV1RoundsRoundIdPut: async (roundId: number, roundUpdate: RoundUpdate, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'roundId' is not null or undefined
            assertParamExists('updateRoundApiV1RoundsRoundIdPut', 'roundId', roundId)
            // verify required parameter 'roundUpdate' is not null or undefined
            assertParamExists('updateRoundApiV1RoundsRoundIdPut', 'roundUpdate', roundUpdate)
            const localVarPath = `/api/v1/rounds/{round_id}`
                .replace(`{${"round_id"}}`, encodeURIComponent(String(roundId)));
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'PUT', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;



            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(roundUpdate, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * RoundsApi - functional programming interface
 * @export
 */
export const RoundsApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = RoundsApiAxiosParamCreator(configuration)
    return {
        /**
         * Create a new round
         * @summary Create Round
         * @param {RoundCreate} roundCreate
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createRoundApiV1RoundsPost(roundCreate: RoundCreate, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<RoundResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.createRoundApiV1RoundsPost(roundCreate, options);
            const index = configuration?.serverIndex ?? 0;
            const operationBasePath = operationServerMap['RoundsApi.createRoundApiV1RoundsPost']?.[index]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, operationBasePath || basePath);
        },
        /**
         * Get a specific round by ID
         * @summary Get Round
         * @param {number} roundId
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async getRoundApiV1RoundsRoundIdGet(roundId: number, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<RoundResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.getRoundApiV1RoundsRoundIdGet(roundId, options);
            const index = configuration?.serverIndex ?? 0;
            const operationBasePath = operationServerMap['RoundsApi.getRoundApiV1RoundsRoundIdGet']?.[index]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, operationBasePath || basePath);
        },
        /**
         * List all rounds
         * @summary List Rounds
         * @param {number} [matchId]
         * @param {number} [skip]
         * @param {number} [limit]
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async listRoundsApiV1RoundsGet(matchId?: number, skip?: number, limit?: number, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<Array<RoundResponse>>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.listRoundsApiV1RoundsGet(matchId, skip, limit, options);
            const index = configuration?.serverIndex ?? 0;
            const operationBasePath = operationServerMap['RoundsApi.listRoundsApiV1RoundsGet']?.[index]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, operationBasePath || basePath);
        },
        /**
         * Update a round
         * @summary Update Round
         * @param {number} roundId
         * @param {RoundUpdate} roundUpdate
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async updateRoundApiV1RoundsRoundIdPut(roundId: number, roundUpdate: RoundUpdate, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<RoundResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.updateRoundApiV1RoundsRoundIdPut(roundId, roundUpdate, options);
            const index = configuration?.serverIndex ?? 0;
            const operationBasePath = operationServerMap['RoundsApi.updateRoundApiV1RoundsRoundIdPut']?.[index]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, operationBasePath || basePath);
        },
    }
};

/**
 * RoundsApi - factory interface
 * @export
 */
export const RoundsApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = RoundsApiFp(configuration)
    return {
        /**
         * Create a new round
         * @summary Create Round
         * @param {RoundCreate} roundCreate
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createRoundApiV1RoundsPost(roundCreate: RoundCreate, options?: any): AxiosPromise<RoundResponse> {
            return localVarFp.createRoundApiV1RoundsPost(roundCreate, options).then((request) => request(axios, basePath));
        },
        /**
         * Get a specific round by ID
         * @summary Get Round
         * @param {number} roundId
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getRoundApiV1RoundsRoundIdGet(roundId: number, options?: any): AxiosPromise<RoundResponse> {
            return localVarFp.getRoundApiV1RoundsRoundIdGet(roundId, options).then((request) => request(axios, basePath));
        },
        /**
         * List all rounds
         * @summary List Rounds
         * @param {number} [matchId]
         * @param {number} [skip]
         * @param {number} [limit]
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        listRoundsApiV1RoundsGet(matchId?: number, skip?: number, limit?: number, options?: any): AxiosPromise<Array<RoundResponse>> {
            return localVarFp.listRoundsApiV1RoundsGet(matchId, skip, limit, options).then((request) => request(axios, basePath));
        },
        /**
         * Update a round
         * @summary Update Round
         * @param {number} roundId
         * @param {RoundUpdate} roundUpdate
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updateRoundApiV1RoundsRoundIdPut(roundId: number, roundUpdate: RoundUpdate, options?: any): AxiosPromise<RoundResponse> {
            return localVarFp.updateRoundApiV1RoundsRoundIdPut(roundId, roundUpdate, options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * RoundsApi - interface
 * @export
 * @interface RoundsApi
 */
export interface RoundsApiInterface {
    /**
     * Create a new round
     * @summary Create Round
     * @param {RoundCreate} roundCreate
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof RoundsApiInterface
     */
    createRoundApiV1RoundsPost(roundCreate: RoundCreate, options?: RawAxiosRequestConfig): AxiosPromise<RoundResponse>;

    /**
     * Get a specific round by ID
     * @summary Get Round
     * @param {number} roundId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof RoundsApiInterface
     */
    getRoundApiV1RoundsRoundIdGet(roundId: number, options?: RawAxiosRequestConfig): AxiosPromise<RoundResponse>;

    /**
     * List all rounds
     * @summary List Rounds
     * @param {number} [matchId]
     * @param {number} [skip]
     * @param {number} [limit]
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof RoundsApiInterface
     */
    listRoundsApiV1RoundsGet(matchId?: number, skip?: number, limit?: number, options?: RawAxiosRequestConfig): AxiosPromise<Array<RoundResponse>>;

    /**
     * Update a round
     * @summary Update Round
     * @param {number} roundId
     * @param {RoundUpdate} roundUpdate
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof RoundsApiInterface
     */
    updateRoundApiV1RoundsRoundIdPut(roundId: number, roundUpdate: RoundUpdate, options?: RawAxiosRequestConfig): AxiosPromise<RoundResponse>;

}

/**
 * RoundsApi - object-oriented interface
 * @export
 * @class RoundsApi
 * @extends {BaseAPI}
 */
export class RoundsApi extends BaseAPI implements RoundsApiInterface {
    /**
     * Create a new round
     * @summary Create Round
     * @param {RoundCreate} roundCreate
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof RoundsApi
     */
    public createRoundApiV1RoundsPost(roundCreate: RoundCreate, options?: RawAxiosRequestConfig) {
        return RoundsApiFp(this.configuration).createRoundApiV1RoundsPost(roundCreate, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Get a specific round by ID
     * @summary Get Round
     * @param {number} roundId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof RoundsApi
     */
    public getRoundApiV1RoundsRoundIdGet(roundId: number, options?: RawAxiosRequestConfig) {
        return RoundsApiFp(this.configuration).getRoundApiV1RoundsRoundIdGet(roundId, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * List all rounds
     * @summary List Rounds
     * @param {number} [matchId]
     * @param {number} [skip]
     * @param {number} [limit]
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof RoundsApi
     */
    public listRoundsApiV1RoundsGet(matchId?: number, skip?: number, limit?: number, options?: RawAxiosRequestConfig) {
        return RoundsApiFp(this.configuration).listRoundsApiV1RoundsGet(matchId, skip, limit, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Update a round
     * @summary Update Round
     * @param {number} roundId
     * @param {RoundUpdate} roundUpdate
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof RoundsApi
     */
    public updateRoundApiV1RoundsRoundIdPut(roundId: number, roundUpdate: RoundUpdate, options?: RawAxiosRequestConfig) {
        return RoundsApiFp(this.configuration).updateRoundApiV1RoundsRoundIdPut(roundId, roundUpdate, options).then((request) => request(this.axios, this.basePath));
    }
}
