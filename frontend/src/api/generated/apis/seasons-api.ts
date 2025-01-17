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
import { SeasonCreate } from '../models';
// @ts-ignore
import { SeasonResponse } from '../models';
/**
 * SeasonsApi - axios parameter creator
 * @export
 */
export const SeasonsApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * Create a new season
         * @summary Create Season
         * @param {SeasonCreate} seasonCreate
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createSeasonApiV1SeasonsPost: async (seasonCreate: SeasonCreate, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'seasonCreate' is not null or undefined
            assertParamExists('createSeasonApiV1SeasonsPost', 'seasonCreate', seasonCreate)
            const localVarPath = `/api/v1/seasons/`;
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
            localVarRequestOptions.data = serializeDataIfNeeded(seasonCreate, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * End a season
         * @summary End Season
         * @param {number} seasonId
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        endSeasonApiV1SeasonsSeasonIdEndPost: async (seasonId: number, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'seasonId' is not null or undefined
            assertParamExists('endSeasonApiV1SeasonsSeasonIdEndPost', 'seasonId', seasonId)
            const localVarPath = `/api/v1/seasons/{season_id}/end`
                .replace(`{${"season_id"}}`, encodeURIComponent(String(seasonId)));
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
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
         * Get a specific season by ID
         * @summary Get Season
         * @param {number} seasonId
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getSeasonApiV1SeasonsSeasonIdGet: async (seasonId: number, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'seasonId' is not null or undefined
            assertParamExists('getSeasonApiV1SeasonsSeasonIdGet', 'seasonId', seasonId)
            const localVarPath = `/api/v1/seasons/{season_id}`
                .replace(`{${"season_id"}}`, encodeURIComponent(String(seasonId)));
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
         * List all seasons
         * @summary List Seasons
         * @param {number} [skip]
         * @param {number} [limit]
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        listSeasonsApiV1SeasonsGet: async (skip?: number, limit?: number, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/seasons/`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

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
         * Start a season
         * @summary Start Season
         * @param {number} seasonId
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        startSeasonApiV1SeasonsSeasonIdStartPost: async (seasonId: number, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'seasonId' is not null or undefined
            assertParamExists('startSeasonApiV1SeasonsSeasonIdStartPost', 'seasonId', seasonId)
            const localVarPath = `/api/v1/seasons/{season_id}/start`
                .replace(`{${"season_id"}}`, encodeURIComponent(String(seasonId)));
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
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
    }
};

/**
 * SeasonsApi - functional programming interface
 * @export
 */
export const SeasonsApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = SeasonsApiAxiosParamCreator(configuration)
    return {
        /**
         * Create a new season
         * @summary Create Season
         * @param {SeasonCreate} seasonCreate
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createSeasonApiV1SeasonsPost(seasonCreate: SeasonCreate, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<SeasonResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.createSeasonApiV1SeasonsPost(seasonCreate, options);
            const index = configuration?.serverIndex ?? 0;
            const operationBasePath = operationServerMap['SeasonsApi.createSeasonApiV1SeasonsPost']?.[index]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, operationBasePath || basePath);
        },
        /**
         * End a season
         * @summary End Season
         * @param {number} seasonId
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async endSeasonApiV1SeasonsSeasonIdEndPost(seasonId: number, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<SeasonResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.endSeasonApiV1SeasonsSeasonIdEndPost(seasonId, options);
            const index = configuration?.serverIndex ?? 0;
            const operationBasePath = operationServerMap['SeasonsApi.endSeasonApiV1SeasonsSeasonIdEndPost']?.[index]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, operationBasePath || basePath);
        },
        /**
         * Get a specific season by ID
         * @summary Get Season
         * @param {number} seasonId
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async getSeasonApiV1SeasonsSeasonIdGet(seasonId: number, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<SeasonResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.getSeasonApiV1SeasonsSeasonIdGet(seasonId, options);
            const index = configuration?.serverIndex ?? 0;
            const operationBasePath = operationServerMap['SeasonsApi.getSeasonApiV1SeasonsSeasonIdGet']?.[index]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, operationBasePath || basePath);
        },
        /**
         * List all seasons
         * @summary List Seasons
         * @param {number} [skip]
         * @param {number} [limit]
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async listSeasonsApiV1SeasonsGet(skip?: number, limit?: number, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<Array<SeasonResponse>>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.listSeasonsApiV1SeasonsGet(skip, limit, options);
            const index = configuration?.serverIndex ?? 0;
            const operationBasePath = operationServerMap['SeasonsApi.listSeasonsApiV1SeasonsGet']?.[index]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, operationBasePath || basePath);
        },
        /**
         * Start a season
         * @summary Start Season
         * @param {number} seasonId
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async startSeasonApiV1SeasonsSeasonIdStartPost(seasonId: number, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<SeasonResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.startSeasonApiV1SeasonsSeasonIdStartPost(seasonId, options);
            const index = configuration?.serverIndex ?? 0;
            const operationBasePath = operationServerMap['SeasonsApi.startSeasonApiV1SeasonsSeasonIdStartPost']?.[index]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, operationBasePath || basePath);
        },
    }
};

/**
 * SeasonsApi - factory interface
 * @export
 */
export const SeasonsApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = SeasonsApiFp(configuration)
    return {
        /**
         * Create a new season
         * @summary Create Season
         * @param {SeasonCreate} seasonCreate
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createSeasonApiV1SeasonsPost(seasonCreate: SeasonCreate, options?: any): AxiosPromise<SeasonResponse> {
            return localVarFp.createSeasonApiV1SeasonsPost(seasonCreate, options).then((request) => request(axios, basePath));
        },
        /**
         * End a season
         * @summary End Season
         * @param {number} seasonId
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        endSeasonApiV1SeasonsSeasonIdEndPost(seasonId: number, options?: any): AxiosPromise<SeasonResponse> {
            return localVarFp.endSeasonApiV1SeasonsSeasonIdEndPost(seasonId, options).then((request) => request(axios, basePath));
        },
        /**
         * Get a specific season by ID
         * @summary Get Season
         * @param {number} seasonId
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getSeasonApiV1SeasonsSeasonIdGet(seasonId: number, options?: any): AxiosPromise<SeasonResponse> {
            return localVarFp.getSeasonApiV1SeasonsSeasonIdGet(seasonId, options).then((request) => request(axios, basePath));
        },
        /**
         * List all seasons
         * @summary List Seasons
         * @param {number} [skip]
         * @param {number} [limit]
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        listSeasonsApiV1SeasonsGet(skip?: number, limit?: number, options?: any): AxiosPromise<Array<SeasonResponse>> {
            return localVarFp.listSeasonsApiV1SeasonsGet(skip, limit, options).then((request) => request(axios, basePath));
        },
        /**
         * Start a season
         * @summary Start Season
         * @param {number} seasonId
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        startSeasonApiV1SeasonsSeasonIdStartPost(seasonId: number, options?: any): AxiosPromise<SeasonResponse> {
            return localVarFp.startSeasonApiV1SeasonsSeasonIdStartPost(seasonId, options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * SeasonsApi - interface
 * @export
 * @interface SeasonsApi
 */
export interface SeasonsApiInterface {
    /**
     * Create a new season
     * @summary Create Season
     * @param {SeasonCreate} seasonCreate
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SeasonsApiInterface
     */
    createSeasonApiV1SeasonsPost(seasonCreate: SeasonCreate, options?: RawAxiosRequestConfig): AxiosPromise<SeasonResponse>;

    /**
     * End a season
     * @summary End Season
     * @param {number} seasonId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SeasonsApiInterface
     */
    endSeasonApiV1SeasonsSeasonIdEndPost(seasonId: number, options?: RawAxiosRequestConfig): AxiosPromise<SeasonResponse>;

    /**
     * Get a specific season by ID
     * @summary Get Season
     * @param {number} seasonId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SeasonsApiInterface
     */
    getSeasonApiV1SeasonsSeasonIdGet(seasonId: number, options?: RawAxiosRequestConfig): AxiosPromise<SeasonResponse>;

    /**
     * List all seasons
     * @summary List Seasons
     * @param {number} [skip]
     * @param {number} [limit]
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SeasonsApiInterface
     */
    listSeasonsApiV1SeasonsGet(skip?: number, limit?: number, options?: RawAxiosRequestConfig): AxiosPromise<Array<SeasonResponse>>;

    /**
     * Start a season
     * @summary Start Season
     * @param {number} seasonId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SeasonsApiInterface
     */
    startSeasonApiV1SeasonsSeasonIdStartPost(seasonId: number, options?: RawAxiosRequestConfig): AxiosPromise<SeasonResponse>;

}

/**
 * SeasonsApi - object-oriented interface
 * @export
 * @class SeasonsApi
 * @extends {BaseAPI}
 */
export class SeasonsApi extends BaseAPI implements SeasonsApiInterface {
    /**
     * Create a new season
     * @summary Create Season
     * @param {SeasonCreate} seasonCreate
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SeasonsApi
     */
    public createSeasonApiV1SeasonsPost(seasonCreate: SeasonCreate, options?: RawAxiosRequestConfig) {
        return SeasonsApiFp(this.configuration).createSeasonApiV1SeasonsPost(seasonCreate, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * End a season
     * @summary End Season
     * @param {number} seasonId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SeasonsApi
     */
    public endSeasonApiV1SeasonsSeasonIdEndPost(seasonId: number, options?: RawAxiosRequestConfig) {
        return SeasonsApiFp(this.configuration).endSeasonApiV1SeasonsSeasonIdEndPost(seasonId, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Get a specific season by ID
     * @summary Get Season
     * @param {number} seasonId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SeasonsApi
     */
    public getSeasonApiV1SeasonsSeasonIdGet(seasonId: number, options?: RawAxiosRequestConfig) {
        return SeasonsApiFp(this.configuration).getSeasonApiV1SeasonsSeasonIdGet(seasonId, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * List all seasons
     * @summary List Seasons
     * @param {number} [skip]
     * @param {number} [limit]
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SeasonsApi
     */
    public listSeasonsApiV1SeasonsGet(skip?: number, limit?: number, options?: RawAxiosRequestConfig) {
        return SeasonsApiFp(this.configuration).listSeasonsApiV1SeasonsGet(skip, limit, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Start a season
     * @summary Start Season
     * @param {number} seasonId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SeasonsApi
     */
    public startSeasonApiV1SeasonsSeasonIdStartPost(seasonId: number, options?: RawAxiosRequestConfig) {
        return SeasonsApiFp(this.configuration).startSeasonApiV1SeasonsSeasonIdStartPost(seasonId, options).then((request) => request(this.axios, this.basePath));
    }
}
