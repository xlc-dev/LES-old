/**
 * This file contains utility functions for handling and formatting messages.
 * The messages are displayed in the messages component that listens to $messages.
 */

import { messages } from "../lib/stores";

/**
 * Checks if the given value is a valid JSON string.
 * @param {string} value - The value to be checked.
 * @returns {boolean} - True if the value is a valid JSON string, false otherwise.
 */
const isJsonString = (value: string): boolean => {
  try {
    JSON.parse(value);
    return true;
  } catch {
    return false;
  }
};

/**
 * Show a message based on the given type of error.
 * @param {(object | string)} error - The error object or string.
 */
const showError = (error: object | string): void => {
  const id = Math.random();
  const cleanedError =
    typeof error === "object" && error.body
      ? Array.isArray(error.body.detail)
        ? `<p class="font-bold mb-2">${error.body.detail[0].loc[1]}</p>${error.body.detail[0].msg}`
        : error.body.detail
      : typeof error === "string" && isJsonString(error)
        ? JSON.parse(error).body.detail[0].msg
        : typeof error === "string"
          ? error
          : "Unknown error";

  messages.update((e) => [...e, { msg: cleanedError, id }]);
};

/**
 * Displays a message.
 * @param {(object | string)} str - The error object or string.
 */
export const message = (str: object | string): void => {
  if (typeof str === "object" || (typeof str === "string" && isJsonString(str))) {
    showError(str);
  } else if (typeof str === "string") {
    showError(str);
  }
};
