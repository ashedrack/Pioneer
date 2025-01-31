import { useState, useCallback } from 'react';
import { AxiosResponse } from 'axios';

interface UseApiReturn<T> {
  data: T | null;
  error: string | null;
  loading: boolean;
  execute: (...params: any[]) => Promise<T>;
}

export function useApi<T>(
  apiFunction: (...params: any[]) => Promise<AxiosResponse<T>>
): UseApiReturn<T> {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const execute = useCallback(
    async (...params: any[]): Promise<T> => {
      try {
        setLoading(true);
        setError(null);
        const response = await apiFunction(...params);
        setData(response.data);
        return response.data;
      } catch (err: any) {
        const errorMessage = err.response?.data?.message || err.message;
        setError(errorMessage);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [apiFunction]
  );

  return {
    data,
    error,
    loading,
    execute,
  };
}

export default useApi;
