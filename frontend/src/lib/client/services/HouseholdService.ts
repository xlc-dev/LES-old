/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { HouseholdCreate } from "../models/HouseholdCreate";
import type { HouseholdRead_Output } from "../models/HouseholdRead_Output";
import type { HouseholdUpdate } from "../models/HouseholdUpdate";
import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";
export class HouseholdService {
  /**
   * Get Households
   * @returns HouseholdRead_Output Successful Response
   * @throws ApiError
   */
  public static getHouseholdsApiHouseholdGet(): CancelablePromise<Array<HouseholdRead_Output>> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/household/",
    });
  }
  /**
   * Post Household
   * @param requestBody
   * @returns any Successful Response
   * @throws ApiError
   */
  public static postHouseholdApiHouseholdPost(
    requestBody: HouseholdCreate
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/household/",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Get Household
   * @param id
   * @returns HouseholdRead_Output Successful Response
   * @throws ApiError
   */
  public static getHouseholdApiHouseholdIdGet(
    id: number
  ): CancelablePromise<HouseholdRead_Output> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/household/{id}",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Update Household
   * @param id
   * @param requestBody
   * @returns HouseholdUpdate Successful Response
   * @throws ApiError
   */
  public static updateHouseholdApiHouseholdIdPatch(
    id: number,
    requestBody: HouseholdUpdate
  ): CancelablePromise<HouseholdUpdate> {
    return __request(OpenAPI, {
      method: "PATCH",
      url: "/api/household/{id}",
      path: {
        id: id,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Delete Household
   * @param id
   * @returns void
   * @throws ApiError
   */
  public static deleteHouseholdApiHouseholdIdDelete(id: number): CancelablePromise<void> {
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/household/{id}",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Get Households By Twinworld
   * @param twinworldId
   * @returns HouseholdRead_Output Successful Response
   * @throws ApiError
   */
  public static getHouseholdsByTwinworldApiHouseholdTwinworldTwinworldIdGet(
    twinworldId: number
  ): CancelablePromise<Array<HouseholdRead_Output>> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/household/twinworld/{twinworld_id}",
      path: {
        twinworld_id: twinworldId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
