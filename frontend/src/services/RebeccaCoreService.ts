export type TestConnectionResponse = {
  ok: boolean;
};

const DEFAULT_ENDPOINT = "http://localhost:8000";

type HealthResponse = {
  status: string;
  meta?: Record<string, unknown>;
};

export class RebeccaCoreService {
  static async testConnection(endpoint: string, token: string): Promise<boolean> {
    const target = endpoint || DEFAULT_ENDPOINT;
    try {
      const response = await fetch(`${target}/health`, {
        method: "GET",
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      });
      if (!response.ok) {
        return false;
      }
      const payload = (await response.json()) as HealthResponse;
      return payload.status === "ok";
    } catch (error) {
      console.warn("Rebecca core connection failed", error);
      return false;
    }
  }
}