import { useCallback } from "react";

import { serversApi } from "../services/api";

import { useFetch } from "./useFetch";

export function useMonitoring() {
  const fetchServers =
    useCallback(
      () => serversApi.list(),
      []
    );

  return useFetch(
    fetchServers,
    [fetchServers]
  );
}