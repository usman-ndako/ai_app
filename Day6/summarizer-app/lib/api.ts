// import { SummaryRequest, SummaryResponse, ApiError } from './types';

// const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

// export class ApiClient {
//   private baseUrl: string;

//   constructor(baseUrl: string = API_BASE_URL) {
//     this.baseUrl = baseUrl;
//   }

//   async summarize(request: SummaryRequest): Promise<SummaryResponse> {
//     try {
//       const response = await fetch(`${this.baseUrl}/summarize`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(request),
//       });

//       if (!response.ok) {
//         const error: ApiError = await response.json();
//         throw new Error(error.detail || 'Failed to generate summary');
//       }

//       const data: SummaryResponse = await response.json();
//       return data;
//     } catch (error) {
//       if (error instanceof Error) {
//         throw error;
//       }
//       throw new Error('An unexpected error occurred');
//     }
//   }

//   async healthCheck(): Promise<boolean> {
//     try {
//       const response = await fetch(`${this.baseUrl}/`);
//       return response.ok;
//     } catch {
//       return false;
//     }
//   }
// }

// // Export singleton instance
// export const apiClient = new ApiClient();

import { SummaryRequest, SummaryResponse, ApiError } from './types';

// Use only the environment variable - no fallback
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

// Validate that the environment variable is set and provide TypeScript assurance
if (!API_BASE_URL) {
  throw new Error(
    'NEXT_PUBLIC_API_URL environment variable is not set. ' +
    'Please set it in .env.local for development and in your hosting platform for production.'
  );
}

// Type assertion since we've validated it above
const validatedApiBaseUrl = API_BASE_URL as string;

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = validatedApiBaseUrl) {
    this.baseUrl = baseUrl;
  }

  async summarize(request: SummaryRequest): Promise<SummaryResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/summarize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const error: ApiError = await response.json();
        throw new Error(error.detail || 'Failed to generate summary');
      }

      const data: SummaryResponse = await response.json();
      return data;
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred');
    }
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/`);
      return response.ok;
    } catch {
      return false;
    }
  }

  // Optional: Add method to get the current API URL for debugging
  getApiUrl(): string {
    return this.baseUrl;
  }
}

// Export singleton instance
export const apiClient = new ApiClient();