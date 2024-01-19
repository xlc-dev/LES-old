/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AlgorithmCreate } from '../models/AlgorithmCreate';
import type { AlgorithmRead } from '../models/AlgorithmRead';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AlgorithmService {
  /**
   * Get Algorithms
   * @returns AlgorithmRead Successful Response
   * @throws ApiError
   */
  public static getAlgorithmsApiAlgorithmGet(): CancelablePromise<Array<AlgorithmRead>> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/api/algorithm/',
    });
  }
  /**
   * Post Algorithm
   * @param requestBody
   * @returns any Successful Response
   * @throws ApiError
   */
  public static postAlgorithmApiAlgorithmPost(
    requestBody: { name: any; description: any; algorithm: string },
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/api/algorithm/',
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Get Algorithm
   * @param id
   * @returns AlgorithmRead Successful Response
   * @throws ApiError
   */
  public static getAlgorithmApiAlgorithmIdGet(
    id: number,
  ): CancelablePromise<AlgorithmRead> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/api/algorithm/{id}',
      path: {
        'id': id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Delete Algorithm
   * @param id
   * @returns void
   * @throws ApiError
   */
  public static deleteAlgorithmApiAlgorithmIdDelete(
    id: number,
  ): CancelablePromise<void> {
    return __request(OpenAPI, {
      method: 'DELETE',
      url: '/api/algorithm/{id}',
      path: {
        'id': id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
