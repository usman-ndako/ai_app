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

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    // Use provided baseUrl or get from environment variable
    this.baseUrl = baseUrl || this.getApiBaseUrl();
  }

  private getApiBaseUrl(): string {
    // This will only run on the client side
    if (typeof window !== 'undefined') {
      // Client-side: use environment variable
      return process.env.NEXT_PUBLIC_API_URL || 'https://ai-app-1-3p2s.onrender.com';
    } else {
      // Server-side: use the production URL directly
      return 'https://ai-app-1-3p2s.onrender.com';
    }
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

  getApiUrl(): string {
    return this.baseUrl;
  }
}

// Export singleton instance
export const apiClient = new ApiClient();