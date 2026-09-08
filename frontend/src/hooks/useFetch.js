import { useEffect, useState } from "react";

export function useFetch(fetchFunction, dependencies = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;

    async function execute() {
      setLoading(true);
      setError(null);

      try {
        const result =
          await fetchFunction();

        if (mounted) {
          setData(result);
        }
      } catch (err) {
        if (mounted) {
          setError(
            err.response?.data?.detail ||
            err.message ||
            "Request failed"
          );
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    execute();

    return () => {
      mounted = false;
    };
  }, dependencies);

  return {
    data,
    loading,
    error
  };
}