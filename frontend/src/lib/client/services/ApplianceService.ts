/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApplianceCreate } from "../models/ApplianceCreate";
import type { ApplianceRead } from "../models/ApplianceRead";
import type { ApplianceTimeWindowCreate } from "../models/ApplianceTimeWindowCreate";
import type { ApplianceTimeWindowRead } from "../models/ApplianceTimeWindowRead";
import type { ApplianceTimeWindowUpdate } from "../models/ApplianceTimeWindowUpdate";
import type { ApplianceUpdate } from "../models/ApplianceUpdate";

import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";

export class ApplianceService {
  /**
   * Get Appliances
   * @returns ApplianceRead Successful Response
   * @throws ApiError
   */
  public static getAppliancesApiApplianceGet(): CancelablePromise<Array<ApplianceRead>> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/appliance/",
    });
  }

  /**
   * Post Appliance
   * @param requestBody
   * @returns any Successful Response
   * @throws ApiError
   */
  public static postApplianceApiAppliancePost(
    requestBody: ApplianceCreate
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/appliance/",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Appliance
   * @param id
   * @returns ApplianceRead Successful Response
   * @throws ApiError
   */
  public static getApplianceApiApplianceIdGet(id: number): CancelablePromise<ApplianceRead> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/appliance/{id}",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Update Appliance
   * @param id
   * @param requestBody
   * @returns ApplianceUpdate Successful Response
   * @throws ApiError
   */
  public static updateApplianceApiApplianceIdPatch(
    id: number,
    requestBody: ApplianceUpdate
  ): CancelablePromise<ApplianceUpdate> {
    return __request(OpenAPI, {
      method: "PATCH",
      url: "/api/appliance/{id}",
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
   * Delete Appliance
   * @param id
   * @returns void
   * @throws ApiError
   */
  public static deleteApplianceApiApplianceIdDelete(id: number): CancelablePromise<void> {
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/appliance/{id}",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Appliance Timewindows
   * @returns ApplianceTimeWindowRead Successful Response
   * @throws ApiError
   */
  public static getApplianceTimewindowsApiApplianceTimewindowGet(): CancelablePromise<
    Array<ApplianceTimeWindowRead>
  > {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/appliance/timewindow",
    });
  }

  /**
   * Post Appliance Timewindow
   * @param requestBody
   * @returns any Successful Response
   * @throws ApiError
   */
  public static postApplianceTimewindowApiApplianceTimewindowPost(
    requestBody: ApplianceTimeWindowCreate
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/appliance/timewindow",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Update Appliance Timewindow
   * @param id
   * @param requestBody
   * @returns ApplianceTimeWindowUpdate Successful Response
   * @throws ApiError
   */
  public static updateApplianceTimewindowApiApplianceTimewindowIdPatch(
    id: number,
    requestBody: ApplianceTimeWindowUpdate
  ): CancelablePromise<ApplianceTimeWindowUpdate> {
    return __request(OpenAPI, {
      method: "PATCH",
      url: "/api/appliance/timewindow/{id}",
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
   * Delete Appliance Timewindow
   * @param id
   * @returns void
   * @throws ApiError
   */
  public static deleteApplianceTimewindowApiAppliancetimewindowIdDelete(
    id: number
  ): CancelablePromise<void> {
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/appliancetimewindow/{id}",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
