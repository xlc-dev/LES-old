/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { EnergyFlowCreate } from "../models/EnergyFlowCreate";
import type { EnergyFlowRead } from "../models/EnergyFlowRead";
import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";
export class EnergyflowService {
  /**
   * Get Energyflows
   * @returns EnergyFlowRead Successful Response
   * @throws ApiError
   */
  public static getEnergyflowsApiEnergyflowGet(): CancelablePromise<Array<EnergyFlowRead>> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/energyflow/",
    });
  }
  /**
   * Post Energyflow
   * @param requestBody
   * @returns any Successful Response
   * @throws ApiError
   */
  public static postEnergyflowApiEnergyflowPost(
    requestBody: EnergyFlowCreate
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/energyflow/",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Get Energyflow
   * @param id
   * @returns EnergyFlowRead Successful Response
   * @throws ApiError
   */
  public static getEnergyflowApiEnergyflowIdGet(id: number): CancelablePromise<EnergyFlowRead> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/energyflow/{id}/",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
