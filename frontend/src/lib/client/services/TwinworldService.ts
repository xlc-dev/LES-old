/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TwinWorldCreate } from "../models/TwinWorldCreate";
import type { TwinWorldRead } from "../models/TwinWorldRead";

import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";

export class TwinworldService {
  /**
   * Get Twinworlds
   * @returns TwinWorldRead Successful Response
   * @throws ApiError
   */
  public static getTwinworldsApiTwinworldGet(): CancelablePromise<Array<TwinWorldRead>> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/twinworld/",
    });
  }

  /**
   * Post Twinworld
   * @param requestBody
   * @returns any Successful Response
   * @throws ApiError
   */
  public static postTwinworldApiTwinworldPost(
    requestBody: TwinWorldCreate
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/twinworld/",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Twinworld
   * @param id
   * @returns TwinWorldRead Successful Response
   * @throws ApiError
   */
  public static getTwinworldApiTwinworldIdGet(id: number): CancelablePromise<TwinWorldRead> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/twinworld/{id}/",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
