/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_upload_energyflow_api_energyflow_upload_post } from "../models/Body_upload_energyflow_api_energyflow_upload_post";
import type { EnergyFlowCreate } from "../models/EnergyFlowCreate";
import type { EnergyFlowRead } from "../models/EnergyFlowRead";
import type { EnergyFlowUploadRead } from "../models/EnergyFlowUploadRead";
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
      url: "/api/energyflow/{id}",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Delete Energyflow
   * @param id
   * @returns void
   * @throws ApiError
   */
  public static deleteEnergyflowApiEnergyflowIdDelete(id: number): CancelablePromise<void> {
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/energyflow/{id}",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Get Energyflow Uploads
   * @returns EnergyFlowUploadRead Successful Response
   * @throws ApiError
   */
  public static getEnergyflowUploadsApiEnergyflowUploadGet(): CancelablePromise<
    Array<EnergyFlowUploadRead>
  > {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/energyflow/upload",
    });
  }
  /**
   * Upload Energyflow
   * @param formData
   * @returns any Successful Response
   * @throws ApiError
   */
  public static uploadEnergyflowApiEnergyflowUploadPost(
    formData: Body_upload_energyflow_api_energyflow_upload_post
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/energyflow/upload",
      formData: formData,
      mediaType: "multipart/form-data",
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Get Energyflow Upload
   * @param id
   * @returns EnergyFlowUploadRead Successful Response
   * @throws ApiError
   */
  public static getEnergyflowUploadApiEnergyflowUploadIdGet(
    id: number
  ): CancelablePromise<EnergyFlowUploadRead> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/energyflow/upload/{id}",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Delete Energyflow Upload
   * @param id
   * @returns void
   * @throws ApiError
   */
  public static deleteEnergyflowUploadApiEnergyflowUploadIdDelete(
    id: number
  ): CancelablePromise<void> {
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/energyflow/upload/{id}",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
